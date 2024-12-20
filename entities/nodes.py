from typing import List, Tuple
from entities.token_ import Token


def indent_str(indent_level):
    return "  " * indent_level  # 2 spaces per level


class DefaultNode:
    def __init__(self):
        self.comment = None

    def set_comment(self, comment):
        self.comment = comment

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}DefaultNode(comment={self.value})"

    def format(self, indent=0):

        return f"{indent_str(indent)}# {self.comment}" if self.comment else ""


class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}ProgramNode(\n"
        for statement in self.statements:
            string += statement.__repr__(indent + 1) + "\n"
        string += f"{indent_str(indent)})"
        return string

    def format(self, indent=0):

        formatted_code = ""
        previous_was_newline = False
        for statement in self.statements:
            if isinstance(statement, NewLineNode):
                if not previous_was_newline:
                    formatted_code += statement.format(indent) + "\n"
                previous_was_newline = True
            else:
                formatted_code += statement.format(indent) + "\n"
                previous_was_newline = False
        return formatted_code.strip()


class AssignmentNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}AssignmentNode({self.identifier}, {self.value.__repr__(indent + 1)})"

    def format(self, indent=0):

        return (
            f"{indent_str(indent)}{self.identifier.format()} = {self.value.format()};"
        )


class DeclarationNode:
    def __init__(
        self,
        type_,
        identifiers,
        is_const=False,
        access_modifier=None,
        modifier=None,
        comment=None,
    ):
        """
        :param type_keyword: The data type of the declaration (e.g., 'int' or 'string')
        :param identifiers: A list of tuples where each tuple contains:
                            - the identifier name (string)
                            - an optional initial value (AST node or None if no initialization)
        """
        self.type: TypeNode = type_
        self.identifiers = identifiers  # List of tuples (identifier, value, comment), where comment is a tuple (comment1, comment2)
        self.is_const = is_const
        self.access_modifier = access_modifier
        self.modifier: List = modifier

    def __repr__(self, indent=0):
        # Start the string with the type keyword
        string = f"{indent_str(indent)}DeclarationNode(const={self.is_const}, access_modifier={self.access_modifier}, modifier={self.modifier}, type={self.type.__repr__(indent+1)}, identifiers=[\n"

        # Add each identifier with its optional initial value
        for identifier, value, comment in self.identifiers:
            if value is None:
                string += f"{indent_str(indent)}{identifier}\n"
            else:
                string += (
                    f"{indent_str(indent)}{identifier} = {value.__repr__(indent + 2)}\n"
                )

        string += f"{indent_str(indent)}])"
        return string

    def format(self, indent=0, inline=False):
        # Start the string with the type keyword
        string = f"{indent_str(indent)}{'const ' if self.is_const else ''}{self.access_modifier + ' ' if self.access_modifier else ''}{self.modifier[0] + ' ' if self.modifier else ''}{self.type.format()} "

        # Add each identifier with its optional initial value
        for i, (identifier, value, comment) in enumerate(self.identifiers):
            string += f"{identifier.format()}"
            if value is not None:
                string += " = "
            if comment[0] is not None:
                string += f"{comment[0].format()} "
            if value is not None:
                string += f"{value.format()}"
            if comment[1] is not None:
                string += f" {comment[1].format()}"
            if i < len(self.identifiers) - 1:
                string += ", "

        if not inline:
            string += ";"

        return string


class BinaryExpressionNode(DefaultNode):
    def __init__(self, left, operator, right):
        super().__init__()
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}BinaryExpressionNode(\n"
        string += f"{indent_str(indent + 1)}left: {self.left.__repr__(indent + 2)}\n"
        string += f"{indent_str(indent + 1)}operator: {self.operator}\n"
        string += f"{indent_str(indent + 1)}comment: {self.comment}\n"
        string += f"{indent_str(indent + 1)}right: {self.right.__repr__(indent + 2)}\n"
        string += f"{indent_str(indent)})"
        return string

    def format(self, indent=0):

        return f"{indent_str(indent)}{self.left.format()} {self.operator} {self.right.format()}"


class IdentifierNode(DefaultNode):
    def __init__(self, value, type_cast=None):
        super().__init__()
        if isinstance(value, Token):
            raise TypeError("Value must not be a Token")
        self.value = value
        self.type_cast = type_cast

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}IdentifierNode(value={self.value}, type_cast={self.type_cast}, comment={self.comment})"

    def format(self, indent=0):

        result = f"{indent_str(indent)}"
        if self.type_cast:
            result += f"({self.type_cast.format()})"
        result += f"{self.value}"
        return result


class GlobalIdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}GlobalIdentifierNode({self.value})"

    def format(self, indent=0):

        return f"${self.value}"


class PointerNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}PointerNode({self.value})"

    def format(self, indent=0):

        return f"&{self.value}"


class NumberNode:
    def __init__(self, value, is_float=False, is_negative=False):
        self.value = value
        self.is_float = is_float
        self.is_negative = is_negative

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}NumberNode(is_float={self.is_float}, is_negative={self.is_negative}, value={self.value})"

    def format(self, indent=0):

        return f"{self.value}"


class BooleanNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}BooleanNode({self.value})"

    def format(self, indent=0):

        return "true" if self.value else "false"


class StringNode(DefaultNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}StringNode({self.value}, comment={self.comment})"

    def format(self, indent=0):

        return f"{self.value}"


class CommentNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CommentNode({self.value})"

    def format(self, indent=0):

        return f"{indent_str(indent)}// {self.value}"


class MultilineCommentNode:
    def __init__(self, lines):
        self.lines = lines

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}MultilineCommentNode([\n"
        for line in self.lines:
            string += f"{indent_str(indent + 1)}{line}\n"
        string += f"{indent_str(indent)}])"
        return string

    def format(self, indent=0):

        result = f"{indent_str(indent)}/*\n"
        for line in self.lines:
            result += f"{indent_str(indent + 1)}{line}\n"
        result += f"{indent_str(indent)}*/"
        return result


class DividerNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}DividerNode({self.value})"

    def format(self, indent=0):

        return f"{self.value}"


class AttributeAccessNode:
    def __init__(self, identifier, attribute):
        self.identifier = identifier
        self.attribute = attribute

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}AttributeAccessNode({self.identifier}, {self.attribute})"

    def format(self, indent=0):

        return f"{self.identifier.format()}.{self.attribute.format()}"


class IndexAccessNode:
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}IndexAccessNode({self.identifier}, {self.index})"

    def format(self, indent=0):

        return f"{self.identifier.format()}[{self.index.format()}]"


class FunctionDeclarationNode:
    def __init__(
        self,
        return_type,
        identifier,
        parameters,
        block,
        access_modifier=None,
        is_constructor=False,
        modifier=None,
        is_main=False,
    ):
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.block = block
        self.access_modifier = access_modifier
        self.is_constructor = is_constructor
        self.modifier = modifier
        self.is_main = is_main

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}FunctionDeclarationNode(\n"
        string += (
            f"{indent_str(indent + 1)}return_type: {self.return_type.__repr__()}\n"
        )
        string += f"{indent_str(indent + 1)}is_main: {self.is_main}\n"
        string += f"{indent_str(indent + 1)}access_modifier: {self.access_modifier}\n"
        string += f"{indent_str(indent + 1)}modifier: {self.modifier}\n"
        string += f"{indent_str(indent + 1)}is_constructor: {self.is_constructor}\n"
        string += f"{indent_str(indent + 1)}identifier: {self.identifier}\n"
        string += f"{indent_str(indent + 1)}parameters: {self.parameters}\n"
        string += f"{indent_str(indent + 1)}block: {self.block}\n"
        string += f"{indent_str(indent + 1)}]\n"
        string += f"{indent_str(indent)})"
        return string

    def format(self, indent=0):

        string = f"{indent_str(indent)}"
        if self.access_modifier is not None:
            string += f"{self.access_modifier} "
        if self.modifier is not None:
            string += f"{self.modifier} "
        if self.return_type is not None:
            string += f"{self.return_type.format()} "
        string += f"{self.identifier}("
        for i, parameter in enumerate(self.parameters):
            string += f"{parameter.type_.format()} {parameter.identifier}"
            if parameter.default_value is not None:
                string += f" = {parameter.default_value.format()}"
            if i < len(self.parameters) - 1:
                string += ", "
        string += ") {\n"
        string += self.block.format(indent + 1, with_brackets=False)
        string += f"\n{indent_str(indent)}" + "}"
        return string


class FunctionCallNode:
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}FunctionCallNode(\n"
        string += f"{indent_str(indent + 1)}identifier: {self.identifier}\n"
        string += f"{indent_str(indent + 1)}arguments: [\n"
        for argument in self.arguments:
            string += argument.__repr__(indent + 2) + "\n"
        string += f"{indent_str(indent + 1)}]\n"
        string += f"{indent_str(indent)})"
        return string

    def format(self, indent=0):

        string = f"{indent_str(indent)}{self.identifier.format()}("
        for i, argument in enumerate(self.arguments):
            string += f"{argument.format()}"
            if i < len(self.arguments) - 1:
                string += ", "
        string += ")"
        return string


class IfStatementNode(DefaultNode):
    def __init__(
        self,
        condition,
        if_block=None,
        inline_statement=None,
        else_if_clauses=None,
        else_node=None,
    ):
        super().__init__()
        self.condition = condition
        self.if_block = if_block
        self.inline_statement = inline_statement
        self.else_if_clauses = else_if_clauses if else_if_clauses is not None else []
        self.else_node = else_node

    def __repr__(self, indent=0):
        result = f"{indent_str(indent)}IfStatementNode(\n"
        result += f"{indent_str(indent + 1)}condition={self.condition},\n"
        result += f"{indent_str(indent + 1)}comment,\n"
        result += f"{indent_str(indent + 1)}if_block={self.if_block},\n"
        result += f"{indent_str(indent + 1)}inline_statement={self.inline_statement},\n"
        result += f"{indent_str(indent + 1)}else_if_clauses=[\n"
        for clause in self.else_if_clauses:
            result += clause.__repr__(indent + 2) + "\n"
        result += f"{indent_str(indent + 1)}],\n"
        result += f"{indent_str(indent + 1)}else_block={self.else_node}\n"
        result += f"{indent_str(indent)})"
        return result

    def format(self, indent=0):
        result = f"{indent_str(indent)}if ({self.condition.format()})"
        if self.if_block is not None:
            result += " {\n"
            result += self.if_block.format(indent + 1)
            result += f"\n{indent_str(indent)}" + "}"
        elif self.inline_statement is not None:
            # If the if statement has else or else if's, parse it as block
            if len(self.else_if_clauses) > 0 or self.else_node is not None:
                result += " {\n"
                result += f"{self.inline_statement.format(indent + 1)}"
                if isinstance(self.inline_statement, FunctionCallNode):
                    result += ";"
                result += "\n" + f"{indent_str(indent)}" + "}"
            else:
                result += f"\n{self.inline_statement.format(indent + 1)}"
                if isinstance(self.inline_statement, FunctionCallNode):
                    result += ";"
        for else_if_clause in self.else_if_clauses:
            result += f"{else_if_clause.format(indent)}"
        if self.else_node:
            result += f"{self.else_node.format(indent)}"
        return result


class ElseIfClauseNode(DefaultNode):
    def __init__(self, condition, block=None, inline_statement=None):
        super().__init__()
        self.condition = condition
        self.block = block
        self.inline_statement = inline_statement

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ElseIfClauseNode(condition={self.condition}, comment={self.comment} block={self.block}, inline_statement={self.inline_statement})"

    def format(self, indent=0):

        result = f" else if ({self.condition.format()})"
        if self.block is not None:
            result += " {\n"
            result += self.block.format(indent + 1)
            result += f"\n{indent_str(indent)}" + "}"
        elif self.inline_statement is not None:
            result += f"\n{self.inline_statement.format(indent + 1)}\n"
        return result


class ElseClauseNode(DefaultNode):
    def __init__(self, block, inline_statement=None):
        super().__init__()
        self.block = block
        self.inline_statement = inline_statement

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ElseClauseNode(comment={self.comment}, block={self.block}, inline_statement={self.inline_statement})"

    def format(self, indent=0):

        result = f" else"
        if self.block is not None:
            result += " {\n"
            result += self.block.format(indent + 1)
            result += f"\n{indent_str(indent)}" + "}"
        elif self.inline_statement is not None:
            result += f"\n{self.inline_statement.format(indent + 1)}"
        return result


class BlockNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self, indent=0):
        result = f"{indent_str(indent)}BlockNode([\n"
        for statement in self.statements:
            result += statement.__repr__(indent + 1) + "\n"
        result += f"{indent_str(indent)}])"
        return result

    def format(self, indent=0, with_brackets=False):
        if with_brackets:
            result = f"{indent_str(indent)}" + "{\n"
        else:
            result = ""
        previous_was_newline = False
        for i in range(len(self.statements)):
            if isinstance(self.statements[i], NewLineNode):
                if not previous_was_newline:
                    result += self.statements[i].format(indent)
                else:
                    continue
                previous_was_newline = True
            else:
                result += self.statements[i].format(indent)
                previous_was_newline = False
            if result[-1] != ";" and result[-1] != "\n" and result[-1] != "}":
                result += ";"
            if i < len(self.statements) - 1:
                result += "\n"
        if with_brackets:
            result += f"{indent_str(indent)}" + "}"
        return result


class ReturnNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ReturnNode({self.expression})"

    def format(self, indent=0):

        if self.expression is None:
            return f"{indent_str(indent)}return;"
        return f"{indent_str(indent)}return {self.expression.format()};"


class BreakNode:
    def __repr__(self, indent=0):
        return f"{indent_str(indent)}BreakNode()"

    def format(self, indent=0):

        return f"{indent_str(indent)}break;"


class WhileLoopNode:
    def __init__(self, condition, block_or_statement):
        self.condition = condition
        self.block_or_statement = block_or_statement

    def __repr__(self, indent=0):
        block_type = (
            "Block" if isinstance(self.block_or_statement, list) else "Statement"
        )
        return (
            f"{indent_str(indent)}WhileLoopNode("
            f"condition={self.condition}, "
            f"{block_type}={self.block_or_statement})"
        )

    def format(self, indent=0):

        result = f"{indent_str(indent)}while ({self.condition.format()})"
        if isinstance(self.block_or_statement, BlockNode):
            result += " {\n"
            result += self.block_or_statement.format(indent + 1)
            result += f"\n{indent_str(indent)}" + "}"
        else:
            result += f"\n{self.block_or_statement.format(indent + 1)}"
        return result


class TypeNode:
    def __init__(self, value, dyn_type=None):
        self.value = value
        self.dyn_type = dyn_type

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}TypeNode({self.value}"
        if self.dyn_type is not None:
            string += f", dyn_type={self.dyn_type}"
        string += ")"
        return string

    def format(self, indent=0):

        return f"{self.value}"


class TemplateTypeNode:
    def __init__(self, template_type_keyword, types):
        self.template_type_keyword = template_type_keyword
        self.types = types

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}TemplateTypeNode(keyword={self.template_type_keyword}, types=[\n"
        for type_ in self.types:
            string += f"{indent_str(indent + 1)}{type_.__repr__(indent)}\n"
        string += f"{indent_str(indent)}])"
        return string

    def format(self, indent=0):

        return f"{self.template_type_keyword}<{', '.join([type_.format() for type_ in self.types])}>"


class ParameterNode:
    def __init__(
        self, type_, identifier, default_value=None, is_pointer=False, is_const=False
    ):
        self.type_ = type_
        self.identifier = identifier
        self.default_value = default_value
        self.is_pointer = is_pointer
        self.is_const = is_const

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ParameterNode(type={self.type_}, identifier={self.identifier}, default_value={self.default_value}, is_pointer={self.is_pointer}, is_const={self.is_const})"

    def format(self, indent=0):

        return f"{self.type_.format()} {'*' if self.is_pointer else ''}{'const ' if self.is_const else ''}{self.identifier}"


class LibraryNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}LibraryNode({self.name})"

    def format(self, indent=0):

        return f"#uses {self.name}"


class CharNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CharNode({self.value})"

    def format(self, indent=0):

        return f"'{self.value}'"


class TernaryExpressionNode:
    def __init__(self, comparison, success_expression, failure_expression):
        self.comparison = comparison
        self.success_expression = success_expression
        self.failure_expression = failure_expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}TernaryExpression({self.comparison}, {self.success_expression}, {self.failure_expression})"

    def format(self, indent=0):

        return f"{indent_str(indent)}{self.comparison.format()} ? {self.success_expression.format()} : {self.failure_expression.format()}"


class ForLoopNode:
    def __init__(self, initialization, condition, increment, block, statement):
        self.initialization = initialization
        self.condition = condition
        self.increment = increment
        self.block: BlockNode = block
        self.statement = statement

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ForLoopNode(initialization={self.initialization}, condition={self.condition}, increment={self.increment}, block={self.block}), statement={self.statement}"

    def format(self, indent=0):
        result = f"{indent_str(indent)}for ("
        result += f"{self.initialization.format(inline=True) if isinstance(self.initialization, DeclarationNode) else self.initialization.format()};"
        result += f" {self.condition.format()};"
        if self.increment is not None:
            result += f" {self.increment.format(semicolon=False)}"
        result += ")"
        if self.block is not None:
            result += " {\n"
            result += self.block.format(indent + 1)
            result += f"\n{indent_str(indent)}" + "}"
        elif self.statement is not None:
            result += f"\n{self.statement.format(indent + 1)}"
        return result


class IncrementAssignmentNode:
    def __init__(self, identifier, operator):
        self.identifier = identifier
        self.operator = operator

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}IncrementAssignmentNode(identifier={self.identifier}, operator={self.operator})"

    def format(self, indent=0, semicolon=True):

        return f"{indent_str(indent)}{self.identifier.format()}{self.operator}" + (";" if semicolon else "")


class CompoundAssignmentNode:
    def __init__(self, identifier, operator, value):
        self.identifier = identifier
        self.operator = operator
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CompundAssignmentNode(identifier={self.identifier}, operator={self.operator}, value={self.value})"

    def format(self, indent=0, semicolon=True):
        return f"{indent_str(indent)}{self.identifier.format()} {self.operator} {self.value.format()}" + (";" if semicolon else "")


class LogicalOrNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}LogicalOrNode(left={self.left}, right={self.right})"
        )

    def format(self, indent=0):
        result = f"{self.left.format()}"
        if self.right is not None:
            result += f" || {self.right.format()}"
        return result


class LogicalAndNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}LogicalAndNode(left={self.left}, right={self.right})"
        )

    def format(self, indent=0):
        result = f"{self.left.format()}"
        if self.right is not None:
            result += f" && {self.right.format()}"
        return result


class NegationNode:
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}NegationNode(operator={self.operator}, expression={self.expression})"

    def format(self, indent=0):
        return f"{self.operator}{self.expression.format()}"

class RelationalNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}RelationalNode(left={self.left}, operator='{self.operator}', right={self.right})"

    def format(self, indent=0):
        return f"{indent_str(indent)}{self.left.format()} {self.operator} {self.right.format()}"

class EnumDeclarationNode:
    def __init__(self, identifier, values):
        self.identifier = identifier
        self.values = values

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}EnumDeclarationNode(identifier={self.identifier}, values=[\n"
        for value in self.values:
            string += value.__repr__(indent + 1) + "\n"
        string += f"{indent_str(indent)}])"
        return string

    def format(self, indent=0):
        result = f"{indent_str(indent)}enum {self.identifier} {{\n"
        for i, value in enumerate(self.values):
            result += f"{value.format(indent + 1)}"
            if i < len(self.values) - 1:
                result += ",\n"
        result += f"\n{indent_str(indent)}" + "};"
        return result


class EnumValueNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}EnumValueNode(identifier={self.identifier}, value={self.value})"

    def format(self, indent=0):
        return (
            f"{indent_str(indent)}{self.identifier} = {self.value}"
            if self.value is not None
            else f"{self.identifier}"
        )

class EnumAccessNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}EnumAccessNode(identifier={self.identifier}, value={self.value})"

    def format(self, indent=0):
        return f"{self.identifier}::{self.value}"


class CaseStatementNode:
    def __init__(self, value, block, is_default=False):
        self.value = value
        self.block: BlockNode = block
        self.is_default: bool = is_default

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CaseStatementNode(is_default={self.is_default}, value={self.value}, block={self.block})"

    def format(self, indent=0):
        if self.is_default:
            return f"{indent_str(indent)}default:\n{self.block.format(indent + 1)}"
        return f"{indent_str(indent)}case {self.value.format()}:\n{self.block.format(indent + 1)}"


class SwitchStatementNode:
    def __init__(self, expression, statements):
        self.expression = expression
        self.statements = statements

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}SwitchStatementNode(\n"
        string += f"{indent_str(indent + 1)}expression: {self.expression}\n"
        string += f"{indent_str(indent + 1)}statements: [\n"
        for case_statement in self.statements:
            string += case_statement.__repr__(indent + 2) + "\n"
        string += f"{indent_str(indent + 1)}]\n"
        string += f"{indent_str(indent)})"
        return string

    def format(self, indent=0):

        result = f"{indent_str(indent)}switch({self.expression.format()}) {{\n"
        for case_statement in self.statements:
            result += case_statement.format(indent + 1) + "\n"
        result += f"{indent_str(indent)}" + "}"
        return result


class BitwiseOrNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}BitwiseOrNode(left={self.left}, right={self.right})"
        )

    def format(self, indent=0):

        result = f"{self.left.format()}"
        if self.right is not None:
            result += f" | {self.right.format()}"
        return result


class BitwiseXorNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}BitwiseXorNode(left={self.left}, right={self.right})"
        )

    def format(self, indent=0):

        result = f"{self.left.format()}"
        if self.right is not None:
            result += f" ^ {self.right.format()}"
        return result


class BitwiseAndNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}BitwiseAndNode(left={self.left}, right={self.right})"
        )

    def format(self, indent=0):

        result = f"{self.left.format()}"
        if self.right is not None:
            result += f" & {self.right.format()}"
        return result


class ShiftNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ShiftNode(left={self.left}, operator={self.operator}, right={self.right})"

    def format(self, indent=0):

        result = f"{self.left.format()}"
        if self.right is not None:
            result += f" {self.operator} {self.right.format()}"


class StructDeclarationNode:
    def __init__(self, identifier, block, inheritance=None):
        self.identifier = identifier
        self.block = block
        self.inheritance = None

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}StructDeclarationNode(inheritance={self.inheritance}, identifier={self.identifier},\n"
        string += self.block.__repr__(indent + 1) + "\n"
        return string

    def format(self, indent=0):

        result = f"{indent_str(indent)}struct {self.identifier} {{\n"
        result += self.block.format(indent + 1) + "\n"
        result += f"{indent_str(indent)}" + "};"
        return result


class ClassDeclarationNode:
    def __init__(self, identifier, block, inheritance=None):
        self.identifier = identifier
        self.block = block
        self.inheritance = inheritance

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}ClassDeclarationNode(inheritance={self.inheritance}, identifier={self.identifier},\n"
        string += self.block.__repr__(indent + 1)
        string += f"{indent_str(indent)}])"
        return string

    def format(self, indent=0):

        result = f"{indent_str(indent)}class {self.identifier}"
        if self.inheritance is not None:
            result += f" : {self.inheritance.format()}"
        result += " {\n"
        result += self.block.format(indent + 1) + "\n"
        result += f"{indent_str(indent)}" + "};"
        return result


class InheritanceNode:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}InheritanceNode(identifier={self.identifier})"

    def format(self, indent=0):

        return f"{self.identifier}"


class TypeCastNode:
    def __init__(self, type_, expression):
        self.type_ = type_
        self.expression = expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}TypeCastNode(type={self.type_}, expression={self.expression})"

    def format(self, indent=0):

        return f"{indent_str(indent)}({self.type_.format()}){self.expression.format()}"


class ClassStaticAccessNode:
    def __init__(self, identifier, attribute):
        self.identifier = identifier
        self.attribute = attribute

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ClassStaticAccessNode(identifier={self.identifier}, attribute={self.attribute})"

    def format(self, indent=0):

        return f"{self.identifier}::{self.attribute}"


class ClassInitializationNode:
    def __init__(self, identifier, arguments, new=False):
        self.identifier = identifier
        self.arguments = arguments
        self.new = new

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ClassInitializationNode(identifier={self.identifier}, arguments={self.arguments}, new={self.new})"

    def format(self, indent=0):

        result = f"{self.identifier}"
        if self.new:
            result += f"new "
        result += "("
        for i, argument in enumerate(self.arguments):
            result += f"{argument.format()}"
            if i < len(self.arguments) - 1:
                result += ", "
        result += ")"
        return result


class ContinueNode:
    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ContinueNode()"

    def format(self, indent=0):

        return f"{indent_str(indent)}continue;"


class TryCatchNode:
    def __init__(self, try_block, catch_block, finally_block=None):
        self.try_block = try_block
        self.catch_block = catch_block
        self.finally_block = finally_block

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}TryCatchNode(try_block={self.try_block}, catch_block={self.catch_block}, finally_block={self.finally_block})"

    def format(self, indent=0):

        result = f"{indent_str(indent)}try " + "{\n"
        result += self.try_block.format(indent + 1) + "\n"
        result += f"{indent_str(indent)}" + "}"
        if self.catch_block is not None:
            result += f" catch " + "{\n"
            result += self.catch_block.format(indent + 1) + "\n"
            result += f"{indent_str(indent)}" + "}"
        if self.finally_block is not None:
            result += f" finally " + "{\n"
            result += self.finally_block.format(indent + 1) + "\n"
            result += f"{indent_str(indent)}" + "}"
        return result


class DoWhileLoopNode:
    def __init__(self, block, condition):
        self.block = block
        self.condition = condition

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}DoWhileLoopNode(block={self.block}, condition={self.condition})"

    def format(self, indent=0):

        result = f"{indent_str(indent)}do " + "{\n"
        result += self.block.format(indent + 1) + "\n"
        result += f"{indent_str(indent)}"
        result += "} "
        result += f"while ({self.condition.format()};"
        return result


class NewLineNode:
    def __repr__(self, indent=0):
        return f"{indent_str(indent)}NewLineNode()"

    def format(self, indent=0):

        return ""


class PropertySetterNode:
    def __init__(self, type, identifier):
        self.type = type
        self.identifier = identifier

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}PropertySetterNode(type={self.type}, identifier={self.identifier})"

    def format(self, indent=0):

        return f"#property {self.type.format()} {self.identifier}"


class EventNode:
    def __init__(self, identifier, parameters):
        self.identifier: IdentifierNode = identifier
        self.parameters: List[ParameterNode] = parameters

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}EventNode(parameters={self.parameters})"

    def format(self, indent=0):

        return f"#event {self.identifier.format()}({', '.join([param.format() for param in self.parameters])})"


class FactorNode:
    def __init__(self, primary, left_comment=None, right_comment=None):
        self.primary = primary
        self.left_comment = left_comment
        self.right_comment = right_comment

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}FactorNode(primary={self.primary}, left_comment={self.left_comment}, right_comment={self.right_comment})"

    def format(self, indent=0):

        result = f"{indent_str(indent)}"
        if self.left_comment is not None:
            result += f"{self.left_comment.format()} "
        result += f"{self.primary.format()}"
        if self.right_comment is not None:
            result += f" {self.right_comment.format()}"
        return result
