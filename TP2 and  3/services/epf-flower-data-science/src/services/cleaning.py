import os
import pandas as pd

def clean_dataset(filename: str):
    """
    Cleans the dataset by removing rows with any missing values.

    Args:
        filename (str): Name of the CSV dataset file (located in the Data folder).

    Returns:
        pd.DataFrame: The cleaned dataset with no empty rows.
    """
    # Define the path to the Data folder
    data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../Data"))
    print(f"Data folder path: {data_folder}")
    file_path = os.path.join(data_folder, filename)

    try:
        # Read the dataset
        df = pd.read_csv(file_path)

        # Remove rows with any missing values
        df_cleaned = df.dropna()

        return df_cleaned
    except FileNotFoundError:
        raise ValueError(f"File '{filename}' not found in the Data folder.")
    except Exception as e:
        raise ValueError(f"Error cleaning the dataset: {str(e)}")
