from entities.nodes import ProgramNode


class Formatter:
    def __init__(self, programNode: ProgramNode):
        self.programNode = programNode

    def format(self):
        return self.programNode.format()