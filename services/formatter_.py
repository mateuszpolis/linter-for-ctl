from entities.nodes import (
    ClassDeclarationNode,
    FunctionCallNode,
    FunctionDeclarationNode,
    NewLineNode,
    ProgramNode,
    StructDeclarationNode,
)


class Formatter:
    def __init__(self, programNode: ProgramNode):
        self.programNode = programNode

    def format(self):
        self.__add_empty_lines_before_and_after()
        return self.programNode.format()

    def __add_empty_lines_before_and_after(self):
        nodes = [FunctionDeclarationNode, ClassDeclarationNode, StructDeclarationNode]

        # Go trhoug all nodes, and add NewLineNodes before and after each node in the list above
        i = 0
        while i < len(self.programNode.statements):
            if type(self.programNode.statements[i]) in nodes:
                self.programNode.statements.insert(i, NewLineNode())
                i += 1  # Skip the newly added NewLineNode
                self.programNode.statements.insert(i + 1, NewLineNode())
                i += 1  # Skip the newly added NewLineNode
                i += 1
            i += 1
