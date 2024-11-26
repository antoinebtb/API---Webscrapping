import os
import json
import kaggle
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

# Define the router
router = APIRouter()

# Load the datasets information from the JSON file
def load_datasets_info():
    current_dir = os.path.dirname(__file__)
    json_file_path = os.path.join(current_dir, "../../config/Dataset.json")
    
    absolute_path = os.path.abspath(json_file_path)
    print(f"Vérification du fichier JSON à: {absolute_path}")
    
    if not os.path.exists(absolute_path):
        print(f"Le fichier Dataset.json n'a pas été trouvé à l'emplacement: {absolute_path}")
        raise HTTPException(status_code=500, detail=f"Le fichier Dataset.json n'a pas été trouvé à l'emplacement: {absolute_path}")
    
    try:
        with open(absolute_path, "r") as json_file:
            datasets_info = json.load(json_file)
        print(f"Le fichier Dataset.json a été chargé avec succès depuis {absolute_path}")
        return datasets_info['datasets']
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la lecture du fichier JSON: {str(e)}")

# Define the dataset download function
def download_dataset_by_name(dataset_name: str):
    datasets_info = load_datasets_info()

    # Find the dataset in the JSON data
    dataset = next((item for item in datasets_info if item["name"].lower() == dataset_name.lower()), None)

    if not dataset:
        raise HTTPException(status_code=404, detail=f"Dataset '{dataset_name}' not found in the JSON file.")

    # Path where the dataset will be saved
    dataset_dir = os.path.join("../../Data")
    os.makedirs(dataset_dir, exist_ok=True)

    try:
        print(f"Attempting to download dataset with ID: {dataset['dataset_id']} to {dataset_dir}")
        
        # Download the dataset using Kaggle API
        kaggle.api.dataset_download_files(dataset["dataset_id"], path=dataset_dir, unzip=True)
        print(f"Dataset '{dataset_name}' downloaded successfully!")
        return {"message": f"Dataset '{dataset_name}' downloaded successfully!"}
    except kaggle.api.kaggle_api_exception.KaggleApiException as e:
        print(f"Kaggle API error: {e}")  # Print error from Kaggle API
        raise HTTPException(status_code=500, detail=f"Kaggle API error: {str(e)}")
    except Exception as e:
        print(f"Error during downloading dataset: {str(e)}")  # Print error for debugging
        raise HTTPException(status_code=500, detail=f"Error downloading dataset: {str(e)}")

# Define the route to trigger dataset download by name
@router.get("/download-dataset/{dataset_name}")
def download_dataset(dataset_name: str):
    """
    Downloads and saves a dataset from Kaggle based on the name provided in the request.
    """
    try:
        # Essayer de télécharger le dataset
        response = download_dataset_by_name(dataset_name)
        return JSONResponse(content=response)
    except HTTPException as e:
        # Si une exception HTTP se produit (comme fichier non trouvé ou autre erreur)
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
