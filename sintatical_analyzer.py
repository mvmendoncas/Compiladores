from lexer import Lexer
from semantic_anayzer import *

class SintaticalAnalyzer:
    def __init__(self, token_list, symbol_table):
        self.symbol_table = symbol_table
        self.token_list = token_list
        self.look_ahead = 0
        self.instructions = []

    def start(self):
        print('\033[32m' + "START" + '\033[0m')
        self.program()
        print('\033[32m' + "END\n" + '\033[0m')
        return self.instructions
       

    def match(self, terminal):
        if(self.token_list[self.look_ahead].token == terminal):
            print("match!: "+ terminal)
            if(self.look_ahead < len(self.token_list)):
                self.look_ahead += 1
        else:
            print('\033[91m' + "Not Found: "+ terminal + '\033[0m')
            print('\033[91m' + "Syntax error line: " + str(self.token_list[self.look_ahead].line) + '\033[0m')
            exit()
 
    def program(self):
        self.match("<programa>")
        print("COMECEII")
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")
        if(self.token_list[self.look_ahead].token == "<fim_arquivo>"):
            self.match("<fim_arquivo>")
        else:
            print('\033[91m' + "Syntax error line: " + str(self.token_list[self.look_ahead].line) + '\033[0m')
            exit()
      
    
    def block(self):
        token_ = self.token_list[self.look_ahead]
      
        if(token_.token == "<tipo>"):
            self.declaracao_variavel()
            self.block()

        elif(token_.token == "<atribuicao>"):              
            self.atribution()
            self.block()
        elif(token_.token == "<variavel>"): #chamada function / procedimento
            if(self.token_list[self.look_ahead + 1].token == "<abre_parenteses>"):
                print("NÃO PASSEI DA CHAMADA SEMANTICA")
                if(verify_parameters(self.token_list, self.symbol_table, self.look_ahead)):
                    print("PASSEI DA CHAMADA SEMANTICA")
                    look_ahead_aux = self.look_ahead
                    instruction_aux = []
                    while self.token_list[look_ahead_aux].token not in ["<fim_comando>","<EOF>"]:
                        instruction_aux.append(self.token_list[look_ahead_aux])
                        look_ahead_aux += 1
                        
                    self.instructions.append(instruction_aux)
                  
                    self.function()
                    self.match("<fim_comando>")

                else:
                    exit()
              
            else:
                self.match("<variavel>")
                self.atribution()
            self.block()
        elif(token_.token == "<declaracao_funcao>"):
            self.declaracao_function()
            self.block()
        elif(token_.token == "<se>"):
            self.condicao()
            self.block()
        elif(token_.token == "<laco>"):
            self.laco()
            self.block()
        elif(token_.token == "<imprime>"):
            self.imprime()
            self.block()
        elif(token_.token == "<declaracao_procedimento>"):
            self.procedure()
            self.block()
      
     
    def declaracao_variavelBooleana(self): 
        self.match("<tipo>")
        self.match("<variavel>")

    def declaracao_variavel(self):
        self.match("<tipo>")
        self.match("<variavel>")
        if(self.token_list[self.look_ahead].token != "<atribuicao>"):
            self.match("<fim_comando>")

    def declaracao_function(self):
        self.match("<declaracao_funcao>")
        self.function()
        self.match("<abre_chaves>")
        self.block()
        self.retorno()
        self.match("<fecha_chaves>")

    def declaracao_procedimento(self):
        self.match("<declaracao_procedimento>")
        self.procedure()
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")
        self.match("<fim_comando>")

        

    def atribution(self):
        look_ahead_aux = self.look_ahead - 1
        instruction_aux = []
        while (look_ahead_aux < len(self.token_list) and self.token_list[look_ahead_aux].token not in ["<fim_comando>", "<EOF>"]):
            instruction_aux.append(self.token_list[look_ahead_aux])
            
            look_ahead_aux += 1
            
        self.instructions.append(instruction_aux)
        print("ANTES DO ANALISADOR SEMANTICO")
        if(verify_attribution(self.token_list, self.symbol_table, self.look_ahead)):
            print("DEPOIS DO ANALISADOR SEMANTICO")
            self.match("<atribuicao>")
            if(self.token_list[self.look_ahead].token == "<operador_booleano>"):
                self.match("<operador_booleano>")
            elif(self.token_list[self.look_ahead].token != "<variavel>"):
                    self.match("<numero>")
                    if(self.token_list[self.look_ahead].token == "<operador_aritmetico>"):
                        while(self.token_list[self.look_ahead].token == "<operador_aritmetico>"):
                            self.match("<operador_aritmetico>")
                            if(self.token_list[self.look_ahead].token == "<numero>"):
                                self.match("<numero>")
                            else:
                                self.match("<variavel>")
            else:
                    if(self.token_list[self.look_ahead + 1].token == "<abre_parenteses>"):
                        self.function()
                    else:
                        self.match("<variavel>")
                        if(self.token_list[self.look_ahead].token == "<operador_aritmetico>"):
                            while(self.token_list[self.look_ahead].token == "<operador_aritmetico>"):
                                self.match("<operador_aritmetico>")
                                if(self.token_list[self.look_ahead].token == "<numero>"):
                                    self.match("<numero>")
                                else:
                                    self.match("<variavel>")
            self.match("<fim_comando>")
        else:
            print('\033[91m' + "Syntax Error line {0} ".format(str(self.token_list[look_ahead_aux].line)) + '\033[0m')
            exit()
        

    def function(self):
        look_ahead_aux = self.look_ahead -1
        instruction_aux = []
        print_end = False
        if self.token_list[look_ahead_aux].token == "<declaracao_funcao>":
            print_end = True
            while self.token_list[look_ahead_aux].token not in ["<abre_chaves>","<EOF>"]:
                #if self.token_list[look_ahead_aux].token != "<operador_booleano>" :
                instruction_aux.append(self.token_list[look_ahead_aux])

                look_ahead_aux += 1


            self.instructions.append(instruction_aux)

        self.match("<variavel>")
        self.match("<abre_parenteses>")
        self.parameters()
        self.match("<fecha_parenteses>")




    def parameters(self):
        
        token_ = self.token_list[self.look_ahead]

        if(token_.token == "<tipo>"):
            self.match("<tipo>")
            self.match("<variavel>")
            if(self.token_list[self.look_ahead].token == "<virgula>"):
                self.parameters()
            else:
                return
        elif(token_.token == "<virgula>"):
            self.match("<virgula>")
            if(self.token_list[self.look_ahead].token != "<variavel>" and self.token_list[self.look_ahead].token != "<numero>" and self.token_list[self.look_ahead].token != "<operador_booleano>" ):
                self.match("<tipo>")
                self.match("<variavel>")
                self.parameters()
            else:
                self.parameters()
                
        elif(token_.token == "<variavel>"):
            self.match("<variavel>")
            if(self.token_list[self.look_ahead].token == "<virgula>"):
                self.parameters()
            return
        elif(token_.token == "<numero>"):
            self.match("<numero>")
            if(self.token_list[self.look_ahead].token == "<virgula>"):
                self.parameters()
            return
        elif(token_.token == "<operador_booleano>"): # ACEITA RECEBER APENAS TRUE OU FALSE
            self.match("<operador_booleano>")
            if(self.token_list[self.look_ahead].token == "<virgula>"):
                self.parameters()
            return
        else:
            return

    def simple_exp(self): #*
        if(verify_expressions(self.token_list, self.symbol_table, self.look_ahead)):
            self.match(self.token_list[self.look_ahead].token) #SE ENTROU NO IF ELE ACEITA QUALQUER COISA QUE VIER
            if(self.token_list[self.look_ahead].token == "<operador_relacional>"):
                self.match("<operador_relacional>")
                if(self.token_list[self.look_ahead].token == "<variavel>"):
                    self.match("<variavel>")
                elif(self.token_list[self.look_ahead].token == "<operador_booleano>"):
                    self.match("<operador_booleano>")
                else:
                    self.match("<numero>")
            else:
                self.match("<operador_aritmetico>")
                if(self.token_list[self.look_ahead].token == "<variavel>"):
                    self.match("<variavel>")
                elif(self.token_list[self.look_ahead].token == "<numero>"):
                    self.match("<numero>") 
                if(self.token_list[self.look_ahead].token == "<operador_relacional>"):
                    self.match("<operador_relacional>")
                    if(self.token_list[self.look_ahead].token == "<variavel>"):
                        self.match("<variavel>")
                    else:
                        self.match("<numero>")
            if(self.token_list[self.look_ahead].token == "<operador_logico>"):
                self.match("<operador_logico>")
             
        else:
            exit()

            
       
    def condicao(self):
        look_ahead_aux = self.look_ahead
        instruction_aux = []
        while self.token_list[look_ahead_aux].token not in ["<abre_chaves>","<EOF>"]:
            #if self.token_list[look_ahead_aux].token != "<operador_booleano>" :
            instruction_aux.append(self.token_list[look_ahead_aux])

            look_ahead_aux += 1
        self.instructions.append(instruction_aux)

        self.match("<se>")
        self.match("<abre_parenteses>")
        self.simple_exp()
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")
        self.instructions.append([self.token_list[self.look_ahead],self.token_list[self.look_ahead -1] ])
        if(self.token_list[self.look_ahead].token == "<senao>"):
            self.match("<senao>")
            self.match("<abre_chaves>")
            self.block()
            self.match("<fecha_chaves>")
            
    def laco(self):
        look_ahead_aux = self.look_ahead
        instruction_aux = []
        while self.token_list[look_ahead_aux].token not in  ["<abre_chaves>","<EOF>"]:
            instruction_aux.append(self.token_list[look_ahead_aux])

            look_ahead_aux += 1
        self.instructions.append(instruction_aux)

        self.match("<laco>")
        self.match("<abre_parenteses>")
        self.simple_exp() 
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block()
        if(self.token_list[self.look_ahead].token == "<pare>"):
            self.match("<pare>")
            self.match("<fim_comando>")
        elif(self.token_list[self.look_ahead].token == "<continue>"):
            self.match("<continue>")
            self.match("<fim_comando>")


        self.instructions.append([self.token_list[self.look_ahead],self.token_list[self.look_ahead -1] ])
        self.match("<fecha_chaves>")
    
    def imprime(self):
        instruction_aux = []
        look_ahead_aux = self.look_ahead

        while look_ahead_aux < len(self.token_list) and self.token_list[look_ahead_aux].token not in ["<fim_comando>","<EOF>"]:
            instruction_aux.append(self.token_list[look_ahead_aux])
            look_ahead_aux += 1

        self.instructions.append(instruction_aux)

        self.match("<imprime>")
        self.match("<abre_parenteses>")
        if(self.token_list[self.look_ahead].token == "<variavel>"):
            self.match("<variavel>") 
        else:
            self.match("<numero>")
        self.match("<fecha_parenteses>")
        self.match("<fim_comando>")
    
    def retorno(self):
        instruction_aux = []

        instruction_aux.append(self.token_list[self.look_ahead])
        instruction_aux.append(self.token_list[self.look_ahead + 1])

        self.instructions.append(instruction_aux)

        self.match("<retorno>")
        if(self.token_list[self.look_ahead].token == "<variavel>"):
            if(verify_variable_return(self.token_list, self.symbol_table, self.look_ahead)):
                self.match("<variavel>")
            else:
                quit()
           
        else:
            self.match("<numero>")
        self.match("<fim_comando>")

        end = [Lexer("<end_func>","end_func",0), Lexer("<end_func>","end_func",0)]
        self.instructions.append(end)
    
    def procedure(self):
        look_ahead_aux = self.look_ahead
        instruction_aux = []

        while self.token_list[look_ahead_aux].token not in ["<fim_comando>","<EOF>"]:
            instruction_aux.append(self.token_list[look_ahead_aux])
            look_ahead_aux += 1

        self.instructions.append(instruction_aux)
        
        self.match("<declaracao_procedimento>")
        self.function()
        self.match("<abre_chaves>")
        if(verify_procedure(self.token_list, self.symbol_table, self.look_ahead)):
            self.block()
        else:
            quit()
        self.match("<fecha_chaves>")

       

        endProc = [Lexer("<end_proc>","<end_proc>",0), Lexer("<end_proc>","endProc",0)]
        self.instructions.append(endProc)