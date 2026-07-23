"""
Trains the minimal and elaborate life expectancy models via predict.py's
train_life_expectancy_model function, and saves each as a bundle
(pipeline + metrics + feature list) under models/, for app.py to load.
"""

import os

import joblib

from predict import train_life_expectancy_model

MODEL_DIR = "models"


def main() -> None:
    os.makedirs(MODEL_DIR, exist_ok=True)

    for name, include_sensitive in [("minimal", False), ("elaborate", True)]:
        result = train_life_expectancy_model(include_sensitive=include_sensitive)

        bundle = {
            "pipeline": result["model"],
            "features": result["features"],
            "train_metrics": result["train_metrics"],
            "test_metrics": result["test_metrics"],
        }

        path = os.path.join(MODEL_DIR, f"{name}.pkl")
        joblib.dump(bundle, path)

        print(f"saved {path}")
        print(f"  features: {result['features']}")
        print(f"  test rmse: {result['test_metrics']['rmse']:.3f}")
        print(f"  test adj r2: {result['test_metrics']['adj_r2']:.3f}")


if __name__ == "__main__":
    main()
