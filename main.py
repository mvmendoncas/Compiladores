from lexical_analyzer import LexicalAnalyzer
from sintatical_analyzer import SintaticalAnalyzer
file = open("code.txt", "r")
text = file.readlines()
file.close()

lexical_analyzer = LexicalAnalyzer(text)
lexical_analyzer.analyze(text)
lexical_analyzer.print_simbols_table()
parser = SintaticalAnalyzer(lexical_analyzer.tokens, lexical_analyzer.simbols_table)
parser.start()
