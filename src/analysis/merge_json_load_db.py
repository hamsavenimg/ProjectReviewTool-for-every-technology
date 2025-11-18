import json
from pymongo import MongoClient

from config.settings import (db_name,errors_db,
    username,
    password,connection
)

def merge_json_data(project_id,checkstyle_json,pmd_json):
    cluster = MongoClient(
        "mongodb+srv://" + username + ":" + password + connection)
    db = cluster[db_name]
    errors_collection = db[errors_db]

    # Call get_errors_collection() inside the function
    """Merges JSON data from multiple sources and stores it in MongoDB using the given project_id."""
    # Load CHECKSTYLE JSON
    with open(checkstyle_json, "r") as file:
        checkstyle_data = json.load(file)

    # Load PMD JSON
    with open(pmd_json, "r") as file:
        pmd_data = json.load(file)

    # Structure to group errors by filename
    errors_by_file = {}

    # Process PMD Errors first
    for file in pmd_data.get("files", []):
        filename = file.get("file_name", "unknown")
        line_count = file.get("line_count", "0")
        errors_by_file[filename] = {
            "file_name": filename,
            "line_count": line_count,
            "violations": []
        }
        for violation in file.get("violations", []):
            errors_by_file[filename]["violations"].append({
                "message": violation.get("message"),
                "line": violation.get("line"),
                "tool": violation.get("tool"),
                "rule": violation.get("rule"),
                "category": violation.get("category"),
                "severity": violation.get("severity")
            })

    # Process Checkstyle Errors
    for file in checkstyle_data.get("files", []):
        filename = file.get("file_name", "unknown")
        if filename not in errors_by_file:
            errors_by_file[filename] = {
                "file_name": filename,
                "line_count": "0",  # Default to 0 if not found in PMD
                "violations": []
            }
        for violation in file.get("violations", []):
            errors_by_file[filename]["violations"].append({
                "message": violation.get("message"),
                "line": violation.get("line"),
                "tool": violation.get("tool"),
                "rule": violation.get("rule"),
                "category": violation.get("category"),
                "severity": violation.get("severity")
            })

    # Prepare a single document with the dynamic _id
    merged_document = {
        "_id": project_id,  # Use dynamic project_id
        "files": list(errors_by_file.values())
    }

    # Insert or update MongoDB document
    errors_collection.replace_one({"_id": project_id}, merged_document, upsert=True)


# If running standalone (for testing purposes)
if __name__ == "__main__":
    project_id = input("Enter project ID: ")
    print(project_id)
    # merge_json_data(project_id)
