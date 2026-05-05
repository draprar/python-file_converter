"""
End-to-end CLI tests.
Tests CLI interface, exit codes, error handling, and user-facing behavior.
"""

import subprocess
import sys

import pandas as pd
import pytest


@pytest.fixture
def sample_csv(tmp_path):
    """Create sample CSV file for testing."""
    file = tmp_path / "sample.csv"
    df = pd.DataFrame(
        {"name": ["Alice", "Bob", "Charlie"], "age": [30, 25, 35], "city": ["NYC", "LA", "Chicago"]}
    )
    df.to_csv(file, index=False)
    return file


@pytest.fixture
def sample_json(tmp_path):
    """Create sample JSON file for testing."""
    import json

    file = tmp_path / "sample.json"
    data = [{"id": 1, "value": 100}, {"id": 2, "value": 200}]
    file.write_text(json.dumps(data))
    return file


def run_convert_cli(args, cwd=None):
    """Run convert CLI and return (exit_code, stdout, stderr)."""
    cmd = [sys.executable, "-m", "file_converter.cli"] + args
    result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


class TestCLIBasic:
    """Test basic CLI functionality."""

    def test_cli_no_args_shows_error(self):
        """Test that running without input argument returns error code."""
        exit_code, stdout, stderr = run_convert_cli([])
        assert exit_code == 1
        assert "Error" in stderr or "Error" in stdout

    def test_cli_list_formats(self):
        """Test --list-formats argument."""
        exit_code, stdout, stderr = run_convert_cli(["--list-formats"])
        assert exit_code == 0
        assert ".csv" in stdout
        assert ".parquet" in stdout
        assert ".json" in stdout

    def test_cli_missing_input_file_returns_error(self):
        """Test that missing input file returns error code 1."""
        exit_code, stdout, stderr = run_convert_cli(["nonexistent.csv"])
        assert exit_code == 1
        assert "Error" in stderr


class TestCLIConversion:
    """Test actual conversion workflows."""

    def test_csv_to_parquet_default(self, sample_csv, tmp_path, monkeypatch):
        """Test default conversion from CSV to Parquet."""
        from file_converter.cli import main

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)
        monkeypatch.setattr("file_converter.cli.DATA_OUTPUT_DIR", tmp_path)
        monkeypatch.setattr("sys.argv", ["convert", str(sample_csv)])

        exit_code = main()

        assert exit_code == 0

        output_file = tmp_path / "sample.parquet"
        assert output_file.exists()

    def test_csv_to_csv_explicit(self, sample_csv, tmp_path, monkeypatch):
        """Test explicit CSV to CSV conversion."""
        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)
        monkeypatch.setattr("file_converter.cli.DATA_OUTPUT_DIR", tmp_path)

        output_file = tmp_path / "result.csv"
        exit_code, stdout, stderr = run_convert_cli(
            [str(sample_csv), str(output_file)], cwd=tmp_path
        )

        assert exit_code == 0
        assert output_file.exists()

        df = pd.read_csv(output_file)
        assert df.shape == (3, 3)

    def test_json_to_csv(self, sample_json, tmp_path, monkeypatch):
        """Test JSON to CSV conversion."""
        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_json.parent)
        monkeypatch.setattr("file_converter.cli.DATA_OUTPUT_DIR", tmp_path)

        output_file = tmp_path / "output.csv"
        exit_code, stdout, stderr = run_convert_cli(
            [str(sample_json), str(output_file)], cwd=tmp_path
        )

        assert exit_code == 0
        assert output_file.exists()


class TestCLIPreview:
    """Test --preview functionality."""

    def test_preview_shows_dataset_info(self, sample_csv, tmp_path, monkeypatch):
        """Test that --preview displays dataset structure."""
        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)
        monkeypatch.setattr("file_converter.cli.DATA_OUTPUT_DIR", tmp_path)

        exit_code, stdout, stderr = run_convert_cli([str(sample_csv), "--preview"], cwd=tmp_path)

        assert exit_code == 0
        assert "Rows: 3" in stdout
        assert "Columns: 3" in stdout
        assert "name" in stdout
        assert "age" in stdout


class TestCLIDropEmpty:
    """Test --drop-empty functionality."""

    def test_drop_empty_removes_null_columns(self, tmp_path, monkeypatch):
        """Test that --drop-empty removes columns with all NaN values."""
        # Create CSV with empty column
        csv_file = tmp_path / "data_with_empty.csv"
        df = pd.DataFrame(
            {"col1": [1, 2, 3], "empty_col": [None, None, None], "col2": ["a", "b", "c"]}
        )
        df.to_csv(csv_file, index=False)

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", tmp_path)
        monkeypatch.setattr("file_converter.cli.DATA_OUTPUT_DIR", tmp_path)

        output_file = tmp_path / "result.csv"
        exit_code, stdout, stderr = run_convert_cli(
            [str(csv_file), str(output_file), "--drop-empty"], cwd=tmp_path
        )

        assert exit_code == 0

        result = pd.read_csv(output_file)
        assert list(result.columns) == ["col1", "col2"]


class TestCLIErrorHandling:
    """Test CLI error handling and exit codes."""

    def test_unsupported_output_format(self, sample_csv, tmp_path, monkeypatch):
        """Test that unsupported output format returns error code 1."""
        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)
        monkeypatch.setattr("file_converter.cli.DATA_OUTPUT_DIR", tmp_path)

        output_file = tmp_path / "output.xyz"
        exit_code, stdout, stderr = run_convert_cli(
            [str(sample_csv), str(output_file)], cwd=tmp_path
        )

        assert exit_code == 1
        assert "Unsupported output format" in stderr

    def test_malformed_json_returns_error(self, tmp_path, monkeypatch):
        """Test that malformed JSON file returns error code 1."""
        bad_json = tmp_path / "bad.json"
        bad_json.write_text("{invalid json}")

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", tmp_path)
        monkeypatch.setattr("file_converter.cli.DATA_OUTPUT_DIR", tmp_path)

        exit_code, stdout, stderr = run_convert_cli([str(bad_json)], cwd=tmp_path)

        assert exit_code == 1
        assert "Error" in stderr

    def test_create_output_directory_if_not_exists(self, sample_csv, tmp_path, monkeypatch):
        """Test that output directory is created automatically."""
        from file_converter.cli import main

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)

        # Nested directory that doesn't exist
        output_dir = tmp_path / "nested" / "deep" / "output"
        output_file = output_dir / "result.csv"

        # Run CLI
        monkeypatch.setattr("sys.argv", ["convert", str(sample_csv), str(output_file)])
        exit_code = main()

        assert exit_code == 0
        assert output_dir.exists()
        assert output_file.exists()


class TestCLINewFeatures:
    """Test new features added in refactoring."""

    def test_empty_dataframe_warning(self, tmp_path, monkeypatch):
        """Test that empty DataFrame shows warning."""
        from file_converter.cli import main

        # Create empty CSV
        empty_csv = tmp_path / "empty.csv"
        empty_csv.write_text("col1,col2\n")  # Header only, no data

        output = tmp_path / "out.csv"

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", tmp_path)
        monkeypatch.setattr("sys.argv", ["convert", str(empty_csv), str(output)])

        import io

        captured_stderr = io.StringIO()
        original_stderr = sys.stderr
        sys.stderr = captured_stderr

        try:
            exit_code = main()
            stderr_output = captured_stderr.getvalue()
        finally:
            sys.stderr = original_stderr

        assert exit_code == 0
        assert "Warning: Loaded DataFrame is empty" in stderr_output

    def test_drop_empty_shows_feedback(self, tmp_path, monkeypatch, capsys):
        """Test that --drop-empty shows how many columns were dropped."""
        from file_converter.cli import main

        # Create CSV with empty columns
        csv_file = tmp_path / "data.csv"
        df = pd.DataFrame(
            {
                "col1": [1, 2, 3],
                "empty1": [None, None, None],
                "col2": ["a", "b", "c"],
                "empty2": [None, None, None],
            }
        )
        df.to_csv(csv_file, index=False)

        output = tmp_path / "out.csv"

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", tmp_path)
        monkeypatch.setattr("sys.argv", ["convert", str(csv_file), str(output), "--drop-empty"])

        exit_code = main()

        assert exit_code == 0

        captured = capsys.readouterr()
        assert "Dropped 2 empty column(s)" in captured.out

        # Verify actual columns removed
        result = pd.read_csv(output)
        assert list(result.columns) == ["col1", "col2"]

    def test_preview_and_drop_empty_combined(self, tmp_path, monkeypatch, capsys):
        """Test combining --preview and --drop-empty flags."""
        from file_converter.cli import main

        # Create CSV with empty column
        csv_file = tmp_path / "data.csv"
        df = pd.DataFrame({"col1": [1, 2, 3], "empty": [None, None, None], "col2": ["a", "b", "c"]})
        df.to_csv(csv_file, index=False)

        output = tmp_path / "out.csv"

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", tmp_path)
        monkeypatch.setattr(
            "sys.argv", ["convert", str(csv_file), str(output), "--preview", "--drop-empty"]
        )

        exit_code = main()

        assert exit_code == 0

        captured = capsys.readouterr()
        assert "Dropped 1 empty column(s)" in captured.out
        assert "Preview:" in captured.out
        assert "Columns: 2" in captured.out  # After dropping

        result = pd.read_csv(output)
        assert list(result.columns) == ["col1", "col2"]


class TestCLIVerboseMode:
    """Test --verbose flag functionality."""

    def test_verbose_mode_shows_file_info(self, sample_csv, tmp_path, monkeypatch, capsys):
        """Test that --verbose shows detailed file information."""
        from file_converter.cli import main

        output = tmp_path / "out.parquet"

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)
        monkeypatch.setattr("sys.argv", ["convert", str(sample_csv), str(output), "--verbose"])

        exit_code = main()

        assert exit_code == 0

        captured = capsys.readouterr()
        # Check for verbose output
        assert "Input file:" in captured.out
        assert "File size:" in captured.out
        assert "Format:" in captured.out
        assert "Loaded" in captured.out
        assert "rows" in captured.out
        assert "columns" in captured.out
        assert "Memory usage:" in captured.out
        assert "Column types:" in captured.out

    def test_verbose_with_preview_combined(self, sample_csv, tmp_path, monkeypatch, capsys):
        """Test combining --verbose and --preview flags."""
        from file_converter.cli import main

        output = tmp_path / "out.csv"

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)
        monkeypatch.setattr(
            "sys.argv", ["convert", str(sample_csv), str(output), "--verbose", "--preview"]
        )

        exit_code = main()

        assert exit_code == 0

        captured = capsys.readouterr()
        # Should show both verbose info and preview
        assert "Input file:" in captured.out
        assert "Memory usage:" in captured.out
        assert "Preview:" in captured.out
        assert "Column names:" in captured.out

    def test_verbose_short_flag(self, sample_csv, tmp_path, monkeypatch, capsys):
        """Test that -v short flag works."""
        from file_converter.cli import main

        output = tmp_path / "out.parquet"

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", sample_csv.parent)
        monkeypatch.setattr("sys.argv", ["convert", str(sample_csv), str(output), "-v"])

        exit_code = main()

        assert exit_code == 0

        captured = capsys.readouterr()
        assert "Input file:" in captured.out
        assert "Loaded" in captured.out


class TestCLIPathTraversal:
    """Test path traversal warnings."""

    def test_path_outside_data_input_shows_warning(self, tmp_path, monkeypatch, capsys):
        """Test that reading from outside data/input shows a warning."""
        from file_converter.cli import main

        # Create file outside data/input
        external_file = tmp_path / "external.csv"
        df = pd.DataFrame({"a": [1, 2, 3]})
        df.to_csv(external_file, index=False)

        output = tmp_path / "out.parquet"

        # Set DATA_INPUT_DIR to different location
        data_input = tmp_path / "data" / "input"
        data_input.mkdir(parents=True)

        monkeypatch.setattr("file_converter.cli.DATA_INPUT_DIR", data_input)
        monkeypatch.setattr("sys.argv", ["convert", str(external_file), str(output)])

        exit_code = main()

        assert exit_code == 0

        captured = capsys.readouterr()
        # Should show warning about reading from absolute path
        assert "Note: Reading from absolute path outside data/input" in captured.err
