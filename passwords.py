import os
import json
from pathvalidate import validate_filename, is_valid_filename


# file extension for vault files
VAULT_EXTENSION = ".vault"


class Account:
    def __init__(self, service, username, password):
        self.service = service
        self.username = username
        self.password = password
    
    def get_account(self):
        return (self.service, self.username, self.password)
    def get_service(self):
        return self.service
    def get_username(self):
        return self.username
    def get_password(self):
        return self.password

class Vault:

    def encrypt_vault(key):
        """
        Helper function to encrypt the vault

        returns True if successful, False if not successful
        """
        pass

    def decrypt_vault(key):
        """
        Helper function to decrypt the vault

        returns a handle to the open file if successful, will throw an exception if not successful
        """
        pass

    def __init__(self, location, key):
        """
        Create new vault object
        """
        
        # trust user input for now, check when class methods are called
        self.location = str(location)
        self.key = str(key)



    def init_vault(self):
        """
        Initialize a new password vault

        location: vault file location
        key: master key for file encryption
        """

        # check if the location is a valid file name, and it does not exist
        if not is_valid_filename(self.location) or os.path.exists(self.location):
            raise ValueError("Error: file path/name is invalid or exists.")

        # remove file extension and add our own extension
        root, _ = os.path.splitext(self.location)
        self.location = root + VAULT_EXTENSION

        # create vault file
        f = open(self.location, 'x')

        # get master key and encrypt the file
        # TODO
        
    def is_vault(self) -> bool:
        """
        Helper function to check if a vault is valid
        
        """

        # check file extension

        # validate JSON data


    def add_account(self, service: str, username: str, password: str):
        """
        Add an account to Vault

        service: website/service name
        username: website/service account username
        password: website/service account password
        """

        # create Account object to hold our data
        self.account = Account(service, username, password)

        # if vault is empty, write current data to vault as JSON and return

        # if vault is full, check for repeated entries

        # if no entries, write new account data to vault and close

        
    def list_accounts():
        """
        List all created accounts in the vault
        
        """
        
        # open the vault and extract the data as a JSON object

        # parse JSON and output in proper formatting

        pass


    def search_accounts(self, service=None, username=None, password=None):
        """
        Search for a specific account in the vault

        returns the account entry matching the search query
        """

        # check search parameters
        if service is None and username is None and password is None:
            raise ValueError("Error: No search parameters passed")

        # open the vault and extract JSON data

        # parse JSON and return specified search query

        return True

    def delete_accounts():
        """
        Delete a specified account from the vault

        returns True if deletion was successful, and False if otherwise
        """

        # open the vault and extract data as JSON

        # warn user if account has more than one password entry

        # remove specified account from JSON

        # write new data to the vault and close

        pass