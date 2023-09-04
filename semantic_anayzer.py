#Essa função verifica se o simbolo do token está na tabela de simbolos e retorna o tipo do simbolo
def get_type(variable, simbols_table):
    if variable.lexer in simbols_table:
        if(simbols_table[variable.lexer].line <= variable.line):
            return simbols_table[variable.lexer].type
        else:
            return False
    return False

#Essa função recebe uma lista de tokens e a tabela de simbolos, a função verifica se a atribuição de valores entre variáveis está correta
def verify_attribution(lista_tokens, tabela_simbolos, look_ahead):

    tipo_declarada = get_type(lista_tokens[look_ahead - 1], tabela_simbolos)

    if(tipo_declarada):
        if(tipo_declarada == "int"):
            tipo_recebida = get_type(lista_tokens[look_ahead + 1], tabela_simbolos)

            if(tipo_recebida):
                if(tipo_recebida == "int"):
                    aux_look_ahead = look_ahead + 2
                    if(lista_tokens[aux_look_ahead].token == "<operador_aritmetico>"):
                        while(lista_tokens[aux_look_ahead - 2].token != "<fim_comando>"):
                            if lista_tokens[aux_look_ahead].token == "<operador_aritmetico>":
                                if(get_type(lista_tokens[aux_look_ahead + 1], tabela_simbolos) == "int"):
                                    pass
                                elif(lista_tokens[aux_look_ahead + 1].token == "<numero>"):
                                    pass
                                else:
                                    print('\033[91m' + "Semantic error in line {0}, arithmetic with wrong values".format(lista_tokens[look_ahead].line) + '\033[0m') #DETALHAR ERRO
                                    return False
                            aux_look_ahead += 2

                        return True
                    else:
                        return True
                elif(tipo_recebida == "func"):
                    
                    if(verify_parameters(lista_tokens, tabela_simbolos, look_ahead + 1)): 
                        return True
                    else:
                        return False
                else:
                    print('\033[91m' + "Semantic error in line {0}, type error".format(lista_tokens[look_ahead].line) + '\033[0m') 
                    return False
            elif(lista_tokens[look_ahead + 1].token == "<numero>"):
                aux_look_ahead = look_ahead + 2
                if(lista_tokens[aux_look_ahead].token == "<operador_aritmetico>"):
                    while(lista_tokens[aux_look_ahead - 2].token != "<fim_comando>"):
                        if lista_tokens[aux_look_ahead].token == "<operador_aritmetico>":
                            if(get_type(lista_tokens[aux_look_ahead + 1], tabela_simbolos) == "int"):                            
                                pass
                            elif(lista_tokens[aux_look_ahead + 1].token == "<numero>"):
                                pass
                            else:
                                print('\033[91m' + "Semantic error in line {0}, arithmetic with wrong values".format(lista_tokens[look_ahead].line) + '\033[0m') #DETALHAR ERRO
                                return False
                        aux_look_ahead += 2
                return True
            elif not tipo_recebida:
                print('\033[91m' + "Semantic error in line {0}, variabel {1} undeclared".format(lista_tokens[look_ahead - 1].line, lista_tokens[look_ahead - 1].lexer) + '\033[0m') #DETALHAR ERRO
                return False
            else:
                print('\033[91m' + "Semantic error in line {0}, type error".format(lista_tokens[look_ahead - 1].line) + '\033[0m') 
                return False
        elif(tipo_declarada == "bool"):
            tipo_recebida = get_type(lista_tokens[look_ahead + 1], tabela_simbolos)
            if(tipo_recebida):
                if(tipo_recebida == "bool"):
                    return True
                elif tipo_recebida == "func":
                    if(verify_parameters(lista_tokens, tabela_simbolos, look_ahead + 1)):
                        return True
                    else:
                        return False
                else:
                    print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(lista_tokens[look_ahead - 1].line, tipo_declarada, tipo_recebida) + '\033[0m') 
                    return False
            elif(lista_tokens[look_ahead + 1].token == "<operador_booleano>"):
                return True
            else:
                print('\033[91m' + "Semantic error in line {0}, type error".format(lista_tokens[look_ahead].line) + '\033[0m') 
                return False
        elif(tipo_declarada == "const"):
            if(lista_tokens[look_ahead + 1].token == "<numero>"):
                return True
            elif(lista_tokens[look_ahead + 1].token == "<operador_booleano>"):
                return True
            else:
                print('\033[91m' + "Semantic error in line {0}, wrong way to declare constant".format(lista_tokens[look_ahead - 2].line) + '\033[0m') 
                return False
    else:
        print('\033[91m' + "Semantic error in line {0}, variabel {1} undeclared".format(lista_tokens[look_ahead].line, lista_tokens[look_ahead - 1].lexer) + '\033[0m') 
        return False

#Essa função verifica se o token atual ou a variável a direita do token atual é um número ou do tipo int
def verify_int(token_list, simbols_table, look_ahead):
    last_value = get_type(token_list[look_ahead], simbols_table)
    if(last_value == "int"):
        return True
    elif(token_list[look_ahead].token == "<numero>"):
        return True
    elif(not last_value): 
        return True
    else:
        print('\033[91m' + "Semantic error line: {0}, expected int but receive bool".format(token_list[look_ahead].line) + '\033[0m')
        return False
#Verifica a correção semântica das expressões, incluindo operações aritméticas e relacionais 
def verify_expressions(token_list, simbols_table, look_ahead):
    first_value = get_type(token_list[look_ahead], simbols_table)
    second_value = get_type(token_list[look_ahead + 2], simbols_table)

    if first_value and second_value:
        if(first_value == "int" and second_value == "int"):
            if(token_list[look_ahead + 3].token == "<operador_relacional>"):
                if(verify_int(token_list, simbols_table, look_ahead + 4)):
                    
                    return True

            else:
                if(token_list[look_ahead + 1].token != "<operador_relacional>" and token_list[look_ahead + 3].token != "<fecha_parenteses>"):
                        if(verify_int(token_list, simbols_table, look_ahead + 4)):
                            return True
                else:
                    if(token_list[look_ahead + 3].token == "<fecha_parenteses>"):
                        if(token_list[look_ahead + 1].token == "<operador_relacional>"):
                            return True
                        else:
                            print('\033[91m' + "Semantic error line: {0}, only bool operations for two cases".format(token_list[look_ahead - 2].line) + '\033[0m')
                            return False
                #return True
        elif(first_value == "bool" and second_value == "bool"):
            if(token_list[look_ahead + 1].lexer == "!=" or token_list[look_ahead + 1].lexer == "=="):
                return True
            else:
                print('\033[91m' + "Semantic error line: {0}, It is not possible to perform arithmetic operations on bool values".format(token_list[look_ahead - 2].line) + '\033[0m')
                return False
        else:
            print('\033[91m' + "Semantic error line: {0}, Incompatible types, expected {1} but receive {2}".format(token_list[look_ahead - 1].line, first_value, second_value) + '\033[0m')
            return False
    elif(token_list[look_ahead].token == "<numero>" and token_list[look_ahead + 2].token == "<numero>"):
        if(verify_int(token_list, simbols_table, look_ahead + 4)):
            return True

    elif(not first_value or not second_value):
        if(first_value):
            if(first_value == "int"):
                if(token_list[look_ahead + 2].token == "<numero>"):
                    if(token_list[look_ahead + 1].token != "<operador_relacional>" and token_list[look_ahead + 3].token != "<fecha_parenteses>"):
                        if(verify_int(token_list, simbols_table, look_ahead + 4)):
                            return True
                    else:
                        if(token_list[look_ahead + 3].token == "<fecha_parenteses>"):
                            if(token_list[look_ahead + 1].token == "<operador_relacional>"):
                                return True
                            else:
                                print('\033[91m' + "Semantic error line: {0}, only bool operations for two cases".format(token_list[look_ahead].line) + '\033[0m')
                                return False



                else:
                    print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(token_list[look_ahead - 2].line) + '\033[0m')
                    return False
            elif(first_value == "bool"):
                if(token_list[look_ahead + 1].lexer == "!=" or token_list[look_ahead + 1].lexer == "=="):
                    if(token_list[look_ahead + 2].token == "<operador_booleano>"):
                        return True                    
                    else:
                        print('\033[91m' + "Semantic error line: {0}, Incompatible types, expected {1} but receive {2}".format(token_list[look_ahead - 1].line, first_value, token_list[look_ahead + 2].token) + '\033[0m')
                        return False
                else:
                    print('\033[91m' + "Semantic error line: {0}, It is not possible to perform arithmetic operations on bool values".format(token_list[look_ahead - 2].line) + '\033[0m')
                    return False
            else:
                print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(token_list[look_ahead - 2].line) + '\033[0m')
                return False
        elif(second_value):
            if(second_value == "int"):
                if(token_list[look_ahead].token == "<numero>"):

                    if(token_list[look_ahead + 1].token != "<operador_relacional>" and token_list[look_ahead + 3].token != "<fecha_parenteses>"):
                        if(verify_int(token_list, simbols_table, look_ahead + 4)):
                            return True
                    else:
                        if(token_list[look_ahead + 3].token == "<fecha_parenteses>"):
                            if(token_list[look_ahead + 1].token == "<operador_relacional>"):
                                return True
                            else:
                                print('\033[91m' + "Semantic error line: {0}, only bool operations for two cases".format(token_list[look_ahead - 2].line) + '\033[0m')
                                return False
                else:
                    print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(token_list[look_ahead - 2].line) + '\033[0m')
                    return False

            else:
                print('\033[91m' + "Semantic error line: {0}, Incompatible types of result".format(token_list[look_ahead - 2].line) + '\033[0m')
                return False
        else:
            pass


#procedimento 
def verify_procedure(token_list, table_simbols, look_ahead):
    while(token_list[look_ahead].token != "<fecha_chaves>"):
        if(token_list[look_ahead].token == "<retorno>"):
            print('\033[91m' + "Semantic error line: {0}, procedure must have no return".format(token_list[look_ahead - 2].line) + '\033[0m')
            return False
        look_ahead += 1
    return True

#return
def verify_variable_return(token_list, table_simbols, look_ahead):
    if(get_type(token_list[look_ahead], table_simbols)):
        return True
    else:
        print('\033[91m' + "Semantic error line: {0}, uninitialized variable".format(token_list[look_ahead - 2].line) + '\033[0m')
        return False
    
def verify_parameters(token_list, table_simbols, look_ahead):
    params_amount = table_simbols[token_list[look_ahead].lexer].parameters_amount
    declared_amount = 0
    look_ahead_aux = (look_ahead + 2)
    cont = look_ahead_aux
    i = 0

    while(token_list[cont].token != "<fecha_parenteses>"):
        if(token_list[cont].token != "<virgula>"):
            declared_amount += 1
        cont += 1


    while(token_list[look_ahead_aux].token != "<fecha_parenteses>" and i < params_amount ):
        if(token_list[look_ahead_aux].token != "<virgula>"):
            #if(lista_tokens[look_ahead_aux].token == "<numero>" and tabela_simbolos[lista_tokens[look_ahead].lexer].listParam[i] == "int"):
            if(table_simbols[token_list[look_ahead].lexer].parameters_list[i] == "int"):
                if(token_list[look_ahead_aux].token == "<numero>"):
                    pass
                elif(token_list[look_ahead_aux].token == "<variavel>"):
                    if(get_type(token_list[look_ahead_aux], table_simbols) == "int"):
                        pass
                    else:
                        print('\033[91m' + "Semantic error line: {0}, variable {1} has a different declaration".format(token_list[look_ahead - 2].line, token_list[look_ahead_aux].lexer) + '\033[0m')
                        return False    
                else:
                    print('\033[91m' + "Semantic error line: {0}, parameter {1} declared wrong".format(token_list[look_ahead - 2].line, token_list[look_ahead_aux].lexer) + '\033[0m')
                    return False
            elif(table_simbols[token_list[look_ahead].lexer].parameters_list[i] == "bool"):
                if(token_list[look_ahead_aux].token == "<operador_relacional>"):
                    pass
                elif(token_list[look_ahead_aux].token == "<variavel>"):
                    if(get_type(token_list[look_ahead_aux], table_simbols) == "bool"):
                        pass
                    else:
                        print('\033[91m' + "Semantic error line: {0}, variable {1} has a different declaration".format(token_list[look_ahead - 2].line, token_list[look_ahead_aux].lexer) + '\033[0m')
                        return False
                else:
                    print('\033[91m' + "Semantic error line: {0}, parameter {1} declared wrong".format(token_list[look_ahead - 2].line, token_list[look_ahead_aux].lexer) + '\033[0m')
                    return False
            i += 1
        look_ahead_aux += 1
    
    if(declared_amount == params_amount):
        return True
    else:
        print('\033[91m' + "Semantic error line: {0}, the functions need {1} parameters".format(token_list[look_ahead - 2].line, params_amount) + '\033[0m')
        return False