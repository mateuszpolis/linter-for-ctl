def indent_str(indent_level):
    return "  " * indent_level  # 2 spaces per level


class DefaultNode:
    def __init__(self):
        self.comment = None

    def set_comment(self, comment):
        self.comment = comment

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}DefaultNode(comment={self.value})"


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
    def __init__(
        self, type_, identifiers, is_const=False, access_modifier=None, modifier=None
    ):
        """
        :param type_keyword: The data type of the declaration (e.g., 'int' or 'string')
        :param identifiers: A list of tuples where each tuple contains:
                            - the identifier name (string)
                            - an optional initial value (AST node or None if no initialization)
        """
        self.type = type_
        self.identifiers = identifiers
        self.is_const = is_const
        self.access_modifier = access_modifier
        self.modifier = modifier

    def __repr__(self, indent=0):
        # Start the string with the type keyword
        string = f"{indent_str(indent)}DeclarationNode(const={self.is_const}, access_modifier={self.access_modifier}, modifier={self.modifier}, type={self.type.__repr__(indent+1)}, identifiers=[\n"

        # Add each identifier with its optional initial value
        for identifier, value in self.identifiers:
            if value is None:
                string += f"{indent_str(indent + 1)}{identifier}\n"
            else:
                string += f"{indent_str(indent + 1)}{identifier} = {value.__repr__(indent + 2)}\n"

        string += f"{indent_str(indent)}])"
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


class IdentifierNode(DefaultNode):
    def __init__(self, value, type_cast=None):
        super().__init__()
        self.value = value
        self.type_cast = type_cast

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}IdentifierNode(value={self.value}, type_cast={self.type_cast}, comment={self.comment})"


class GlobalIdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}GlobalIdentifierNode({self.value})"


class PointerNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}PointerNode({self.value})"


class NumberNode:
    def __init__(self, value, is_float=False, is_negative=False):
        self.value = value
        self.is_float = is_float
        self.is_negative = is_negative

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}NumberNode(is_float={self.is_float}, is_negative={self.is_negative}, value={self.value})"


class BooleanNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}BooleanNode({self.value})"


class StringNode(DefaultNode):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}StringNode({self.value}, comment={self.comment})"


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
    def __init__(self, parameters, block, type_=None):
        self.parameters = parameters
        self.block = block
        self.type = type_

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}MainNode(\n"
        string += f"{indent_str(indent + 1)}type: {self.type}\n"
        string += f"{indent_str(indent + 1)}parameters: {self.parameters}\n"
        string += f"{indent_str(indent + 1)}block: {self.block}\n"
        string += f"{indent_str(indent)})"
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


class ElseIfClauseNode(DefaultNode):
    def __init__(self, condition, block=None, inline_statement=None):
        super().__init__()
        self.condition = condition
        self.block = block
        self.inline_statement = inline_statement

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ElseIfClauseNode(condition={self.condition}, comment={self.comment} block={self.block}, inline_statement={self.inline_statement})"


class ElseClauseNode(DefaultNode):
    def __init__(self, block, inline_statement=None):
        super().__init__()
        self.block = block
        self.inline_statement = inline_statement

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ElseClauseNode(comment={self.comment}, block={self.block}, inline_statement={self.inline_statement})"


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


class NegationNode:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}NegationNode(expression={self.expression})"


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


class LibraryNode:
    def __init__(self, name):
        self.name = name

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}LibraryNode({self.name})"


class CharNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CharNode({self.value})"


class TernaryExpressionNode:
    def __init__(self, comparison, success_expression, failure_expression):
        self.comparison = comparison
        self.success_expression = success_expression
        self.failure_expression = failure_expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}TernaryExpression({self.comparison}, {self.success_expression}, {self.failure_expression})"


class ForLoopNode:
    def __init__(self, initialization, condition, increment, block, statement):
        self.initialization = initialization
        self.condition = condition
        self.increment = increment
        self.block = block
        self.statement = statement

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ForLoopNode(initialization={self.initialization}, condition={self.condition}, increment={self.increment}, block={self.block}), statement={self.statement}"


class IncrementAssignmentNode:
    def __init__(self, identifier, operator):
        self.identifier = identifier
        self.operator = operator

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}IncrementAssignmentNode(identifier={self.identifier}, operator={self.operator})"


class CompoundAssignmentNode:
    def __init__(self, identifier, operator, value):
        self.identifier = identifier
        self.operator = operator
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CompundAssignmentNode(identifier={self.identifier}, operator={self.operator}, value={self.value})"


class LogicalOrNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}LogicalOrNode(left={self.left}, right={self.right})"
        )


class LogicalAndNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}LogicalAndNode(left={self.left}, right={self.right})"
        )


class NegationNode:
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}NegationNode(operator={self.operator}, expression={self.expression})"


class RelationalNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}RelationalNode(left={self.left}, operator='{self.operator}', right={self.right})"


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


class EnumValueNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}EnumValueNode(identifier={self.identifier}, value={self.value})"


class EnumAccessNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}EnumAccessNode(identifier={self.identifier}, value={self.value})"


class CaseStatementNode:
    def __init__(self, value, block, is_default=False):
        self.value = value
        self.block = block
        self.is_default = is_default

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}CaseStatementNode(is_default={self.is_default}, value={self.value}, block={self.block})"


class SwitchStatementNode:
    def __init__(self, expression, case_statements):
        self.expression = expression
        self.case_statements = case_statements

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}SwitchStatementNode(\n"
        string += f"{indent_str(indent + 1)}expression: {self.expression}\n"
        string += f"{indent_str(indent + 1)}case_statements: [\n"
        for case_statement in self.case_statements:
            string += case_statement.__repr__(indent + 2) + "\n"
        string += f"{indent_str(indent + 1)}]\n"
        string += f"{indent_str(indent)})"
        return string


class BitwiseOrNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}BitwiseOrNode(left={self.left}, right={self.right})"
        )


class BitwiseXorNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}BitwiseXorNode(left={self.left}, right={self.right})"
        )


class BitwiseAndNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self, indent=0):
        return (
            f"{indent_str(indent)}BitwiseAndNode(left={self.left}, right={self.right})"
        )


class ShiftNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ShiftNode(left={self.left}, operator={self.operator}, right={self.right})"


class StructDeclarationNode:
    def __init__(self, identifier, block, inheritance=None):
        self.identifier = identifier
        self.block = block
        self.inheritance = None

    def __repr__(self, indent=0):
        string = f"{indent_str(indent)}StructDeclarationNode(inheritance={self.inheritance}, identifier={self.identifier},\n"
        string += self.block.__repr__(indent + 1) + "\n"
        return string


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


class InheritanceNode:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}InheritanceNode(identifier={self.identifier})"


class TypeCastNode:
    def __init__(self, type_, expression):
        self.type_ = type_
        self.expression = expression

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}TypeCastNode(type={self.type_}, expression={self.expression})"


class ClassStaticAccessNode:
    def __init__(self, identifier, attribute):
        self.identifier = identifier
        self.attribute = attribute

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ClassStaticAccessNode(identifier={self.identifier}, attribute={self.attribute})"


class ClassInitializationNode:
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ClassInitializationNode(identifier={self.identifier}, arguments={self.arguments})"


class ContinueNode:
    def __repr__(self, indent=0):
        return f"{indent_str(indent)}ContinueNode()"

class TryCatchNode:
    def __init__(self, try_block, catch_block, finally_block=None):
        self.try_block = try_block
        self.catch_block = catch_block
        self.finally_block = finally_block

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}TryCatchNode(try_block={self.try_block}, catch_block={self.catch_block}, finally_block={self.finally_block})"
    
class DoWhileLoopNode:
    def __init__(self, block, condition):
        self.block = block
        self.condition = condition

    def __repr__(self, indent=0):
        return f"{indent_str(indent)}DoWhileLoopNode(block={self.block}, condition={self.condition})"