# Project Metadata
import glob
import os


PROJECT_NAME = "Javaproject_finjspy"
VERSION = 49
# TECHNOLOGY = ["Java","Javascript"]
# TECHNOLOGY = ["Python"]
TECHNOLOGY = ["Java","Python","Javascript"]
TECH = ", ".join(TECHNOLOGY)
DEVELOPER = "capstone"
EMAIL = "capstone@uplsnipe.com"

# Paths for Java analysis
JAVA_PATH = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JavaFiles"
CHECKSTYLE_CONFIG_FILE = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/config_files/checkstyle.xml"
CHECKSTYLE_OUTPUT_FILE = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/OutputFiles/checkstyle.txt"
PMD_CONFIG_FILE = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/config_files/pmd-ruleset.xml"
PMD_OUTPUT_FILE = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/OutputFiles/pmd.txt"
CHECKSTYLE_JSON = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/checkstyle.json"
PMD_JSON = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/pmd.json"

# Paths for final output
FINAL_JSON = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/outputProjectRating.json"
RATINGS_JSON = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/java_severity_counts.json"

# Paths for ESLint tool
ESLINT_CONFIG_FILE = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/config_files/.eslintrc.js"
JS_PATH = "./uploaded_projects/"
# JS_PATH = "../data/JavascriptFiles/"
JS_FILES = glob.glob(os.path.join(JS_PATH, "**", "*.js"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.ts"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.jsx"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.tsx"), recursive=True) + \
           glob.glob(os.path.join(JS_PATH, "**", "*.html"), recursive=True)
ESLINT_JSON = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/eslint_output_fullstack.json"
ESLINT_EXPORT_JSON = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/javascript_severity_counts.json"

# paths of python tools
TEST_DIRECTORY = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/PythonFiles"
OUTPUT_PROJECT_ERRORS = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/python_ProjectErrors.json"
OUTPUT_PROJECT_RATING = "F:/UPL_live_Project/ProjectReviewToolBackend/ProjectReviewTool/data/JsonFiles/python_ProjectRating.json"

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