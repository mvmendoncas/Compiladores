class Expression:
    def __init__(self, type, line):
        self.type = type
        self.line = line

class ExpressionFunction:
    def __init__(self, type, line, parameters_amount, parameters_list):
        self.type = type
        self.line = line
        self.parameters_amount = parameters_amount
        self.parameters_list = parameters_list
        