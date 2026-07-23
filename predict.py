"""
Training function for the WHO Life Expectancy linear regression model.

This module provides a function to train a linear regression model
on the WHO Life Expectancy dataset, with an option to include or
exclude sensitive features from the training process.

It also provides an interactive prediction function that:
1. Prompts the user for consent to use sensitive data.
2. Collects Pydantic-validated inputs for the chosen model.
3. Returns a life expectancy prediction with expected error (RMSE).
"""

from __future__ import annotations

from typing import Literal

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, ValidationError
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


# ---------------------------------------------------------------------------
# Pydantic models for input validation
# ---------------------------------------------------------------------------

REGION_LIST = [
    "Africa",
    "Asia",
    "Central America and Caribbean",
    "European Union",
    "Middle East",
    "North America",
    "Oceania",
    "Rest of Europe",
    "South America",
]

VALID_REGIONS = Literal[
    "Africa",
    "Asia",
    "Central America and Caribbean",
    "European Union",
    "Middle East",
    "North America",
    "Oceania",
    "Rest of Europe",
    "South America",
]


class SensitiveModelInput(BaseModel):
    """Input schema for the full (sensitive) model."""

    Region: VALID_REGIONS = Field(
        description="Geographic region of the country"
    )
    GDP_per_capita: float = Field(
        gt=0, description="GDP per capita (USD)"
    )
    Adult_mortality: float = Field(
        ge=0,
        description="Adult mortality rate (probability of dying between 15-60 years per 1000 population)",
    )
    Under_five_deaths: float = Field(
        ge=0,
        description="Deaths of children under five years old per 1000 live births",
    )
    Economy_status_Developed: int = Field(
        ge=0, le=1, description="1 if the country is developed, 0 otherwise"
    )


class MinimalModelInput(BaseModel):
    """Input schema for the minimal (non-sensitive) model."""

    Region: VALID_REGIONS = Field(
        description="Geographic region of the country"
    )
    Year: int = Field(
        ge=2000, le=2030, description="Year of the record (2000-2030)"
    )
    GDP_per_capita: float = Field(
        gt=0, description="GDP per capita (USD)"
    )
    Population_mln: float = Field(
        gt=0, description="Population in millions"
    )

    @property
    def log_GDP(self) -> float:
        """Natural log of GDP per capita, computed from raw input."""
        return float(np.log(self.GDP_per_capita))

    @property
    def log_Population(self) -> float:
        """Natural log of population (millions), computed from raw input."""
        return float(np.log(self.Population_mln))


def train_life_expectancy_model(include_sensitive: bool = True,
                                test_size: float = 0.2,
                                random_state: int = 42):   
    """
    Train a linear regression model for predicting life expectancy.

    Parameters
    ----------
    include_sensitive : bool, default=True
        If True, use all available features including sensitive ones
        (e.g., Infant_deaths, Adult_mortality, HIV incidents, etc.).
        If False, use only a reduced set of less sensitive features
        (e.g., Log_GDP, Log_population, Schooling, Economy_status).
    test_size : float, default=0.2
        Proportion of the dataset to include in the test split.
    random_state : int, default=42
        Random state for reproducibility of the train/test split.
    n_features_to_select : int, default=5
        Number of features to select via backward sequential feature selection.

    Returns
    -------
    dict
        A dictionary containing:
        - 'train_metrics': dict with 'rmse' and 'adj_r2' for training set
        - 'test_metrics': dict with 'rmse' and 'adj_r2' for testing set
        - 'model': the fitted Pipeline object (preprocessor + selector + model)
    """
    # Load and prepare the data
    data = pd.read_csv('Life Expectancy Data.csv')

    # Feature engineering: log transforms to make skewed distributions approximate a normal distribution
    data['log_GDP'] = np.log(data['GDP_per_capita'])
    data['log_Population'] = np.log(data['Population_mln'])
    data['Child_mortality_1_to_5'] = data['Under_five_deaths'] - data['Infant_deaths'] 

    # Define feature sets based on sensitivity flag
    if include_sensitive:
        feature_df = data[['Region',
                           'GDP_per_capita',
                        #    'log_GDP',
                           'Adult_mortality',
                        #    'Child_mortality_1_to_5',
                           'Under_five_deaths',
                        #    'Infant_deaths',
                           'Economy_status_Developed',
                           'Life_expectancy']]
    else:
        feature_df = data[['Region',
                           'Year',
                        #    'GDP_per_capita',
                           'log_GDP',
                        #    'Population_mln',
                           'log_Population',
                        #    'Schooling',
                        #    'Economy_status_Developed',
                           'Life_expectancy']]

    X = feature_df.drop(columns=['Life_expectancy'])
    y = feature_df['Life_expectancy']

    # Identify column types for preprocessing
    numeric_features = X.select_dtypes(include=["int64", "float64"]).columns
    categorical_features = X.select_dtypes(include=["object"]).columns

    # Drop 'Country' from categorical features (too many unique values for OHE)
    if 'Country' in categorical_features:
        categorical_features = categorical_features.drop('Country')

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        shuffle=True
    )

    # Build preprocessing pipeline
    numeric_transformer = Pipeline([
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ('encoder', OneHotEncoder(drop='first', handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
    # Full pipeline
    pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])

    # Fit the pipeline
    pipeline.fit(X_train, y_train)

    # Get the number of features selected for adjusted R2 calculation
    n_selected = len(pipeline.named_steps['model'].coef_)
    
    # Get the feature names used in the model
    all_feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()
    clean_names = [name.split("__", 1)[1] for name in all_feature_names]

    # Get the best model
    best_model = pipeline.named_steps['model']

    # Calculate metrics
    train_predictions = pipeline.predict(X_train)
    test_predictions = pipeline.predict(X_test)

    train_rmse = root_mean_squared_error(y_train, train_predictions)
    test_rmse = root_mean_squared_error(y_test, test_predictions)

    train_adj_r2 = _adj_r2_score(y_train, train_predictions, n_selected)
    test_adj_r2 = _adj_r2_score(y_test, test_predictions, n_selected)

    train_metrics = {
        'rmse': train_rmse,
        'adj_r2': train_adj_r2,
    }

    test_metrics = {
        'rmse': test_rmse,
        'adj_r2': test_adj_r2,
    }

    return {
        'train_metrics': train_metrics,
        'test_metrics': test_metrics,
        'model': pipeline,
        'features': clean_names,
        'best_model': best_model
    }


def _adj_r2_score(y_true, y_pred, n_features):
    """Calculate adjusted R-squared score."""
    r2 = r2_score(y_true, y_pred)
    n = len(y_true)
    adjusted_r2 = 1 - ((1 - r2) * (n - 1) / (n - n_features - 1))
    return adjusted_r2


def predict_life_expectancy() -> None:
    """
    Interactive prediction function.

    1. Asks the user for consent to use sensitive (advanced) population data.
    2. Trains the appropriate model.
    3. Prompts the user for feature values (Pydantic-validated).
    4. Outputs the predicted life expectancy and expected error (RMSE).
    """
    # --- Consent prompt (as specified by WHO project brief) ---
    consent = input(
        "Do you consent to using advanced population data, which may "
        "include protected information, for better accuracy? (Y/N): "
    ).strip().upper()

    include_sensitive = consent == "Y"

    if include_sensitive:
        print("\n[Using ELABORATE model with sensitive features]\n")
    else:
        print("\n[Using MINIMAL model without sensitive features]\n")

    # Train the selected model
    result = train_life_expectancy_model(include_sensitive=include_sensitive)
    pipeline = result["model"]
    test_rmse = result["test_metrics"]["rmse"]

    # --- Collect user inputs with Pydantic validation ---
    print("Please enter the following population statistics:\n")

    if include_sensitive:
        input_data = _collect_sensitive_input()
        # Build a DataFrame matching the model's expected columns
        df_input = pd.DataFrame([{
            "Region": input_data.Region,
            "GDP_per_capita": input_data.GDP_per_capita,
            "Adult_mortality": input_data.Adult_mortality,
            "Under_five_deaths": input_data.Under_five_deaths,
            "Economy_status_Developed": input_data.Economy_status_Developed,
        }])
    else:
        input_data = _collect_minimal_input()
        df_input = pd.DataFrame([{
            "Region": input_data.Region,
            "Year": input_data.Year,
            "log_GDP": input_data.log_GDP,
            "log_Population": input_data.log_Population,
        }])

    # --- Prediction ---
    prediction = pipeline.predict(df_input)[0]

    print("\n" + "=" * 50)
    print(f"  Predicted Life Expectancy: {prediction:.2f} years")
    print(f"  Expected Error (RMSE):     ±{test_rmse:.2f} years")
    print("=" * 50 + "\n")


def _prompt_region() -> str:
    """Display a numbered list of regions and return the selected region name."""
    print("  Region:\n")
    for i, region in enumerate(REGION_LIST, start=1):
        print(f"    {i}. {region}")
    choice = input("\n  Enter region number: ")
    idx = int(choice) - 1
    if idx < 0 or idx >= len(REGION_LIST):
        raise ValueError(f"Invalid choice. Please enter a number between 1 and {len(REGION_LIST)}.")
    return REGION_LIST[idx]


def _collect_sensitive_input() -> SensitiveModelInput:
    """Prompt the user for sensitive model features with validation."""
    while True:
        try:
            region = _prompt_region()
            gdp = input("  GDP per capita (USD, e.g. 11006): ")
            adult_mort = input("  Adult mortality rate (per 1000, e.g. 105.82): ")
            under_five = input("  Under-five deaths (per 1000 live births, e.g. 13.0): ")
            economy = input("  Economy status developed? (1=Yes, 0=No): ")

            data = SensitiveModelInput(
                Region=region.strip(),
                GDP_per_capita=float(gdp),
                Adult_mortality=float(adult_mort),
                Under_five_deaths=float(under_five),
                Economy_status_Developed=int(economy),
            )
            return data
        except (ValidationError, ValueError) as e:
            print(f"\n  [Validation Error] {e}\n  Please try again.\n")


def _collect_minimal_input() -> MinimalModelInput:
    """Prompt the user for minimal model features with validation."""
    while True:
        try:
            region = _prompt_region()
            year = input("  Year (2000-2030, e.g. 2015): ")
            gdp = input("  GDP per capita (USD, e.g. 11006): ")
            pop = input("  Population in millions (e.g. 78.53): ")

            data = MinimalModelInput(
                Region=region.strip(),
                Year=int(year),
                GDP_per_capita=float(gdp),
                Population_mln=float(pop),
            )
            return data
        except (ValidationError, ValueError) as e:
            print(f"\n  [Validation Error] {e}\n  Please try again.\n")


if __name__ == '__main__':
    predict_life_expectancy()