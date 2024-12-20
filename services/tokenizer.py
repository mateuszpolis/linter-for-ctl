import re

from entities.token_ import Token, TokenKind

KEYWORDS = [
    "while",
    "for",
    "return",
    "break",
    "continue",
    "true",
    "false",
    "null",
    "uses",
    "const",
    "enum",
    "switch",
    "case",
    "default",
    "struct",
    "class",
    "try",
    "catch",
    "finally",
    "do",
    "new",
]
MODIFIERS = ["static", "global", "synchronized"]
ACCESS_MODIFIERS = ["public", "private", "protected"]
BASE_TYPE_KEYWORDS = [
    "string",
    "int",
    "float",
    "bool",
    "void",
    "mapping",
    "file",
    "uint",
    "time",
    "anytype",
    "errClass",
    "mixed",
    "ulong",
    "char",
    "unsigned",
    "bit64",
    "shape",
    "bit32",
    "long",
    "palette",
]
TYPE_KEYWORDS = []
LIBRARY_TYPE_KEYWORDS = [
    "OaTestResultEnvironment",
    "OaTestResultStatistic",
    "LogEntry",
    "OaTestResult",
    "OsInfo",
    "TfString",
    "ProjEnvProject",
    "fitLookUpTable",
    "ProjEnvComponent",
    "JsonFile",
    "OaTestResultFileFormat",
    "TfTestRunner",
    "LogReader",
    "TfTestProject",
    "TfNotifier",
    "TfErrHdl",
    "DCSUI",
    "LookUpTable",
    "LookUpTableEntry",
    "Scope",
    "Trend",
    "Plot",
    "PmFitUi",
    "HvFitUi"
]
TEMPLATE_TYPE_KEYWORDS = ["vector", "shared_ptr"]
ARITHMETIC_OPERATORS = [
    "+",
    "-",
    "*",
    "/",
    "%",
    "++",
    "--",
]
ASSIGNMENT_OPERATORS = ["+=", "-=", "*=", "/=", "%=", "="]
COMPARISON_OPERATORS = ["==", "!=", ">", ">=", "<", "<="]
LOGICAL_OPERATORS = ["&&", "||", "!"]
SYMBOLS = [
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    ",",
    ";",
    ":",
    ".",
    "$",
    "#",
    "?",
    ":",
    "&",
    "::",
    "&",
    "|",
    "^",
    "~",
    "<<",
    ">>",
]


class Tokenizer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.line = 1
        self.column = 1

        self.__create_type_keywords()

    def __create_type_keywords(self):
        for keyword in BASE_TYPE_KEYWORDS:
            TYPE_KEYWORDS.append(keyword)
            TYPE_KEYWORDS.append("dyn_" + keyword)
            TYPE_KEYWORDS.append("dyn_dyn_" + keyword)

    def tokenize(self):
        tokens = []
        while self.pos < len(self.code):
            if token := self.__match_keyword():
                self.column += len(token.value)
            elif main_keyword := self.__match_main_keyword():
                token = Token(
                    TokenKind.MAIN_KEYWORD, main_keyword, self.line, self.column
                )
                self.column += len(main_keyword)
            elif type_keyword := self.__match_type_keyword():
                token = Token(
                    TokenKind.TYPE_KEYWORD, type_keyword, self.line, self.column
                )
                self.column += len(type_keyword)
            elif template_type_keyword := self.__match_template_type_keyword():
                token = Token(
                    TokenKind.TEMPLATE_TYPE_KEYWORD,
                    template_type_keyword,
                    self.line,
                    self.column,
                )
                self.column += len(template_type_keyword)
            elif access_modifier := self.__match_access_identifier():
                token = Token(
                    TokenKind.ACCESS_MODIFIER,
                    access_modifier,
                    self.line,
                    self.column,
                )
            elif modifier := self.__match_modifier():
                token = Token(TokenKind.MODIFIER, modifier, self.line, self.column)
                self.column += len(modifier)
            elif identifier := self.__match_identifier():
                token = Token(TokenKind.IDENTIFIER, identifier, self.line, self.column)
                self.column += len(identifier)
            elif multiline_comment := self.__match_multiline_comment():
                token = Token(
                    TokenKind.MULTI_LINE_COMMENT,
                    multiline_comment,
                    self.column,
                    self.line,
                )
                self.column += len(multiline_comment)
            elif comment := self.__match_comment():
                token = Token(TokenKind.COMMENT, comment, self.line, self.column)
                self.column += len(comment)
            elif token := self.__match_operator():
                self.column += len(token.value)
            elif number := self.__match_number():
                token = Token(TokenKind.NUMBER, number, self.line, self.column)
                self.column += len(number)
            elif symbol := self.__match_symbol():
                token = Token(TokenKind.SYMBOL, symbol, self.line, self.column)
                self.column += len(symbol)
            elif string := self.__match_string():
                token = Token(TokenKind.STRING_LITERAL, string, self.line, self.column)
                self.column += len(string)
            elif char := self.__match_char():
                token = Token(TokenKind.CHAR, char, self.line, self.column)
                self.column += len(char)
            elif divider := self.__match_divider():
                token = Token(TokenKind.DIVIDER, divider, self.line, self.column)
                self.column += len(divider)
            elif r := self.__match_whitespace():
                whitespace, new_line, new_line_start = r
                token = Token(TokenKind.WHITESPACE, whitespace, self.line, self.column)
                if new_line:
                    self.line += 1
                    self.column = new_line_start
            elif _ := self.__match_newline():
                token = Token(TokenKind.NEWLINE, None, self.line, self.column)
                self.line += 2
                self.column = 1
            else:
                raise SyntaxError(
                    f"Unexpected character {self.code[self.pos]} at line {self.line}, column {self.column}"
                )
            tokens.append(token)

        if not tokens or tokens[-1].kind != TokenKind.EOF:
            tokens.append(Token(TokenKind.EOF, "", self.line, self.column))

        return tokens

    def __match_keyword(self):
        # Regular expression to match "else if" with any amount of whitespace in between
        else_if_pattern = re.compile(r"else\s+if\b")

        # Check for "else if" with flexible whitespace
        match = else_if_pattern.match(self.code[self.pos :])
        if match:
            self.pos += match.end()
            return Token(TokenKind.ELSE_IF, "else if", self.line, self.column)

        # Check for "if"
        elif (
            self.code[self.pos : self.pos + 2] == "if"
            and not self.code[self.pos + 2].isalnum()
        ):
            self.pos += 2
            return Token(TokenKind.IF, "if", self.line, self.column)

        # Check for "else"
        elif (
            self.code[self.pos : self.pos + 4] == "else"
            and not self.code[self.pos + 4].isalnum()
        ):
            self.pos += 4
            return Token(TokenKind.ELSE, "else", self.line, self.column)

        # Check other keywords
        for keyword in KEYWORDS:
            if (
                self.code[self.pos : self.pos + len(keyword)] == keyword
                and not self.code[self.pos + len(keyword)].isalnum()
            ):
                self.pos += len(keyword)
                return Token(TokenKind.KEYWORD, keyword, self.line, self.column)

        return None

    def __match_type_keyword(self):
        keywordArr = TYPE_KEYWORDS + LIBRARY_TYPE_KEYWORDS
        for keyword in keywordArr:
            end_pos = self.pos + len(keyword)
            if self.code[self.pos : end_pos] == keyword:
                # Check if the next character (if exists) is not a valid identifier continuation
                if end_pos >= len(self.code) or not (
                    self.code[end_pos].isalnum() or self.code[end_pos] == "_"
                ):
                    self.pos = end_pos
                    return keyword
        return None

    def __match_operator(self):
        # Helper function to sort operators by length in descending order
        def sort_operators_by_length(operators):
            return sorted(operators, key=len, reverse=True)

        # Sort operators by length (longer operators first)
        sorted_comparison_operators = sort_operators_by_length(COMPARISON_OPERATORS)
        sorted_arithmetic_operators = sort_operators_by_length(ARITHMETIC_OPERATORS)
        sorted_logical_operators = sort_operators_by_length(LOGICAL_OPERATORS)
        sorted_assignment_operators = sort_operators_by_length(ASSIGNMENT_OPERATORS)

        # Check for comparison operators first
        for operator in sorted_comparison_operators:
            if self.code[self.pos : self.pos + len(operator)] == operator:
                # Special handling for '<' and '>'
                if operator in {"<", ">"}:
                    # Ensure it's not part of '<<' or '>>'
                    next_pos = self.pos + len(operator)
                    if next_pos < len(self.code) and self.code[next_pos] in {"<", ">"}:
                        continue  # Skip this match and let '<<' or '>>' handle it
                self.pos += len(operator)
                return Token(
                    TokenKind.COMPARISON_OPERATOR, operator, self.line, self.column
                )

        # Check for assignment operators
        for operator in sorted_assignment_operators:
            if self.code[self.pos : self.pos + len(operator)] == operator:
                self.pos += len(operator)
                return Token(
                    TokenKind.ASSIGNMENT_OPERATOR, operator, self.line, self.column
                )

        # Check for arithmetic operators
        for operator in sorted_arithmetic_operators:
            if self.code[self.pos : self.pos + len(operator)] == operator:
                self.pos += len(operator)
                return Token(
                    TokenKind.ARITHMETIC_OPERATOR, operator, self.line, self.column
                )

        # Check for logical operators
        for operator in sorted_logical_operators:
            if self.code[self.pos : self.pos + len(operator)] == operator:
                self.pos += len(operator)
                return Token(
                    TokenKind.LOGICAL_OPERATOR, operator, self.line, self.column
                )

        return None

    def __match_identifier(self):
        if self.code[self.pos].isalpha() or self.code[self.pos] == "_":
            start = self.pos
            self.pos += 1
            while self.pos < len(self.code) and (
                self.code[self.pos].isalnum() or self.code[self.pos] == "_"
            ):
                self.pos += 1
            return self.code[start : self.pos]
        return None

    def __match_number(self):
        start = self.pos

        # Hexadecimal: starts with '0x' or '0X'
        if self.code[self.pos : self.pos + 2].lower() == "0x":
            self.pos += 2
            while (
                self.pos < len(self.code)
                and self.code[self.pos] in "0123456789abcdefABCDEF"
            ):
                self.pos += 1
            # Check for unsigned suffix 'U' or long suffix 'L'
            if self.pos < len(self.code) and self.code[self.pos] in "uUlL":
                self.pos += 1
            return self.code[start : self.pos]

        # Binary: starts with '0b' or '0B'
        if self.code[self.pos : self.pos + 2].lower() == "0b":
            self.pos += 2
            while self.pos < len(self.code) and self.code[self.pos] in "01":
                self.pos += 1
            # Check for unsigned suffix 'U' or long suffix 'L'
            if self.pos < len(self.code) and self.code[self.pos] in "uUlL":
                self.pos += 1
            return self.code[start : self.pos]

        # Octal: starts with '0o' or '0O'
        if self.code[self.pos : self.pos + 2].lower() == "0o":
            self.pos += 2
            while self.pos < len(self.code) and self.code[self.pos] in "01234567":
                self.pos += 1
            # Check for unsigned suffix 'U' or long suffix 'L'
            if self.pos < len(self.code) and self.code[self.pos] in "uUlL":
                self.pos += 1
            return self.code[start : self.pos]

        # Floating-point: includes '.', 'e', or 'E'
        if self.code[self.pos].isdigit() or (
            self.pos + 1 < len(self.code)
            and self.code[self.pos] == "."
            and self.code[self.pos + 1].isdigit()
        ):
            has_dot = False
            has_exponent = False
            while self.pos < len(self.code):
                char = self.code[self.pos]
                if char == ".":
                    if has_dot:  # Second dot in number is invalid
                        break
                    has_dot = True
                elif char in "eE":
                    if has_exponent:  # Second exponent is invalid
                        break
                    has_exponent = True
                    self.pos += 1  # Move past 'e' or 'E'
                    if (
                        self.pos < len(self.code) and self.code[self.pos] in "+-"
                    ):  # Handle exponent sign
                        self.pos += 1
                    continue
                elif not char.isdigit():
                    break
                self.pos += 1
            # Check for optional floating-point suffix 'f' or 'F'
            if self.pos < len(self.code) and self.code[self.pos] in "fF":
                self.pos += 1
            return self.code[start : self.pos]

        # Decimal: digits only, allows underscores and optionally 'U' or 'L'
        if self.code[self.pos].isdigit():
            while self.pos < len(self.code):
                if self.code[self.pos] == "_":  # Allow underscores in numbers
                    self.pos += 1
                    continue
                elif not self.code[self.pos].isdigit():
                    break
                self.pos += 1
            # Check for unsigned suffix 'U' or long suffix 'L'
            if self.pos < len(self.code) and self.code[self.pos] in "uUlL":
                self.pos += 1
            return self.code[start : self.pos]

        return None

    def __match_whitespace(self) -> tuple:
        start = self.pos
        # Check for whitespace and single newline (but not empty lines)
        new_line = False
        new_line_start = None
        while self.pos < len(self.code) and (
            self.code[self.pos].isspace() or self.code[self.pos] == "\n"
        ):
            if self.code[self.pos] == "\n":  # Check if the newline starts an empty line
                temp_pos = self.pos + 1
                new_line = True
                new_line_start = 1
                while temp_pos < len(self.code) and self.code[temp_pos].isspace():
                    if (
                        self.code[temp_pos] == "\n"
                    ):  # Found a second newline, so not whitespace
                        return None
                    temp_pos += 1
                    new_line_start += 1
            self.pos += 1

        # Only return a match if we haven't detected an empty line (two consecutive newlines)
        return (
            self.code[start : self.pos] if start < self.pos else None,
            new_line,
            new_line_start,
        )

    def __match_newline(self):
        start = self.pos
        if self.code[self.pos] == "\n":
            temp_pos = self.pos + 1

            # Check if it's followed by another newline, possibly with only whitespace in between
            while temp_pos < len(self.code) and self.code[temp_pos].isspace():
                if self.code[temp_pos] == "\n":
                    self.pos = temp_pos + 1  # Move past the second newline
                    return self.code[start : self.pos]
                temp_pos += 1

        return None

    def __match_symbol(self):
        sorted_symbols = sorted(SYMBOLS, key=len, reverse=True)

        for symbol in sorted_symbols:
            if self.code[self.pos : self.pos + len(symbol)] == symbol:
                self.pos += len(symbol)
                return symbol
        return None

    def __match_char(self):
        char_regex = re.compile(r"'.*?'")

        match = char_regex.match(self.code[self.pos :])
        if match:
            self.pos += len(match.group())
            return match.group()

        return None

    def __match_string(self):
        str_regex = re.compile(r'(["\'])(?:\\.|[^\\])*?\1')

        match = str_regex.match(self.code[self.pos :])
        if match:
            self.pos += len(match.group())
            return match.group()

        return None

    def __match_divider(self):
        start = self.pos
        if self.code[self.pos] == "─":
            self.pos += 1

            if self.code[self.pos] == "/" and self.code[self.pos + 1] == "/":
                self.pos += 2
                while self.pos < len(self.code) and self.code[self.pos] != "\n":
                    self.pos += 1
                return self.code[start : self.pos]

            while self.pos < len(self.code) and self.code[self.pos] == "─":
                self.pos += 1
            return self.code[start : self.pos]
        elif self.code[self.pos] == "═":
            self.pos += 1
            while self.pos < len(self.code) and self.code[self.pos] == "═":
                self.pos += 1
            return self.code[start : self.pos]

        return None

    def __match_comment(self):
        if self.code[self.pos] == "/" and self.code[self.pos + 1] == "/":
            self.pos += 2
            start = self.pos
            while self.pos < len(self.code) and self.code[self.pos] != "\n":
                self.pos += 1
            return self.code[start : self.pos]
        return None

    def __match_main_keyword(self):
        if (
            self.code[self.pos : self.pos + 4] == "main"
            and not self.code[self.pos + 4].isalnum()
        ):
            self.pos += 4
            return "main"
        return None

    def __match_multiline_comment(self):
        if self.code[self.pos : self.pos + 2] == "/*":
            is_doc_comment = self.code[self.pos : self.pos + 3] == "/**"
            self.pos += 2 if not is_doc_comment else 3  # Skip '/*' or '/**'
            start = self.pos

            while (
                self.pos < len(self.code) and self.code[self.pos : self.pos + 2] != "*/"
            ):
                if self.code[self.pos] == "\n":
                    self.line += 1
                    self.column = 1
                else:
                    self.column += 1
                self.pos += 1

            if self.pos < len(self.code):
                end = self.pos
                self.pos += 2  # Skip '*/'
                return self.code[start:end]  # Return the content of the comment
        return None

    def __match_template_type_keyword(self):
        for keyword in TEMPLATE_TYPE_KEYWORDS:
            if (
                self.code[self.pos : self.pos + len(keyword)] == keyword
                and not self.code[self.pos + len(keyword)].isalnum()
            ):
                self.pos += len(keyword)
                return keyword
        return None

    def __match_access_identifier(self):
        for keyword in ACCESS_MODIFIERS:
            if (
                self.code[self.pos : self.pos + len(keyword)] == keyword
                and not self.code[self.pos + len(keyword)].isalnum()
            ):
                self.pos += len(keyword)
                return keyword
        return None

    def __match_modifier(self):
        for keyword in MODIFIERS:
            if (
                self.code[self.pos : self.pos + len(keyword)] == keyword
                and not self.code[self.pos + len(keyword)].isalnum()
            ):
                self.pos += len(keyword)
                return keyword
        return None
