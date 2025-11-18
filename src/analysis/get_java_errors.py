import json
import os
import platform
import subprocess
import xml.etree.ElementTree as ET

from . import metrics_db_load

# Define severity weightages
severity_weights = {
    "critical": 5,
    "major": 3,
    "minor": 1,
    "warning": 0.5
}

severity_counts = {
    "critical": 0,
    "major": 0,
    "minor": 0,
    "warning": 0
}

# Define PMD rule set category mappings
pmd_category_mapping = {
    "Code Style": "code_style",
    "Best Practices": "best_practices",
    "Security": "security",
    "Multithreading": "security",
    "Complexity": "complexity",
    "Performance": "complexity",
    "Design": "complexity",
    "Documentation": "documentation",
    "Error Prone": "best_practices"
}

# Define Checkstyle rule classification
checkstyle_category_mapping = {
    "naming": "code_style",
    "whitespace": "code_style",
    "indentation": "code_style",
    "javadoc": "documentation",
    "imports": "code_style",
    "modifier": "code_style",
    "performance": "complexity",
    "efficiency": "complexity",
    "sizes":"complexity",
    "blocks":"code_style",
    "annotation":"best_practices",
    "metrics":"complexity"
}
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

# Parse Checkstyle output XML file to calculate score
def parse_checkstyle_out_score(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for file in root.findall("file"):
        for error in file.findall("error"):
            # rule_name = error.get("source", "").lower()
            category_name = error.get("source").rsplit('.', 2)[-2]
            # Determine category
            category = "code_style"  # Default category
            for key, value in checkstyle_category_mapping.items():
                if key in category_name:
                    category = value
                    break
            part2 = error.get("source").rsplit('.', 1)[-1]
            severity = error.get("severity", "Unknown")
            rule = part2
            severity_label = classify_checkstyle_error(severity, rule)
            category_counts[category] += 1
            # Apply severity weight
            category_severity_counts[category] += severity_weights[severity_label]


# Parse PMD output XML file
def parse_pmd_out_score(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespace = {"pmd": "http://pmd.sourceforge.net/report/2.0.0"}


    # for file in root.findall("file"):
    #     for violation in file.findall("violation"):
    for file in root.findall("pmd:file", namespace):
        file_name = file.get("name")
        # file_name_extract = os.path.basename(os.path.normpath(file_name))

        for violation in file.findall("pmd:violation", namespace):
            rule_set = violation.get("ruleset")
            severity = violation.get("priority")  # PMD priority is 1 (highest) to 5 (lowest)

            # Map PMD priority to custom severity levels
            if severity == "1":
                severity_label = "critical"
            elif severity == "2":
                severity_label = "major"
            elif severity == "3":
                severity_label = "minor"
            else:
                severity_label = "warning"

            # Determine category
            category = pmd_category_mapping.get(rule_set, "best_practices")  # Default to best practices
            severity_counts[severity_label] += 1
            # Apply severity weight
            category_severity_counts[category] += severity_weights[severity_label]
            category_counts[category] += 1

# def run_checkstyle(java_file, config_file, output_file,output_format="xml"):
def run_checkstyle(java_file, config_file, output_file, output_format):
    """
    Run Checkstyle on a Java file and return the output.

    :param output_file:
    :param java_file: Path to the Java file to check.
    :param config_file: Path to the Checkstyle configuration file.
    :param output_format: Output format ('xml' or 'json').
    :return: Checkstyle output as a string.
    """
    # checkstyle_jar = "../checkstyle-10.21.1-all.jar"  # Update this if your JAR version differs
    # base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Goes from analysis/ to ProjectReviewTool/
    base_dir = os.getcwd()
    checkstyle_jar = os.path.join(base_dir, "checkstyle-10.21.1-all.jar")
    # print("Resolved Checkstyle path:", checkstyle_jar)
    # checkstyle_jar = os.path.abspath("../checkstyle-10.21.1-all.jar")
    if not os.path.exists(checkstyle_jar):
        raise FileNotFoundError(f"{checkstyle_jar} not found. Ensure Checkstyle is downloaded.")

    command = [
        "java",
        "-jar",
        checkstyle_jar,
        "-c",
        config_file,
        "-f",
        output_format,
        java_file,
    ]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # print(f"Checkstyle error:\n{e.stderr}")
        f = open(output_file,"w")
        f.write(e.stdout)
        f.close()
        # return None
        return e.stdout

def run_pmd(java_file, config_file, output_file):
    # Resolve base directory relative to this script
    # base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'pmd-bin-7.9.0', 'bin'))
    # Go two levels up from this file → ProjectReviewTool/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    # Then go into the PMD bin directory
    pmd_bin_dir = os.path.join(project_root, 'pmd-bin-7.9.0', 'bin')
    # Select script based on OS
    if platform.system() == 'Windows':
        pmd_executable = os.path.join(pmd_bin_dir, 'pmd.bat')
    else:
        pmd_executable = os.path.join(pmd_bin_dir, 'pmd')
    command = [pmd_executable,
               'check', '-d',
               java_file,
               '-R', config_file,
               '-f', 'xml',
               '-r', output_file]

    # Run the command using subprocess
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        # print("PMD Output:")
        # print(result.stdout)
    except subprocess.CalledProcessError as e:
        # print(f"Error running PMD: {e}")
        print(f"output: {e.stderr}")


def convert_checkstyle_xml_to_json(xml_file,json_file):
    """
    Parses the Checkstyle XML output and extracts useful information.

    Args:
        xml_output (str): The XML output from Checkstyle.

    Returns:
        list: A list of dictionaries containing parsed error details.
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        results = {
                    # "_id":"AIDisha_v1",
                   "files": []
                  }
        # # Initialize counters for each severity level
        # severity_counts = {
        #     "critical": 0,
        #     "major": 0,
        #     "minor": 0,
        #     "warning": 0
        # }
        for file_elem in root.findall("file"):
            file_name = file_elem.attrib.get("name", "Unknown")
            file_name_extract = os.path.basename(os.path.normpath(file_name))
            issues = []
            msgs = []
            for error_elem in file_elem.findall("error"):
                part1 = error_elem.attrib.get("source").rsplit('.', 2)[-2]
                part2 = error_elem.attrib.get("source").rsplit('.', 1)[-1]
                severity = error_elem.attrib.get("severity", "Unknown")
                rule = part2

                # Call classify_checkstyle_error to classify severity
                custom_severity = classify_checkstyle_error(severity, rule)
                # Increment the severity count
                if custom_severity in severity_counts:
                    severity_counts[custom_severity] += 1
                msg = {
                    "message": error_elem.attrib.get("message", "Unknown"),
                    "line": error_elem.attrib.get("line", "Unknown"),
                    "tool": "checkstyle",
                    "rule": part1,
                    "category": part2,
                    "severity":custom_severity
                }
                msgs.append(msg)
            results["files"].append({"file_name": file_name_extract, "violations": msgs})

        with open(json_file, "w", encoding="utf-8") as json_out:
            json.dump(results, json_out, indent=4)
        # Print out the counts of each severity level
        # print("------Checkstyle------")
        # print(f"Critical: {severity_counts['critical']}")
        # print(f"Major: {severity_counts['major']}")
        # print(f"Minor: {severity_counts['minor']}")
        # print(f"Warning: {severity_counts['warning']}")
        return msgs
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return []


def convert_pmd_xml_to_json(xml_file, json_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        namespace = {"pmd": "http://pmd.sourceforge.net/report/2.0.0"}

        results = {"files":[]}

        # # Initialize counters for each severity level
        # severity_counts = {
        #     "critical": 0,
        #     "major": 0,
        #     "minor": 0,
        #     "warning": 0
        # }
        for file in root.findall("pmd:file", namespace):
            file_name = file.get("name")
            file_name_extract = os.path.basename(os.path.normpath(file_name))
            # Count the number of lines in the file
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    line_count = sum(1 for _ in f)
            except FileNotFoundError:
                line_count = 0  # Handle case where file might not be available
            violations = []

            for violation in file.findall("pmd:violation", namespace):
                # Extract and map priority to severity
                severity = map_priority_to_severity(violation.get("priority"))

                # Increment the severity count
                # if severity in severity_counts:
                #     severity_counts[severity] += 1
                violation_data = {
                    "message": violation.text.strip() if violation.text else "",
                    "line": violation.get("beginline"),
                    "tool": "pmd",
                    "rule":violation.get("ruleset"),
                    "category": violation.get("rule"),
                    "severity":severity
                }
                violations.append(violation_data)

            results["files"].append({"file_name": file_name_extract,"line_count":line_count,"violations": violations})

        with open(json_file, "w", encoding="utf-8") as json_out:
            json.dump(results, json_out, indent=4)

    except Exception as e:
        print(f"Error processing file: {e}")

# Function to map priority to severity
def map_priority_to_severity(priority):
    # Define the priority to severity mapping
    if priority == "1":
        return "critical"
    elif priority == "2":
        return "major"
    elif priority == "3":
        return "minor"
    elif priority in ["4","5"]:
        return "warning"
    else:
        return "unknown"  # Default case if the priority is not in the expected range

def classify_checkstyle_error(severity, rule):
    """Classify Checkstyle error into custom severity levels: critical, major, minor, warning."""
    critical_rules = [
        # "MissingOverrideCheck",  # Missing @Override annotation
        "SystemExitCheck",  # Usage of System.exit()
        # "EmptyCatchBlockCheck",  # Empty catch blocks
        "FinalizeCheck",  # Finalizer method usage
        "UnreachableCodeCheck",  # Unreachable code
        # "MissingSerialVersionUIDCheck",  # Missing serialVersionUID
        "CyclicInheritanceCheck",  # Cyclic inheritance
        "ThreadInterruptCheck",  # Thread interruption without handling
        "SensitiveInformationCheck",  # Hardcoded sensitive information
        # "EqualsHashCodeCheck",  # Incorrect use of equals() and hashCode()
        "NonAtomicOperationCheck",  # Non-atomic operations in multithreading
        "ReflectionUsageCheck"  # Unsafe reflection usage
    ]

    # Define major rules.
    major_rules = [
        "EmptyCatchBlockCheck",  # Empty catch blocks
        "MissingOverrideCheck",  # Missing @Override annotation
        "MethodLengthCheck",  # Methods that are too long
        "ClassLengthCheck",  # Classes that are too large
        "CyclomaticComplexityCheck",  # High cyclomatic complexity
        "WhitespaceAroundCheck",  # Improper whitespace around operators
        # "IndentationCheck",  # Incorrect indentation
        "JavadocMethodCheck",  # Missing Javadoc for methods
        "JavadocClassCheck",  # Missing Javadoc for classes
        "JavadocTypeCheck",  # Missing Javadoc for types
        "MethodNameCheck",  # Incorrect method naming conventions
        "ClassNameCheck",  # Incorrect class naming conventions
        "ParameterNameCheck",  # Incorrect parameter naming conventions
        "VisibilityModifierCheck",  # Incorrect use of visibility modifiers
        "EmptyBlockCheck",  # Empty code blocks
        "MagicNumberCheck",  # Hardcoded magic numbers
        "LocalVariableNameCheck",  # Incorrect local variable names
        "IllegalImportCheck",  # Illegal imports
        "UnnecessaryCastingCheck",  # Unnecessary type casting
        "FinalLocalVariableCheck",  # Missing final keyword on local variables
        "FinalInstanceFieldCheck",  # Missing final keyword on instance fields
        ]

    # Define minor rules.
    minor_rules = [
        "IndentationCheck",  # Incorrect indentation
        "EqualsHashCodeCheck",  # Incorrect use of equals() and hashCode()
        "MissingSerialVersionUIDCheck",  # Missing serialVersionUID
        "LineLengthCheck",  # Lines that are too long
        "WhitespaceBeforeCommentCheck",  # Missing whitespace before comments
        "EmptyStatementCheck",  # Empty statements
        "UnusedImportsCheck",  # Unused imports
        "JavadocMethodCheck",  # Missing or incorrect Javadoc for methods
        "JavadocClassCheck",  # Missing or incorrect Javadoc for classes
        "JavadocTypeCheck",  # Missing or incorrect Javadoc for types
        "MethodNameCheck",  # Incorrect method naming conventions
        "ParameterNameCheck",  # Incorrect parameter naming conventions
        "ReturnCountCheck",  # Too many return statements in a method
        "ConstructorNameCheck",  # Incorrect constructor naming
        "TypeParameterNameCheck",  # Incorrect type parameter naming
        "FileNameCheck",  # Incorrect file name
        "FinalLocalVariableCheck",  # Local variables that should be final
        "NeedBracesCheck",  # Missing space after keywords like if, while
        "StringLiteralConcatenationCheck"  # String concatenation inside loops
        ]

    # Check if the error severity and rule match the critical rules
    if severity == "error" and rule in critical_rules:
        return "critical"
    elif severity == "error" and rule in major_rules:
        return "major"
    elif severity == "error" and rule in minor_rules:
        return "minor"
    else:
        return "warning"

def count_lines_in_project(directory, extension=".java"):
    total_lines = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(extension):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    total_lines += sum(1 for _ in f)  # Count lines in the file
    return total_lines

def main(project_id,java_path,checkstyle_config_file,checkstyle_output_file,
                    pmd_config_file,pmd_output_file,checkstyle_json,pmd_json):
    # Reset counts to zero for fastapi re-entry
    for key in category_severity_counts:
        category_severity_counts[key] = 0
    for key in category_counts:
        category_counts[key] = 0
    for key in severity_counts:
        severity_counts[key] = 0
    # Run Checkstyle and get XML output
    checkstyle_xml_output = run_checkstyle(java_path, checkstyle_config_file,
                                           checkstyle_output_file,output_format="xml")
    run_pmd(java_path,pmd_config_file,pmd_output_file)

    convert_checkstyle_xml_to_json(checkstyle_output_file, checkstyle_json)
    # print("Category Severity Scores:", category_severity_counts)
    parse_checkstyle_out_score(checkstyle_output_file)

    # ---------------------------------------------------------
    convert_pmd_xml_to_json(pmd_output_file, pmd_json)
    parse_pmd_out_score(pmd_output_file)

    total_lines_of_code = count_lines_in_project(java_path)
    # print(f"Total lines of code in Java files: {total_lines_of_code}")

    metrics_db_load.get_data(project_id ,total_lines_of_code,category_severity_counts,
                                         category_counts,severity_counts)


if __name__ == "__main__":
    # main()  # Runs only when executed directly, NOT when imported
    print("Running get_java_errors.py as standalone script.")