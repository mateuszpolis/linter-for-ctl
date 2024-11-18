def indent_str(indent_level):
    return "  " * indent_level  # 2 spaces per level


class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}ProgramNode(\n"
        for statement in self.statements:
            string += statement.__repr__(indent + 1) + "\n"
        string += f"{indent_str(indent)})"
        return string


class StatementNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}StatementNode({self.identifier}, {self.value.__repr__(indent + 1)})"


class AssignmentNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}AssignmentNode({self.identifier}, {self.value.__repr__(indent + 1)})"


class DeclarationNode:
    def __init__(self, type_, identifiers):
        """
        :param type_keyword: The data type of the declaration (e.g., 'int' or 'string')
        :param identifiers: A list of tuples where each tuple contains:
                            - the identifier name (string)
                            - an optional initial value (AST node or None if no initialization)
        """
        self.type = type_
        self.identifiers = identifiers

    def __repr__(self, indent=0):
        # Start the string with the type keyword
        string = f"{indent_str(indent)}DeclarationNode(type={self.type.__repr__(indent+1)}, identifiers=[\n"

        # Add each identifier with its optional initial value
        for identifier, value in self.identifiers:
            if value is None:
                string += f"{indent_str(indent + 1)}{identifier}\n"
            else:
                string += f"{indent_str(indent + 1)}{identifier} = {value.__repr__(indent + 2)}\n"

        string += f"{indent_str(indent)}])"
        return string


class BinaryExpressionNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}BinaryExpressionNode(\n"
        string += f"{indent_str(indent + 1)}left: {self.left.__repr__(indent + 2)}\n"
        string += f"{indent_str(indent + 1)}operator: {self.operator}\n"
        string += f"{indent_str(indent + 1)}right: {self.right.__repr__(indent + 2)}\n"
        string += f"{indent_str(indent)})"
        return string


class IdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}IdentifierNode({self.value})"


class GlobalIdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}GlobalIdentifierNode({self.value})"


class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}NumberNode({self.value})"


class StringNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}StringNode({self.value})"


class OperatorNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}OperatorNode({self.value})"


class KeywordNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}KeywordNode({self.value})"


class SymbolNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}SymbolNode({self.value})"


class CommentNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CommentNode({self.value})"


class MultilineCommentNode:
    def __init__(self, lines):
        self.lines = lines

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}MultilineCommentNode([\n"
        for line in self.lines:
            string += f"{indent_str(indent + 1)}{line}\n"
        string += f"{indent_str(indent)}])"
        return string


class DividerNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}DividerNode({self.value})"


class WhitespaceNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}WhitespaceNode({self.value})"


class AttributeAccessNode:
    def __init__(self, identifier, attribute):
        self.identifier = identifier
        self.attribute = attribute

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}AttributeAccessNode({self.identifier}, {self.attribute})"


class IndexAccessNode:
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}IndexAccessNode({self.identifier}, {self.index})"


class FunctionDeclarationNode:
    def __init__(self, return_type, identifier, parameters, block):
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.block = block

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}FunctionDeclarationNode(\n"
        string += (
            f"{indent_str(indent + 1)}return_type: {self.return_type.__repr__()}\n"
        )
        string += f"{indent_str(indent + 1)}identifier: {self.identifier}\n"
        string += f"{indent_str(indent + 1)}parameters: {self.parameters}\n"
        string += f"{indent_str(indent + 1)}block: {self.block}\n"
        string += f"{indent_str(indent + 1)}]\n"
        string += f"{indent_str(indent)})"
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


class MainNode:
    def __init__(self, parameters, block):
        self.parameters = parameters
        self.block = block

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}MainNode(\n"
        string += f"{indent_str(indent + 1)}parameters: {self.parameters}\n"
        string += f"{indent_str(indent + 1)}block: {self.block}\n"
        string += f"{indent_str(indent)})"
        return string


class IfStatementNode:
    def __init__(self, condition, if_block, else_if_clauses=None, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_if_clauses = else_if_clauses if else_if_clauses is not None else []
        self.else_block = else_block

    def __repr__(self, indent=0):
        result = f"{indent_str(indent)}IfStatementNode(\n"
        result += f"{indent_str(indent + 1)}condition={self.condition},\n"
        result += f"{indent_str(indent + 1)}if_block={self.if_block},\n"
        result += f"{indent_str(indent + 1)}else_if_clauses=[\n"
        for clause in self.else_if_clauses:
            result += clause.__repr__(indent + 2) + "\n"
        result += f"{indent_str(indent + 1)}],\n"
        result += f"{indent_str(indent + 1)}else_block={self.else_block}\n"
        result += f"{indent_str(indent)})"
        return result


class ElseIfClauseNode:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ElseIfClauseNode(condition={self.condition}, block={self.block})"


class ElseClauseNode:
    def __init__(self, block):
        self.block = block

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ElseClauseNode(block={self.block})"


class BlockNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self, indent=0):
        result = f"{indent_str(indent)}BlockNode([\n"
        for statement in self.statements:
            result += statement.__repr__(indent + 1) + "\n"
        result += f"{indent_str(indent)}])"
        return result


class ReturnNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ReturnNode({self.expression})"


class BreakNode:
    def __repr__(self, indent=0):
        return f"{indent_str(indent)}BreakNode()"


class WhileLoopNode:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}WhileLoopNode(condition={self.condition}, block={self.block})"


class TypeNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"TypeNode({self.value})"


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


class ParameterNode:
    def __init__(self, type_, identifier):
        self.type_ = type_
        self.identifier = identifier

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ParameterNode(type={self.type_}, identifier={self.identifier})"
