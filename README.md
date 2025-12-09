# KeyPass Password Manager
```text
                                                 
 m    m               mmmmm                      
 #  m"   mmm   m   m  #   "#  mmm    mmm    mmm  
 #m#    #"  #  "m m"  #mmm#" "   #  #   "  #   " 
 #  #m  #""""   #m#   #      m"""#   """m   """m 
 #   "m "#mm"   "#    #      "mm"#  "mmm"  "mmm" 
                 m'                              
```

### (Not to be confused with KeePass)

This is my submission for COMP-10247 final assignment.

The goal is to write an example password manager that allows a user to create encrypted "vaults" holding encrypted login information. A user will be able to easily create, retrieve, and update their saved passwords via a command line interface. This program allows you to create multiple vaults at once, and only requires the .vault file along with the master key to manage a vault.

I used the cryptography library to manage the encryption and decryption of the file. An **Account** class manages the individual account data, and provides a few helper functions. The **Vault** class does most of the work, implementing all of the necessary functionality. The **keypass.py** file contains the main logic of the program, and the class definitions are in the **passwords.py** file.

## Requirements:

- Store, retrieve, and manage passwords encrypted in a local file that requires a master password to unlock.  
- Options: add, list, search, delete entries.  Could optionally integrate cryptography or keyring.


## Usage:

> python keypass.py [option]
> 
> usage: keypass.py [-h] {init,add,list,search,del}


To create a vault, use the **init** option. You will be prompted to include a vault name and a master key that will be used in authentication.

To add an account to the vault, use the **add** option. Specify the vault name (including the extension) and your key, and you will be able to add a service, username, and password. You are able to add multiple accounts of the same service to a vault. *Note: Accounts with the same service and username (duplicates) can be added, but will also be deleted together!*

To list entries, use the **list** option. Specifying a valid vault and key will list all accounts in the vault.

To search for an account, use the **account** option. Specify a valid vault and key along with a query will search the vault for a match. Any account with a matching *service* or *username* will be listed.

To delete an account from the vault, use the **del** option. This will prompt you for a service and username, and will delete any matching entries.

