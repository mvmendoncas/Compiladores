def get_type(variable, simbols_table):
    if variable.lexer in simbols_table:
        if(simbols_table[variable.lexer].line <= variable.line):
            return simbols_table[variable.lexer].type
        else:
            return False
    return False


def verify_attribution(token_list, simbols_table, look_ahead):

    declared_type = get_type(token_list[look_ahead - 1], simbols_table)

    if(declared_type):
        if(declared_type == "int"):
            received_type = get_type(token_list[look_ahead + 1], simbols_table)
            if(received_type):
                if(received_type == "int"):
                    aux_look_ahead = look_ahead + 2
                    if(token_list[aux_look_ahead].token == "<operador_aritmetico>"):
                        while(token_list[aux_look_ahead - 2].token != "<fim_comando>"):
                            if token_list[aux_look_ahead].token == "<operador_aritmetico>":
                                if(get_type(token_list[aux_look_ahead + 1], simbols_table) == "int"):
                                    #return True
                                    pass
                                elif(token_list[aux_look_ahead + 1].token == "<numero>"):
                                    #return True
                                    pass
                                else:
                                    print('\033[91m' + "Semantic error in line {0}, arithmetic with wrong values".format(token_list[look_ahead].line) + '\033[0m') #DETALHAR ERRO
                                    return False
                            aux_look_ahead += 2

                        return True
                    else:
                        return True
                elif(received_type == "func"):
                    if(verify_parameters(token_list, simbols_table, look_ahead + 1)): ################ aquiiiiiiiiiiiiiiiiiiiiiiiiiiiii
                        return True
                    else:
                        return False
                else:
                    print('\033[91m' + "Semantic error in line {0}, type error".format(token_list[look_ahead].line) + '\033[0m') #DETALHAR ERRO
                    return False
            elif(token_list[look_ahead + 1].token == "<numero>"):
                aux_look_ahead = look_ahead + 2
                if(token_list[aux_look_ahead].token == "<operador_aritmetico>"):
                    while(token_list[aux_look_ahead - 2].token != "<fim_comando>"):
                        if token_list[aux_look_ahead].token == "<operador_aritmetico>":
                            if(get_type(token_list[aux_look_ahead + 1], simbols_table) == "int"):
                                #return True
                                pass
                            elif(token_list[aux_look_ahead + 1].token == "<numero>"):
                                #return True
                                pass
                            else:
                                print('\033[91m' + "Semantic error in line {0}, arithmetic with wrong values".format(token_list[look_ahead].line) + '\033[0m') #DETALHAR ERRO
                                return False
                        aux_look_ahead += 2
                return True
            elif not received_type:
                print('\033[91m' + "Semantic error in line {0}, variabel {1} undeclared".format(token_list[look_ahead - 1].line, token_list[look_ahead - 1].lexer) + '\033[0m') #DETALHAR ERRO
                return False
            else:
                print('\033[91m' + "Semantic error in line {0}, type error".format(token_list[look_ahead - 1].line) + '\033[0m') #DETALHAR ERRO
                return False
        elif(declared_type == "bool"):
            received_type = get_type(token_list[look_ahead + 1], simbols_table)
            if(received_type):
                if(received_type == "bool"):
                    return True
                elif received_type == "func":
                    if(verify_parameters(token_list, simbols_table, look_ahead + 1)):
                        return True
                    else:
                        return False
                else:
                    print('\033[91m' + "Semantic error in line {0}, Incompatible types, expected {1} but receive {2}".format(token_list[look_ahead - 1].line, declared_type, received_type) + '\033[0m') #DETALHAR ERRO
                    return False
            elif(token_list[look_ahead + 1].token == "<palavraBooleana>"):
                return True
            else:
                print('\033[91m' + "Semantic error in line {0}, type error".format(token_list[look_ahead].line) + '\033[0m') #DETALHAR ERRO
                return False
    else:
        print('\033[91m' + "Semantic error in line {0}, variabel {1} undeclared".format(token_list[look_ahead].line, token_list[look_ahead - 1].lexer) + '\033[0m') #DETALHAR ERRO
        return False

def verify_int(token_list, simbols_table, look_ahead):
    last_value = get_type(token_list[look_ahead], simbols_table)
    if(last_value == "int"):
        return True
    elif(token_list[look_ahead].token == "<numero>"):
        return True
    elif(not last_value): ## olhar depois se está correto
        return True
    else:
        print('\033[91m' + "Semantic error line: {0}, expected int but receive boolean".format(token_list[look_ahead].line) + '\033[0m')
        return False
    
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
                            print('\033[91m' + "Semantic error line: {0}, only boolean operations for two cases".format(token_list[look_ahead - 2].line) + '\033[0m')
                            return False
                #return True
        elif(first_value == "bool" and second_value == "bool"):
            if(token_list[look_ahead + 1].lexer == "!=" or token_list[look_ahead + 1].lexer == "=="):
                return True
            else:
                print('\033[91m' + "Semantic error line: {0}, It is not possible to perform arithmetic operations on boolean values".format(token_list[look_ahead - 2].line) + '\033[0m')
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
                                print('\033[91m' + "Semantic error line: {0}, only boolean operations for two cases".format(token_list[look_ahead].line) + '\033[0m')
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
                    print('\033[91m' + "Semantic error line: {0}, It is not possible to perform arithmetic operations on boolean values".format(token_list[look_ahead - 2].line) + '\033[0m')
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
                                print('\033[91m' + "Semantic error line: {0}, only boolean operations for two cases".format(token_list[look_ahead - 2].line) + '\033[0m')
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
        print('\033[91m' + "Semantic error line: {0}, uninitialized variable".format(token_list[look_ahead - 2].linha) + '\033[0m')
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
            #if(lista_tokens[look_ahead_aux].nome == "<numerico>" and tabela_simbolos[lista_tokens[look_ahead].lexema].listParam[i] == "int"):
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