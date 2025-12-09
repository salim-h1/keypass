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

    # if user chose to add a password, ask for Vault and decryption key
    if userargs.mode == "add":

        fname = input("enter the vault name > ")
        key = input("enter your vault master key > ")

        try:
            vault = Vault(fname, key)
        except Exception as e:
            print(e)
            sys.exit(-1)
        
        if not vault.is_vault():
            print("Vault is invalid! Please check your key or filename.")
            sys.exit(-1)
        
        service = input("enter the service name > ")
        username = input("enter the associated username > ")
        password = input("enter the associated password > ")

        vault.add_account(service, username, password)
        print("Your account has been added!")
    
    # if user chooses to list account data, do the following
    if userargs.mode == "list":

        fname = input("enter the vault name > ")
        key = input("enter your vault master key > ")

        try:
            vault = Vault(fname, key)
        except Exception as e:
            print(e)
            sys.exit(-1)

        if not vault.is_vault():
            print("Vault is invalid! Please check your key or filename.")
            sys.exit(-1)
        
        vault.list_accounts()
        print("Done!")
    
    # if user chooses to search, do the following
    if userargs.mode == "search":

        fname = input("enter the vault name > ")
        key = input("enter your vault master key > ")

        try:
            vault = Vault(fname, key)
        except Exception as e:
            print(e)
            sys.exit(-1)

        if not vault.is_vault():
            print("Vault is invalid! Please check your key or filename.")
            sys.exit(-1)

        query = input("enter your search query (account/username) > ")
        vault.search_accounts(query)

        print("Done!")
    
    # if user chose to delete, do the following
    if userargs.mode == "del":

        fname = input("enter the vault name > ")
        key = input("enter your vault master key > ")

        try:
            vault = Vault(fname, key)
        except Exception as e:
            print(e)
            sys.exit(-1)

        if not vault.is_vault():
            print("Vault is invalid! Please check your key or filename.")
            sys.exit(-1)

        # ask for username and service in case of multiple entries
        # if there are duplicates, they will be deleted together
        service = input("enter the account service to delete > ")
        username = input("enter the account username to delete > ")
        vault.delete_account(service, username)

        print("Done!")




        


