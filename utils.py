import parsing as p
import argparse
import time

def create_log(main_walk, stocks, process, file_name):
    fd = open(file_name + '.txt', 'w+')
    fd.write('main_walk :\n\n')
    for epoch in main_walk:
        fd.write(str(epoch) + '\n')
    fd.write("\nstocks:\n\n")
    for epoch in stocks:
        fd.write(str(epoch) + ' : ' + str(stocks[epoch]) + '\n')

def get_args_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='configuration file')
    parser.add_argument('time', type=int, help='delay')
    options = parser.parse_args()
    return options

def print_pre_infos(stocks, process, optimize):
    len_stocks = p.get_stock_process(stocks, process)
    print("\n- \033[4mFile informations\033[0m :\n")
    print("\n\033[38;5;204m#\033[0m",end='')
    for k in range(10):
        for i in range(196, 201):
            print("\033[38;5;{}m-\033[0m".format(i), end='')
            for j in range(201, 196):
                print("\033[38;5;{}m-\033[0m".format(j), end='')
    print("\033[38;5;204m#\033[0m",end='')
    print("\n")
    print("{} \033[1mprocesses\033[0m / {} \033[1mstocks\033[0m / {} to \033[1moptimize\033[0m.".format(len(process), len_stocks, len(optimize)))
    print("\n\033[38;5;204m#\033[0m",end='')
    for k in range(10):
        for i in range(196, 201):
            print("\033[38;5;{}m-\033[0m".format(i), end='')
            for j in range(201, 196):
                print("\033[38;5;{}m-\033[0m".format(j), end='')
    print("\033[38;5;204m#\033[0m",end='')
    print("\n")
    print("- \033[4mStocks\033[0m :\n")
    for tmp in stocks:
        print("\033[0;49m{}\033[0m : \033[1;49;32m{}\033[0m".format(tmp, stocks[tmp]))
    print("\n\033[38;5;204m#\033[0m",end='')
    for k in range(10):
        for i in range(196, 201):
            print("\033[38;5;{}m-\033[0m".format(i), end='')
            for j in range(201, 196):
                print("\033[38;5;{}m-\033[0m".format(j), end='')
    print("\033[38;5;204m#\033[0m",end='')
    print("\n")
    print("- \033[4mProcesses\033[0m :\n")
    for tmp in process:
        print("\033[1m{}\033[0m : {} : {} : {}".format(tmp[0], tmp[1], tmp[2], tmp[3]))
    print("\n\033[38;5;204m#\033[0m",end='')
    for k in range(10):
        for i in range(196, 201):
            print("\033[38;5;{}m-\033[0m".format(i), end='')
            for j in range(201, 196):
                print("\033[38;5;{}m-\033[0m".format(j), end='')
    print("\033[38;5;204m#\033[0m",end='')
    print("\n")
    print("- \033[4mTo optimize\033[0m :\n")
    for tmp in optimize:
        print("\033[1m{}\033[0m".format(tmp))
    print("\n\033[38;5;204m#\033[0m",end='')
    for k in range(10):
        for i in range(196, 201):
            print("\033[38;5;{}m-\033[0m".format(i), end='')
            for j in range(201, 196):
                print("\033[38;5;{}m-\033[0m".format(j), end='')
    print("\033[38;5;204m#\033[0m")
    print("\n")
    print("- \033[4mMain walk\033[0m :\n")
    
