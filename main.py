import re
import argparse
from parser_ import Parser
from token_ import TokenError
from tokenizer import Tokenizer

def main():
    parser = argparse.ArgumentParser(description="Custom formatter for .ctl files.")
    parser.add_argument("input_file", help="Path to the input .ctl file")
    parser.add_argument("-o", "--output_file", help="Path to the output formatted file", default="formatted_output.ctl")
    
    args = parser.parse_args()

    with open(args.input_file, 'r') as file:
        code = file.read()
        
    tokenizer = Tokenizer(code=code)
    
    try:
        tokens = tokenizer.tokenize()
    except SyntaxError as e:
        print(e)
        return
    
    print("TOKENIZATION SUCCESSFUL\n\n")

    parser = Parser(tokens=tokens)    
    try:
        ast = parser.parse()
    except TokenError as e:
        print(e)
        return
    
    output_ast_file = args.input_file[:-4] + ".ast"
    with open(output_ast_file, 'w') as file:
        file.write(str(ast))

    print("PARSING SUCCESSFUL\n\n")
    print(f"AST saved to {output_ast_file}")

    # with open(args.output_file, 'w') as file:
    #     file.write(formatted_code)
    
    # print(f"Formatted code saved to {args.output_file}")

if __name__ == "__main__":
    main()
