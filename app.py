from fastapi import FastAPI, File, UploadFile, Request
import os
import sys
import io
import certifi
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
import pymongo

from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, HTMLResponse
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# =========================
# MongoDB Setup (optional)
# =========================
ca = certifi.where()
mongo_db_url = os.getenv("MONGO_DB_URL")
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

# =========================
# FastAPI App
# =========================
app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# =========================
# Load Model ONCE (IMPORTANT)
# =========================
try:
    preprocessor = load_object("final_model/preprocessor.pkl")
    final_model = load_object("final_model/model.pkl")
    network_model = NetworkModel(preprocessor=preprocessor, model=final_model)

    print("✅ Model loaded successfully")

except Exception as e:
    print("❌ Model loading failed:", str(e))
    network_model = None

# =========================
# Routes
# =========================

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# -------------------------
# TRAIN
# -------------------------
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is Successful")

    except Exception as e:
        raise NetworkSecurityException(e, sys)

# -------------------------
# PREDICT
# -------------------------
@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        if network_model is None:
            return Response("Model not loaded properly", status_code=500)

        # =========================
        # Read CSV safely
        # =========================
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        print("📊 Data received:", df.shape)
        print("🧾 Columns:", df.columns.tolist())

        if df.empty:
            return Response("Uploaded file is empty", status_code=400)

        # =========================
        # Validate schema
        # =========================
        try:
            expected_cols = list(preprocessor.feature_names_in_)
            missing_cols = set(expected_cols) - set(df.columns)

            if missing_cols:
                return Response(
                    f"Missing columns: {missing_cols}",
                    status_code=400
                )

        except Exception:
            print("⚠️ Could not validate schema (skipping)")

        # =========================
        # Prediction
        # =========================
        try:
            y_pred = network_model.predict(df)
            print("✅ Prediction successful")

        except Exception as e:
            print("❌ Prediction error:", str(e))
            return Response(f"Prediction failed: {str(e)}", status_code=500)

        # =========================
        # Attach predictions
        # =========================
        df["predicted_column"] = y_pred

        # =========================
        # Save output
        # =========================
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)

        # =========================
        # Convert to HTML
        # =========================
        table_html = df.to_html(classes="table table-striped")

        # =========================
        # TEMPLATE RESPONSE (FIXED)
        # =========================
        try:
            return templates.TemplateResponse(
                request,
                "table.html",
                {"table": table_html}
            )
        except Exception as e:
            print("⚠️ Template failed, using fallback:", str(e))
            return HTMLResponse(content=table_html)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

# =========================
# Run Server
# =========================
if __name__ == "__main__":
    run(app=app, host="localhost", port=8000)