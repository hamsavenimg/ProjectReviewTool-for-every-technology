import os
import json
import subprocess
import sys

from radon.complexity import cc_visit
from radon.visitors import ComplexityVisitor
from . import metrics_db_load

SEVERITY_WEIGHTS = {"critical": 5, "major": 3, "minor": 1, "warning": 0.5}
CATEGORY_WEIGHTS = {"code_style": 0.2, "best_practices": 0.2, "security": 0.3, "complexity": 0.2, "documentation": 0.1}
category_totals = {cat: [] for cat in CATEGORY_WEIGHTS}
# category_severity_scores = {cat: 0 for cat in CATEGORY_WEIGHTS}
# Initialize category severity counts
category_severity_scores = {
    "code_style": 0,
    "best_practices": 0,
    "security": 0,
    "complexity": 0,
    "documentation": 0
}

def load_and_transform_json(file_path):
    """Load JSON and rename 'errors' to 'violations'."""
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        return []

    with open(file_path, "r") as f:
        data = json.load(f)

    for entry in data:
        if "errors" in entry:
            entry["violations"] = entry.pop("errors")

    return data


def run_pylint(file_path):
    """Runs pylint and extracts error details."""
    result = subprocess.run([sys.executable, "-m","pylint", file_path, "--enable=all", "--output-format=json"], capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return []



def run_bandit(file_path):
    """Runs bandit for security analysis."""
    result = subprocess.run([sys.executable, "-m", "bandit", "-r", file_path, "-f", "json"], capture_output=True, text=True)
    try:
        return json.loads(result.stdout).get("results", [])
    except json.JSONDecodeError:
        return []


def run_radon(file_path):
    """Runs radon to analyze code complexity."""
    with open(file_path, "r") as f:
        code = f.read()
    return cc_visit(code)


def classify_pylint_rule(rule):
    """Maps pylint rules to categories and severity levels."""
    best_practices_rules = {"E1101", "E0602", "R0201", "R0913", "W0201"}  # Example best practices rules

    rule_mapping = {
        "C": ("code_style", "minor"),
        "E": ("best_practices", "major") if rule in best_practices_rules else ("Unknown", "minor"),
        "W": ("best_practices", "minor"),
        "R": ("best_practices", "minor"),
        "F": ("security", "critical"),
    }

    docstring_rules = {"C0114", "C0115", "C0116"}  # Missing module, class, function docstring
    if rule in docstring_rules:
        return "documentation", "minor"

    return rule_mapping.get(rule[0], ("Unknown", "minor"))


def categorize_pylint_errors(errors, file_path):
    """Categorizes pylint errors into predefined categories."""
    categorized_errors = []
    for error in errors:
        category, severity = classify_pylint_rule(error["message-id"])


        points = SEVERITY_WEIGHTS.get(severity, 1)
        category_severity_scores[category]  += points
        categorized_errors.append({

            "line": error.get("line", 0),
            "message": error.get("message", ""),
            "tool": "pylint",
            "rule": error.get("message-id", ""),
            "severity": severity,
            "points": points,
            "category": category
        })
    return categorized_errors


def categorize_bandit_errors(errors, file_path):
    """Categorizes Bandit security errors."""
    categorized_errors = []
    for error in errors:
        severity = "critical" if error["issue_severity"] == "HIGH" else "major"
        points = SEVERITY_WEIGHTS[severity]
        category_severity_scores["security"]  += points
        categorized_errors.append({

            "line": error["line_number"],
            "message": error["issue_text"],
            "tool": "bandit",
            "rule": error["test_id"],
            "severity": severity,
            "points": points,
            "category": "security"
        })
    return categorized_errors


def categorize_radon_results(complexities, file_path):
    """Categorizes Radon complexity results."""
    categorized_errors = []
    for block in complexities:
        severity = "minor" if block.complexity < 10 else "major"
        points = SEVERITY_WEIGHTS[severity]
        category_severity_scores["complexity"] += points
        categorized_errors.append({

            "line": block.lineno,
            "message": f"Cyclomatic Complexity: {block.complexity}",
            "tool": "radon",
            "rule": "cyclomatic-complexity",
            "severity": severity,
            "points": points,
            "category": "complexity"
        })
    return categorized_errors


def calculate_scores(results):
    """Calculates category and overall scores based on all analyzed files."""
    category_totals = {cat: [] for cat in CATEGORY_WEIGHTS}
    for file_result in results:
        violations = file_result.get("violations", [])
        for cat in CATEGORY_WEIGHTS:
            category_score = 100 - sum(err["points"] for err in violations if err["category"] == cat)
            category_totals[cat].append(max(category_score, 0))

    avg_category_scores = {
        cat: round(sum(scores) / len(scores), 2) if scores else 100
        for cat, scores in category_totals.items()
    }
    overall_score = round(sum(avg_category_scores[cat] * weight for cat, weight in CATEGORY_WEIGHTS.items()), 2)
    return avg_category_scores, overall_score

def count_lines_of_code(file_path):
    """Counts the number of non-empty and non-comment lines in a file."""
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Ignore empty lines and comment lines
    code_lines = [line for line in lines if line.strip() and not line.strip().startswith("#")]
    return len(code_lines)


def main(project_id,test_directory,output_python_errors):
    """Main function to analyze all Python files in the test directory."""
    results = []
    loc=0

    # Reset counts to zero for fastapi re-entry
    for key in category_severity_scores:
        category_severity_scores[key] = 0

    total_category_counts = {cat: 0 for cat in CATEGORY_WEIGHTS}
    total_severity_counts = {sev: 0 for sev in SEVERITY_WEIGHTS}
    if not os.path.exists(test_directory):
        print(f"Error: The directory '{test_directory}' does not exist.")
    for root, _, files in os.walk(test_directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                file_path = file_path.replace("\\", "/")  # Convert to forward slashes
                file_name = file_path.split("/")[-1]
                loc = count_lines_of_code(file_path)

                pylint_errors = categorize_pylint_errors(run_pylint(file_path), file_path)
                bandit_errors = categorize_bandit_errors(run_bandit(file_path), file_path)
                radon_errors = categorize_radon_results(run_radon(file_path), file_path)

                all_errors = pylint_errors + bandit_errors + radon_errors

                severity_counts = {sev: sum(1 for e in all_errors if e["severity"] == sev) for sev in
                                   total_severity_counts}
                category_counts = {cat: sum(1 for e in all_errors if e["category"] == cat) for cat in
                                   total_category_counts}

                for cat in total_category_counts:
                    total_category_counts[cat] += category_counts[cat]
                for sev in total_severity_counts:
                    total_severity_counts[sev] += severity_counts[sev]
                results.append({
                    "file_name": file_name,
                    "line_count": loc,
                    "violations": all_errors
                })
    output_errors = {"files": results}
    avg_category_scores, overall_score = calculate_scores(results)

    with open(output_python_errors, "w") as f:
        json.dump(output_errors, f, indent=4)

    metrics_db_load.get_data(project_id, loc, category_severity_scores,
                           total_category_counts, total_severity_counts)


if __name__ == "__main__":
    main()
