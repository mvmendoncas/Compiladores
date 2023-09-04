from lexer import Lexer

class IntermediateCode:

    def __init__(self, instructions_list):
        self.instructions_list = instructions_list
        self.labels = 0 
        self.lastLabelWhile = []
        self.labelsElse = []
    #Essa função imprime a lista de instruções 
    def printInstructionsList(self):
        for i in range(len(self.instructions_list)):
            for j in range(len(self.instructions_list[i])):
                print(self.instructions_list[i][j].lexer, end=" ")
            print("") 
    #Esta função é o ponto de entrada principal para a geração de código intermediário.
    # Ela percorre a lista de instruções e chama funções específicas com base no tipo de instrução encontrada.
    def start(self):
        file = open("output.txt", 'w')

        print('\033[4m' + "CODIGO INTERMEDIARIO:" + '\033[0m')
        for i in range(len(self.instructions_list)):
            print("")
            file.write("\n")

            if(self.instructions_list[i][1].token) == "<atribuicao>": 
                self.gen_attr(self.instructions_list[i], file) #chamando funcao para gerar codigo para atribuicao

            elif(self.instructions_list[i][0].token) == "<se>":
                self.gen_if(self.instructions_list[i], file)

            elif(self.instructions_list[i][0].token) == "<laco>" or self.instructions_list[i][0].token == "<fecha_chaves>":
                self.gen_while(self.instructions_list[i], file)
            
            elif(self.instructions_list[i][0].token) == "<variavel>": #chamada procedure
                self.gen_call_proc(self.instructions_list[i], file)

            elif(self.instructions_list[i][0].token) == "<declaracao_funcao>":
                self.gen_func(self.instructions_list[i], file)
            
            elif(self.instructions_list[i][0].token) == "<end_func>":
                print("end_func")
                file.write("end_func" + "\n")

            elif(self.instructions_list[i][0].token == "<declaracao_procedimento>"):
                self.gen_proc(self.instructions_list[i], file)

            elif(self.instructions_list[i][0].token) == "<end_proc>":
                print("end_proc")
                file.write("end_proc" + "\n")

            elif(self.instructions_list[i][0].token) == "<retorno>":
                print("{0} {1}".format(self.instructions_list[i][0].lexer, self.instructions_list[i][1].lexer))
                file.write("{0} {1}".format(self.instructions_list[i][0].lexer, self.instructions_list[i][1].lexer) + "\n")

            elif(self.instructions_list[i][0].token) == "<imprime>":
                 a = print("print({0})".format(self.instructions_list[i][2].lexer))
                 file.write("print({0})".format(self.instructions_list[i][2].lexer) + "\n")
        
        file.close()

    def gen_if(self, instruction, file):
        if(instruction[0].lexer == "if"):
            listAux = []

            for item in instruction:
                if item.lexer not in ["if","(",")"]:
                    listAux.append(item)

            #self.gen_attr(listAux, arq)

            self.labels += 1
            print("ifFalse",end=" ")
            file.write("ifFalse ")

            for item in listAux:
                print(item.lexer, end="")
                file.write(item.lexer + "")

            if len(self.lastLabelWhile) != 0:
                self.labels += 1 
            print(" goto: L{0}".format(self.labels))
            file.write(" goto: L{0}".format(self.labels) + "\n")
            
            self.labelsElse.append(self.labels)

        else:
            pop = self.labelsElse.pop()
            print("L{0}:".format(pop))
            file.write("L{0}:".format(pop) + "\n")
            #print("else")

    def gen_while(self, instruction, file):
        if(instruction[0].lexer == "while"):
            listAux = []
            for item in instruction:
                if item.lexer not in ["while","(",")"]:
                    listAux.append(item)


            self.labels += 1
            #self.lastLabelWhile = self.labels
            self.lastLabelWhile.append(self.labels)
            print("L{0}:".format(self.labels))
            file.write("L{0}:".format(self.labels) + "\n")
            
            #self.gen_attr(listAux, arq)
            print("whileFalse",end=" ")
            file.write("whileFalse ")
            for item in listAux:
                print(item.lexer, end="")
                file.write(item.lexer + "")

            print(" goto: L{0}".format(self.labels + 1))
            file.write(" goto: L{0}".format(self.labels + 1) + "\n")

            #self.labelsElse.append(self.labels)
        else:
            pop = self.lastLabelWhile.pop()
            file.write("goto: L{0}".format(pop) + "\n")
            file.write("L{0}:".format(pop + 1) + "\n")
            print("goto: L{0}".format(pop))
            print("L{0}:".format(pop + 1))

    def gen_attr(self, instruction, file):
        if(len(instruction) == 3):
            for item in instruction:
                print(item.lexer,end=" ")
                file.write(item.lexer + " ")
            print("")
            file.write("\n")
        else:
            if(instruction[3].token == "<abre_parenteses>"): #chamada de funcao
                contParam = 0
                i = 4
                if len(instruction) > 5:
                    while(instruction[i + 1].token != "<fecha_parenteses>"):
                        i += 1
                    while(instruction[i].token != "<abre_parenteses>"):
                        if instruction[i].lexer != ",":
                            print("_param = {0} ".format(instruction[i].lexer))
                            file.write("_param = {0} ".format(instruction[i].lexer) + "\n")
                            contParam += 1
                        i -= 1
                
                print("{0} = call {1},{2}".format(instruction[0].lexer, instruction[2].lexer, contParam))
                file.write("{0} = call {1},{2}".format(instruction[0].lexer, instruction[2].lexer, contParam) + "\n")

            else:
                print("_t0 = {0} {1} {2}".format(instruction[2].lexer, instruction[3].lexer, instruction[4].lexer))
                file.write("_t0 = {0} {1} {2}".format(instruction[2].lexer, instruction[3].lexer, instruction[4].lexer) + "\n")
                previous = 0
                i = 5
                while(i < len(instruction)):
                    print("_t{0} = _t{1} {2} {3}".format(previous + 1,previous,instruction[i].lexer,instruction[i+1].lexer))
                    file.write("_t{0} = _t{1} {2} {3}".format(previous + 1,previous,instruction[i].lexer,instruction[i+1].lexer) + "\n")

                    previous += 1

                    i += 2
            
                print("{0} = _t{1}".format(instruction[0].lexer,previous))
                file.write("{0} = _t{1}".format(instruction[0].lexer,previous) + "\n")

    def gen_call_proc(self, instruction, file):

        contParam = 0
        i = 2
        if len(instruction) > 3:
            while(instruction[i + 1].token != "<fecha_parenteses>"):
                i += 1
            while(instruction[i].token != "<abre_parenteses>"):
                if instruction[i].lexer != ",":
                    print("_param = {0} ".format(instruction[i].lexer))
                    file.write("_param = {0} ".format(instruction[i].lexer) + "\n")
                    contParam += 1
                i -= 1
        
        print("call {0},{1}".format(instruction[0].lexer, contParam))
        file.write("call {0},{1}".format(instruction[0].lexer, contParam) + "\n")

    def gen_func(self, instruction, file):
        print("func {0}:\nbegin_func:".format(instruction[1].lexer))
        file.write("func {0}:\nbegin_func:".format(instruction[1].lexer) + "\n")
        

    def gen_proc(self, instruction, file):  
        print("proc {0}:\nbegin_proc:".format(instruction[1].lexer))
        file.write("proc {0}:\nbegin_proc:".format(instruction[1].lexer) + "\n")