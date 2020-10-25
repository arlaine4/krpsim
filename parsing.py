import sys

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
    i = raw.find('(')
    j = raw.find(')')
    needed = raw[i+1:j]
    needed = create_furniture_list(needed)
    next = raw[j+1::]
    i = next.find('(')
    j = next.find(')')
    result = next[i+1:j]
    result = create_furniture_list(result)
    return [name, needed, result, int(cycle.replace('\n', ''))]

def init_stocks(ressource):
	"""Parsing du fichier source et initialisation des stocks"""
	stock = {}
	process = []
	optimize = {}
	with open(ressource, 'r') as file:
		tmp = file.readline()
		while tmp:
			pars = tmp.split(':') if tmp[0] != '#' else ''
			if (len(pars) == 2) and pars[0] != 'optimize':
				pars[1] = pars[1].replace('\n', '')
				stock[pars[0]] = int(pars[1])
			elif (len(pars) > 2):
				process.append(parse_process(pars[0], tmp, pars[-1]))
			tmp = file.readline()
			if "optimize:" in tmp and tmp[0] != '#':
				#Faire une boucle si jamais on doit optimize plusieurs elems
				index = tmp.find(':')
				optimize[tmp[0:index]] = tmp[index::].replace('\n', '')
				optimize["optimize"] = optimize["optimize"].replace('(', '')
				optimize["optimize"] = optimize["optimize"].replace(')', '')
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
