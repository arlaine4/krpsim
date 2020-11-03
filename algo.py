import sys
import parsing
import time
import utils

def start_opti_process(stocks, process, optimize, delay, file_name):
	if optimize == "time" or optimize == "":
		prio_process = process
	else:
		prio_process = parsing.get_prio_process(process, optimize)
	try:
		delay = int(delay)
	except:
		print("Error in delay parameter, please enter a correct input.")
		sys.exit(0)
	optimize_call_processes(stocks, process, prio_process, optimize, delay)

def	optimize_call_processes(stocks, process, prio_process, optimize, delay):
	start_time = time.time()
	main_walk = []
	id_p = 0
	timer = 0
	print(prio_process)
	"""while round(time.time() - start_time, 2) < delay:
		print("id : ", id_p)
		if check_process_callable(prio_process[id_p], stocks):
			main_walk, stocks, timer = call_process(main_walk, stocks, prio_process, id_p, timer)
			print("process_call : ", process[id_p])
			id_p = refresh_id_p(id_p, prio_process, stocks)
		else:
			id_p = refresh_id_p(id_p, prio_process, stocks)
		if id_p == -1:
			print(main_walk)
			print("Optimization is over, stopping now.")
			sys.exit(0)
		print("stocks : ", stocks)"""
	#req, id_opti = parsing.get_optimize_req(optimize, process)
	#prio_process = [process[id_opti] + prio_process] # ??
	"""while round(time.time() - start_time, 2) < delay:
		print("id_p : ", id_p)
		id_p = refresh_id_p(id_p, prio_process, stocks)
		#check si on peut appeler un autre process dans la liste des prio_process
		#a partir de id_p
		if id_p == -1:
			print("Optimization over, stopping now.")
			sys.exit(0)
		main_walk, stocks, timer = call_process(main_walk, stocks, prio_process, id_p, timer)
		print(stocks)"""

def	refresh_id_p(id_p, prio_process, stocks):
	#list_req = []
	#for i in range(id_p, len(prio_process)):
		#if prio_process[i][2]:
			#list_req.append(prio_process[i][2])
	if check_process_callable(prio_process[0], stocks):
		return 0
	else:
		if id_p + 1 < len(prio_process):
			if check_process_callable(prio_process[id_p + 1], stocks):
				return id_p + 1
			else:
				while id_p < len(prio_process):
					if check_process_callable(prio_process[id_p], stocks):
						return id_p
					else:
						id_p += 1
		return id_p
	"""if check_process_callable(prio_process[id_p], stocks):
		return id_p
	else:
		print(prio_process)
		while id_p < len(prio_process):
			if id_p + 1 < len(prio_process):
				id_p += 1
			if check_process_callable(prio_process[id_p], stocks):
				return id_p
	return -1"""

def	get_process_to_call(stocks, prio_process, id_p):
	i = id_p
	while i < len(prio_process):
		if check_process_callable(prio_process[i], stocks):
			return i
		i += 1
	if id_p + 1 < len(prio_process):
		return id_p + 1
	else:
		return 0

def check_process_callable(process, stocks):
	#Check si on peut appeller le process suivant ou si les stocks ne le permettent pas
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
			elif stocks[tmp] >= requirements[tmp]:
				return True
	return False

def	call_process(main_walk, stocks, process, id_p, timer):
	requirements = process[id_p][1]
	results = process[id_p][2]
	time = process[id_p][3]
	list_requirements = []
	print("process in call process  : ",process[id_p])
	for name in requirements: #get keys in dico
		list_requirements.append(name)
	for n in list_requirements: #maj des stocks
		if stocks[n] - requirements[n] >= 0:
			stocks[n] -= requirements[n]
	if results is not None:
		for tmp in results:
			if tmp in stocks:
				stocks[tmp] += results[tmp]
			else:
				stocks[tmp] = results[tmp]
	main_walk.append([timer, process[id_p][0]])
	return main_walk, stocks, timer + time

"""def call_process(main_walk, stocks, process, id_p, timer):
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
