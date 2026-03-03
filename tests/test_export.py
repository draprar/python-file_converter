import pandas as pd
from file_converter.exporters.csv_exporter import export_csv


def test_export_csv_creates_file(tmp_path):
    df = pd.DataFrame({"a": [1, 2, 3]})
    output = tmp_path / "out.csv"

    export_csv(df, output)

    assert output.exists()
    loaded = pd.read_csv(output)
    assert loaded.shape == (3, 1)