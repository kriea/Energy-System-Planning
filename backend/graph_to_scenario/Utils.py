"""
This file contains utility functions for the graph_to_scenario module
conains functions to laod json files, excel files
"""

import json
import pandas as pd
from pathlib import Path


@staticmethod
def load_json(file_path):
    """Loads a JSON file from the given path."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file at {file_path}")
    except Exception as e:
        print(f"Unexpected error loading JSON file: {e}")
    return {}


@staticmethod
def load_excel(file_path: str, sheet_name: str) -> pd.DataFrame:
    """
    Loads an Excel file from the given path and sheet name.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str): The name of the sheet to load.

    Returns:
        pd.DataFrame: The loaded DataFrame with cleaned column names.
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, sheet_name=sheet_name)

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Unexpected error loading Excel file: {e}")

    # Return an empty DataFrame on error
    return pd.DataFrame()


@staticmethod
def load_default_technology_data(default_values_excel: str) -> dict:
    """
    Loads defaults from the given Excel sheet and stores them in a dictionary.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str): The name of the sheet to load (default is "Technology").

    Returns:
        dict: A dictionary where the key is the technology type and the value is its defaults.
    """
    try:
        # Load the specified sheet
        df = load_excel(default_values_excel, "Technology")  # pandas dataframe

        # Create a dictionary to store defaults
        defaults = {}
        for _, row in df.iterrows():
            # Skip rows with an empty or missing "technology_type"
            if pd.isna(row.get("technology_type")) or row.isnull().all():
                continue

            # Use the "technology_type" column as the key
            tech_type = row["technology_type"].strip().lower()

            # Convert the row to a dictionary of defaults (excluding the "technology_type" column)
            defaults[tech_type] = row.drop("technology_type").to_dict()

        return defaults
    except FileNotFoundError:
        print(f"Error: File not found at {default_values_excel}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return {}


@staticmethod
def get_timestep(
    file_path: str, scenario_name: str = "default", sheet_name: str = "Timestep"
) -> str:
    """
    Gets the timestep for a specific scenario name from the given Excel file.

    Args:
        file_path (str): Path to the Excel file.
        scenario_name (str): The name of the scenario to fetch the timestep for (default is "default").
        sheet_name (str): The name of the sheet to load (default is "Timestep").

    Returns:
        str: The timestep for the given scenario name. Returns None if not found.
    """
    try:
        # Load the Timestep sheet
        df = load_excel(file_path, "Timestep")

        # Create a dictionary where the key is the scenario name and the value is the timestep
        timesteps = {}
        for _, row in df.iterrows():
            # Skip rows with an empty or missing "scenario name"
            if pd.isna(row.get("scenario name")) or row.isnull().all():
                continue

            # Use the "scenario name" column as the key
            scenario = row["scenario name"].strip().lower()

            # Store the timestep value
            timesteps[scenario] = row["timestep"]

        # Return the timestep for the requested scenario
        return timesteps.get(scenario_name.lower(), None)  # None if not found
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None
