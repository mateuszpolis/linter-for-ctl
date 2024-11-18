from enum import Enum


class Token:
    def __init__(self, kind, value, line, column):
        self.kind = kind
        self.value = value
        self.line = line
        self.column = column

    def __str__(self) -> str:
        value = self.value.replace("\n", "\\n").replace("\t", "\\t")
        return f"{self.kind}({self.value}) at line {self.line}, column {self.column}"

    def __repr__(self) -> str:
        return self.__str__()


class TokenError(BaseException):
    def __init__(self, error, token):
        # Store the error message and token information
        self.error = error
        self.token = token
        # Format the error message to include line and column
        self.message = f"{error} at line {token.line}, column {token.column}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class TokenKind(Enum):
    WHITESPACE = "WHITESPACE"
    EOF = "EOF"
    IDENTIFIER = "IDENTIFIER"
    NUMBER = "NUMBER"
    ARITHMETIC_OPERATOR = "ARITHMETIC_OPERATOR"
    COMPARISON_OPERATOR = "COMPARISON_OPERATOR"
    LOGICAL_OPERATOR = "LOGICAL_OPERATOR"
    ASSIGNMENT_OPERATOR = "ASSIGNMENT_OPERATOR"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    STRING_LITERAL = "STRING_LITERAL"
    COMMENT = "COMMENT"
    MULTI_LINE_COMMENT = "MULTI_LINE_COMMENT"
    DIVIDER = "DIVIDER"
    TYPE_KEYWORD = "TYPE_KEYWORD"
    MAIN_KEYWORD = "MAIN_KEYWORD"
    IF = "IF"
    ELSE = "ELSE"
    ELSE_IF = "ELSE_IF"
    TEMPLATE_TYPE_KEYWORD = "TEMPLATE_TYPE_KEYWORD"
    CHAR = "CHAR"
