from enum import Enum

class Token:
  def __init__(self, kind, value, line, column):
    self.kind = kind
    self.value = value
    self.line = line
    self.column = column
  
  def __str__(self) -> str:
    value = self.value.replace('\n', '\\n').replace('\t', '\\t')
    return f'{self.kind}({value})'
  
  def __repr__(self) -> str:
    return self.__str__()
  
class TokenKind(Enum):
  WHITESPACE = 'WHITESPACE'
  EOF = 'EOF'
  IDENTIFIER = 'IDENTIFIER'
  NUMBER = 'NUMBER'
  OPERATOR = 'OPERATOR'
  KEYWORD = 'KEYWORD'
  SYMBOL = 'SYMBOL'
  STRING_LITERAL = 'STRING_LITERAL'
  COMMENT = 'COMMENT'
  DIVIDER = 'DIVIDER'
  TYPE_KEYWORD = 'TYPE_KEYWORD'
  
