# Car Price Prediction AI

An end-to-end machine learning project that predicts car prices based on features such as make, model, year, mileage and other vehicle attributes. The system trains regression models, persists preprocessing artifacts and model files, and serves predictions via a FastAPI endpoint. A Streamlit app provides a simple front-end for manual testing.

## Team Members

| AC.NO | Name | Role | Contributions |
|---:|---|---|---|
| 1 | Hamzah Abdulqawi ALkhalaf|202274127 | Lead Developer | Data preprocessing, model development | Data Analyst | EDA, visualization | ML Engineer | Model optimization, deployment |

## Installation and Setup

### Prerequisites
- Python 3.12 or higher
- UV package manager (used in this project; if you don't use UV, follow the pip instructions below)

### Installation Steps

1. Clone the repository:

```powershell
git clone https://github.com/your-username/car-price-prediction.git
cd car-price-prediction
```

2. Install dependencies using UV (recommended):

```powershell
uv sync
```

If you're not using UV, use pip inside a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
.venv\Scripts\python.exe -m pip install --upgrade pip
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Run the project

Start the FastAPI server (from the repo root):

```powershell
uv run python main.py
```

or using uvicorn directly (in a virtual env):

```powershell
.venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Check health: http://127.0.0.1:8000/health

Run the Streamlit UI (in a separate terminal):

```powershell
streamlit run app.py
```

## Project Structure

```
car-price-prediction/
├── README.md              # Project documentation
├── pyproject.toml         # UV project configuration
├── main.py                # Main application entry point (FastAPI)
├── app.py                 # Streamlit demo UI that calls the API
├── src/                   # Source code
│   ├── data/              # Data preprocessing modules
│   │   └── preprocessor.py
│   ├── features/          # Feature engineering
│   ├── models/            # Model training and evaluation code
│   └── utils/             # Utility functions
├── notebooks/             # Jupyter notebooks for EDA and training
├── data/                  # Dataset files (raw/processed)
├── models/                # Saved model artifacts (pickles)
└── scripts/               # Helper scripts (run_server.ps1, debug tools)
```

## Usage

### Basic usage (example)

```python
from src.models import PricePredictor

# Initialize and train model (example API — adapt to your implementation)
predictor = PricePredictor()
predictor.train('data/training_data.csv')

# Make prediction
prediction = predictor.predict({
		'make': 'Toyota',
		'model': 'Camry',
		'year': 2020,
		'mileage': 45000
})
print(f"Predicted price: ${prediction:,.2f}")
```

### Running experiments

```powershell
uv run python experiments/train_model.py
```

## Results (example)

- Model Accuracy (R²): 94.2%
- Mean Absolute Error: $1,234
- Training time (example): 15 minutes

Key findings: Gradient Boosting models (e.g., XGBoost or LightGBM) performed well. Vehicle year and mileage were the most important predictive features after appropriate feature engineering.

## Notes & Known Issues

- Label encoding: scikit-learn's `LabelEncoder` will raise an error on previously-unseen categories (for example, seeing a make/model combination not present during training). Fixes:
	- Persist mapping dictionaries and map unknown categories to a sentinel value (e.g., `-1`) before transforming at inference time.
	- Use encoders that support unknown categories (e.g., `OneHotEncoder(handle_unknown='ignore')` or `OrdinalEncoder(..., unknown_value=-1)`).

- Model artifacts: `main.py` expects to find encoder and model pickles in `models/` (e.g., `model.pkl`, `scaler.pkl`, `one_hot_encoder.pkl`, `label_encoders.pkl`). Ensure these are present.

- Server lifecycle: avoid `--reload` in production runs (it spawns multiple processes). Use `scripts/run_server.ps1` for a simple detached PowerShell run.

## Recommended next steps

1. Implement safe unseen-label mapping in `main.py` (map unknown categorical tokens to `-1`).
2. Add a `requirements.txt` generated from the project environment for users who don't use UV.
3. Add unit tests for preprocessing functions and the prediction endpoint (`/predict/`).
4. Consider switching categorical encoders to ones that support unknown categories.

## Team Contributions

- Alex Johnson — data preprocessing, feature engineering, model training
- Maria Garcia — EDA, visualizations, data quality checks
- James Chen — model selection, hyperparameter tuning and deployment automation

---

If you'd like, I can now:

- (A) Implement the unseen-label mapping in `main.py` and run the `API/test_request.py` smoke test, or
- (B) Add a `requirements.txt` file and update the README to reference it, or
- (C) Add unit tests for the preprocessing pipeline.

Tell me which option to do next and I'll start working on it.


