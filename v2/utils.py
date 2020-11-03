import argparse

def	parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('file', action='store', type=str, help='path to the configuration file.')
	parser.add_argument('time', action='store', type=int, help='delay allowed.')
	options = parser.parse_args()
	return options
