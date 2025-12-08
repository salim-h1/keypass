import os
import json
from pathvalidate import validate_filename, is_valid_filename
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64


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
    
    # these two methods are for serialization/deserialization of Accounts
    def to_dict(self):
        return {
            "service": self.service,
            "username": self.username,
            "password": self.password,
        }
    @staticmethod
    def from_dict(data):
        return Account(
            data["service"],
            data["username"],
            data["password"]
        )

class Vault:

    def encrypt_vault(self):
        """
        Helper function to encrypt the vault

        returns True if successful
        """

        key_bytes = self.key.encode()

        # generate a random salt (store it for decryption)
        salt = os.urandom(16)

        # derive a key from the password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(key_bytes))

        cipher = Fernet(key)

        with open(self.location, "rb") as f:
            data = f.read()

        encrypted_data = cipher.encrypt(data)

        with open(self.location, "wb") as f:
            f.write(salt + encrypted_data)

        print(f"{self.location} has been successfully encrypted!")
        return True



    def decrypt_vault(self):
        """
        Helper function to decrypt the vault

        returns True if successful
        """

        key_bytes = key.encode()

        with open(self.location, "rb") as f:
            file_data = f.read()

        # extract salt (16 bytes)
        salt = file_data[:16]
        encrypted_data = file_data[16:]

        # derive the key using the same salt
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(key_bytes))

        cipher = Fernet(key)
        decrypted_data = cipher.decrypt(encrypted_data)

        with open(self.location, "wb") as f:
            f.write(decrypted_data)

        print(f"{self.location} has been successfully decrypted.")
        return True


    def __init__(self, location, key):
        """
        Create new vault object
        """
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

        # encrypt the file
        try:
            self.encrypt_vault()
        except Exception as e:
            print(e)

        
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
        new_account = Account(service, username, password)

        try:
            self.decrypt_vault()
        except Exception as e:
            print(e)

        # if vault is empty, write current data to vault as JSON, encrypt the vault, then return
        if os.path.getsize(self.location) == 0:
            with open(self.location, "w") as f:
                json.dump(new_account.to_dict(), f, indent=4)
            try:
                self.encrypt_vault()
            except Exception as e:
                print(e)
            return

        # if the vault is not empty, get all current data, append our new account to the dict, and then rewrite it to the vault
        with open(self.location, "r") as f:
            data = json.load(f)
        accounts = [Account.from_dict(acc) for acc in data]
        accounts.append(new_account)

        # save accounts to file
        data = [acc.to_dict() for acc in accounts]
        with open(self.location, "w") as f:
            json.dump(data, f, indent=4)
        
        # encrypt the file again
        try:
            self.encrypt_vault()
        except Exception as e:
            print(e)
        return



        
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