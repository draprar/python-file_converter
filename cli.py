import argparse
from pathlib import Path

from file_converter.core.pipeline import load_file
from file_converter.exporters.csv_exporter import export_csv
from file_converter.exporters.parquet_exporter import export_parquet


def main():
    parser = argparse.ArgumentParser(
        description="Universal file → DataFrame → export tool"
    )

    parser.add_argument(
        "input",
        help="Input file path"
    )

    parser.add_argument(
        "-o", "--output",
        default="data/output/output.parquet",
        help="Output file path"
    )

    parser.add_argument(
        "--format",
        choices=["csv", "parquet"],
        default="parquet",
        help="Output format"
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Show DataFrame preview"
    )

    parser.add_argument(
        "--drop-empty",
        action="store_true",
        help="Drop columns with all NaN values"
    )

    args = parser.parse_args()

    df = load_file(args.input)

    if args.drop_empty:
        df = df.dropna(axis=1, how="all")

    if args.preview:
        print("\n--- PREVIEW (first 3 rows) ---")
        print(df.head(3))
        print("\n--- SHAPE ---")
        print(df.shape)
        print("\n--- COLUMNS ---")
        for col in df.columns:
            print(col)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "csv":
        export_csv(df, output)
    else:
        export_parquet(df, output)

    print(f"\n✔ Saved → {output}")


if __name__ == "__main__":
    main()
