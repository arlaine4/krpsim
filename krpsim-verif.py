import sys
import argparse

def get_verif_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', type=str, help='configuration file to compare to log')
    parser.add_argument('log_file', type=str, help='log file')
    options = parser.parse_args()
    return options

def get_log_file(log_file_name):
    """try:
        fd = open(log_file_name, 'r+')
    except:
        print("log file does not exist, please run krpsim with {} first.".format(log_file_name[0:len(log_file_name) - 4]))
    return fd"""

if __name__ == "__main__":
    options = get_verif_args()
    #log_file = get_log_file(options.log_file)
