# WHO Life Expectancy Prediction

A linear regression project that predicts life expectancy across countries using data provided by the World Health Organisation. The dataset covers records between 2000 and 2015 across 179 countries.

The project includes both a CLI prediction script and an interactive Streamlit web application.

## Project Structure

```
.
├── app/
│   ├── app.py                      # Streamlit web application (main entry point)
│   ├── components.py               # Reusable HTML rendering components
│   ├── colours.py                  # Colour palette and region list constants
│   ├── helpers.py                  # Data loading utilities
│   ├── styles.py                   # Global CSS styles
│   ├── train_and_save_models.py    # Script to train and serialise models
│   ├── models/
│   │   ├── elaborate.pkl           # Pre-trained elaborate model bundle
│   │   └── minimal.pkl             # Pre-trained minimal model bundle
│   ├── Life Expectancy Data.csv    # WHO dataset (app copy)
│   ├── Flag_of_WHO.svg             # WHO flag used in hero banner
│   └── who-emblem.png              # WHO emblem asset
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
├── eda-and-model-creation.ipynb    # Exploratory data analysis and model development notebook
├── Life Expectancy Data.csv        # WHO dataset
├── requirements.txt                # Pinned Python dependencies
└── README.md
```

## Model Training Pipeline

The training pipeline (`train_life_expectancy_model` in `predict.py`) performs the following steps:

1. **Data loading** - Reads the WHO Life Expectancy CSV dataset.
2. **Feature engineering** - Applies log transforms to GDP and population to normalise skewed distributions.
3. **Feature selection** - Selects either a sensitive or minimal feature set based on user consent.
4. **Preprocessing** - Numeric features are standard-scaled; categorical features (Region) are one-hot encoded.
5. **Train/test split** - 80/20 split with a fixed random state for reproducibility.
6. **Model fitting** - A scikit-learn `Pipeline` combining the preprocessor and a `LinearRegression` model.
7. **Evaluation** - Reports RMSE and Adjusted R-squared on both train and test sets.

### Two Models

| Model | Features | Test RMSE |
|-------|----------|-----------|
| Elaborate (sensitive) | Region, GDP per capita, Adult mortality, Under-five deaths, Economy status | ~1.25 |
| Minimal (non-sensitive) | Region, Year, log(GDP per capita), log(Population) | ~4.54 |

The elaborate model uses health-related features that some countries consider sensitive. The minimal model avoids these, relying only on publicly available economic and demographic data.

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

Windows (cmd):
```cmd
venv\Scripts\activate
```

Windows (PowerShell):
```powershell
venv\Scripts\Activate.ps1
```

macOS / Linux:
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

## Streamlit Web Application

The `app/` directory contains a fully interactive Streamlit web application that provides a visual interface for life expectancy prediction.

### Running the App

```bash
streamlit run app/app.py
```

### App Features

- **WHO-branded UI** — Hero banner with the WHO flag, UN Blue colour scheme, and a custom Streamlit theme.
- **Data consent flow** — Users choose whether to allow sensitive health features before any prediction is made.
- **Two model modes** — The app dynamically loads the minimal or elaborate model bundle depending on consent.
- **Live prediction** — Adjustable inputs (region, GDP, population, mortality, etc.) feed straight into the trained scikit-learn pipeline.
- **Confidence visualisation** — Results include a prediction card, an RMSE-based confidence range, and a visual confidence interval bar.
- **Model transparency** — Displays test RMSE and Adjusted R² metrics, plus an expandable "About this estimate" section explaining training data provenance.

### Re-training the Models

If you update the dataset or model logic, regenerate the serialised bundles:

```bash
python app/train_and_save_models.py
```

This trains both the minimal and elaborate pipelines and saves them as `.pkl` files under `app/models/`.

---

## Running the Prediction Script (CLI)

```bash
python predict.py
```

### Features of `predict.py`

- **Data consent prompt** - On launch, asks whether the user consents to using advanced population data (which may include protected information). This determines which model is trained and used.
- **Pydantic-validated input** - All user inputs are validated using Pydantic models with type checking, range constraints, and allowed-value enforcement. Invalid entries display a clear error and re-prompt.
- **Numbered region selection** - Regions are presented as a numbered list so the user only needs to type a number rather than the full region name.
- **Automatic log transforms** - For the minimal model, the user provides raw GDP per capita and population values; log transformations are computed internally.
- **Prediction with confidence context** - The output includes both the predicted life expectancy and the expected error (test RMSE of the model), giving the user a sense of prediction reliability.

### Example CLI Session

```
Do you consent to using advanced population data, which may include
protected information, for better accuracy? (Y/N): N

[Using MINIMAL model without sensitive features]

Please enter the following population statistics:

  Region:
    1. Africa
    2. Asia
    3. Central America and Caribbean
    4. European Union
    5. Middle East
    6. North America
    7. Oceania
    8. Rest of Europe
    9. South America
  Enter region number: 4
  Year (2000-2030, e.g. 2015): 2015
  GDP per capita (USD, e.g. 11006): 25742
  Population in millions (e.g. 78.53): 46.44

==================================================
  Predicted Life Expectancy: 80.12 years
  Expected Error (RMSE):     +/-4.54 years
==================================================
```
