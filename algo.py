import sys
import parsing
import time
import utils

def start_opti_process(stocks, process, optimize, delay):
    try:
        delay = int(delay)
    except:
        print("Error in delay parameter, please enter a correct input.")
        sys.exit(0)
    #print("Before optimization content :")
    #print("File is \033[32mvalid\033[0m, {} stocks, {} processes and {} to optimize" \
	#.format(len(stocks), len_pro, len(optimize)))
    utils.print_pre_infos(stocks, process, optimize)
    #main_walk, stocks, timer = optimize_processes(stocks, process, optimize, delay)

def check_process_callable(process, stocks):
    """Check si on peut appeller le process suivant ou si les stocks ne le permettent pas"""
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

def call_process(main_walk, stocks, process, id_p):
    """Appel des process et update des stocks, de l'id du process,
    du timer et de la main_walk"""
    #UPDATE LA MAIN WALK
    #print("process in call process  : ",process[id_p])
    requirements = process[id_p][1]
    results = process[id_p][2]
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
    if id_p + 1 < len(process): #check si on passe au process suivant ou si on revient au debut
        id_p += 1
    else:
        id_p = 0
    return main_walk, stocks, id_p,

def optimize_processes(stocks, process, optimize, delay):
    start_time = time.time()
    main_walk = [] #liste de delay a l'arrivee au process et le nom du process
    #return stocks actualisees et la main_walk + une variable delay que on actualise
    # de 1 a chaque tour de boucle et de + delay du process si on l'active
    #boucler tant que les process le permettent si le time n'est pas fourni ???
    timer = 0
    id_p = 0
    continue_ = True
    while round(time.time() - start_time, 2) < delay:
        if check_process_callable(process[id_p], stocks):
            main_walk, stocks, id_p = call_process(main_walk, stocks, process, id_p)
            #print("stock after call process : ", stocks)
        elif not check_process_callable(process[id_p], stocks):
            break
        if id_p == len(process):
            id_p = 0
        elif id_p + 1 < len(process) and not check_process_callable(process[id_p], stocks):
            id_p += 1
    return main_walk, stocks, timer
