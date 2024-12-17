import os
import shutil
import xml.etree.ElementTree as ET
import html

# Define input and output directories
SOURCE_DIR = "panels"
DEST_DIR = "panels_scripts"


def extract_scripts_from_xml(file_path):
    """
    Extract content from all <script> tags in the XML file.
    Combine them with a newline if there are multiple scripts.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        scripts = []
        # Search for all script tags
        for script in root.findall(".//script"):
            script_text = script.text  # Text content of the script tag
            if script_text:
                # Remove CDATA tags and decode HTML entities
                clean_script = html.unescape(script_text.strip())
                clean_script = clean_script.replace("<![CDATA[", "").replace("]]>", "")
                scripts.append(clean_script)

        return "\n".join(scripts)

    except ET.ParseError as e:
        print(f"Error parsing XML file {file_path}: {e}")
        return ""
    except Exception as e:
        print(f"Unexpected error in file {file_path}: {e}")
        return ""


def process_directory(source_dir, dest_dir):
    """
    Recursively process the source directory and create the same structure in dest_dir.
    Convert XML files to .ctl files with extracted script contents.
    """
    for root, dirs, files in os.walk(source_dir):
        # Compute the corresponding destination directory
        relative_path = os.path.relpath(root, source_dir)
        current_dest_dir = os.path.join(dest_dir, relative_path)

        # Create the destination directory if it doesn't exist
        os.makedirs(current_dest_dir, exist_ok=True)

        for file in files:
            if file.endswith(".xml"):
                source_file_path = os.path.join(root, file)
                dest_file_name = os.path.splitext(file)[0] + ".ctl"
                dest_file_path = os.path.join(current_dest_dir, dest_file_name)

                # Extract script content and write to new .ctl file
                script_content = extract_scripts_from_xml(source_file_path)
                if script_content:
                    with open(dest_file_path, "w", encoding="utf-8") as ctl_file:
                        ctl_file.write(script_content)
                else:
                    print(f"No script content found in {source_file_path}")


def main():
    # Remove existing destination directory if it exists
    if os.path.exists(DEST_DIR):
        shutil.rmtree(DEST_DIR)
    os.makedirs(DEST_DIR, exist_ok=True)

    print("Processing XML files...")
    process_directory(SOURCE_DIR, DEST_DIR)
    print(f"Script processing complete. Output saved to: {DEST_DIR}")


if __name__ == "__main__":
    main()
