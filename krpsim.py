import sys
import parsing
import algo
import utils

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong number of arguments.")
        sys.exit()
    options = utils.get_args_argparse()
    stock_lst, process_lst, optimize = parsing.init_stocks(options.file)
    algo.start_opti_process(stock_lst, process_lst, optimize, options.time, options.file)
