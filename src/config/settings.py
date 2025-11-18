# Project Metadata
import glob
import os
from pathlib import Path

# Get the project root dynamically
BASE_DIR = Path(__file__).resolve().parents[2]  # Adjust as needed
# Paths for Java analysis
JAVA_PATH =  BASE_DIR /"data"/"JavaFiles"
CHECKSTYLE_CONFIG_FILE = BASE_DIR /"config_files"/"checkstyle.xml"
CHECKSTYLE_OUTPUT_FILE = BASE_DIR /"data"/"OutputFiles"/"checkstyle.txt"
PMD_CONFIG_FILE = BASE_DIR /"config_files"/"pmd-ruleset.xml"
PMD_OUTPUT_FILE = BASE_DIR /"data"/"OutputFiles/pmd.txt"
CHECKSTYLE_JSON = BASE_DIR /"data"/"JsonFiles"/"checkstyle.json"
PMD_JSON = BASE_DIR /"data"/"JsonFiles"/"pmd.json"

# Paths for final output
FINAL_JSON = BASE_DIR /"data"/"JsonFiles"/"outputProjectRating.json"
RATINGS_JSON =BASE_DIR /"data"/"JsonFiles"/"java_severity_counts.json"

# Paths for ESLint tool
ESLINT_CONFIG_FILE = BASE_DIR /"config_files"/".eslintrc.js"
JS_PATH = "./uploaded_projects/"
# JS_PATH = "../data/JavascriptFiles/"
JS_FILES = glob.glob(os.path.join(JS_PATH, "**", "*.js"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.ts"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.jsx"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.tsx"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.html"), recursive=True)
ESLINT_JSON = BASE_DIR /"data"/"JsonFiles"/"eslint_output_fullstack.json"
ESLINT_EXPORT_JSON = BASE_DIR /"data"/"JsonFiles"/"javascript_severity_counts.json"

# paths of python tools
# TEST_DIRECTORY = BASE_DIR /"data"/"PythonFiles"
OUTPUT_PROJECT_ERRORS = BASE_DIR /"data"/"JsonFiles"/"python_ProjectErrors.json"
OUTPUT_PROJECT_RATING = BASE_DIR /"data"/"JsonFiles"/"python_ProjectRating.json"

# MongoDB connection
connection = "@cluster0.ozobt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# username   = "xxxxxxxxxxxxx"
# password   = "xxxxxxxxxxxxx"
username   = "hamsaganesh21"
password   = "mongodbhamsa"
db_name    = "CapstoneReview"
ratings_db = "ProjectRating"
errors_db  = "ProjectErrors"
metrics_db ="ProjectMetrics"
projects_db ="Projects"