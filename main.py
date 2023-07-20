from lexical_analyzer import LexicalAnalyzer

file = open("code.txt", "r")
text = file.readlines()
file.close()

lexical_analyzer = LexicalAnalyzer(text)
lexical_analyzer.analyze(text)
lexical_analyzer.print_simbols_table()
