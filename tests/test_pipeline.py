import pandas as pd
import pytest

from file_converter.core.pipeline import load_file


def test_load_csv_success(tmp_path):
    file = tmp_path / "data.csv"
    file.write_text("a,b\n1,2\n3,4")

    df = load_file(file)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)


def test_load_missing_file(tmp_path):
    file = tmp_path / "missing.csv"

    with pytest.raises(ValueError):
        load_file(file)


def test_load_unsupported_extension(tmp_path):
    file = tmp_path / "data.xyz"
    file.write_text("dummy")

    with pytest.raises(ValueError):
        load_file(file)