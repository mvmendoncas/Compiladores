from lexical_analyzer import LexicalAnalyzer
from sintatical_analyzer import SintaticalAnalyzer
from intermediate_code import IntermediateCode

file = open("code.txt", "r")
text = file.readlines()
file.close()

lexical_analyzer = LexicalAnalyzer(text)
lexical_analyzer.analyze(text)
lexical_analyzer.print_simbols_table()
#lexical_analyzer.print_token_list()
#parser = SintaticalAnalyzer(lexical_analyzer.tokens, lexical_analyzer.simbols_table)
#instructions = parser.start()


#gen = IntermediateCode(instructions)
#gen.start()