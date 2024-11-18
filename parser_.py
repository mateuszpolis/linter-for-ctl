from nodes import AssignmentNode, AttributeAccessNode, BinaryExpressionNode, BlockNode, BreakNode, CommentNode, DeclarationNode, DividerNode, ElseIfClauseNode, FunctionCallNode, FunctionDeclarationNode, GlobalIdentifierNode, IdentifierNode, IfStatementNode, IndexAccessNode, MainNode, MultilineCommentNode, NumberNode, ProgramNode, ReturnNode, StringNode
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
    raise TokenError(SyntaxError(f'Expected {kind} but got {self.__current().kind}. Token: {self.__current()}', self.__current().line, self.__current().column), self.__current())
  
  def parse(self):
    statements = []
    while self.__current().kind != TokenKind.EOF:
      statement = self.__parse_statement()
      statements.append(statement)
    return ProgramNode(statements)
  
  # Non-terminal parsing functions

  def __parse_statement(self):
    if self.__detect_assignment():
      return self.__parse_assignment()
    elif self.__match(TokenKind.TYPE_KEYWORD) and self.__peek().kind == TokenKind.IDENTIFIER and (self.__peek(2).value == ";" or self.__peek(2).value == "=" or self.__peek(2).value == ","):
      return self.__parse_declaration()
    elif self.__match(TokenKind.TYPE_KEYWORD) and self.__peek().kind == TokenKind.IDENTIFIER and self.__peek(2).value == "(":
      return self.__parse_function_declaration()
    elif self.__detect_function_call():
      function_call = self.__parse_expression()
      self.__consume(TokenKind.SYMBOL)
      return function_call
    elif self.__match(TokenKind.DIVIDER):
      divider_value = self.__consume(TokenKind.DIVIDER).value
      return DividerNode(divider_value)
    elif self.__match(TokenKind.COMMENT):
      comment = self.__consume(TokenKind.COMMENT)
      return CommentNode(comment.value)
    elif self.__match(TokenKind.IF):
      return self.__parse_if_statement()
    elif self.__match(TokenKind.MAIN_KEYWORD):
      return self.__parse_main()
    elif self.__match(TokenKind.MULTI_LINE_COMMENT):
      multi_line_comment = self.__consume(TokenKind.MULTI_LINE_COMMENT)
      return MultilineCommentNode(multi_line_comment.value.split('\n'))
    elif self.__match(TokenKind.KEYWORD) and self.__current().value == "return":
      return self.__parse_return_statement()
    elif self.__match(TokenKind.KEYWORD) and self.__current().value == "break":
       return self.__parse_break_statement()
    else:
      raise TokenError(SyntaxError("Unexpected statement. Token: " + str(self.__current()), self.__current().line, self.__current().column), self.__current())

  # Helper functions for detecting specific statement types

  def __detect_assignment(self):
    # Start by checking if we have an identifier
    if self.__match(TokenKind.IDENTIFIER):
        n = 1
        
        # Loop to handle attribute and index access on the left side
        while self.__peek(n).kind == TokenKind.SYMBOL:
            next_symbol = self.__peek(n).value
            if next_symbol == ".":
                # Attribute access expects another identifier after the dot
                if self.__peek(n + 1).kind == TokenKind.IDENTIFIER:
                    n += 2
                else:
                    return False
            elif next_symbol == "[":
                # Index access expects an expression and a closing bracket
                n += 1  # Move past "["
                while not (self.__peek(n).kind == TokenKind.SYMBOL and self.__peek(n).value == "]"):
                    n += 1
                n += 1  # Move past "]"
            else:
                break

        # After parsing the left side, expect an "=" operator for assignment
        if self.__peek(n).kind == TokenKind.ASSIGNMENT_OPERATOR:
            return True

    return False

  def __detect_function_call(self):
    # Start by checking if we have an identifier, which is the root of the potential function call
    if not self.__match(TokenKind.IDENTIFIER):
        return False

    n = 1  # Start peeking after the initial identifier
    
    # Loop to handle attribute and index access, building up the expression chain
    while self.__peek(n).kind == TokenKind.SYMBOL:
        next_symbol = self.__peek(n).value
        
        if next_symbol == ".":
            # Attribute access expects another identifier after the dot
            if self.__peek(n + 1).kind == TokenKind.IDENTIFIER:
                n += 2
            else:
                return False  # Invalid attribute access

        elif next_symbol == "[":
            # Index access expects an expression and a closing bracket
            n += 1  # Move past "["
            # Scan until we find the matching "]"
            while not (self.__peek(n).kind == TokenKind.SYMBOL and self.__peek(n).value == "]"):
                n += 1
                if n >= len(self.tokens):  # Prevent infinite loop if "]" is missing
                    return False
            n += 1  # Move past "]"

        else:
            break

    # After building up the expression chain, check if the next token is "(" for a function call
    if self.__peek(n).kind == TokenKind.SYMBOL and self.__peek(n).value == "(":
        return True

    return False

  # Non-terminal parsing functions

  def __parse_assignment(self):
    # Use parse_factor to parse the left side, allowing for complex access expressions
    left = self.__parse_factor()
    
    # Expect "=" operator
    if not self.__match(TokenKind.ASSIGNMENT_OPERATOR):
        raise TokenError("Expected '=' in assignment", self.__current())
    self.__consume(TokenKind.ASSIGNMENT_OPERATOR)

    # Parse the right side (assignment value) as a comparison, allowing for complex expressions returning boolean values as well
    value = self.__parse_comparison()
    
    # Expect a semicolon
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
        raise TokenError("Expected ';' at the end of assignment", self.__current())
    self.__consume(TokenKind.SYMBOL)

    return AssignmentNode(left, value)

  
  def __parse_expression(self):
    # Parse the left side (higher precedence first)
    left = self.__parse_term()
    
    # Handle addition and subtraction (lower precedence)
    while self.__match(TokenKind.ARITHMETIC_OPERATOR) and self.__current().value in ['+', '-']:
        operator = self.__consume(TokenKind.ARITHMETIC_OPERATOR)
        right = self.__parse_term()
        left = BinaryExpressionNode(left, operator.value, right)
    
    return left
  
  def __parse_term(self):
    # Parse the left side
    left = self.__parse_factor()
    
    # Handle multiplication and division (higher precedence than + and -)
    while self.__match(TokenKind.ARITHMETIC_OPERATOR) and self.__current().value in ['*', '/']:
        operator = self.__consume(TokenKind.ARITHMETIC_OPERATOR)
        right = self.__parse_factor()
        left = BinaryExpressionNode(left, operator.value, right)
    
    return left
  
  def __parse_factor(self):
    # Start by parsing a primary expression
    node = self.__parse_primary()

    # Handle attribute access (.) and list indexing ([]), potentially followed by a function call
    while True:
        if self.__match(TokenKind.SYMBOL) and self.__current().value == ".":
            # Consume the dot and parse the attribute name
            self.__consume(TokenKind.SYMBOL)
            attribute = self.__consume(TokenKind.IDENTIFIER).value
            node = AttributeAccessNode(node, attribute)
            
        elif self.__match(TokenKind.SYMBOL) and self.__current().value == "[":
            # Handle list indexing as usual
            self.__consume(TokenKind.SYMBOL)
            index = self.__parse_expression()
            if not (self.__match(TokenKind.SYMBOL) and self.__current().value == "]"):
                raise SyntaxError("Expected closing ']' for list access")
            self.__consume(TokenKind.SYMBOL)
            node = IndexAccessNode(node, index)

        else:
            # No more access chaining, break out of the loop
            break
        
        # Check if the attribute is followed by a function call
        if self.__match(TokenKind.SYMBOL) and self.__current().value == "(":
            node = self.__parse_function_call(node)  # Treat as a function call on the attribute

    return node


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
        print (self.__current())
        raise SyntaxError("Expected a primary expression")

  def __parse_declaration(self):
    # Expect and consume the type keyword (e.g., "string")
    type_keyword = self.__consume(TokenKind.TYPE_KEYWORD)

    # Parse the first identifier
    identifier = self.__consume(TokenKind.IDENTIFIER)
    identifiers = [(identifier, None)]  # Start a list to hold identifiers and their initial values

    # Check if there's an initialization (only allowed for a single identifier)
    if self.__match(TokenKind.ASSIGNMENT_OPERATOR):
        # Consume the "="
        self.__consume(TokenKind.ASSIGNMENT_OPERATOR)
        
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

    block = self.__parse_block()

    # Return a FunctionDeclarationNode with the parsed information
    return FunctionDeclarationNode(type_keyword.value, function_name.value, parameters, block)
  
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
  
  def __parse_function_call(self, function_expression=None):
    # If no function expression is provided, assume a standalone function call with an identifier
    if function_expression is None:
        # Expect and consume the function name (identifier)
        function_expression = IdentifierNode(self.__consume(TokenKind.IDENTIFIER).value)

    # Expect and consume the opening parenthesis
    self.__consume(TokenKind.SYMBOL)
    
    # Parse arguments (expressions within parentheses)
    arguments = self.__parse_arguments()
    
    # Expect and consume the closing parenthesis
    self.__consume(TokenKind.SYMBOL)
    
    return FunctionCallNode(function_expression, arguments)

  
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

  def __parse_main(self):
    # Expect and consume the "main" keyword
    self.__consume(TokenKind.MAIN_KEYWORD)

    # Expect and consume the opening parenthesis for the main function parameter list
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == "("):
        raise SyntaxError("Expected '(' after 'main'")
    self.__consume(TokenKind.SYMBOL)

    # Parse the argument list for the main function (should be empty)
    parameters = self.__parse_parameter_list()      

    # Expect and consume the closing parenthesis for the main function parameter list
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ")"):
        raise SyntaxError("Expected ')' after main function parameter list")
    self.__consume(TokenKind.SYMBOL)

    block = self.__parse_block()

    # Return a FunctionDeclarationNode with the parsed information
    return MainNode(parameters, block)
  
  def __parse_if_statement(self):
    # Consume the "if" keyword
    self.__consume(TokenKind.IF)
    
    # Parse the condition within parentheses
    self.__consume(TokenKind.SYMBOL)
    condition = self.__parse_comparison()
    self.__consume(TokenKind.SYMBOL)
    
    # Parse the "if" block
    if_block = self.__parse_block()
    
    # Parse any "else if" clauses
    else_if_clauses = []
    while self.__match(TokenKind.ELSE_IF):
        self.__consume(TokenKind.ELSE_IF)
        
        self.__consume(TokenKind.SYMBOL)
        else_if_condition = self.__parse_comparison()
        self.__consume(TokenKind.SYMBOL)
        
        else_if_block = self.__parse_block()
        else_if_clauses.append(ElseIfClauseNode(else_if_condition, else_if_block))
    
    # Parse an optional "else" clause
    else_block = None
    if self.__match(TokenKind.ELSE):
        self.__consume(TokenKind.ELSE)
        else_block = self.__parse_block()
    
    return IfStatementNode(condition, if_block, else_if_clauses, else_block)

  def __parse_block(self):
    statements = []
    self.__consume(TokenKind.SYMBOL)
    while not (self.__match(TokenKind.SYMBOL) and self.__current().value == "}"):
        statements.append(self.__parse_statement())
    self.__consume(TokenKind.SYMBOL)
    return BlockNode(statements)
  
  def __parse_comparison(self):
    # Parse the left side of the comparison
    left = self.__parse_expression()

    # Check for comparison operators
    while self.__match(TokenKind.COMPARISON_OPERATOR):
        operator = self.__consume(TokenKind.COMPARISON_OPERATOR)
        right = self.__parse_expression()
        left = BinaryExpressionNode(left, operator.value, right)
    
    return left

  def __parse_return_statement(self):
      # Consume the "return" keyword
      self.__consume(TokenKind.KEYWORD)

      # Parse the return value expression if present
      expression = None
      if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
          expression = self.__parse_expression()

      # Expect and consume the semicolon at the end of the return statement
      if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
          raise SyntaxError("Expected ';' at the end of return statement")
      self.__consume(TokenKind.SYMBOL)

      return ReturnNode(expression)
  
  def __parse_break_statement(self):
    # Consume the "break" keyword
    self.__consume(TokenKind.KEYWORD)

    # Expect and consume the semicolon at the end of the break statement
    if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
        raise SyntaxError("Expected ';' at the end of break statement")
    self.__consume(TokenKind.SYMBOL)

    return BreakNode()