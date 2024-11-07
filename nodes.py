def indent_str(indent_level):
    return "  " * indent_level  # 2 spaces per level

class ProgramNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self, indent=0):
        string = f'{indent_str(indent)}ProgramNode(\n'
        for statement in self.statements:
            string += statement.__repr__(indent + 1) + '\n'
        string += f'{indent_str(indent)})'
        return string

class StatementNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}StatementNode({self.identifier}, {self.value.__repr__(indent + 1)})'

class AssignmentNode:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}AssignmentNode({self.identifier}, {self.value.__repr__(indent + 1)})'

class DeclarationNode:
    def __init__(self, type_keyword, identifiers):
        """
        :param type_keyword: The data type of the declaration (e.g., 'int' or 'string')
        :param identifiers: A list of tuples where each tuple contains:
                            - the identifier name (string)
                            - an optional initial value (AST node or None if no initialization)
        """
        self.type_keyword = type_keyword
        self.identifiers = identifiers

    def __repr__(self, indent=0):
        # Start the string with the type keyword
        string = f'{indent_str(indent)}DeclarationNode(type={self.type_keyword}, identifiers=[\n'
        
        # Add each identifier with its optional initial value
        for identifier, value in self.identifiers:
            if value is None:
                string += f'{indent_str(indent + 1)}{identifier}\n'
            else:
                string += f'{indent_str(indent + 1)}{identifier} = {value.__repr__(indent + 2)}\n'
        
        string += f'{indent_str(indent)}])'
        return string


class BinaryExpressionNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self, indent=0):
        string = f'{indent_str(indent)}BinaryExpressionNode(\n'
        string += f'{indent_str(indent + 1)}left: {self.left.__repr__(indent + 2)}\n'
        string += f'{indent_str(indent + 1)}operator: {self.operator}\n'
        string += f'{indent_str(indent + 1)}right: {self.right.__repr__(indent + 2)}\n'
        string += f'{indent_str(indent)})'
        return string

class IdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}IdentifierNode({self.value})'
    
class GlobalIdentifierNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}GlobalIdentifierNode({self.value})'

class NumberNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}NumberNode({self.value})'

class StringNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}StringNode({self.value})'

class OperatorNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}OperatorNode({self.value})'

class KeywordNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}KeywordNode({self.value})'

class SymbolNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}SymbolNode({self.value})'    

class CommentNode:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self, indent=0):
        return f'{indent_str(indent)}CommentNode({self.value})'

class DividerNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}DividerNode({self.value})'

class WhitespaceNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}WhitespaceNode({self.value})'
    
class AttributeAccessNode:
    def __init__(self, identifier, attribute):
        self.identifier = identifier
        self.attribute = attribute

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}AttributeAccessNode({self.identifier}, {self.attribute})'
    
class IndexAccessNode:
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index

    def __repr__(self, indent=0):
        return f'{indent_str(indent)}IndexAccessNode({self.identifier}, {self.index})'
    
class FunctionDeclarationNode:
    def __init__(self, return_type, identifier, parameters, statements):
        self.return_type = return_type
        self.identifier = identifier
        self.parameters = parameters
        self.statements = statements

    def __repr__(self, indent=0):
        string = f'{indent_str(indent)}FunctionDeclarationNode(\n'
        string += f'{indent_str(indent + 1)}return_type: {self.return_type}\n'
        string += f'{indent_str(indent + 1)}identifier: {self.identifier}\n'
        string += f'{indent_str(indent + 1)}parameters: {self.parameters}\n'
        string += f'{indent_str(indent + 1)}statements: [\n'
        for statement in self.statements:
            string += statement.__repr__(indent + 2) + '\n'
        string += f'{indent_str(indent + 1)}]\n'
        string += f'{indent_str(indent)})'
        return string
    
class FunctionCallNode:
    def __init__(self, identifier, arguments):
        self.identifier = identifier
        self.arguments = arguments

    def __repr__(self, indent=0):
        string = f'{indent_str(indent)}FunctionCallNode(\n'
        string += f'{indent_str(indent + 1)}identifier: {self.identifier}\n'
        string += f'{indent_str(indent + 1)}arguments: [\n'
        for argument in self.arguments:
            string += argument.__repr__(indent + 2) + '\n'
        string += f'{indent_str(indent + 1)}]\n'
        string += f'{indent_str(indent)})'
        return string