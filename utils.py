import parsing as p

def get_stock_process(process):
    len_ = 0
    for elem in process:
        len_ += 1
    return len_

def print_pre_infos(stocks, process, optimize):
    len_stocks = get_len_all_stocks(process) + len(stocks)
    print("\n- File informations :\n")
    print("#-------------------------------------------#")
    print("{} \033[1mprocesses\033[0m / {} \033[1mstocks\033[0m / {} to \033[1moptimize\033[0m.".format(p.get_stock_process(process), len_stocks, len(optimize)))
    print("#-------------------------------------------#\n")
    print("- Stocks :\n")
    for tmp in stocks:
        print(tmp)
    print(stocks)

