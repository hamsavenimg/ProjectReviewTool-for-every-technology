import logging
import os
import sys

from bson import ObjectId
from fastapi import FastAPI, HTTPException,File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel
from urllib.parse import unquote
from typing import List
from datetime import datetime
import zipfile
import io

# src/analysis/rating_fast_api.py
from ..config.settings import (db_name,ratings_db,errors_db,projects_db,
    username,
    password,connection
)

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import main_tool_analysis

cluster = MongoClient("mongodb+srv://"+ username + ":" + password + connection)
db = cluster[db_name]

ratings_collection = db[ratings_db]
errors_collection = db[errors_db]
projects_collection = db[projects_db]

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Get current date and time
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M")

# Path to save uploaded files
UPLOAD_FOLDER = "../uploaded_projects"

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# File extension mapping
EXTENSION_FOLDERS = {
    ".java": "java",
    ".py": "python",
    ".js": "eslint",
    ".jsx":"eslint",
    ".ts":"eslint",
    ".tsx":"eslint",
    ".html":"eslint",
    ".css": "css",
    ".cpp": "cpp",
    ".cs": "csharp"
}

# Pydantic model for request validation
class Rating(BaseModel):
    project_name: str
    rating: float
    review: str

# Helper function to convert ObjectId to string
def serialize_doc(doc):
    doc["_id"] = str(doc["_id"])  # Convert ObjectId to string
    return doc

@app.post("/api/upload_project/")
async def upload_project(
project_name: str = Form(...),
        developer_name: str = Form(...),
        description: str = Form(...),
        technology: str = Form(...),
        file: UploadFile = File(...),
):
    # Generate project_id (string format)
    project_id = f"{project_name}_{developer_name}"

    # Check if the project exists
    existing_project = projects_collection.find_one({"_id": project_id})

    # Determine version
    if existing_project:
        new_version = existing_project["version"] + 1
    else:
        new_version = 1

    # Create a folder to store extracted project files
    project_folder = os.path.join(UPLOAD_FOLDER, f"{project_name}_v{new_version}")
    os.makedirs(project_folder, exist_ok=True)

    # store technologies based on file extensions in a set
    uploaded_technologies = set()  # Using a set to avoid duplicates

    # Save the uploaded ZIP file to disk
    zip_file_path = os.path.join(project_folder, f"{project_name}_v{new_version}.zip")
    content = await file.read()  # Read file content

    with open(zip_file_path, "wb") as f:
        f.write(content)

        # Extract ZIP and sort files
        extracted_files = []
        with zipfile.ZipFile(io.BytesIO(content), "r") as zip_ref:
            for file_name in zip_ref.namelist():
                if file_name.endswith("/"):  # Skip directories
                    continue

                file_ext = os.path.splitext(file_name)[1].lower()
                folder_name = EXTENSION_FOLDERS.get(file_ext, "others")  # Default to 'others'

                uploaded_technologies.add(folder_name )

                # Create extension-specific folder inside project folder
                folder_path = os.path.join(project_folder, folder_name)
                os.makedirs(folder_path, exist_ok=True)

                # Extract file to respective folder
                extracted_file_path = os.path.join(folder_path, os.path.basename(file_name))
                with zip_ref.open(file_name) as source, open(extracted_file_path, "wb") as target:
                    target.write(source.read())

                extracted_files.append(extracted_file_path)

    # Prepare project metadata
    project_data = {
        "_id": project_id,  # Use project_id as unique key
        "name": project_name,
        "developer": developer_name,
        "technology": technology,
        "description": description,
        "version": new_version,
        "uploaded_at": datetime.utcnow(),
        "file_path": project_folder,
        "technologies": list(uploaded_technologies),
        "zip_file": content
    }

    # Update or Insert into MongoDB
    if existing_project:
        projects_collection.update_one({"_id": project_id}, {"$set": project_data})
        message = "Project updated successfully"
    else:
        projects_collection.insert_one(project_data)
        message = "New project created successfully"

    return {
        "message": message,
        "project_id": project_id,
        "version": new_version,
        "file_path": project_folder,
        "extracted_files": extracted_files,
    }

@app.post("/api/run_project/{project_id}")
async def run_project(project_id: str):
    # Print all stored project IDs for debugging
    # all_projects = projects_collection.find({}, {"_id": 1})
    # stored_ids = [p["_id"] for p in all_projects]
    # print("Stored Project IDs:", stored_ids)  # Debugging
    #
    # print("Received Project ID:", project_id)  # Debugging
    # Fetch project details from MongoDB
    project = projects_collection.find_one({"_id": project_id})
    if project:
        # print(project["file_path"])  # Extract file path
        # Projects_filepath_read.get_projects_analyze(project_id)
        project_name = project.get("name", "N/A")
        developer = project.get("developer", "N/A")
        technology = project.get("technology", "N/A")
        version = project.get("version", "N/A")
        uploaded_at = project.get("uploaded_at", "N/A")
        file_path = project.get("file_path", "N/A")
        technologies = project.get("technologies", "N/A")
        email = developer + "@uplsnipe.com"
        print(f"Technologies: {technologies}", file_path)
        generated_project_id = f"{project_name}_v{version}_{date_str}{time_str}"
        print("Generated Project ID:", generated_project_id)  # Use project_id in main.py
        main_tool_analysis(generated_project_id, project_name, developer, version, technology,
                                 file_path, technologies, email)
    else:
        print("not found")  # Project not found
        raise HTTPException(status_code=404, detail="Project not found")

@app.get("/api/rating")
async def get_ratings():
    try:
        project_ratings = list(ratings_collection.find({}).sort([("date", -1),("time", -1)]))
        return {"Ratings": [serialize_doc(doc) for doc in project_ratings]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rating")
async def add_rating(rating: Rating):
    try:
        result = ratings_collection.insert_one(rating.model_dump())
        return {"message": "Rating added successfully", "id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/rating/{rating_id}")
async def update_rating(rating_id: str, rating: Rating):
    try:
        updated = ratings_collection .update_one({"_id": ObjectId(rating_id)}, {"$set": rating.dict()})
        if updated.modified_count == 0:
            raise HTTPException(status_code=404, detail="Rating not found")
        return {"message": "Rating updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rating/{rating_id}")
async def get_rating(rating_id: str):
    try:
        project_ratings = ratings_collection.find_one({"_id": rating_id})
        if not project_ratings:
            raise HTTPException(status_code=404, detail="No errors found for the given project")
        return {"Rating": serialize_doc(project_ratings)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data/{project_id}")
async def get_data(project_id: str):
    try:
        decoded_project_id = unquote(project_id)
        # print(f"Decoded project_id: {decoded_project_id}")  # Debugging
        project_errors = errors_collection.find_one({"_id": project_id})
        if not project_errors:
            raise HTTPException(status_code=404, detail="No errors found for the given project")
        return {"Errors": serialize_doc(project_errors)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rating/dashboard/{rating_id}")
def get_project_rating(rating_id: str):
    """Fetch project rating data from MongoDB"""
    logging.info("API Called: /api/project-rating")

    data = ratings_collection.find_one({"_id": rating_id})

    # print("Raw MongoDB Data:", data)  # Debugging

    if not data:
        raise HTTPException(status_code=404, detail="No project rating data found")

    # Extract category scores
    # category_counts = data.get("code_style", 0)
    # print(category_counts)
    # Extract severity counts
    # severity_counts = data.get("critical", 0)

    # Calculate total errors
    total_errors = sum([
        int(data.get("critical", 0)),
        int(data.get("major", 0)),
        int(data.get("minor", 0)),
        int(data.get("warning", 0))
    ])
    # print(f"Total Errors Calculated: {total_errors}")
    #
    # # Pie Chart Data
    pie_chart_data = [
        {"name": "Critical", "value": data.get("critical", 0), "color": "#dc3545"},
        {"name": "Major", "value": data.get("major", 0), "color": "#ff5733"},
        {"name": "Minor", "value": data.get("minor", 0), "color": "#ffc107"},
        {"name": "Warnings", "value": data.get("warning", 0), "color": "#00C49F"},
    ]
    pie_chart_data = [entry for entry in pie_chart_data if entry["value"] > 0]  # Remove empty entries

    # Bar Chart Data
    bar_chart_data = [
        {"category": "Code Style", "score": data.get("code_style", 0), "color": "#9F9FF8"},
        {"category": "Best Practices", "score": data.get("best_practices", 0), "color": "#0000FF"},
        {"category": "Security", "score": data.get("security", 0), "color": "#FF0000"},
        {"category": "Complexity", "score": data.get("complexity", 0), "color": "#FFA500"},
        {"category": "Documentation", "score": data.get("documentation", 0), "color": "#008000"},
    ]
    bar_chart_data = [entry for entry in bar_chart_data if entry["score"] > 0]  # Remove empty entries

    return {
        "overallProjectScore": data.get("project_score", 0),  # Corrected field name
        "totalErrors": total_errors,
        "criticalMajor": data.get("critical", 0) + data.get("major", 0),
        "minorWarnings": data.get("minor", 0) + data.get("warning", 0),
        "pieData": pie_chart_data,
        "barData": bar_chart_data
    }

@app.get("/api/error/dashboard/{project_id}")
def get_project_errors(project_id: str):
  try:
    """Fetch project errors from MongoDB"""
    print("API Called: /api/error/dashboard/")

    project_error = errors_collection.find_one({"_id": project_id})
    # print("📝 Raw MongoDB Response:", project_error)
    if not project_error:
        raise HTTPException(status_code=404, detail="No errors found for the given project")
    # return {"Errors": document}

    formatted_errors = []
    for file in project_error.get("files", []):
        violations_list = file.get("violations", [])

        # Normalize severity counts (convert to lowercase for consistency)
        severity_counts = {"critical": 0, "major": 0, "minor": 0, "warning": 0}

        for violation in violations_list:
            severity = violation.get("severity", "").lower()  # Convert to lowercase
            if severity in severity_counts:
                severity_counts[severity] += 1

        formatted_errors.append({
            "file": file.get("file_name", "Unknown"),
            "lines": file.get("line_count", 0),
            "totalErrors": sum(severity_counts.values()),
            "critical": severity_counts["critical"],
            "major": severity_counts["major"],
            "minor": severity_counts["minor"],
            "warnings": severity_counts["warning"],
        })

    # print("Project Errors API Response:", formatted_errors)
    return {"files": formatted_errors}
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))