import json
from collections import defaultdict

from config.settings import (db_name,metrics_db,
    username,
    password,connection
)

import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://" + username + ":" + password + connection)
db = cluster[db_name]
collection = db[metrics_db]

# Aggregated result storage
aggregated_data = {
    'total_lines_of_code': 0,
    'category_severity_counts': defaultdict(float),
    'category_counts': defaultdict(int),
    'severity_counts': defaultdict(int)
}

def get_project_data(project_id):
    """
    Fetches data from MongoDB.

    If project_id is provided, it returns data for that project.
    If no project_id is given, it returns all projects.

    Parameters:
        - project_id (str, optional): The specific project to retrieve.

    Returns:
        - List of documents (or a single document if project_id is provided).
    """
    if project_id:
        # Fetch a single project by its ID
        data = collection.find_one({"_id": project_id})
        return data if data else f"Project '{project_id}' not found."
    else:
        return  "No projects found."


def calculate_final_score(metrics_data):
    # Summing values from each entry in the metrics array
    for entry in metrics_data['metrics']:
        aggregated_data['total_lines_of_code'] += entry['total_lines_of_code']

        for key, value in entry['category_severity_counts'].items():
            aggregated_data['category_severity_counts'][key] += value

        for key, value in entry['category_counts'].items():
            aggregated_data['category_counts'][key] += value

        for key, value in entry['severity_counts'].items():
            aggregated_data['severity_counts'][key] += value
    # Convert defaultdict to normal dict
    aggregated_data['category_severity_counts'] = dict(aggregated_data['category_severity_counts'])
    aggregated_data['category_counts'] = dict(aggregated_data['category_counts'])
    aggregated_data['severity_counts'] = dict(aggregated_data['severity_counts'])

    # Print the aggregated result
    # print(aggregated_data)
    # Compute final category-wise scores
    category_scores = {}
    for category, count in aggregated_data['category_severity_counts'].items():
        if aggregated_data['total_lines_of_code'] > 0:
            category_scores[category] = round(
                           max(0, 100 - ((count / aggregated_data['total_lines_of_code']) * 100)), 2)
        else:
            category_scores[category] = 100  # If no code, default to a perfect score

    #  Print category-wise scores
    # print("Category Scores:")
    # for category, score in category_scores.items():
    #      print(f"{category}: {score:.2f}")

    # Define category weightages
    category_weights = {
        "code_style": 0.3,
        "best_practices": 0.3,
        "security": 0.1,
        "complexity": 0.2,
        "documentation": 0.1
    }

    # Compute final weighted score
    final_score = round(sum(category_scores[cat] * weight for cat, weight in category_weights.items()), 2)
    return final_score,aggregated_data['category_counts'],aggregated_data['severity_counts']


def calculate_rating(project_id):
     data = get_project_data(project_id)
     final_score,category_counts,severity_counts = calculate_final_score(data)
     # print(final_score,category_counts)
     return final_score,category_counts,severity_counts
