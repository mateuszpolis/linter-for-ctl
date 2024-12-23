import argparse
import os
import subprocess


def run_main_for_ctl_files(base_directory, output_file):
    with open(output_file, "w") as result_file:
        error_count = 0
        no_error_count = 0
        # Walk through each directory and subdirectory
        for root, _, files in os.walk(base_directory):
            for file in files:
                if file.endswith(".ctl"):
                    # Full path to the .ctl file
                    ctl_file_path = os.path.join(root, file)

                    try:
                        # Run the main.py script with the .ctl file
                        command = ["python", "main.py", ctl_file_path]
                        output = subprocess.check_output(
                            command, text=True, stderr=subprocess.STDOUT
                        )

                        # Write the result to the output file if it's not empty
                        if output:
                            error_count += 1
                            result_file.write(f"File: {ctl_file_path}\n")
                            result_file.write(f"Output:\n{output}\n")
                            result_file.write(
                                "=" * 40 + "\n"
                            )  # Separator for readability
                        else:
                            no_error_count += 1

                    except subprocess.CalledProcessError as e:
                        # Handle errors gracefully and log them
                        result_file.write(f"File: {ctl_file_path}\n")
                        result_file.write(f"Error:\n{e.output}\n")
                        result_file.write("=" * 40 + "\n")

        # Write the summary to the output file
        result_file.write(f"Total errors found: {error_count}\n")
        result_file.write(f"Total files with no errors: {no_error_count}\n")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Run main.py for .ctl files recursively in a directory."
    )
    parser.add_argument("path", help="The base directory to search for .ctl files.")
    parser.add_argument(
        "-o",
        "--output",
        default="results.txt",
        help="The name of the output file (default: results.txt).",
    )
    args = parser.parse_args()

    base_directory = args.path
    output_file = args.output

    run_main_for_ctl_files(base_directory, output_file)
