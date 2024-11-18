import re
import argparse
from parser_ import Parser
from token_ import TokenError
from tokenizer import Tokenizer

def main():
    parser = argparse.ArgumentParser(description="Custom formatter for .ctl files.")
    parser.add_argument("input_file", help="Path to the input .ctl file")
    parser.add_argument("-o", "--output_file", help="Path to the output formatted file", default=None)
    parser.add_argument("-a", "--ast_file", help="Path to the output AST file (for debugging)", default=None)    
    
    args = parser.parse_args()

    # Read the input file
    with open(args.input_file, 'r') as file:
        code = file.read()
        
    # Initialize tokenizer
    tokenizer = Tokenizer(code=code)
    
    # Tokenize the input code
    try:
        tokens = tokenizer.tokenize()
    except SyntaxError as e:
        print(e)
        return

    # Initialize parser with tokens
    parser = Parser(tokens=tokens)    
    try:
        ast = parser.parse()
    except TokenError as e:
        print("Token error:", e)
        return
    except SyntaxError as e:
        print("Syntax error:", e)
        return
    
    # Determine output file path for formatted code
    output_file_path = args.output_file if args.output_file else args.input_file

    # Save the AST file if -a is specified
    if args.ast_file:
        with open(args.ast_file, 'w') as file:
            file.write(str(ast))
        print(f"AST saved to {args.ast_file}")

    # Save the formatted output to the specified output path
    formatted_code = str(ast)
    with open(output_file_path, 'w') as file:
        file.write(formatted_code)
    print(f"Formatted code saved to {output_file_path}")

if __name__ == "__main__":
    main()
