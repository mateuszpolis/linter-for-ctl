import re
from token_ import Token, TokenKind

KEYWORDS = ['if', 'else', 'while', 'for', 'return', 'break', 'continue', 'true', 'false', 'null']
TYPE_KEYWORDS = ['string', 'dyn_string', 'int', 'dyn_int', 'float', 'dyn_float', 'bool', 'dyn_bool', 'void', 'main', 'dyn_dyn_string']
OPERATORS = ['+', '-', '*', '/', '%', '==', '!=', '>', '>=', '<', '<=', '&&', '||', '!', '=', '+=', '-=', '*=', '/=', '%=', '++', '--']
SYMBOLS = ['(', ')', '{', '}', '[', ']', ',', ';', ':', '.', '$']

class Tokenizer:
  def __init__(self, code):
    self.code = code
    self.pos = 0
    self.line = 1
    self.column = 1

  def tokenize(self):
    tokens = []
    while self.pos < len(self.code):
      if keyword := self.__match_keyword():
        token = Token(TokenKind.KEYWORD, keyword, self.line, self.column)
        self.column += len(keyword)
      elif type_keyword := self.__match_type_keyword():
        token = Token(TokenKind.TYPE_KEYWORD, type_keyword, self.line, self.column)
        self.column += len(type_keyword)
      elif identifier := self.__match_identifier():
        token = Token(TokenKind.IDENTIFIER, identifier, self.line, self.column)
        self.column += len(identifier)
      elif comment := self.__match_comment():
        token = Token(TokenKind.COMMENT, comment, self.line, self.column)
        self.column += len(comment)
      elif operator := self.__match_operator():
        token = Token(TokenKind.OPERATOR, operator, self.line, self.column)
        self.column += len(operator)
      elif number := self.__match_number():
        token = Token(TokenKind.NUMBER, number, self.line, self.column)
        self.column += len(number)
      elif symbol := self.__match_symbol():
        token = Token(TokenKind.SYMBOL, symbol, self.line, self.column)
        self.column += len(symbol)
      elif string := self.__match_string():
        token = Token(TokenKind.STRING_LITERAL, string, self.line, self.column)
        self.column += len(string)
      elif divider := self.__match_divider():
        token = Token(TokenKind.DIVIDER, divider, self.line, self.column)
        self.column += len(divider)
      elif whitespace := self.__match_whitespace():
        token = Token(TokenKind.WHITESPACE, whitespace, self.line, self.column)
        self.line += whitespace.count('\n')
        self.column = 1
      else:
        raise SyntaxError(f'Unexpected character {self.code[self.pos]} at line {self.line}, column {self.column}')
      tokens.append(token)

    if not tokens or tokens[-1].kind != TokenKind.EOF:
      tokens.append(Token(TokenKind.EOF, '', self.line, self.column))

    return tokens
  
  def __match_keyword(self):
    for keyword in KEYWORDS:
      if self.code[self.pos:self.pos + len(keyword)] == keyword and not self.code[self.pos + len(keyword)].isalnum():
        self.pos += len(keyword)
        return keyword 
    return None
  
  def __match_type_keyword(self):
    for keyword in TYPE_KEYWORDS:
      if self.code[self.pos:self.pos + len(keyword)] == keyword and not self.code[self.pos + len(keyword)].isalnum():
        self.pos += len(keyword)
        return keyword 
    return None

  def __match_operator(self):
    for operator in OPERATORS:
      if self.code[self.pos:self.pos + len(operator)] == operator:
        self.pos += len(operator)
        return operator
    return None
  
  def __match_identifier(self):
    if self.code[self.pos].isalpha() or self.code[self.pos] == '_':
      start = self.pos
      self.pos += 1
      while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == '_'):
        self.pos += 1
      return self.code[start:self.pos]
    return None
  
  def __match_number(self):
    if self.code[self.pos].isdigit():
      start = self.pos
      self.pos += 1
      while self.pos < len(self.code) and self.code[self.pos].isdigit():
        self.pos += 1
      return self.code[start:self.pos]
    return None
  
  def __match_whitespace(self):
    if self.code[self.pos].isspace():
      start = self.pos
      self.pos += 1
      while self.pos < len(self.code) and self.code[self.pos].isspace():
        self.pos += 1
      return self.code[start:self.pos]
    return None
  
  def __match_symbol(self):
    for symbol in SYMBOLS:
      if self.code[self.pos:self.pos + len(symbol)] == symbol:
        self.pos += len(symbol)
        return symbol
    return None

  def __match_string(self):
    str_regex = re.compile(r'\".*?\"')
      
    match = str_regex.match(self.code[self.pos:])
    if match:
      self.pos += len(match.group())
      return match.group()
    
    return None
  
  def __match_divider(self):
    start = self.pos
    if self.code[self.pos] == '─':
      self.pos += 1

      if self.code[self.pos] == '/' and self.code[self.pos + 1] == '/':
        self.pos += 2
        while self.pos < len(self.code) and self.code[self.pos] != '\n':
          self.pos += 1
        return self.code[start:self.pos]

      while self.pos < len(self.code) and self.code[self.pos] == '─':
        self.pos += 1
      return self.code[start:self.pos]
    elif self.code[self.pos] == '═':
      self.pos += 1
      while self.pos < len(self.code) and self.code[self.pos] == '═':
        self.pos += 1
      return self.code[start:self.pos]
    
    return None
  
  def __match_comment(self):
    start = self.pos
    if self.code[self.pos] == '/' and self.code[self.pos + 1] == '/':
      self.pos += 2
      while self.pos < len(self.code) and self.code[self.pos] != '\n':
        self.pos += 1
      return self.code[start:self.pos]
    return None