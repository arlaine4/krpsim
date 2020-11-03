import utils
import parsing

if __name__ == "__main__":
	options = utils.parse_args()
	stocks, list_instances, optimize = parsing.init_instances_processes(options.file)
	print(stocks, '\n')
	print(list_instances, '\n')
	print(optimize)
