from lexer import Lexer
from expressions import *

class LexicalAnalyzer:
    def __init__(self, text):
        self.text = text
        self.tokens = []
        self.simbols_table = {}

    def analyze(self, text):
        buffer = ""
        now_line = 1
        for line in text:
            for i in range(len(line)):
                if(i + 1 < len(line)):
                    buffer += line[i]
                    if(self.verify_delimiters(buffer, now_line)):
                        buffer = ""
                        continue
                    elif(line[i + 1] == " " or line[i + 1] == "\n" or line[i + 1] == "{" or line[i + 1] == "}" or line[i + 1] == "(" or line[i + 1] == ")" or line[i + 1] == ";" or line[i + 1] == ","):
                                buffer = buffer.strip()
                                self.verify_reserved_simbols(buffer, now_line, line, i)
                                buffer = ""
            buffer = ""
            now_line += 1
        self.tokens.append(Lexer("<fim_arquivo>", "EOF", (now_line + 1)))

        
    def verify_delimiters(self, buffer, line):
        if(buffer == " "):
            return True
        elif(buffer == "{"):
            self.tokens.append(Lexer("<abre_chaves>", "{", line))
            return True
        elif(buffer == "}"):
            self.tokens.append(Lexer("<fecha_chaves>", "}", line))
            return True
        elif(buffer == "("):
            self.tokens.append(Lexer("<abre_parenteses>", "(", line))
            return True
        elif(buffer == ")"):
            self.tokens.append(Lexer("<fecha_parenteses>", ")", line))
            return True
        elif(buffer == ";"):
            self.tokens.append(Lexer("<fim_comando>", ";", line))
            return True
        else:
            return False
        
    def verify_reserved_simbols(self, buffer, line, text, i):
        if(buffer == "main"):
            self.tokens.append(Lexer("<programa>", "main", line))
            return True
        if(buffer == "int"):
            self.tokens.append(Lexer("<tipo>", "inteiro", line))
            return True
        if(buffer == "bool"):
            self.tokens.append(Lexer("<tipo>", "booleano", line))
            return True
        if(buffer == "procedure"):
            self.tokens.append(Lexer("<declaracao_procedimento>", "procedimento", line))
            return True
        if(buffer == "func"):
            self.tokens.append(Lexer("<declaracao_funcao>", "funcao", line))
            return True
        if(buffer == "if"):
            self.tokens.append(Lexer("<condicao>", "if", line))
            return True
        if(buffer == "else"):
            self.tokens.append(Lexer("<condicao>", "else", line))
            return True
        if(buffer == "while"):
            self.tokens.append(Lexer("<laco>", "while", line))
            return True
        if(buffer == "do"):
            self.tokens.append(Lexer("<laco>", "do", line))
            return True
        if(buffer == "return"):
            self.tokens.append(Lexer("<retorno>", "return", line))
            return True
        if(buffer == "input"):
            self.tokens.append(Lexer("<leitura>", "input", line))
            return True
        if(buffer == "print"):
            self.tokens.append(Lexer("<imprime>", "print", line))
            return True
        if(buffer == "break"):
            self.tokens.append(Lexer("<pare>", "break", line))
            return True
        if(buffer == "continue"):
            self.tokens.append(Lexer("<continue>", "continue", line))
            return True
        if(buffer == "!="):
            self.tokens.append(Lexer("<operador_relacional>", "!=", line))
            return True
        if(buffer == "=="):
            self.tokens.append(Lexer("<operador_relacional>", "==", line))
            return True
        if(buffer == "<"):
            self.tokens.append(Lexer("<operador_relacional>", "<", line))
            return True
        if(buffer == "<="):
            self.tokens.append(Lexer("<operador_relacional>", "<=", line))
            return True
        if(buffer == ">"):
            self.tokens.append(Lexer("<operador_relacional>", ">", line))
            return True
        if(buffer == ">="):
            self.tokens.append(Lexer("<operador_relacional>", ">=", line))
            return True
        if(buffer == "+"):
            self.tokens.append(Lexer("<operador_aritmetico>", "+", line))
            return True
        if(buffer == "-"):
            self.tokens.append(Lexer("<operador_aritmetico>", "-", line))
            return True
        if(buffer == "/"):
            self.tokens.append(Lexer("<operador_aritmetico>", "/", line))
            return True
        if(buffer == "*"):
            self.tokens.append(Lexer("<operador_aritmetico>", "*", line))
            return True
        if(buffer == "mod"):
            self.tokens.append(Lexer("<operador_aritmetico>", "mod", line))
            return True
        if(buffer == "&&"):
            self.tokens.append(Lexer("<operador_logico>", "&&", line))
            return True
        if(buffer == "||"):
            self.tokens.append(Lexer("<operador_logico>", "||", line))
            return True
        if(buffer == "mod"):
            self.tokens.append(Lexer("<operador_termo>", "mod", line))
            return True
        if(buffer == "="):
            self.tokens.append(Lexer("<atribuicao>", "=", line))
            return True
        elif (buffer == ","):
            self.tokens.append(Lexer("<virgula>",",",line))
            return True
        if(buffer == "True"):
            self.tokens.append(Lexer("<operador_booleano>", "True", line))
            return True
        if(buffer == "False"):
            self.tokens.append(Lexer("<operador_booleano>", "False", line))
            return True
        else:
            self.variables(buffer, line, text, i)

    def variables(self, buffer, line, text, i):
        aux = buffer[0].upper() >= 'A' and buffer[0].upper() <= 'Z'
        if ((aux)):
            for c in buffer:
                if ((c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z') or (c >= '0' and c <= '9')):
                    continue
                else:
                    print('\033[91m' + "Error variable line: " + str(line) + '\033[0m')
                    quit()
            
            last_token = self.tokens[len(self.tokens) - 1]
            if(buffer not in self.simbols_table):
                if(last_token.token == "<tipo>"):
                    if(last_token.lexer == "int"):
                        self.simbols_table[buffer] = Expression("int", line)
                    elif(last_token.lexer == "bool"):
                        self.simbols_table[buffer] = Expression("bool", line)

                elif(last_token.token == "<declaracao_funcao>"):
                    j = i
                    listParameters = []
                    amountParameters = 0

                    while(text[j] != ")"):
                        verifyInt = text[j - 2] + text[j - 1] + text[j]
                        verifyBool = text[j - 6] + text[j - 5] + text[j - 4] + text[j - 3 ] + text[j - 2]+ text[j]

                        if(verifyInt == "int" ):
                            amountParameters += 1
                            listParameters.append(Expression("int", line))

                        elif(verifyBool == "bool"):
                            amountParameters += 1
                            listParameters.append(Expression("bool", line))
                        
                        j += 1
                    self.simbols_table[buffer] = ExpressionFunction("function", line, amountParameters, listParameters)
                elif(last_token.token == "<declaracao_procedimento>"):
                    j = i
                    listParameters = []
                    amountParameters = 0

                    while(text[j] != ")"):
                        verifyInt = text[j - 2] + text[j - 1] + text[j]
                        verifyBool = text[j - 6] + text[j - 5] + text[j - 4] + text[j - 3 ] + text[j - 2]+ text[j]

                        if(verifyInt == "int" ):
                            amountParameters += 1
                            listParameters.append(Expression("int", line))

                        elif(verifyBool == "bool"):
                            amountParameters += 1
                            listParameters.append(Expression("bool", line))
                        
                        j += 1
                    self.simbols_table[buffer] = ExpressionFunction("procedure", line, amountParameters, listParameters)
                
        
                self.tokens.append(Lexer("<variavel>", buffer, line))

            else:
                if(self.tokens[len(self.tokens) - 1].token != "<tipo>" and self.tokens[len(self.tokens) - 1].token != "<declaracao_funcao>" and self.tokens[len(self.tokens) - 1].token != "<declaracao_procedimento>"):
                   self.tokens.append(Lexer("<variavel>", buffer, line))
                else:
                    print('\033[91m' + "Error variable {0} already declared ".format(buffer) + '\033[0m')
                    quit()
        else:
            for c in buffer:
                if (c >= '0' and c <= '9'):
                    continue
                else:
                    print('\033[91m' + "Error variable line: " + str(line) + '\033[0m')
                    quit()
            self.tokens.append(Lexer("<numero>", buffer, line))

    def print_token_list(self):
            for token in self.tokens:
                print(token.type + " " + token.lexer + " " + str(token.line) + "\n")

    def print_simbols_table(self):
        print('\033[32m'  + "Tabela de simbolos: " + '\033[0m')
        for key in self.simbols_table:
            if type(self.simbols_table[key]) is Expression:
                print("Variavel: " + key + " Tipo: " + self.simbols_table[key].type + " Linha: " + str(self.simbols_table[key].line))
            else:
                print("Funcao/Procedimento: " + key + " Tipo: " + self.simbols_table[key].type + " Linha: " + str(self.simbols_table[key].line) + " Quantidade de parametros: " + str(self.simbols_table[key].parameters_amount))
                for parameter in self.simbols_table[key].parameters_list:
                    print("Tipo do parametro: " + parameter.type + " Linha: " + str(parameter.line))


        

