import json
from pymongo import MongoClient

from config.settings import (db_name,errors_db,
    username,
    password,connection
)
def load_json_data(project_id,eslint_json):
    cluster = MongoClient(
        "mongodb+srv://" + username + ":" + password + connection)
    db = cluster[db_name]
    errors_collection = db[errors_db]
    """Merges JSON data from multiple sources and stores it in MongoDB using the given project_id."""

    # Load ESLint JSON
    with open(eslint_json, "r") as file:
        eslint_data = json.load(file)

    new_files = eslint_data.get("files", [])

    if new_files:
        errors_collection.update_one(
            {"_id": project_id},
            {"$push": {"files": {"$each": new_files}}},
            upsert=True
        )

    # print(f"Merged data stored with ID: {project_id}")


# If running standalone (for testing purposes)
if __name__ == "__main__":
    project_id = input("Enter project ID: ")

