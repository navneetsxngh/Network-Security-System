# Network Security System

An end-to-end machine learning pipeline for network intrusion detection. The system automates the full lifecycle of a classification model — from data ingestion through MongoDB to model training and experiment tracking — with a modular, production-ready architecture.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Running the Pipeline](#running-the-pipeline)
- [Experiment Tracking](#experiment-tracking)
- [License](#license)

---

## Overview

The Network Security System is designed to detect anomalous or malicious network traffic using supervised machine learning. Raw network data is stored in MongoDB Atlas, validated against a defined schema, transformed for model compatibility, and used to train a classification model. All pipeline stages are logged and their artifacts are persisted for reproducibility.

---

## Architecture

The training pipeline executes the following sequential stages:

```
MongoDB Atlas
      |
      v
Data Ingestion      →  Pulls raw data and produces train/test splits
      |
      v
Data Validation     →  Validates schema conformity and data drift
      |
      v
Data Transformation →  Applies preprocessing (imputation, scaling, encoding)
      |
      v
Model Training      →  Trains a classifier, evaluates metrics, registers model
      |
      v
MLflow / DagsHub    →  Tracks experiments, parameters, and metrics
```

Each stage produces a serialised artifact that is passed as input to the next stage, ensuring full traceability across runs.

---

## Project Structure

```
Network-Security-System/
│
├── networksecurity/                  # Core package
│   ├── components/                   # Pipeline stage implementations
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   └── model_trainer.py
│   ├── entity/                       # Config and artifact dataclasses
│   │   └── config_entity.py
│   ├── exception/                    # Custom exception handler
│   │   └── exception.py
│   └── logging/                      # Structured logger
│       └── logger.py
│
├── data/                             # Raw dataset files
├── data_schema/                      # Schema definition for validation
├── Artifacts/                        # Pipeline run artifacts
├── final_model/                      # Saved production model
├── logs/                             # Runtime log files
├── mlruns/                           # MLflow run metadata
├── .github/workflows/                # CI/CD workflow definitions
│
├── main.py                           # Pipeline entry point
├── push_data.py                      # Utility to push data to MongoDB
├── setup.py                          # Package installation config
├── requirements.txt                  # Python dependencies
├── Dockerfile                        # Container definition
└── test_mongodb.py                   # MongoDB connection test
```

---

## Tech Stack

| Category              | Technology                        |
|-----------------------|-----------------------------------|
| Language              | Python 3.x                        |
| Machine Learning      | scikit-learn                      |
| Data Storage          | MongoDB Atlas (via pymongo)       |
| Experiment Tracking   | MLflow, DagsHub                   |
| Data Processing       | pandas, NumPy                     |
| Configuration         | PyYAML, python-dotenv             |
| Containerisation      | Docker                            |
| CI/CD                 | GitHub Actions                    |

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- A MongoDB Atlas account with a configured cluster
- A DagsHub account (for remote experiment tracking)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/navneetsxngh/Network-Security-System.git
cd Network-Security-System
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file in the project root with the following variables:

```env
MONGO_DB_URL=<your_mongodb_atlas_connection_string>
DAGSHUB_TOKEN=<your_dagshub_access_token>
```

### Pushing Data to MongoDB

If you are setting up the database for the first time, run:

```bash
python push_data.py
```

This utility uploads the raw dataset from the `data/` directory to your configured MongoDB collection.

---

## Running the Pipeline

To execute the full training pipeline:

```bash
python main.py
```

The pipeline will run the four stages in sequence. Progress and stage outputs are logged to the console and to files under the `logs/` directory. Serialised artifacts from each stage are saved under `Artifacts/`.

### Running with Docker

```bash
docker build -t network-security-system .
docker run --env-file .env network-security-system
```

---

## Experiment Tracking

The project integrates with **MLflow** and **DagsHub** for experiment management. Each pipeline run logs:

- Hyperparameters and model configuration
- Evaluation metrics (accuracy, F1-score, precision, recall)
- Serialised model artifacts

To view the MLflow UI locally:

```bash
mlflow ui
```

Then open `http://localhost:5000` in your browser.

For remote tracking, experiments are synchronised to your DagsHub repository automatically when the `DAGSHUB_TOKEN` environment variable is set.

---

## License

This project is licensed under the **Apache License 2.0**. See the [LICENSE](LICENSE) file for details.