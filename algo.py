import sys
import parsing
import time
import utils

def	start_opti_process(stocks, process, optimize, delay):
	try:
		delay = int(delay)
	except:
		print("Error in delay parameter, please enter a correct input.")
		sys.exit(0)
	len_pro = utils.get_len_process(process)
	print("Before optimization content :")
	print("File is \033[32mvalid\033[0m, {} stocks, {} processes and {} to optimize" \
		.format(len(stocks), len_pro, len(optimize)))
	main_walk, stocks, timer = optimize_processes(stocks, process, optimize, delay)
	utils.print_final_result(main_walk, stocks, timer)

def	check_process_callable(process, stocks):
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
	#print("require : ",requirements)
	#print("stocks : ",stocks)
	return True

def	call_process(main_walk, stocks, process, id_p, timer):
	print("process in call process  : ",process[id_p])
	requirements = process[id_p][1]
	results = process[id_p][2]
	time = process[id_p][3]
	list_requirements = []
	for name in requirements:
		list_requirements.append(name)
	for n in list_requirements:
		stocks[n] -= requirements[n]
	for tmp in results:
		stocks[tmp] = results[tmp]
	if id_p + 1 < len(process):
		id_p += 1
	else:
		id_p = 0
	return main_walk, stocks, id_p, timer + time

def	optimize_processes(stocks, process, optimize, delay):
	main_walk = [] #liste de delay a l'arrivee au process et le nom du process
	#return stocks actualisees et la main_walk + une variable delay que on actualise
	# de 1 a chaque tour de boucle et de + delay du process si on l'active
	timer = 0
	id_p = 0
	continue_ = True
	while timer < delay and continue_:
		if check_process_callable(process[id_p], stocks):
			main_walk, stocks, id_p, timer = call_process(main_walk, stocks, process, id_p, timer)
			print("stock after call process : ", stocks)
		else:
			break
		timer += 1
		if check_process_callable(process[id_p], stocks):
			continue_ = True
		else:
			continue_ = False
		timer += 1
	return main_walk, stocks, timer
