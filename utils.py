import parsing as p


def print_pre_infos(stocks, process, optimize):
    len_stocks = p.get_stock_process(stocks, process)
    print("\n- File informations :\n")
    print("#-------------------------------------------#")
    print("{} \033[1mprocesses\033[0m / {} \033[1mstocks\033[0m / {} to \033[1moptimize\033[0m.".format(len(process), len_stocks, len(optimize)))
    print("#-------------------------------------------#\n")
    print("- Stocks :\n")
    # for tmp in stocks:
        # print()
    print(stocks)

