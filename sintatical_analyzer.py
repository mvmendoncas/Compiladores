from lexer import Lexer

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
            #self.look_ahead += 1
#----------------------------------------------------------------------------------------------------
    def program(self):
        self.match("<program>")
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")

               
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
                if(verificar_parameters(self.token_list, self.symbol_table, self.look_ahead)):
                    look_ahead_aux = self.look_ahead
                    instruction_aux = []
                    while self.token_list[look_ahead_aux].token not in ["<fim_comando>","<EOF>"]:
                        instruction_aux.append(self.token_list[look_ahead_aux])
                        look_ahead_aux += 1
                        
                    self.instructions.append(instruction_aux)
                    
                    self.function()
                    self.match("<fim_comando>")
                else:
                    #print('\033[91m' + "Error line {0} ".format((self.token_list[look_ahead_aux].line) + '\033[0m'))
                    exit()
            else:
                self.match("<variavel>")
                self.atribution()
            self.block()
        elif(token_.token == "<declaracao_func>"):
            self.declaracao_function()
            self.block()
        elif(token_.token == "<condition>"):
            self.condition()
            self.block()
        elif(token_.token == "<laco>"):
            self.laco()
            self.block()
        elif(token_.token == "<imprimir>"):
            #print(self.token_list[self.look_ahead].lexema)
            self.imprimir()
            self.block()
        elif(token_.token == "<procedimento>"):
            self.procedure()
            self.block()
        elif(token_.token == "<constante>"):
            self.match("<constante>")
            self.match("<variavel>")
            if(verificar_atribuicao(self.token_list, self.symbol_table, self.look_ahead)):
                self.match("<atribuicao>")
                if(self.token_list[self.look_ahead].token == "<palavraBooleana>"):
                    self.match("<palavraBooleana>")
                elif(self.token_list[self.look_ahead].token != "<variavel>"):
                    self.match("<numerico>")
            else:
                quit()
            self.match("<fim_comando>")
            self.block()
        else:
            #print('\033[93m' + "block Syntax error line: " + str(token_.line) + '\033[0m')
            return

    def declaracao_variavelBooleana(self): ## não é chamadooo
        self.match("<tipo>")
        self.match("<variavel>")
        #self.match("<fim_comando>")

    def declaracao_variavel(self):
        self.match("<tipo>")
        self.match("<variavel>")
        if(self.token_list[self.look_ahead].token != "<atribuicao>"):
            self.match("<fim_comando>")

    def declaracao_function(self):
        self.match("<declaracao_func>")
        self.function()
        self.match("<abre_chaves>")
        self.block()
        self.retorno()
        self.match("<fecha_chaves>")

    def atribution(self):
        look_ahead_aux = self.look_ahead - 1
        instruction_aux = []
        while(self.token_list[look_ahead_aux].token not in ["<fim_comando>", "<EOF>"]):
            instruction_aux.append(self.token_list[look_ahead_aux])

            look_ahead_aux += 1
        self.instructions.append(instruction_aux)

        if verificar_atribuicao(self.token_list, self.symbol_table, self.look_ahead):
            self.match("<atribuicao>")
            if(self.token_list[self.look_ahead].token == "<palavraBooleana>"):
                self.match("<palavraBooleana>")
            elif(self.token_list[self.look_ahead].token != "<variavel>"):
                self.match("<numerico>")
                if(self.token_list[self.look_ahead].token == "<aritmeticas>"):
                    while(self.token_list[self.look_ahead].token == "<aritmeticas>"):
                        self.match("<aritmeticas>")
                        if(self.token_list[self.look_ahead].token == "<numerico>"):
                            self.match("<numerico>")
                        else:
                            self.match("<variavel>")
            else:
                if(self.token_list[self.look_ahead + 1].token == "<abre_parenteses>"):
                    self.function()
                else:
                    self.match("<variavel>")
                    if(self.token_list[self.look_ahead].token == "<aritmeticas>"):
                        while(self.token_list[self.look_ahead].token == "<aritmeticas>"):
                            self.match("<aritmeticas>")
                            if(self.token_list[self.look_ahead].token == "<numerico>"):
                                self.match("<numerico>")
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
        if self.token_list[look_ahead_aux].token == "<declaracao_func>":
            print_end = True
            while self.token_list[look_ahead_aux].token not in ["<abre_chaves>","<EOF>"]:
                #if self.token_list[look_ahead_aux].token != "<palavraBooleana>" :
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
            if(self.token_list[self.look_ahead].token != "<variavel>" and self.token_list[self.look_ahead].token != "<numerico>" and self.token_list[self.look_ahead].token != "<palavraBooleana>" ):
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
        elif(token_.token == "<numerico>"):
            self.match("<numerico>")
            if(self.token_list[self.look_ahead].token == "<virgula>"):
                self.parameters()
            return
        elif(token_.token == "<palavraBooleana>"): # ACEITA RECEBER APENAS TRUE OU FALSE
            self.match("<palavraBooleana>")
            if(self.token_list[self.look_ahead].token == "<virgula>"):
                self.parameters()
            return
        else:
            return

    def simple_exp(self): #*
        if verificar_expressao(self.token_list, self.symbol_table, self.look_ahead): ## VERIFICO SE A EXPRESSÃO ESTA CORRETA
            self.match(self.token_list[self.look_ahead].token) #SE ENTROU NO IF ELE ACEITA QUALQUER COISA QUE VIER
            if(self.token_list[self.look_ahead].token == "<booleanas>"):
                self.match("<booleanas>")
                if(self.token_list[self.look_ahead].token == "<variavel>"):
                    self.match("<variavel>")
                elif(self.token_list[self.look_ahead].token == "<palavraBooleana>"):
                    self.match("<palavraBooleana>")
                else:
                    self.match("<numerico>")
            else:
                self.match("<aritmeticas>")
                if(self.token_list[self.look_ahead].token == "<variavel>"):
                    self.match("<variavel>")
                elif(self.token_list[self.look_ahead].token == "<numerico>"):
                    self.match("<numerico>")

                
                if(self.token_list[self.look_ahead].token == "<booleanas>"):
                    self.match("<booleanas>")
                    if(self.token_list[self.look_ahead].token == "<variavel>"):
                        self.match("<variavel>")
                    else:
                        self.match("<numerico>")
        else:
           
            exit()

    def condition(self):
        look_ahead_aux = self.look_ahead
        instruction_aux = []
        while self.token_list[look_ahead_aux].token not in ["<abre_chaves>","<EOF>"]:
            #if self.token_list[look_ahead_aux].token != "<palavraBooleana>" :
            instruction_aux.append(self.token_list[look_ahead_aux])

            look_ahead_aux += 1
        self.instructions.append(instruction_aux)

        self.match("<condicao>")
        self.match("<abre_parenteses>")
        self.simple_exp()
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block()
        self.match("<fecha_chaves>")

        self.instructions.append([self.token_list[self.look_ahead],self.token_list[self.look_ahead]])
        self.match("<condicao>")
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
        self.simple_exp() #*
        self.match("<fecha_parenteses>")
        self.match("<abre_chaves>")
        self.block()
        if(self.token_list[self.look_ahead].token == "<continuar>"):
            self.match("<continuar>")
            self.match("<fim_comando>")
        elif(self.token_list[self.look_ahead].token == "<parar>"):
            self.match("<parar>")
            self.match("<fim_comando>")


        self.instructions.append([self.token_list[self.look_ahead],self.token_list[self.look_ahead -1] ])
        self.match("<fecha_chaves>")
    
    def imprimir(self):
        instruction_aux = []
        look_ahead_aux = self.look_ahead

        while self.token_list[look_ahead_aux].token not in ["<fim_comando>","<EOF>"]:
            instruction_aux.append(self.token_list[look_ahead_aux])
            look_ahead_aux += 1

        self.instructions.append(instruction_aux)

        self.match("<imprimir>")
        self.match("<abre_parenteses>")
        if(self.token_list[self.look_ahead].token == "<variavel>"):
            self.match("<variavel>") # Falta constante
        elif(self.token_list[self.look_ahead].token == "<constante>"):
            self.match("<constante>")
        else:
            self.match("<numerico>")
        self.match("<fecha_parenteses>")
        self.match("<fim_comando>")
    
    def retorno(self):
        instruction_aux = []

        instruction_aux.append(self.token_list[self.look_ahead])
        instruction_aux.append(self.token_list[self.look_ahead + 1])

        self.instructions.append(instruction_aux)

        self.match("<retorno>")
        if(self.token_list[self.look_ahead].token == "<variavel>"):
            if(verificar_retorno_variavel(self.token_list, self.symbol_table, self.look_ahead)):
                self.match("<variavel>")
            else:
                quit()
        else:
            self.match("<numerico>")
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

        self.match("<procedimento>")
        self.function()
        self.match("<abre_chaves>")
        if(verificar_procedimento(self.token_list, self.symbol_table, self.look_ahead)):
            self.block()
        else:
            quit()
        self.match("<fecha_chaves>")

        endProc = [Lexer("<end_proc>","<end_proc>",0), Lexer("<end_proc>","endProc",0)]
        self.instructions.append(endProc)