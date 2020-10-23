import sys
import parsing

class   Process():
    def __init__(self):
        self.list_process = [] #liste de liste avec dans chaque sous liste un name et needs_qty et result_qty
        # needs_qty liste de dico, pareil pour result_qty

class   Stock():
    def __init__(self):
        self.list_stocks = [] #liste de liste avec nom du stock et qty + mettre a jour a chque action de process

    def init_stocks(self, ressource):
        self.set_list_stocks(ressource)

#-------------------------------------------------------------------------
# Getteurs et setteurs

    def set_list_stocks(self, ressource):
        self.list_stocks = parsing.init_stocks(ressource)

    def get_list_stocks(self):
        return self.list_stocks

#
#-------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Wrong number of arguments.")
        sys.exit()
    stocks = Stock()
    stocks.init_stocks(sys.argv[1])
