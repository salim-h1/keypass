import sys
import argparse
import cryptography
from passwords import *


BANNER = '                                              \n\
        m    m               mmmmm                      \n\
        #  m"   mmm   m   m  #   "#  mmm    mmm    mmm  \n\
        #m#    #"  #  "m m"  #mmm#" "   #  #   "  #   " \n\
        #  #m  #""""   #m#   #      m"""#   """m   """m \n\
        #   "m "#mm"   "#    #      "mm"#  "mmm"  "mmm" \n\
                        m\'                             \n'

args = argparse.ArgumentParser(
    description="KeyPass Password Manager"
)
args.add_argument(
    "mode",
    choices=["init", "add", "list", "search", "del"],
    type=str,
    help="init/add/list/search/del :: create new vault, add new passwords, retrieve passwords, search passwords, or delete passwords"
)



if __name__ == "__main__":

    # print out a fancy banner
    print(BANNER)

    # get user supplied arguments
    userargs = args.parse_args()

    # if user chose to initialize a vault, create a new Vault instance
    if userargs.mode == "init":
        
        # get file name and key
        fname = input("choose your vault file name > ")
        key = input("choose a master password > ")
        
        try:
            vault = Vault(fname, key)
            vault.init_vault()
        except Exception as e:
            print(e)
            sys.exit(-1)
        
        print(f"\nVault has been created succesfully :: {vault.location}")
        print("Bye bye!")
        sys.exit(0)

    # if user chose to add a password, ask for Vault and decryption key
    if userargs.mode == "add":

        fname = input("enter the vault name > ")
        key = input("enter your vault master key > ")

        try:
            vault = Vault(fname, key)
        except Exception as e:
            print(e)
            sys.exit(-1)
        
        


