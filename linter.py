import argparse
import os
from services.formatter_ import Formatter
from services.parser_ import Parser
from entities.token_ import TokenError
from services.tokenizer import Tokenizer


def process_file(input_file, output_file=None, ast_file=None):
    """Process a single file: tokenize, parse, format, and save output."""
    # Read the input file
    with open(input_file, "r") as file:
        code = file.read()

    # Initialize tokenizer
    tokenizer = Tokenizer(code=code)

    # Tokenize the input code
    try:
        tokens = tokenizer.tokenize()
    except SyntaxError as e:
        print(f"Syntax error in {input_file}: {e}")
        return

    # Initialize parser with tokens
    parser = Parser(tokens=tokens)
    try:
        ast = parser.parse()
    except TokenError as e:
        print(f"Parsing error in {input_file}: Token error: {e}")
        return
    except SyntaxError as e:
        print(f"Parsing error in {input_file}: Syntax error: {e}")
        return

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
    with open(output_file_path, 'w') as file:
        file.write(formatted_code)
    print(f"Formatted code saved to {output_file_path}")


def process_directory(input_dir):
    """Recursively process all .ctl files in a directory."""
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".ctl"):
                input_file_path = os.path.join(root, file)
                print(f"Processing file: {input_file_path}")
                process_file(input_file_path)


def main():
    parser = argparse.ArgumentParser(description="Custom formatter for .ctl files.")
    parser.add_argument("input_path", help="Path to the input file or folder")
    parser.add_argument(
        "-o", "--output_file", help="Path to the output formatted file (only for single file)", default=None
    )
    parser.add_argument(
        "-a", "--ast_file", help="Path to the output AST file (only for single file)", default=None
    )

    args = parser.parse_args()

    # Check if input_path is a file or a directory
    if os.path.isfile(args.input_path):
        # Single file mode
        if args.output_file or args.ast_file:
            print("Processing a single file with optional -o and -a flags.")
        process_file(args.input_path, args.output_file, args.ast_file)
    elif os.path.isdir(args.input_path):
        # Directory mode
        if args.output_file or args.ast_file:
            print("Error: -o and -a flags are not allowed when processing a folder.")
            return
        print(f"Processing all .ctl files in directory: {args.input_path}")
        process_directory(args.input_path)
    else:
        print(f"Error: {args.input_path} is not a valid file or directory.")


if __name__ == "__main__":
    main()