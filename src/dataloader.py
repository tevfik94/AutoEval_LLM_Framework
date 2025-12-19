import pandas as pd
import yaml
import os


class DataLoader:
    def __init__(self, config_path="config.yaml"):
        """
        Initialize the loader by reading the config file.
        """
        self.config = self._load_config(config_path)

    def _load_config(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found at {path}")
        with open(path, "r") as file:
            return yaml.safe_load(file)

    def load_data(self):
        """
        Reads the CSV and creates a standardized list of records.
        Returns: List of dictionaries ready for the Judge.
        """
        input_path = self.config["input_file"]
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Data file not found at {input_path}")

        # Load CSV
        # checks if it is csv or excel
        if input_path.endswith(".csv"):
            df = pd.read_csv(input_path)
        elif input_path.endswith(".xlsx"):
            df = pd.read_excel(input_path)
        else:
            raise ValueError("Unsupported file format. Please use .csv or .xlsx")

        # Get column mappings from config
        mapping = self.config["columns"]
        q_col = mapping["question_col"]
        a_col = mapping["answer_col"]
        cap_col = mapping["capability_col"]
        gt_col = mapping.get("ground_truth_col", None)

        # Validate columns exist
        missing_cols = [c for c in [q_col, a_col, cap_col] if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing columns in CSV: {missing_cols}")

        # Standardize Data
        records = []
        for index, row in df.iterrows():
            record = {
                "id": index,
                "question": row[q_col],
                "answer": row[a_col],
                "capability": row[cap_col],
                "ground_truth": (
                    row[gt_col] if gt_col and gt_col in df.columns else None
                ),
            }
            records.append(record)

        print(f"✅ Successfully loaded {len(records)} records from {input_path}")
        return records


# Simple test block to run this file directly
if __name__ == "__main__":
    loader = DataLoader()
    data = loader.load_data()
    print("Sample Record:", data[0])

import sys

print(sys.executable)
