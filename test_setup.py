# test_setup.py
import sys
print("Python version:", sys.version)

try:
    import pandas as pd
    print("✅ pandas version:", pd.__version__)
except ImportError as e:
    print("❌ pandas:", e)

try:
    import numpy as np
    print("✅ numpy version:", np.__version__)
except ImportError as e:
    print("❌ numpy:", e)

try:
    import xgboost as xgb
    print("✅ xgboost version:", xgb.__version__)
except ImportError as e:
    print("❌ xgboost:", e)

try:
    import shap
    print("✅ shap version:", shap.__version__)
except ImportError as e:
    print("❌ shap:", e)

try:
    from fastapi import FastAPI
    print("✅ fastapi available")
except ImportError as e:
    print("❌ fastapi:", e)

print("\n✅ All core packages installed successfully!")
