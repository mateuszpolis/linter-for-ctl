from nodes import AssignmentNode, AttributeAccessNode, BinaryExpressionNode, DeclarationNode, FunctionCallNode, FunctionDeclarationNode, GlobalIdentifierNode, IdentifierNode, IndexAccessNode, NumberNode, ProgramNode, StringNode
from token_ import TokenError, TokenKind


class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.pos = 0

  def __current(self):
    while self.pos < len(self.tokens) and self.tokens[self.pos].kind == TokenKind.WHITESPACE:
        self.pos += 1
    return self.tokens[self.pos]
  
  def __peek(self, n=1):
    pos = self.pos
    for _ in range(n):
      pos += 1
      while pos < len(self.tokens) and self.tokens[pos].kind == TokenKind.WHITESPACE:
          pos += 1
    return self.tokens[pos]
  
  def __advance(self):
    self.pos += 1
    while self.pos < len(self.tokens) and self.tokens[self.pos].kind == TokenKind.WHITESPACE:
        self.pos += 1
  
  def __match(self, kind):    
    if self.__current().kind == kind:      
      return True
    return False
  
  def __consume(self, kind):
    if self.__match(kind):
      token = self.__current()
      self.__advance()
      return token
    raise SyntaxError(f'Expected {kind} but got {self.__current().kind}. Token: {self.__current()}', self.__current().line, self.__current().column)
  
  def parse(self):
    statements = []
    while self.__current().kind != TokenKind.EOF:
      statement = self.__parse_statement()
      statements.append(statement)
    return ProgramNode(statements)
  
  # Non-terminal parsing functions

  def __parse_statement(self):
    if self.__match(TokenKind.IDENTIFIER) and self.__peek().kind == TokenKind.OPERATOR and self.__peek().value == "=":
      return self.__parse_assignment()
    elif self.__match(TokenKind.TYPE_KEYWORD) and self.__peek().kind == TokenKind.IDENTIFIER and (self.__peek(2).value == ";" or self.__peek(2).value == "=" or self.__peek(2).value == ","):
      return self.__parse_declaration()
    elif self.__match(TokenKind.TYPE_KEYWORD) and self.__peek().kind == TokenKind.IDENTIFIER and self.__peek(2).value == "(":
       return self.__parse_function_declaration()
    elif self.__match(TokenKind.IDENTIFIER) and self.__peek().kind == TokenKind.SYMBOL and self.__peek().value == "(":
      function_call = self.__parse_function_call()
      # Expect a semicolon
      self.__consume(TokenKind.SYMBOL)
      return function_call
    elif self.__match(TokenKind.DIVIDER):
      return self.__consume(TokenKind.DIVIDER)
    elif self.__match(TokenKind.COMMENT):
       return self.__consume(TokenKind.COMMENT)
    else:
      raise TokenError(SyntaxError("Unexpected statement. Token: " + str(self.__current()), self.__current().line, self.__current().column), self.__current())
    
  def __parse_assignment(self):
    identifier = self.__consume(TokenKind.IDENTIFIER)
    # Expect "=" operator
    self.__consume(TokenKind.OPERATOR)
    value = self.__parse_expression()
    # Expect a semicolon
    self.__consume(TokenKind.SYMBOL) 
    return AssignmentNode(identifier, value)
  
  def __parse_expression(self):
    # Parse the left side (higher precedence first)
    left = self.__parse_term()
    
    # Handle addition and subtraction (lower precedence)
    while self.__match(TokenKind.OPERATOR) and self.__current().value in ['+', '-']:
        operator = self.__consume(TokenKind.OPERATOR)
        right = self.__parse_term()
        left = BinaryExpressionNode(left, operator.value, right)
    
    return left
  
  def __parse_term(self):
    # Parse the left side
    left = self.__parse_factor()
    
    # Handle multiplication and division (higher precedence than + and -)
    while self.__match(TokenKind.OPERATOR) and self.__current().value in ['*', '/']:
        operator = self.__consume(TokenKind.OPERATOR)
        right = self.__parse_factor()
        left = BinaryExpressionNode(left, operator.value, right)
    
    return left
  
  def __parse_factor(self):
    # Start with the primary element (could be a number, identifier, or expression in parentheses)
    left = self.__parse_primary()
    
    # Handle attribute access and indexing (highest precedence)
    while True:
        if self.__match(TokenKind.SYMBOL) and self.__current().value == '.':
            # Consume the '.' and parse the attribute name
            self.__consume(TokenKind.SYMBOL)
            attribute = self.__consume(TokenKind.IDENTIFIER)
            left = AttributeAccessNode(left, attribute.value)
        
        elif self.__match(TokenKind.SYMBOL) and self.__current().value == '[':
            # Consume the '[' and parse the index expression
            self.__consume(TokenKind.SYMBOL)
            index = self.__parse_expression()
            if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ']'):
                raise SyntaxError("Expected closing ']' for list access")
            self.__consume(TokenKind.SYMBOL)
            left = IndexAccessNode(left, index)
        
        else:
            # No more attribute or index access
            break
    
    return left

  def __parse_primary(self):   
    if self.__match(TokenKind.NUMBER):
        return NumberNode(int(self.__consume(TokenKind.NUMBER).value))
    elif self.__match(TokenKind.STRING_LITERAL):
        return StringNode(self.__consume(TokenKind.STRING_LITERAL).value)
    elif self.__match(TokenKind.IDENTIFIER) and self.__peek().kind == TokenKind.SYMBOL and self.__peek().value == "(":
        return self.__parse_function_call()
    elif self.__match(TokenKind.IDENTIFIER):  
        return IdentifierNode(self.__consume(TokenKind.IDENTIFIER).value)
    elif self.__match(TokenKind.SYMBOL) and self.__current().value == "$":
        # Consume the "$" symbol
        self.__consume(TokenKind.SYMBOL)
        
        # Expect an identifier immediately following the "$"
        if not self.__match(TokenKind.IDENTIFIER):
            raise SyntaxError("Expected identifier after '$'")
        
        # Parse the identifier as a global variable
        identifier = self.__consume(TokenKind.IDENTIFIER)
        return GlobalIdentifierNode(identifier.value)
    elif self.__match(TokenKind.SYMBOL) and self.__current().value == "(":
        # __Consume the opening parenthesis
        self.__consume(TokenKind.SYMBOL)
        
        # Parse the inner expression
        expression = self.__parse_expression()
        
        # Expect and __consume the closing parenthesis
        if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ")"):
            raise SyntaxError("Expected closing parenthesis")
        self.__consume(TokenKind.SYMBOL)
        
        return expression
    else:
        raise SyntaxError("Expected a primary expression")

  def __parse_declaration(self):
    # Expect and consume the type keyword (e.g., "string")
    type_keyword = self.__consume(TokenKind.TYPE_KEYWORD)

    # Parse the first identifier
    identifier = self.__consume(TokenKind.IDENTIFIER)
    identifiers = [(identifier, None)]  # Start a list to hold identifiers and their initial values

    # Check if there's an initialization (only allowed for a single identifier)
    if self.__match(TokenKind.OPERATOR) and self.__current().value == "=":
        # Consume the "="
        self.__consume(TokenKind.OPERATOR)
        
        # Parse the initial value for the single identifier
        initial_value = self.__parse_expression()
        identifiers[0] = (identifier, initial_value)  # Update the first identifier with its initial value

        # Ensure there are no more identifiers after initialization
        if self.__match(TokenKind.SYMBOL) and self.__current().value == ",":
            raise SyntaxError("Cannot initialize multiple variables in a single declaration")
    
    # Parse additional identifiers if present (no initialization allowed)
    while self.__match(TokenKind.SYMBOL) and self.__current().value == ",":
        # Consume the comma
        self.__consume(TokenKind.SYMBOL)
        
        # Expect and consume the next identifier
        identifier = self.__consume(TokenKind.IDENTIFIER)
        identifiers.append((identifier, None))  # Add the identifier without initialization

    # Expect and consume the semicolon at the end of the declaration
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
        raise SyntaxError("Expected ';' at the end of declaration")
    self.__consume(TokenKind.SYMBOL)

    # Return a DeclarationNode with the type and list of identifiers
    return DeclarationNode(type_keyword.value, identifiers)

  def __parse_function_declaration(self):
    # Expect and consume the type keyword (e.g., "string")
    type_keyword = self.__consume(TokenKind.TYPE_KEYWORD)

    # Expect and consume the function name (identifier)
    function_name = self.__consume(TokenKind.IDENTIFIER)

    # Expect and consume the opening parenthesis for the parameter list
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == "("):
        raise SyntaxError("Expected '(' after function name")
    self.__consume(TokenKind.SYMBOL)

    # Parse the parameter list
    parameters = self.__parse_parameter_list()

    # Expect and consume the closing parenthesis for the parameter list
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ")"):
        raise SyntaxError("Expected ')' after parameter list")
    self.__consume(TokenKind.SYMBOL)

    # Expect and consume the opening brace for the function body
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == "{"):
        raise SyntaxError("Expected '{' before function body")
    self.__consume(TokenKind.SYMBOL)

    # Parse the statements in the function body
    statements = []
    while not (self.__match(TokenKind.SYMBOL) and self.__current().value == "}"):
        statement = self.__parse_statement()
        statements.append(statement)

    # Expect and consume the closing brace for the function body
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == "}"):
        raise SyntaxError("Expected '}' after function body")
    self.__consume(TokenKind.SYMBOL)

    # Return a FunctionDeclarationNode with the parsed information
    return FunctionDeclarationNode(type_keyword.value, function_name.value, parameters, statements)
  
  def __parse_parameter_list(self):
    # Start with an empty list of parameters
    parameters = []
    
    # Check for the case where there are no parameters
    if self.__match(TokenKind.SYMBOL) and self.__current().value == ")":
        return parameters
    
    # Parse the first parameter
    parameter = self.__parse_parameter()
    parameters.append(parameter)
    
    # Parse additional parameters if present
    while self.__match(TokenKind.SYMBOL) and self.__current().value == ",":
        # Consume the comma
        self.__consume(TokenKind.SYMBOL)
        
        # Parse the next parameter
        parameter = self.__parse_parameter()
        parameters.append(parameter)
    
    return parameters
  
  def __parse_parameter(self):
    # Expect and consume the type keyword (e.g., "string")
    type_keyword = self.__consume(TokenKind.TYPE_KEYWORD)

    # Expect and consume the parameter name (identifier)
    parameter_name = self.__consume(TokenKind.IDENTIFIER)

    # Return a tuple with the type keyword and parameter name
    return (type_keyword.value, parameter_name.value)
  
  def __parse_function_call(self):
    # Expect and consume the function name (identifier)
    function_name = self.__consume(TokenKind.IDENTIFIER).value

    # Expect and consume the opening parenthesis
    self.__consume(TokenKind.SYMBOL)
    
    # Parse arguments (expressions within parentheses)
    arguments = self.__parse_arguments()
    
    # Expect and consume the closing parenthesis
    self.__consume(TokenKind.SYMBOL)
    
    return FunctionCallNode(function_name, arguments)
  
  def __parse_arguments(self):
    # Start with an empty list of arguments
    arguments = []
    
    # Check for the case where there are no arguments
    if self.__match(TokenKind.SYMBOL) and self.__current().value == ")":
        return arguments
    
    # Parse the first argument
    argument = self.__parse_expression()
    arguments.append(argument)
    
    # Parse additional arguments if present
    while self.__match(TokenKind.SYMBOL) and self.__current().value == ",":
        # Consume the comma
        self.__consume(TokenKind.SYMBOL)
        
        # Parse the next argument
        argument = self.__parse_expression()
        arguments.append(argument)
    
    return arguments
