import json
import pandas as pd
import os


class Reporter:
    def __init__(self, config):
        self.output_path = config["output_file"]

    def save_results(self, results):
        """
        Saves the list of evaluated records to JSON and CSV.
        """
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        # 1. Save as JSON (Preserves structure)
        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=4, ensure_ascii=False)

        # 2. Save as CSV (For Excel/Humans)
        # We change the extension from .json to .csv
        csv_path = self.output_path.replace(".json", ".csv")

        # Convert list of dicts to DataFrame
        df = pd.DataFrame(results)

        # Reorder columns to put Score/Reasoning at the front (if they exist)
        cols = [
            "id",
            "score",
            "reasoning",
            "question",
            "answer",
            "ground_truth",
            "capability",
        ]
        # Filter to ensure we only use columns that actually exist in the data
        final_cols = [c for c in cols if c in df.columns]

        df = df[final_cols]
        df.to_csv(
            csv_path, index=False, encoding="utf-8-sig"
        )  # sig handles Arabic encoding in Excel

        print(f"\n📊 Report generated successfully!")
        print(f"   -> JSON: {self.output_path}")
        print(f"   -> CSV:  {csv_path}")
