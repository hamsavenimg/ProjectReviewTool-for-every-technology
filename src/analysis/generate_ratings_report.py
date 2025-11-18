import json

import pymongo
from pymongo import MongoClient

from config.settings import (db_name,ratings_db,
    username,
    password,connection
)
cluster = MongoClient("mongodb+srv://" + username + ":" + password + connection)
db = cluster[db_name]
collection = db[ratings_db]

def prepare_project_rating_json_data(project_id,project_name,version,technology,date,time,status,project_score,
                                         category_counts,severity_counts,
                                        developer, email) :
    # Construct the JSON data
    data = {
        "_id": project_id,
        "project_name": project_name,
        "version": version,
        "technology": technology,
        "date": date,
        "time": time,
        "status": status,
        "project_score": project_score,
        "code_style": category_counts["code_style"],
        "best_practices": category_counts["best_practices"],
        "security": category_counts["security"],
        "complexity": category_counts["complexity"],
        "documentation": category_counts["documentation"],
        "critical": severity_counts["critical"],
        "major": severity_counts["major"],
        "minor": severity_counts["minor"],
        "warning": severity_counts["warning"],
        "developer": developer,
        "email": email
    }
    return data

def load_data_to_project_rating_table(project_id,data):
    # Insert into MongoDB
    try:
        collection.insert_one(data)
        # print(f"Data for project '{data['project_name']}' inserted successfully.")
    except Exception as e:
        print("Error inserting data:", e)

def ratings_table_load(project_id,project_name,version,technology,date,time,status,
                                         category_counts,severity_counts
                                        ,project_score,developer, email) :
    ratings_data = prepare_project_rating_json_data(project_id,project_name, version, technology,
                                     date, time, status,project_score,
                                     category_counts, severity_counts,
                                     developer, email)

    load_data_to_project_rating_table(project_id,ratings_data)