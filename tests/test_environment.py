
import numpy as np
import pandas as pd


def test_pandas_dataframe():
    df = pd.DataFrame({
        "product": ["A", "B", "C"],
        "sales": [100, 200, 300],
    })

    assert len(df) == 3
    assert df["sales"].sum() == 600


def test_numpy():
    values = np.array([10, 20, 30])

    assert values.mean() == 20
