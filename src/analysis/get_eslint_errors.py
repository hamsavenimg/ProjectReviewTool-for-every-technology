import glob
import os
import platform
import xml.etree.ElementTree as ET
import subprocess
import json
from . import metrics_db_load
from datetime import datetime
from pathlib import Path
from pickle import FALSE

# Define severity weightages
severity_weights = {
    "critical": 5,
    "major": 3,
    "minor": 1,
    "warning": 0.5
}

# severity_numbers = {
#     "critical": 0,
#     "major": 0,
#     "minor": 0,
#     "warning": 0
# }

# Initialize counters for each severity level
# severity_counts = {
#     "critical": 0,
#     "major": 0,
#     "minor": 0,
#     "warning": 0
# }

# Define Eslint rule set category mappings
eslint_category_mapping = {
    # Code Style Issues
    "Literal": "code_style",
    "Identifier": "code_style",
    "Punctuator": "code_style",
    "TSAnyKeyword": "code_style",
    "TSNonNullExpression": "code_style",
    "ArrowFunctionExpression": "code_style",
    "Property": "code_style",
    "BinaryExpression": "code_style",
    # "VariableDeclaration": "code_style",
    "OpenTagStart": "code_style",
    # "Tag": "code_style",
    # "Attribute": "code_style",
    # "AttributeValue": "code_style",
    "OpenTagEnd": "code_style",
    "Line": "code_style",

    # Best Practices
    "ImportDeclaration": "best_practices",
    "VariableDeclaration": "best_practices",
    "MemberExpression": "best_practices",
    "FunctionDeclaration": "best_practices",
    # "CallExpression": "best_practices",
    "ArrayExpression": "best_practices",
    "Program": "best_practices",

    # Design Issues
    "IfStatement": "complexity",
    "BlockStatement": "complexity",

    # Security Issues
    "CallExpression": "security",  # Potentially unsafe calls like eval()

    # Documentation Issues
    "Tag": "documentation",
    "Attribute": "documentation",
    "AttributeValue": "documentation"
}

# Initialize category severity counts
# category_severity_counts = {
#     "code_style": 0,
#     "best_practices": 0,
#     "security": 0,
#     "complexity": 0,
#     "documentation": 0
# }

# category_counts = {
#     "code_style": 0,
#     "best_practices": 0,
#     "security": 0,
#     "complexity": 0,
#     "documentation": 0
# }

def check_eslint(config_file,js_path1):
    """Runs ESLint on the specified JavaScript file and returns violations."""
    try:
        js_path = Path(js_path1).resolve()
        # Collect JS/TS/HTML files recursively
        js_files = glob.glob(str(js_path / "**/*.js"), recursive=True) + \
                   glob.glob(str(js_path / "**/*.ts"), recursive=True) + \
                   glob.glob(str(js_path / "**/*.jsx"), recursive=True) + \
                   glob.glob(str(js_path / "**/*.tsx"), recursive=True) + \
                   glob.glob(str(js_path / "**/*.html"), recursive=True)
        # Normalize to absolute paths
        normalized_js_files = [str(Path(f).resolve()) for f in js_files]
        # Detect platform and choose appropriate ESLint command
        eslint_command = "eslint.CMD" if platform.system() == "Windows" else "eslint"
        result = subprocess.run(
            [eslint_command, "--config", config_file, "--format", "json"]
             + js_files,
            # + normalized_js_files,
            capture_output=True,
            text=True,
            cwd=str(js_path1),
            # cwd=eslint_config_file.parent,
            check=False, encoding="utf-8"
        )
        eslint_output = json.loads(result.stdout)
        return eslint_output
    except subprocess.CalledProcessError as e:
        print("Error running ESLint:", e)
        return e.stderr
    except json.JSONDecodeError:
        print("Error parsing ESLint output. Ensure ESLint is correctly installed and configured.")
        return {}

def get_line_count(file_path):
    """Returns the number of lines in a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return sum(1 for _ in f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0  # Default to 0 if file can't be read


def convert_eslint_json(eslint_output,output_filename,category_counts,category_severity_counts,severity_counts):
        converted_output = {
            "files": []
           }

        for file in eslint_output:
            file_path = file["filePath"]  # Get full file path
            line_count = get_line_count(file_path)  # Count lines

            file_entry = {
                "file_name": file["filePath"].split("\\")[-1],  # Extract file name only
                "line_count":line_count,
                "violations": []
            }

            for message in file["messages"]:
                severity = message.get("severity")
                rule = message.get("ruleId")
                # Call classify_checkstyle_error to classify severity
                custom_severity = classify_eslint_error(severity, rule)
                # Increment the severity count
                if custom_severity in severity_counts:
                    severity_counts[custom_severity] += 1
                severity_label = classify_eslint_error(severity, rule)
                category_name = message.get("nodeType") or "code_style"

                category1 = "code_style"
                for key, value in eslint_category_mapping.items():
                    if key in category_name:
                        category1 = value
                        break
                category_counts[category1] += 1
                # Apply severity weight
                category_severity_counts[category1] += severity_weights[severity_label]
                violation = {
                    # "message": message["message"],
                     "message": str(message.get("message","N/A")),
                    "line": str(message.get("line", "N/A")),
                    "tool": "eslint",
                    "rule": message["ruleId"] if message["ruleId"] else "unknown",
                    "category":  message["nodeType"] if message["nodeType"] else "unknown",
                    # "severity":"major" if message.get("severity") == 2 else "warning"
                    "severity": custom_severity
                }
                file_entry["violations"].append(violation)
            converted_output["files"].append(file_entry)

        # output_filename = "../JsonFiles/eslint_output_metricstemp.json"
        with open(output_filename, "w", encoding="utf-8") as json_file:
            json.dump(converted_output, json_file, indent=4)
        # Print out the counts of each severity level
        # print("----- Eslint -----")
        # print(f"Critical: {severity_counts['critical']}; Score : {severity_counts['critical'] * 5}")
        # print(f"Major: {severity_counts['major']}; Score : {severity_counts['major'] * 3}")
        # print(f"Minor: {severity_counts['minor']}; Score : {severity_counts['minor'] * 1}")
        # print(f"Warning: {severity_counts['warning']}; Score : {severity_counts['warning'] * 0.5}")


def classify_eslint_error(severity, rule):
    """Classify Eslint error into custom severity levels: critical, major, minor, warning."""
    critical_rules = [
       "@typescript-eslint/no-explicit-any",
       "import/no-unresolved",
       "import/no-cycle",
       "no-use-before-define",
       "@html-eslint/require-doctype",
       "@html-eslint/require-lang",
       "@html-eslint/require-title"
    ]

    # Define major rules.
    major_rules = [
       "@typescript-eslint/no-unused-vars",
       "react-hooks/rules-of-hooks",
       "@html-eslint/no-duplicate-id",
       "@html-eslint/require-img-alt",
       "no-var",
       "eqeqeq",
       "@html-eslint/no-target-blank",
       "@html-eslint/require-li-container"
    ]

    # Define minor rules.
    minor_rules = [
       "import/order",
       "no-lonely-if",
       "prefer-const",
       "arrow-body-style",
       "object-shorthand",
       "curly",
       "func-style",
       "@html-eslint/lowercase",
       "@html-eslint/element-newline"
    ]

    warnings = [
       "no-console",
       "react-hooks/exhaustive-deps",
       "@typescript-eslint/no-non-null-assertion",
       "@html-eslint/no-skip-heading-levels",
       "no-multiple-empty-lines",
       "no-trailing-spaces",
       "arrow-parens",
       "brace-style",
       "space-before-blocks"
    ]
    # Check if the error severity and rule match the critical rules
    if severity == 2 and rule in critical_rules:
        return "critical"
    elif severity == 2 and rule in major_rules:
        return "major"
    elif severity == 2 and rule in minor_rules:
        return "minor"
    elif severity == 1 and rule in warnings:
        return "warning"
    else:
        return "minor"

def count_lines_in_project(file_list1):
    js_path = Path(file_list1).resolve()
    # Collect JS/TS/HTML files recursively
    file_list = glob.glob(str(js_path / "**/*.js"), recursive=True) + \
                glob.glob(str(js_path / "**/*.ts"), recursive=True) + \
                glob.glob(str(js_path / "**/*.jsx"), recursive=True) + \
                glob.glob(str(js_path / "**/*.tsx"), recursive=True) + \
                glob.glob(str(js_path / "**/*.html"), recursive=True)
    total_lines = 0
    for file in file_list:
        if os.path.isfile(file):  # Ensure it's a valid file
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    total_lines += sum(1 for _ in f)
            except Exception as e:
                print(f"Error reading file {file}: {e}")
    return total_lines


def main(project_id,config_file,js_path,output_filename):
    # Initialize category severity counts
    category_severity_counts = {
        "code_style": 0,
        "best_practices": 0,
        "security": 0,
        "complexity": 0,
        "documentation": 0
    }
    category_counts = {
        "code_style": 0,
        "best_practices": 0,
        "security": 0,
        "complexity": 0,
        "documentation": 0
    }
    # Initialize counters for each severity level
    severity_counts = {
        "critical": 0,
        "major": 0,
        "minor": 0,
        "warning": 0
    }

    eslint_output = check_eslint(config_file,js_path)
    convert_eslint_json(eslint_output,output_filename,category_counts,category_severity_counts,severity_counts)

    total_lines_of_code = count_lines_in_project(js_path)
    # print(f"Total lines of code in Java files: {total_lines_of_code}")
    # print(category_severity_counts,category_counts,severity_counts)
    metrics_db_load.get_data(project_id,total_lines_of_code, category_severity_counts,
                           category_counts, severity_counts)

if __name__ == "__main__":
    main()