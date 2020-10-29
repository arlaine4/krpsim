import sys
import parsing
import time
import utils

def start_opti_process(stocks, process, optimize, delay, file_name):
    opti_needs, id_opti = parsing.get_optimize_req(optimize, process)
    prio_process = parsing.get_prio_process(opti_needs, process, optimize)

"""def start_opti_process(stocks, process, optimize, delay, file_name):
    try:
        delay = int(delay)
    except:
        print("Error in delay parameter, please enter a correct input.")
        sys.exit(0)

def check_process_callable(process, stocks):
    ""Check si on peut appeller le process suivant ou si les stocks ne le permettent pas""
    requirements = process[1]
    list_elems = []
    for elem in requirements: #get dico keys from requirements
        list_elems.append(elem)
    for tmp in list_elems: #check if keys exist in stocks
        if tmp not in stocks:
            return False
        elif tmp in stocks:
            if stocks[tmp] < requirements[tmp]:
                return False
    return True

def call_process(main_walk, stocks, process, id_p, timer):
	""Appel des process et update des stocks, de l'id du process,
	du timer et de la main_walk""
	#UPDATE LA MAIN WALK
	#print("process in call process  : ",process[id_p])
	requirements = process[id_p][1]
	results = process[id_p][2]
	time = process[id_p][3]
	list_requirements = []
	for name in requirements: #recup cle dico
		list_requirements.append(name)
	for n in list_requirements: #maj des stocks
		stocks[n] -= requirements[n]
	if results is not None:
		for tmp in results: #ajout results and stocks ou maj si le nom du result exist deja
			if tmp in stocks:
				stocks[tmp] += results[tmp]
			else:
				stocks[tmp] = results[tmp]
	main_walk.append([timer, process[id_p][0]])
	if id_p + 1 < len(process): #check si on passe au process suivant ou si on revient au debut
		id_p += 1
	else:
		id_p = 0
	return main_walk, stocks, id_p, timer + time

def check_optimize_in_dico(optimize, elem):
    lst_optimize = []
    for i in range(len(optimize)):
        lst_optimize.append(optimize[i])
    j = 0
    for name in lst_optimize:
        if name in elem:
            return True
    return False

def get_optimize_req(optimize, process):
    req = []
    id_p = 0
    i = 0
    for elem in process:
        if elem[2]:
            bool_ = check_optimize_in_dico(optimize, elem[2])
            if bool_:
                req = elem[2]
                id_p = i
                return req, id_p
            else:
                pass
        i += 1

    ""#-------------------------------------------------
    #Do a function for this
    for elem in main_walk:
        print("{}:{}".format(elem[0], elem[1]))
    print("\n- \033[4mStocks\033[0m :\n")
    for elem in stocks:
        print("  {} => {}".format(elem, stocks[elem]))
    print()
    #-------------------------------------------------"""
