import argparse
import os
from services.formatter_ import Formatter
from services.parser_ import Parser
from entities.token_ import TokenError
from services.tokenizer import Tokenizer

# Global statistics counters
files_with_errors = 0
files_successful = 0
total_files = 0
error_log_file = "lint_errors.txt"


def process_file(input_file, output_file=None, ast_file=None):
    """Process a single file: tokenize, parse, format, and save output."""
    global files_with_errors, files_successful, total_files
    total_files += 1

    try:
        # Read the input file
        with open(input_file, "r") as file:
            code = file.read()

        # Initialize tokenizer
        tokenizer = Tokenizer(code=code)

        # Tokenize the input code
        tokens = tokenizer.tokenize()

        # Initialize parser with tokens
        parser = Parser(tokens=tokens)
        ast = parser.parse()

        # Format the code
        formatter = Formatter(ast)
        formatted_code = formatter.format()

        # Determine output file path for formatted code
        output_file_path = output_file if output_file else input_file

        # Save the AST file if provided
        if ast_file:
            with open(ast_file, "w") as file:
                file.write(str(ast))
            print(f"AST saved to {ast_file}")

        # Save the formatted output
        with open(output_file_path, "w") as file:
            file.write(formatted_code)
        print(f"Formatted code saved to {output_file_path}")

        files_successful += 1  # File processed successfully

    except (SyntaxError, TokenError) as e:
        print(f"Error in {input_file}: {e}")
        log_error(input_file, e)  # Log the error
        files_with_errors += 1


def log_error(file_path, error):
    """Log errors to lint_errors.txt."""
    with open(error_log_file, "a") as log_file:
        log_file.write(f"File: {file_path}\nError: {error}\n\n")


def process_directory(input_dir):
    """Recursively process all .ctl files in a directory."""
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".ctl"):
                input_file_path = os.path.join(root, file)
                print(f"Processing file: {input_file_path}")
                process_file(input_file_path)


def display_statistics():
    """Display statistics about linting results."""
    if total_files == 0:
        print("No files were processed.")
        return

    success_percentage = (files_successful / total_files) * 100
    error_percentage = (files_with_errors / total_files) * 100

    print("\n--- Linting Results ---")
    print(f"Total files processed: {total_files}")
    print(f"Files successful: {files_successful}")
    print(f"Files with errors: {files_with_errors}")
    print(f"Success rate: {success_percentage:.2f}%")
    print(f"Error rate: {error_percentage:.2f}%")


def main():
    parser = argparse.ArgumentParser(description="Custom formatter for .ctl files.")
    parser.add_argument("input_path", help="Path to the input file or folder")
    parser.add_argument(
        "-o",
        "--output_file",
        help="Path to the output formatted file (only for single file)",
        default=None,
    )
    parser.add_argument(
        "-a",
        "--ast_file",
        help="Path to the output AST file (only for single file)",
        default=None,
    )

    args = parser.parse_args()

    # Clear previous error log
    if os.path.exists(error_log_file):
        os.remove(error_log_file)

    # Check if input_path is a file or a directory
    if os.path.isfile(args.input_path):
        if args.output_file or args.ast_file:
            print("Processing a single file with optional -o and -a flags.")
        process_file(args.input_path, args.output_file, args.ast_file)
    elif os.path.isdir(args.input_path):
        if args.output_file or args.ast_file:
            print("Error: -o and -a flags are not allowed when processing a folder.")
            return
        print(f"Processing all .ctl files in directory: {args.input_path}")
        process_directory(args.input_path)
    else:
        print(f"Error: {args.input_path} is not a valid file or directory.")
        return

    # Display linting statistics
    display_statistics()


if __name__ == "__main__":
    main()
