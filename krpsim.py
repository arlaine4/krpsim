import sys
import parsing
import algo

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong number of arguments.")
        sys.exit()
    stock_lst, process_lst, optimize = parsing.init_stocks(sys.argv[1])
    algo.start_opti_process(stock_lst, process_lst, optimize, sys.argv[2])
