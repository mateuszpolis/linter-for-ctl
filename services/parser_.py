from typing import Any, List, Tuple

from entities.nodes import (AssignmentNode, AttributeAccessNode, BinaryExpressionNode,
                   BitwiseAndNode, BitwiseOrNode, BitwiseXorNode, BlockNode,
                   BooleanNode, BreakNode, CaseStatementNode, CharNode,
                   ClassDeclarationNode, ClassInitializationNode,
                   ClassStaticAccessNode, CommentNode, CompoundAssignmentNode,
                   ContinueNode, DeclarationNode, DividerNode, DoWhileLoopNode, ElseClauseNode,
                   ElseIfClauseNode, EnumAccessNode, EnumDeclarationNode,
                   EnumValueNode, ForLoopNode, FunctionCallNode,
                   FunctionDeclarationNode, GlobalIdentifierNode,
                   IdentifierNode, IfStatementNode, IncrementAssignmentNode,
                   IndexAccessNode, InheritanceNode, LibraryNode,
                   LogicalAndNode, LogicalOrNode,
                   MultilineCommentNode, NegationNode, NewLineNode, NumberNode,
                   ParameterNode, PointerNode, ProgramNode, RelationalNode,
                   ReturnNode, ShiftNode, StringNode, StructDeclarationNode,
                   SwitchStatementNode, TemplateTypeNode,
                   TernaryExpressionNode, TryCatchNode, TypeCastNode, TypeNode,
                   WhileLoopNode)
from entities.token_ import Token, TokenError, TokenKind


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.symbol_table = {
            "enums": {},  # Maps enum names to their values
            "structs": {},  # Maps struct names to their fields
            "classes": {},  # Maps class names to their fields
        }
        self.statements = []

    def __current(self):
        while (
            self.pos < len(self.tokens)
            and self.tokens[self.pos].kind == TokenKind.WHITESPACE
        ):
            self.pos += 1
        return self.tokens[self.pos]

    def __peek(self, n=1) -> Token:
        pos = self.pos
        for _ in range(n):
            pos += 1
            while (
                pos < len(self.tokens) and self.tokens[pos].kind == TokenKind.WHITESPACE
            ):
                pos += 1
        return self.tokens[pos]

    def __advance(self) -> bool:
        """Advance to the next token

        Returns:
            bool: Whether NewLineNode should be appended before
        """
        newline = False

        self.pos += 1
        while (
            self.pos < len(self.tokens)
            and self.tokens[self.pos].kind == TokenKind.WHITESPACE
        ):
            if self.tokens[self.pos].kind == TokenKind.WHITESPACE and self.tokens[self.pos].value == "\n":
                newline = True
            self.pos += 1

        return newline

    def __match(self, kind):
        if self.__current().kind == kind:
            return True
        return False

    def __consume(self, kind) -> Token:        
        if self.__match(kind):
            token = self.__current()
            append_newline = self.__advance()
            if append_newline:
                # TODO: This is not a good approach, but newlines need to be done
                pass
                # print(f"Appending newline. {token}")
                # self.statements.append(NewLineNode)
            return token
        raise TokenError(
            SyntaxError(
                f"Expected {kind} but got {self.__current().kind}. Token: {self.__current()}",
                self.__current().line,
                self.__current().column,
            ),
            self.__current(),
        )

    def parse(self):        
        while self.__current().kind != TokenKind.EOF:
            statement = self.__parse_statement()
            self.statements.append(statement)
        return ProgramNode(self.statements)

    # Non-terminal parsing functions

    def __parse_statement(self):
        if self.__detect_assignment():
            return self.__parse_assignment()
        elif self.__detect_function_declaration():
            return self.__parse_function_declaration()
        elif self.__detect_declaration():
            return self.__parse_declaration()
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
            if_statement = self.__parse_if_statement()
            # Check for optional ';' at the end of the if statement
            if self.__match(TokenKind.SYMBOL) and self.__current().value == ";":
                self.__consume(TokenKind.SYMBOL)
            return if_statement        
        elif self.__match(TokenKind.MULTI_LINE_COMMENT):
            multi_line_comment = self.__consume(TokenKind.MULTI_LINE_COMMENT)
            return MultilineCommentNode(multi_line_comment.value.split("\n"))
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "return":
            return self.__parse_return_statement()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "break":
            return self.__parse_break_statement()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "while":
            return self.__parse_while_statement()
        elif self.__match(TokenKind.SYMBOL) and self.__current().value == "#":
            return self.__parse_library_import()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "for":
            return self.__parse_for_loop()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "enum":
            return self.__parse_enum_declaration()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "switch":
            return self.__parse_switch_statement()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "struct":
            return self.__parse_struct_declaration()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "class":
            return self.__parse_class_declaration()
        elif self.__match(TokenKind.SYMBOL) and self.__current().value == "{":
            return self.__parse_block()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "continue":
            return self.__parse_continue_statement()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "try":
            return self.__parse_try_catch()
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "do":
            return self.__parse_do_while_loop()
        else:
            raise TokenError(
                SyntaxError("Unexpected statement"),
                self.__current(),
            )

    # Helper functions for detecting specific statement types

    def __detect_class_initialization(self):
        if self.__detect_type(self.__current()) and self.__peek().value == "(":
            return True
        return False

    def __detect_declaration(self) -> bool:
        """Detect declaration

        Returns:
            bool: Wheter declaration is detected or not
        """
        if (
            self.__detect_type(self.__current())
            and self.__peek().kind == TokenKind.IDENTIFIER
            and (
                self.__peek(2).value == ";"
                or self.__peek(2).value == "="
                or self.__peek(2).value == ","
            )
        ):
            return True
        elif (
            self.__match(TokenKind.TEMPLATE_TYPE_KEYWORD) and self.__peek().value == "<"
        ):
            return True
        elif self.__match(TokenKind.KEYWORD) and self.__current().value == "const":
            return True
        elif self.__match(TokenKind.ACCESS_MODIFIER):
            return True
        else:
            return False

    def __detect_function_declaration(self):
        peek_index = 0

        # Check for optional access modifier
        if self.__current().kind == TokenKind.ACCESS_MODIFIER:
            peek_index += 1

        # Check for optional modifier (e.g., static, global)
        if self.__peek(peek_index).kind == TokenKind.MODIFIER:
            peek_index += 1

        # Check for optional type
        if self.__detect_type(self.__peek(peek_index)):
            peek_index += 1

        # Check for identifier (it is not necessary for constructors)
        if self.__peek(peek_index).kind == TokenKind.IDENTIFIER:
            peek_index += 1

        # The function might be a main function
        if self.__peek(peek_index).kind == TokenKind.MAIN_KEYWORD:
            peek_index += 1

        # Check for opening parenthesis '('
        if self.__peek(peek_index).value == "(":
            peek_index += 1

            # Find the closing parenthesis ')'
            while self.__peek(peek_index).value != ")":
                peek_index += 1
            peek_index += 1  # Move past the closing parenthesis

            # Check if the next token is the opening brace '{'
            if self.__peek(peek_index).value == "{":
                return True

        # If none of the patterns match, it's not a function declaration
        return False

    def __detect_type(self, token):
        if token.kind == TokenKind.TYPE_KEYWORD:
            return True
        if token.kind == TokenKind.TEMPLATE_TYPE_KEYWORD:
            return True

        # Check if the token is a dynamically created type (enum, struct, class)
        if token.kind == TokenKind.IDENTIFIER:
            if token.value in self.symbol_table["enums"]:
                return True
            if token.value in self.symbol_table["structs"]:
                return True
            if token.value in self.symbol_table["classes"]:
                return True

        return False

    def __parse_function_declaration(self) -> FunctionDeclarationNode:
        """FunctionDeclaration -> AccessModifier? Modifier? Type? (identifier | "main") "(" ParameterList? ")" Block_summary_

        Raises:
            SyntaxError: When the function declaration is missing a block
            SyntaxError: When the function declaration is missing a closing parenthesis

        Returns:
            FunctionDeclarationNode: The parsed function declaration node
        """
        # Check if the function declaration starts with an access modifier
        access_modifier = None
        if self.__current().kind == TokenKind.ACCESS_MODIFIER:
            access_modifier = self.__consume(TokenKind.ACCESS_MODIFIER).value

        # Parse optional modifiers (static, global, etc.)
        modifiers = []
        while self.__current().kind == TokenKind.MODIFIER:
            modifiers.append(self.__consume(TokenKind.MODIFIER).value)

        # Check if the next token is a type or skip it
        type_ = None
        if self.__detect_type(self.__current()):
            type_ = self.__parse_type()

        function_name = None
        is_constructor = False
        is_main = False
        # If the next token is '(' this function is a constructor and we skip the identifier parsing
        if (self.__match(TokenKind.IDENTIFIER) or self.__match(TokenKind.MAIN_KEYWORD)) and self.__peek().value == "(":
            # Check if the function is a 'main' function
            if self.__match(TokenKind.MAIN_KEYWORD):
                is_main = True
                function_name = self.__consume(TokenKind.MAIN_KEYWORD)
            else:
                # Expect and consume the function name (identifier)
                function_name = self.__consume(TokenKind.IDENTIFIER)                
        elif self.__match(TokenKind.SYMBOL) and self.__current().value == "(":
            function_name = type_
            is_constructor = True

        # Expect and consume the opening parenthesis for the parameter list
        if not (
            self.__current().kind == TokenKind.SYMBOL and self.__current().value == "("
        ):
            raise SyntaxError("Expected '(' after function name")
        self.__consume(TokenKind.SYMBOL)

        # Parse the parameter list
        parameters = self.__parse_parameter_list()

        # Expect and consume the closing parenthesis for the parameter list
        if not (
            self.__current().kind == TokenKind.SYMBOL and self.__current().value == ")"
        ):
            raise SyntaxError("Expected ')' after parameter list")
        self.__consume(TokenKind.SYMBOL)

        # Parse the block
        block = self.__parse_block()

        # Return a FunctionDeclarationNode with the parsed information
        return FunctionDeclarationNode(
            type_,
            function_name.value,
            parameters,
            block,
            access_modifier,
            is_constructor,
            modifiers[0] if len(modifiers) > 0 else None,
            is_main,
        )

    def __detect_assignment(self):
        # Check for Increment assignment
        # The '++i' case
        if self.__match(TokenKind.ARITHMETIC_OPERATOR) and self.__current().value in [
            "++",
            "--",
        ]:
            return True

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
                    while not (
                        self.__peek(n).kind == TokenKind.SYMBOL
                        and self.__peek(n).value == "]"
                    ):
                        n += 1
                    n += 1  # Move past "]"
                else:
                    break

            # After parsing the left side, expect an assignment operator for assignment
            if self.__peek(n).kind == TokenKind.ASSIGNMENT_OPERATOR:
                return True
            # The 'i++' case
            elif self.__peek(n).kind == TokenKind.ARITHMETIC_OPERATOR and self.__peek(
                n
            ).value in ["++", "--"]:
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
                while not (
                    self.__peek(n).kind == TokenKind.SYMBOL
                    and self.__peek(n).value == "]"
                ):
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

    def __parse_conditional_expression(self):
        """ConditionalExpression -> TernaryExpression | Comparison"""
        # First parse Comparison
        condition = self.__parse_comparison()

        # Check if the next token is "?" for a ternary expression
        if not self.__match(TokenKind.SYMBOL) or self.__current().value != "?":
            return condition
        self.__consume(TokenKind.SYMBOL)

        # Parse the true branch
        true_branch = self.__parse_expression()

        # Expect the ":" operator
        if not self.__match(TokenKind.SYMBOL) or self.__current().value != ":":
            raise TokenError("Expected ':' in ternary expression", self.__current())
        self.__consume(TokenKind.SYMBOL)

        # Parse the false branch
        false_branch = self.__parse_expression()

        return TernaryExpressionNode(condition, true_branch, false_branch)

    def __parse_assignment(self, parse_semicolon=True):
        # Check if the assignment is a increment or decrement operation of kind ++i or --i
        if self.__match(TokenKind.ARITHMETIC_OPERATOR) and self.__current().value in [
            "++",
            "--",
        ]:
            operator = self.__consume(TokenKind.ARITHMETIC_OPERATOR)
            left = self.__parse_factor()
            if parse_semicolon:
                if not (
                    self.__match(TokenKind.SYMBOL) and self.__current().value == ";"
                ):
                    raise TokenError(
                        "Expected ';' at the end of increment/decrement",
                        self.__current(),
                    )
                self.__consume(TokenKind.SYMBOL)
            return IncrementAssignmentNode(left, operator.value)

        # Parse the left-hand side
        left = self.__parse_factor()

        # Determine the type of assignment
        if self.__match(TokenKind.ASSIGNMENT_OPERATOR):
            operator = self.__current().value

            if operator == "=":
                self.__consume(TokenKind.ASSIGNMENT_OPERATOR)
                value = self.__parse_conditional_expression()

                # Expect a semicolon
                if (
                    not (
                        self.__match(TokenKind.SYMBOL) and self.__current().value == ";"
                    )
                    and parse_semicolon
                ):
                    raise TokenError(
                        "Expected ';' at the end of assignment", self.__current()
                    )
                if parse_semicolon:
                    self.__consume(TokenKind.SYMBOL)

                return AssignmentNode(left, value)

            elif operator in ["+=", "-=", "*=", "/=", "%="]:
                self.__consume(TokenKind.ASSIGNMENT_OPERATOR)
                value = self.__parse_conditional_expression()

                # Expect a semicolon
                if (
                    not (
                        self.__match(TokenKind.SYMBOL) and self.__current().value == ";"
                    )
                    and parse_semicolon
                ):
                    raise TokenError(
                        "Expected ';' at the end of compound assignment",
                        self.__current(),
                    )
                if parse_semicolon:
                    self.__consume(TokenKind.SYMBOL)

                return CompoundAssignmentNode(left, operator, value)

        elif self.__match(TokenKind.ARITHMETIC_OPERATOR):
            operator = self.__current().value

            if operator in ["++", "--"]:
                self.__consume(TokenKind.ARITHMETIC_OPERATOR)

                # Expect a semicolon
                if (
                    not (
                        self.__match(TokenKind.SYMBOL) and self.__current().value == ";"
                    )
                    and parse_semicolon
                ):
                    raise TokenError(
                        "Expected ';' at the end of increment/decrement",
                        self.__current(),
                    )
                if parse_semicolon:
                    self.__consume(TokenKind.SYMBOL)

                return IncrementAssignmentNode(left, operator)

        raise TokenError("Invalid assignment statement", self.__current())

    def __parse_expression(self) -> Any:
        """Expression -> Term ( ("+" | "-") Comment? Term )*

        Returns:
            Any: The parsed expression node
        """
        left = self.__parse_term()

        while self.__match(
            TokenKind.ARITHMETIC_OPERATOR
        ) and self.__current().value in ["+", "-"]:
            operator = self.__consume(TokenKind.ARITHMETIC_OPERATOR)

            # Check for a comment after the operator
            comment = None
            if self.__match(TokenKind.COMMENT):
                comment = self.__consume(TokenKind.COMMENT).value

            right = self.__parse_term()
            left = BinaryExpressionNode(left, operator.value, right)

            if comment:
                left.set_comment(comment)

        return left

    def __parse_term(self):
        """Term -> Factor ( ("*" | "/" | "%") Factor )*

        Returns:
            _type_: _description_
        """
        # Parse the left side
        left = self.__parse_factor()

        # Handle multiplication and division (higher precedence than + and -)
        while self.__match(
            TokenKind.ARITHMETIC_OPERATOR
        ) and self.__current().value in ["*", "/", "%"]:
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
                if not (
                    self.__match(TokenKind.SYMBOL) and self.__current().value == "]"
                ):
                    raise TokenError(
                        "Expected closing ']' for list access", self.__current()
                    )
                self.__consume(TokenKind.SYMBOL)
                node = IndexAccessNode(node, index)

            else:
                # No more access chaining, break out of the loop
                break

            # Check if the attribute is followed by a function call
            if self.__match(TokenKind.SYMBOL) and self.__current().value == "(":
                node = self.__parse_function_call(
                    node
                )  # Treat as a function call on the attribute

        return node

    def __parse_primary(self):
        if self.__match(TokenKind.NUMBER) or (
            self.__match(TokenKind.ARITHMETIC_OPERATOR)
            and self.__current().value == "-"
            and self.__peek().kind == TokenKind.NUMBER
        ):
            if (
                self.__match(TokenKind.ARITHMETIC_OPERATOR)
                and self.__current().value == "-"
            ):
                self.__consume(TokenKind.ARITHMETIC_OPERATOR)
                return NumberNode(
                    self.__consume(TokenKind.NUMBER).value, is_negative=True
                )

            value = self.__consume(TokenKind.NUMBER).value
            if (
                self.__current().kind == TokenKind.SYMBOL
                and self.__current().value == "."
            ):
                self.__consume(TokenKind.SYMBOL)
                return NumberNode(value, is_float=True)
            return NumberNode(value)
        elif self.__match(TokenKind.STRING_LITERAL):
            return StringNode(self.__consume(TokenKind.STRING_LITERAL).value)
        elif self.__match(TokenKind.CHAR):
            return CharNode(self.__consume(TokenKind.CHAR).value)
        elif self.__match(TokenKind.KEYWORD) and (
            self.__current().value == "true" or self.__current().value == "false"
        ):
            return BooleanNode(self.__consume(TokenKind.KEYWORD).value)
        elif (
            self.__match(TokenKind.IDENTIFIER)
            and self.__peek().kind == TokenKind.SYMBOL
            and self.__peek().value == "("
        ):
            return self.__parse_function_call()
        elif self.__detect_type(self.__current()) and self.__peek().value == "::":
            return self.__parse_double_colon_access()
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
        elif self.__match(TokenKind.SYMBOL) and self.__current().value == "&":
            # Consume the "&" symbol
            self.__consume(TokenKind.SYMBOL)

            # Expect an identifier immediately following the "&"
            if not self.__match(TokenKind.IDENTIFIER):
                raise SyntaxError("Expected identifier after '&")

            # Parse the identifier as a pointer
            identifier = self.__consume(TokenKind.IDENTIFIER)
            return PointerNode(identifier.value)
        elif (
            self.__match(TokenKind.SYMBOL)
            and self.__current().value == "("
            and self.__detect_type(self.__peek())
        ):
            return self.__parse_type_cast()
        elif self.__match(TokenKind.SYMBOL) and self.__current().value == "(":
            # __Consume the opening parenthesis
            self.__consume(TokenKind.SYMBOL)

            # Parse the inner expression
            expression = self.__parse_conditional_expression()

            # Expect and __consume the closing parenthesis
            if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ")"):
                raise SyntaxError("Expected closing parenthesis")
            self.__consume(TokenKind.SYMBOL)

            return expression
        elif self.__detect_class_initialization():
            return self.__parse_class_initialization()
        else:
            raise SyntaxError(
                "Expected a primary expression. Token: " + str(self.__current())
            )

    def __parse_type(self):
        # If the current token is a type keyword, consume it and return the value
        if self.__match(TokenKind.TYPE_KEYWORD):
            return TypeNode(self.__consume(TokenKind.TYPE_KEYWORD).value)

        # If the current token is a template type keyword, parse the template type
        if self.__match(TokenKind.TEMPLATE_TYPE_KEYWORD):
            return self.__parse_template_type()

        if self.__match(TokenKind.IDENTIFIER):
            return self.__parse_dynamic_type()

        raise SyntaxError(
            "Expected a type keyword or identifier. Token: " + str(self.__current())
        )

    def __parse_dynamic_type(self) -> TypeNode:
        """Parse a dynamically created type (enum, struct, class)

        Raises:
            SyntaxError: If the type is not defined

        Returns:
            TypeNode: The parsed type node
        """
        identifier = self.__consume(TokenKind.IDENTIFIER).value

        dyn_type = None
        if identifier in self.symbol_table["enums"]:
            dyn_type = "enum_type"
        if identifier in self.symbol_table["structs"]:
            dyn_type = "struct_type"
        if identifier in self.symbol_table["classes"]:
            dyn_type = "class_type"

        if dyn_type is None:
            raise SyntaxError(
                f"Type '{identifier}' is not defined. Token: {self.__current()}"
            )

        return TypeNode(identifier, dyn_type)

    def __parse_template_type(self):
        # Consume the template type keyword
        keyword = self.__consume(TokenKind.TEMPLATE_TYPE_KEYWORD)

        # Expect and consume the opening angle bracket
        if not (
            self.__match(TokenKind.COMPARISON_OPERATOR)
            and self.__current().value == "<"
        ):
            raise SyntaxError("Expected '<' after template type keyword")
        self.__consume(TokenKind.COMPARISON_OPERATOR)

        # Expect at least one inner type
        inner_types = []
        inner_types.append(self.__parse_type())
        # Parse additional inner types if present
        while self.__match(TokenKind.SYMBOL) and self.__current().value == ",":
            # Consume the comma
            inner_types.append(self.__parse_type())

        # Expect and consume the closing angle bracket
        if not (
            self.__match(TokenKind.COMPARISON_OPERATOR)
            and self.__current().value == ">"
        ):
            raise SyntaxError("Expected '>' after template type")
        self.__consume(TokenKind.COMPARISON_OPERATOR)

        # Return the template node
        return TemplateTypeNode(keyword, inner_types)

    def __parse_declaration(self, parse_semicolon: bool = True) -> DeclarationNode:
        """
        Declaration -> AccessModifier? Modifier? ("const" (Type | ε) | Type) identifier ("=" ConditionalExpression)?
                    ("," identifier ("=" ConditionalExpression)*)? ";"

        Args:
            parse_semicolon (bool, optional): Whether to parse the semicolon at the end of the declaration. Defaults to True.

        Raises:
            SyntaxError: If the declaration is missing a semicolon at the end.

        Returns:
            DeclarationNode: The parsed declaration node.
        """
        # Parse optional AccessModifier
        access_modifier = None
        if self.__match(TokenKind.ACCESS_MODIFIER):
            access_modifier = self.__consume(TokenKind.ACCESS_MODIFIER).value

        # Parse optional Modifiers (e.g., static, global, etc.)
        modifiers = []
        while self.__match(TokenKind.MODIFIER):
            modifiers.append(self.__consume(TokenKind.MODIFIER).value)

        # Check if the declaration starts with "const"
        is_const = False
        if self.__match(TokenKind.KEYWORD) and self.__current().value == "const":
            is_const = True
            self.__consume(TokenKind.KEYWORD)  # Consume "const"

        # Parse Type if present (Type is optional if "const" is present)
        type_ = None
        if not is_const or (
            (
                self.__match(TokenKind.TEMPLATE_TYPE_KEYWORD)
                or self.__match(TokenKind.TYPE_KEYWORD)
            )
            and not self.__peek().value == "="
        ):
            type_ = self.__parse_type()

        # Parse the first identifier
        identifier = IdentifierNode(self.__consume(TokenKind.IDENTIFIER).value)
        identifiers = []  # Start a list to hold identifiers and their initial values

        # Check if there's an initialization for the first identifier
        initial_value = None
        if self.__match(TokenKind.ASSIGNMENT_OPERATOR):
            # Consume the "="
            self.__consume(TokenKind.ASSIGNMENT_OPERATOR)
            # Parse the initial value
            initial_value = self.__parse_conditional_expression()

        identifiers.append((identifier, initial_value))

        # Parse additional identifiers, each optionally initialized
        while self.__match(TokenKind.SYMBOL) and self.__current().value == ",":
            # Consume the comma
            self.__consume(TokenKind.SYMBOL)

            # Expect and consume the next identifier
            identifier = IdentifierNode(self.__consume(TokenKind.IDENTIFIER).value)

            # Check if there's an initialization for this identifier
            initial_value = None
            if self.__match(TokenKind.ASSIGNMENT_OPERATOR):
                # Consume the "="
                self.__consume(TokenKind.ASSIGNMENT_OPERATOR)
                # Parse the initial value
                initial_value = self.__parse_conditional_expression()

            identifiers.append((identifier, initial_value))

        # Expect and consume the semicolon at the end of the declaration
        if (
            not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";")
            and parse_semicolon
        ):
            raise SyntaxError(
                "Expected ';' at the end of declaration. Token: "
                + str(self.__current())
            )
        if parse_semicolon:
            self.__consume(TokenKind.SYMBOL)

        # Return a DeclarationNode with the access_modifier, modifiers, type, list of identifiers, and const flag
        return DeclarationNode(type_, identifiers, is_const, access_modifier, modifiers)

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
        # Check if there is a 'const' keyword
        is_const = False
        if self.__match(TokenKind.KEYWORD) and self.__current().value == "const":
            is_const = True
            self.__consume(TokenKind.KEYWORD)

        # Parse Type
        type_ = self.__parse_type()

        # Check if the parameter is a pointer
        is_pointer = False
        if self.__match(TokenKind.SYMBOL) and self.__current().value == "&":
            is_pointer = True
            self.__consume(TokenKind.SYMBOL)

        # Expect and consume the parameter name (identifier)
        parameter_name = self.__consume(TokenKind.IDENTIFIER)

        # Check if there is a '=' sign for default parameter value
        default_value = None
        if self.__match(TokenKind.ASSIGNMENT_OPERATOR):
            # Consume the '='
            self.__consume(TokenKind.ASSIGNMENT_OPERATOR)
            # Parse the default value
            default_value = self.__parse_conditional_expression()

        # Return a tuple with the type keyword and parameter name
        return ParameterNode(
            type_, parameter_name.value, default_value, is_pointer, is_const
        )

    def __parse_function_call(self, function_expression=None):
        # If no function expression is provided, assume a standalone function call with an identifier
        if function_expression is None:
            # Expect and consume the function name (identifier)
            function_expression = IdentifierNode(
                self.__consume(TokenKind.IDENTIFIER).value
            )

        # Expect and consume the opening parenthesis
        self.__consume(TokenKind.SYMBOL)

        # Parse arguments (expressions within parentheses)
        arguments = self.__parse_argument_list()

        # Expect and consume the closing parenthesis
        self.__consume(TokenKind.SYMBOL)

        return FunctionCallNode(function_expression, arguments)

    def __parse_argument_list(self):
        """ArgumentList -> Expression Comment? ("," Comment? Expression)*

        Returns:
            List: List of parsed arguments
        """
        # Start with an empty list of arguments
        arguments = []

        # Check for the case where there are no arguments
        if self.__match(TokenKind.SYMBOL) and self.__current().value == ")":
            return arguments

        # Parse the first argument
        argument = self.__parse_expression()

        # Check for a comment after the argument
        comment = None
        if self.__match(TokenKind.COMMENT):
            comment = CommentNode(self.__consume(TokenKind.COMMENT).value)
            argument.set_comment(comment.value)

        arguments.append(argument)

        # Parse additional arguments if present
        while self.__match(TokenKind.SYMBOL) and self.__current().value == ",":
            # Consume the comma
            self.__consume(TokenKind.SYMBOL)

            # Check for a comment after the argument
            comment = None
            if self.__match(TokenKind.COMMENT):
                comment = CommentNode(self.__consume(TokenKind.COMMENT).value)

            # Parse the next argument
            argument = self.__parse_expression()
            if comment:
                argument.set_comment(comment.value)
            arguments.append(argument)

        return arguments

    def __parse_if_statement(self) -> IfStatementNode:
        """IfStatement -> "if" Comment? "(" Comparison ")" (InlineStatement | Block) (ElseIfClause)* (ElseClause)?

        Returns:
            IfStatementNode: The parsed if statement node
        """
        # Consume the "if" keyword
        self.__consume(TokenKind.IF)

        # Check for a comment after the "if" keyword
        comment = None
        if self.__match(TokenKind.COMMENT):
            comment = CommentNode(self.__consume(TokenKind.COMMENT).value)

        # Parse the condition within parentheses
        self.__consume(TokenKind.SYMBOL)
        condition = self.__parse_comparison()
        self.__consume(TokenKind.SYMBOL)

        # Check if there is a block, or a single statement
        if self.__match(TokenKind.SYMBOL) and self.__current().value == "{":
            if_block = self.__parse_block()
            inline_statement = None
        else:
            if_block = None
            inline_statement = self.__parse_statement()

        # Parse any "else if" clauses
        else_if_clauses = []
        while self.__match(TokenKind.ELSE_IF):
            else_if_clauses.append(
                self.__parse_else_if_clause()
            )

        # Parse an optional "else" clause
        else_node = None
        if self.__match(TokenKind.ELSE):
            else_node = self.__parse_else_clause()

        node = IfStatementNode(
            condition, if_block, inline_statement, else_if_clauses, else_node
        )

        if comment:
            node.set_comment(comment.value)

        return node
    
    def __parse_else_clause(self):
        """ElseClause -> "else" Comment? (InlineStatement | Block)

        Returns:
            ElseClauseNode: The parsed else clause node
        """
        self.__consume(TokenKind.ELSE)

        # Check for a comment after the "else" keyword
        comment = None
        if self.__match(TokenKind.COMMENT):
            comment = CommentNode(self.__consume(TokenKind.COMMENT).value)
        
        # Check if there is a block, or a single statement
        if self.__match(TokenKind.SYMBOL) and self.__current().value == "{":
            else_block = self.__parse_block()
            else_inline_statement = None
        else:
            else_block = None
            else_inline_statement = self.__parse_statement()
        
        node = ElseClauseNode(else_block, else_inline_statement)
        if comment:
            node.set_comment(comment.value)
        return node

    def __parse_else_if_clause(self) -> ElseIfClauseNode:
        """"else" "if" Comment? "(" Comparison ")" (InlineStatement | Block)

        Returns:
            ElseIfClauseNode: The parsed else if clause node
        """
        self.__consume(TokenKind.ELSE_IF)

        # Check for a comment after the "else if" keyword
        comment = None
        if self.__match(TokenKind.COMMENT):
            comment = CommentNode(self.__consume(TokenKind.COMMENT).value)

        self.__consume(TokenKind.SYMBOL)
        else_if_condition = self.__parse_comparison()
        self.__consume(TokenKind.SYMBOL)

        # Check if there is a block, or a single statement
        if self.__match(TokenKind.SYMBOL) and self.__current().value == "{":
            else_if_block = self.__parse_block()
            else_if_inline_statement = None
        else:
            else_if_block = None
            else_if_inline_statement = self.__parse_statement()
        else_if_node = ElseIfClauseNode( else_if_condition, else_if_block, else_if_inline_statement)
        if comment:
            else_if_node.set_comment(comment.value)
        return else_if_node
        

    def __parse_block(self):
        statements = []
        self.__consume(TokenKind.SYMBOL)
        while not (self.__match(TokenKind.SYMBOL) and self.__current().value == "}"):
            statements.append(self.__parse_statement())
        self.__consume(TokenKind.SYMBOL)
        return BlockNode(statements)

    def __parse_comparison(self):
        if self.__detect_declaration():
            return self.__parse_declaration(parse_semicolon=False)
        elif self.__detect_assignment():
            return self.__parse_assignment(parse_semicolon=False)
        else:
            return self.__parse_logical_or()

    def __parse_logical_or(self):
        left = self.__parse_logical_and()

        while (
            self.__match(TokenKind.LOGICAL_OPERATOR) and self.__current().value == "||"
        ):
            operator = self.__consume(TokenKind.LOGICAL_OPERATOR)  # Consume '||'
            right = self.__parse_logical_and()
            left = LogicalOrNode(left, right)

        return left

    def __parse_logical_and(self):
        left = self.__parse_negation()

        while (
            self.__match(TokenKind.LOGICAL_OPERATOR) and self.__current().value == "&&"
        ):
            operator = self.__consume(TokenKind.LOGICAL_OPERATOR)  # Consume '&&'
            right = self.__parse_negation()
            left = LogicalAndNode(left, right)

        return left

    def __parse_negation(self):
        if (
            self.__match(TokenKind.LOGICAL_OPERATOR) and self.__current().value == "!"
        ) or (self.__match(TokenKind.SYMBOL) and self.__current().value == "~"):
            operator = self.__current().value  # Capture the operator ('!' or '~')
            self.__consume(
                self.__current().kind
            )  # Consume the operator based on its kind
            expression = self.__parse_negation()  # Parse the negated expression
            return NegationNode(operator, expression)  # Pass the operator to the node

        return self.__parse_bitwise_or()

    def __parse_bitwise_or(self):
        left = self.__parse_bitwise_xor()

        while self.__match(TokenKind.SYMBOL) and self.__current().value == "|":
            operator = self.__consume(TokenKind.SYMBOL)  # Consume '|'
            right = self.__parse_bitwise_xor()
            left = BitwiseOrNode(left, right)

        return left

    def __parse_bitwise_xor(self):
        left = self.__parse_bitwise_and()

        while self.__match(TokenKind.SYMBOL) and self.__current().value == "^":
            operator = self.__consume(TokenKind.SYMBOL)  # Consume '^'
            right = self.__parse_bitwise_and()
            left = BitwiseXorNode(left, right)

        return left

    def __parse_bitwise_and(self):
        left = self.__parse_shift()

        while self.__match(TokenKind.SYMBOL) and self.__current().value == "&":
            operator = self.__consume(TokenKind.SYMBOL)  # Consume '&'
            right = self.__parse_shift()
            left = BitwiseAndNode(left, right)

        return left

    def __parse_shift(self):
        left = self.__parse_relational()

        while self.__match(TokenKind.SYMBOL) and self.__current().value in ("<<", ">>"):
            operator = self.__consume(TokenKind.SYMBOL)  # Consume '<<' or '>>'
            right = self.__parse_relational()
            left = ShiftNode(left, operator, right)

        return left

    def __parse_relational(self):
        left = self.__parse_expression()

        if self.__match(TokenKind.COMPARISON_OPERATOR):
            operator = self.__consume(TokenKind.COMPARISON_OPERATOR).value
            right = self.__parse_expression()
            return RelationalNode(left, operator, right)

        return left

    def __parse_return_statement(self):
        # Consume the "return" keyword
        self.__consume(TokenKind.KEYWORD)

        # Parse the return value expression if present
        expression = None
        if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
            expression = self.__parse_conditional_expression()

        # Expect and consume the semicolon at the end of the return statement
        if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
            raise SyntaxError(
                "Expected ';' at the end of return statement. Token: "
                + str(self.__current())
            )
        self.__consume(TokenKind.SYMBOL)

        return ReturnNode(expression)

    def __parse_break_statement(self):
        # Consume the "break" keyword
        self.__consume(TokenKind.KEYWORD)

        # Expect and consume the semicolon at the end of the break statement
        if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
            raise SyntaxError(
                "Expected ';' at the end of break statement. Token: "
                + str(self.__current())
            )
        self.__consume(TokenKind.SYMBOL)

        return BreakNode()

    def __parse_while_statement(self):
        # Consume the "while" keyword
        self.__consume(TokenKind.KEYWORD)

        # Consume '('
        self.__consume(TokenKind.SYMBOL)

        # Parse the condition
        condition = self.__parse_comparison()

        # Consume ')'
        self.__consume(TokenKind.SYMBOL)

        # Peek to determine if the next token starts a block or a single statement
        if self.__current().kind == TokenKind.SYMBOL and self.__current().value == "{":
            # Parse the block
            block_or_statement = self.__parse_block()
        else:
            # Parse a single statement
            block_or_statement = self.__parse_statement()

        return WhileLoopNode(condition, block_or_statement)

    def __parse_library_import(self):
        # Consume the '#' symbol
        self.__consume(TokenKind.SYMBOL)

        # Consume the 'uses' keyword
        self.__consume(TokenKind.KEYWORD)

        # Consume the library name
        library_name = self.__consume(TokenKind.STRING_LITERAL)

        return LibraryNode(library_name.value)

    def __parse_for_loop(self) -> ForLoopNode:
        """ForLoop -> "for" "(" ForInitialization ";" Comparison ";" Assignment? ")" (Block | Statement)

        Returns:
            ForLoopNode: The ForLoopNode
        """
        # Consume the "for" keyword
        self.__consume(TokenKind.KEYWORD)

        # Consume '('
        self.__consume(TokenKind.SYMBOL)

        # Parse the initialization statement
        initialization = self.__parse_for_loop_initialization()

        # Consume the semicolon
        self.__consume(TokenKind.SYMBOL)

        # Parse the condition
        condition = self.__parse_comparison()

        # Consume the semicolon
        self.__consume(TokenKind.SYMBOL)

        increment = None
        # The increment statement is not necessary
        if not self.__match(TokenKind.SYMBOL):
            # Parse the increment statement
            increment = self.__parse_assignment(parse_semicolon=False)

        # Consume ')'
        self.__consume(TokenKind.SYMBOL)

        block = None
        statement = None
        # Check if the next symbol is '{'
        if self.__match(TokenKind.SYMBOL):
            # Parse the block
            block = self.__parse_block()
        # Otherwise parse the signle statement
        else:
            statement = self.__parse_statement()

        return ForLoopNode(initialization, condition, increment, block, statement)

    def __parse_enum_declaration(self) -> EnumDeclarationNode:
        """EnumDeclaration -> "enum" identifier "{" EnumValue ("," EnumValue)* "}"

        Returns:
            EnumDeclarationNode: The parsed enum declaration node
        """

        # Consume the "enum" keyword
        self.__consume(TokenKind.KEYWORD)

        # Check if the symbol is already in the symbol table
        if (
            self.__match(TokenKind.IDENTIFIER)
            and self.__current().value in self.symbol_table["enums"]
        ):
            raise SyntaxError(
                f"Enum '{self.__current().value}' is already defined. Token: {self.__current()}"
            )

        # Parse the enum name
        enum_name = self.__consume(TokenKind.IDENTIFIER).value

        # Consume '{'
        self.__consume(TokenKind.SYMBOL)

        # Parse the first enum value
        enum_values = []

        # Parse additional enum values if present
        while self.__match(TokenKind.IDENTIFIER):
            # Consume the EnumValue
            enum_values.append(self.__parse_enum_value())

            # Check if there are more enum values to parse
            if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ","):
                break

            # Consume the ','
            self.__consume(TokenKind.SYMBOL)

        # Consume '}'
        self.__consume(TokenKind.SYMBOL)

        # Consume the ';'
        self.__consume(TokenKind.SYMBOL)

        # Add the enum to the symbol table
        self.symbol_table["enums"][enum_name] = enum_values

        return EnumDeclarationNode(enum_name, enum_values)

    def __parse_enum_value(self) -> EnumValueNode:
        """EnumValue -> identifier ("=" number)?

        Returns:
            EnumValueNode: The parsed enum value node
        """
        # Parse the enum value name
        enum_value_name = self.__consume(TokenKind.IDENTIFIER).value

        # Check if there is assignment
        if self.__match(TokenKind.SYMBOL):
            return EnumValueNode(enum_value_name, None)

        # Consume the '='
        self.__consume(TokenKind.ASSIGNMENT_OPERATOR)

        # Parse the enum value
        enum_value = self.__consume(TokenKind.NUMBER).value

        return EnumValueNode(enum_value_name, enum_value)

    def __parse_enum_access(self) -> EnumAccessNode:
        """EnumAccess -> identifier "::" identifier

        Returns:
            EnumAccessNode: The parsed enum access node
        """

        # Parse the enum name
        enum_name = self.__consume(TokenKind.IDENTIFIER).value

        # Consume the '::'
        self.__consume(TokenKind.SYMBOL)

        # Parse the enum value name
        enum_value_name = self.__consume(TokenKind.IDENTIFIER).value

        return EnumAccessNode(enum_name, enum_value_name)

    def __parse_switch_statement(self) -> SwitchStatementNode:
        """SwitchStatement -> "switch" "(" Expression ")" "{" SwitchCase* "}"_summary_

        Returns:
            SwitchStatementNode: The parsed switch statement node
        """
        # Consume the "switch" keyword
        self.__consume(TokenKind.KEYWORD)

        # Consume '('
        self.__consume(TokenKind.SYMBOL)

        # Parse the switch expression
        switch_expression = self.__parse_expression()

        # Consume ')'
        self.__consume(TokenKind.SYMBOL)

        # Consume '{'
        self.__consume(TokenKind.SYMBOL)

        # Parse the switch cases
        cases = []
        while self.__match(TokenKind.KEYWORD) and (
            self.__current().value == "case" or self.__current().value == "default"
        ):
            cases.append(self.__parse_case_statement())

        # Consume '}'
        self.__consume(TokenKind.SYMBOL)

        return SwitchStatementNode(switch_expression, cases)

    def __parse_case_statement(self) -> CaseStatementNode:
        """SwitchCase -> "case" Expression ":" ReturnStatement | "default" ":" ReturnStatement

        Returns:
            CaseStatementNode: The parsed case statement node
        """

        # Check if the case is the default case
        if self.__match(TokenKind.KEYWORD) and self.__current().value == "default":
            # Consume the "default" keyword
            self.__consume(TokenKind.KEYWORD)

            # Consume ':'
            self.__consume(TokenKind.SYMBOL)

            # Parse the return statement
            return_statement = self.__parse_statement()

            return CaseStatementNode(None, return_statement, is_default=True)

        # Consume the "case" keyword
        self.__consume(TokenKind.KEYWORD)

        # Parse the case expression
        case_expression = self.__parse_expression()

        # Consume ':'
        self.__consume(TokenKind.SYMBOL)

        # Parse the return statement
        return_statement = self.__parse_statement()

        return CaseStatementNode(case_expression, return_statement)

    def __parse_struct_declaration(self) -> StructDeclarationNode:
        """StructDeclaration -> "struct" identifier Inheritance? Block ";"

        Returns:
            StructDeclarationNode: The parsed struct declaration node
        """

        # Consume the "struct" keyword
        self.__consume(TokenKind.KEYWORD)

        # Parse the struct name
        struct_name = self.__consume(TokenKind.IDENTIFIER).value

        # Check for inheritance
        inheritance = None
        if self.__match(TokenKind.SYMBOL) and self.__current().value == ":":
            # Consume the ':'
            self.__consume(TokenKind.SYMBOL)
            # Consume the type
            inheritance = InheritanceNode(self.__parse_type())

        # Parse the struct block
        block = self.__parse_block()

        # Add the struct to the symbol table
        self.symbol_table["structs"][struct_name] = block

        # Parse the semicolon
        self.__consume(TokenKind.SYMBOL)

        return StructDeclarationNode(struct_name, block, inheritance)

    def __parse_class_declaration(self) -> ClassDeclarationNode:
        """ClassDeclaration -> "class" identifier Block ";"

        Returns:
            ClassDeclarationNode: The parsed class declaration
        """

        # Consume the "class" keyword
        self.__consume(TokenKind.KEYWORD)

        # Parse the class name
        class_name = self.__consume(TokenKind.IDENTIFIER).value

        # Add the class name to the symbol table before parsing the block, since the block functions may reference the class
        self.symbol_table["classes"][class_name] = {}

        # Check for inheritance
        inheritance = None
        if self.__match(TokenKind.SYMBOL) and self.__current().value == ":":
            # Consume the ':'
            self.__consume(TokenKind.SYMBOL)
            # Consume the type
            inheritance = InheritanceNode(self.__parse_type())

        # Parse the class block
        block = self.__parse_block()

        # Add the class block to the symbol table
        self.symbol_table["classes"][class_name] = block

        # Parse the semicolon
        self.__consume(TokenKind.SYMBOL)

        return ClassDeclarationNode(class_name, block, inheritance)

    def __parse_type_cast(self) -> TypeCastNode:
        """TypeCast -> "(" Type ")" Expression

        Returns:
            TypeCastNode: The parsed type cast node
        """
        # Parse "("
        self.__consume(TokenKind.SYMBOL)

        # Parse the type
        type_ = self.__parse_type()

        # Parse ")"
        self.__consume(TokenKind.SYMBOL)

        # Parse the expression
        expression = self.__parse_expression()

        return TypeCastNode(type_, expression)

    def __parse_for_loop_initialization(self) -> Any:
        """ForInitialization -> Declaration | Assignment | identifier

        Returns:
            Any: The appropriate Node.
        """
        # Check for declaration
        if self.__detect_declaration():
            return self.__parse_declaration(parse_semicolon=False)
        elif self.__detect_assignment():
            return self.__parse_assignment(parse_semicolon=False)
        else:
            return IdentifierNode(self.__consume(TokenKind.IDENTIFIER).value)

    def __parse_class_static_access(self) -> ClassStaticAccessNode:
        """ClassStaticAccess -> identifier "::" (FunctionCall | identifier)

        Returns:
            ClassStaticAccessNode: The parsed class static access node
        """

        # Parse the class name
        class_name = self.__parse_type().value

        # Consume the '::'
        self.__consume(TokenKind.SYMBOL)

        # Check if the next token is a function call
        if self.__detect_function_call():
            # Parse the function call
            function_call = self.__parse_function_call()
            return ClassStaticAccessNode(class_name, function_call)
        # Otherwise, parse the identifier
        else:
            # Parse the identifier
            identifier = self.__consume(TokenKind.IDENTIFIER).value
            return ClassStaticAccessNode(class_name, IdentifierNode(identifier))

    def __parse_double_colon_access(self) -> EnumAccessNode | ClassStaticAccessNode:
        """Parse the double colon access, which can be either an enum access or a class static access

        Returns:
            EnumAccessNode | ClassStaticAccessNode: The parsed enum access or class static access node
        """

        # Check if the identifier is an enum or class
        if self.__current().value in self.symbol_table["enums"]:
            return self.__parse_enum_access()
        elif self.__current().value in self.symbol_table["classes"]:
            return self.__parse_class_static_access()
        elif self.__detect_type(self.__current()):
            # If the type is imported from a library parse it as static access for now. In the future check the imports.
            return self.__parse_class_static_access()
        else:
            raise SyntaxError(
                f"Type '{self.__current().value}' is not defined. Token: {self.__current()}"
            )

    def __parse_class_initialization(self) -> ClassInitializationNode:
        """ClassInitialization -> Type "(" ArgumentList? ")"

        Returns:
            ClassInitializationNode: The parsed class initialization node
        """

        # Parse the class type
        class_type = self.__parse_type()

        # Consume '('
        self.__consume(TokenKind.SYMBOL)

        # Parse the argument list
        arguments = self.__parse_argument_list()

        # Consume ')'
        self.__consume(TokenKind.SYMBOL)

        return ClassInitializationNode(class_type, arguments)

    def __parse_continue_statement(self) -> ContinueNode:
        """ContinueStatement   -> "continue" ";"

        Returns:
            ContinueNode: The parsed continue node
        """
        # Consume the "continue" keyword
        self.__consume(TokenKind.KEYWORD)

        # Expect and consume the semicolon at the end of the continue statement
        if not (self.__match(TokenKind.SYMBOL) and self.__current().value == ";"):
            raise SyntaxError(
                "Expected ';' at the end of continue statement. Token: "
                + str(self.__current())
            )
        self.__consume(TokenKind.SYMBOL)

        return ContinueNode()

    def __parse_try_catch(self) -> TryCatchNode:
        """TryCatchStatement -> "try" Block "catch" Block ("finally" Block)?

        Returns:
            TryCatchNode: The parsed try-catch node
        """

        # Consume the "try" keyword
        self.__consume(TokenKind.KEYWORD)

        # Parse the try block
        try_block = self.__parse_block()

        # Consume the "catch" keyword
        self.__consume(TokenKind.KEYWORD)

        # Parse the catch block
        catch_block = self.__parse_block()

        # Parse the optional "finally" block
        finally_block = None
        if self.__match(TokenKind.KEYWORD) and self.__current().value == "finally":
            self.__consume(TokenKind.KEYWORD)
            finally_block = self.__parse_block()

        return TryCatchNode(try_block, catch_block, finally_block)
    
    def __parse_do_while_loop(self) -> DoWhileLoopNode:
        """DoWhileLoop -> "do" Block "while" "(" Comparison ")" ";"

        Returns:
            DoWhileLoopNode: The parsed do-while loop node
        """
        # Consume the "do" keyword
        self.__consume(TokenKind.KEYWORD)

        # Parse the block
        block = self.__parse_block()

        # Consume the "while" keyword
        self.__consume(TokenKind.KEYWORD)

        # Consume '('
        self.__consume(TokenKind.SYMBOL)

        # Parse the condition
        condition = self.__parse_comparison()

        # Consume ')'
        self.__consume(TokenKind.SYMBOL)

        # Consume ';'
        self.__consume(TokenKind.SYMBOL)

        return DoWhileLoopNode(condition, block)