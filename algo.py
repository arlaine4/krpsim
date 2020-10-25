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

def	optimize_processes(stocks, process, optimize, delay):
	main_walk = [] #liste de delay a l'arrivee au process et le nom du process
	#return stocks actualisees et la main_walk + une variable delay que on actualise
	# de 1 a chaque tour de boucle et de + delay du process si on l'active
	timer = 0
	return main_walk, stocks, timer
