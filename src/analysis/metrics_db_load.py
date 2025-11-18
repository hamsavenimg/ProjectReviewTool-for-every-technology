import json

import pymongo
from pymongo import MongoClient

from config.settings import (db_name,metrics_db,
    username,
    password,connection
)
def get_data(project_id,total_lines_of_code,category_severity_counts,
                                         category_counts,severity_counts):
    cluster = MongoClient(
        # "mongodb+srv://" + username + ":" + password + "@cluster0.ozobt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    "mongodb+srv://" + username + ":" + password + connection)
    db = cluster[db_name]
    metrics_collection = db[metrics_db]
    # Build the update query
    insert_data = {
        "total_lines_of_code": total_lines_of_code,
        "category_severity_counts": category_severity_counts,
        "category_counts": category_counts,
        "severity_counts": severity_counts
    }

    # Update or insert into MongoDB
    metrics_collection.update_one(
        {"_id": project_id},  # Find by project_id
        {"$push": {"metrics": insert_data}},  # Append to array
        upsert=True  # Insert if not exists
    )