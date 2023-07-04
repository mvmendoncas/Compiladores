class Lexer:
    def __init__(token, lexer, line):
        self.token = token
        self.lexer = lexer
        self.line = line

    def print(self):
        print("Token: " + self.token + "\nLexer: " + self.lexer + "\nLine: " + self.line)