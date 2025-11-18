import glob
import os
import sys
from datetime import datetime
from config.settings import (
     CHECKSTYLE_CONFIG_FILE, CHECKSTYLE_OUTPUT_FILE,
    PMD_CONFIG_FILE, PMD_OUTPUT_FILE, CHECKSTYLE_JSON, PMD_JSON,
    ESLINT_CONFIG_FILE, JS_FILES, ESLINT_JSON, OUTPUT_PROJECT_ERRORS
)

from analysis  import (
    get_java_errors,get_eslint_errors,python_analyzer,
    calculate_rating,generate_ratings_report,merge_json_load_db,json_errors_load)

# Get current date and time
now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
time_str = now.strftime("%H:%M")

# Function to call different scripts based on technology values
def analyze_technologies(project_id,technologies,file_path):
    for tech in technologies:
        if tech.lower() == "java":
            print("java")
            get_java_errors.main(project_id, file_path + "/java", CHECKSTYLE_CONFIG_FILE, CHECKSTYLE_OUTPUT_FILE,
                                PMD_CONFIG_FILE, PMD_OUTPUT_FILE, CHECKSTYLE_JSON, PMD_JSON)
            merge_json_load_db.merge_json_data(project_id,CHECKSTYLE_JSON,PMD_JSON)
        elif tech.lower() == "eslint":
            print("eslint")
            get_eslint_errors.main(project_id,ESLINT_CONFIG_FILE,file_path + "/eslint",ESLINT_JSON)
            json_errors_load.load_json_data(project_id, ESLINT_JSON)
        elif tech.lower() == "python":
            print("python")
            python_analyzer.main(project_id,file_path + "/python",OUTPUT_PROJECT_ERRORS)
            json_errors_load.load_json_data(project_id, OUTPUT_PROJECT_ERRORS)
        else:
            print(f"No specific script for {tech}")

def main_tool_analysis(project_id,project_name,developer,version,technology,file_path,technologies,email):
    # Run analysis
    analyze_technologies(project_id,technologies,file_path)
    project_score, category_counts, severity_counts = calculate_rating.calculate_rating(project_id)

    if project_score > 60:
       status = "Pass"
    else:
       status = "Needs Rework"
    generate_ratings_report.ratings_table_load(project_id, project_name, version, technology, date_str, time_str, status,
                                             category_counts, severity_counts,
                                             project_score, developer, email)


if __name__ == "__main__":
    main_tool_analysis()