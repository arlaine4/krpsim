import sys
import re
from copy import deepcopy

def check_optimize_in_dico(optimize, elem):
    lst_optimize = []
    for i in range(len(optimize)):
        lst_optimize.append(optimize[i])
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
                req = elem[1]
                id_p = i
                return req, id_p
        else:
            pass
        i += 1
    return None, -1

def bubble_sort_process(process, opti_needs):
    tmp_lst = []
    nb = 20000
    for elem in process:
        if len(elem[1]) < nb:
            nb = len(elem[1])
    for elem in process:
        if len(elem[1]) == nb:
            tmp_lst.append(elem)
    if len(tmp_lst) > 1:
        i = 0
        index_prio = 0
        tmp_sum = sum(tmp_lst[0][1].values())
        while i < len(tmp_lst):
            if sum(tmp_lst[i][1].values()) < tmp_sum:
                index_prio = i
                tmp_sum = sum(tmp_lst[i][1].values())
            i += 1
        return tmp_lst[index_prio]
    if tmp_lst[0]:
        return tmp_lst[0]
    else:
        return None

def get_prio_process(process, optimize):
    tmp_opt = optimize
    opti_needs = []
    prio_process = []
    i = 0
    while i < 10:
        opti_needs, id_opti = get_optimize_req(tmp_opt, process)
        if id_opti != -1 and process[id_opti] not in prio_process:
            prio_process.append(process[id_opti])
        if not opti_needs:
            break
        tmp_opt = list(opti_needs.keys())
        # print(tmp_opt)
        # print(process[id_opti])
        i += 1
    for elem in prio_process:
        print(elem)
    return prio_process

def get_stock_process(stocks, process):
    visited = []
    count = len(stocks)
    for key in stocks:
        visited.append(key)
    for i in range(len(process)):
        if process[i][2] != None:
            for key in process[i][2]:
                if key not in visited:
                    visited.append(key)
                    count += 1
    return count

def create_furniture_list(raw):
    list_s = {}
    if ';' in raw:
        first = raw.split(';')
        for elem in first:
            pars = elem.split(':')
            pars[1] = pars[1].replace('\n', '')
            list_s[pars[0]] = int(pars[1])
    else:
        pars = raw.split(':')
        pars[1] = pars[1].replace('\n', '')
        list_s[pars[0]] = int(pars[1])
    return list_s

def parse_process(name, raw, cycle):
    needed = None
    result = None
    i = raw.find('(')
    j = raw.find(')')
    if raw[i] == '(' and raw[j] == ')':
        needed = raw[i + 1:j]
        needed = create_furniture_list(needed)
    next = raw[j + 1::]
    i = next.find('(')
    j = next.find(')')
    if next[i] == '(' and next[j] == ')':
        result = next[i + 1:j]
        result = create_furniture_list(result)
    return [name, needed, result, int(cycle.replace('\n', ''))]

def get_optimized(optimize, str):
    tmp = str.split(';')
    for elem in tmp:
        optimize.append(re.sub('[^a-zA-Z_]', '', elem))
    return optimize

def init_stocks(ressource):
    """Parsing du fichier source et initialisation des stocks"""
    stock = {}
    process = []
    optimize = []
    try :
        test = open(ressource, 'r')
        test.close()
    except:
        print("Please give a valid file")
        exit(1)
    with open(ressource, 'r') as file:
        tmp = file.readline()
        while tmp:
            pars = tmp.split(':') if tmp[0] != '#' else ''
            if (len(pars) == 2) and pars[0] != 'optimize':
                pars[1] = pars[1].replace('\n', '')
                stock[pars[0]] = int(pars[1])
            elif (len(pars) > 2):
                process.append(parse_process(pars[0], tmp, pars[-1]))
            if len(pars) >= 2 and pars[0] == 'optimize':
                optimize = get_optimized(optimize, pars[1])
            tmp = file.readline()
    if not optimize:
        print("Optimize info missing, stopping now.")
        sys.exit()
    if len(stock) == 0:
        print("There is no stock available, stopping now.")
        sys.exit()
    if len(process) == 0:
        print("There is no process to optimize, stopping now.")
        sys.exit()
    return stock, process, optimize
