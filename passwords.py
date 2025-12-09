import os
import json
from pathvalidate import is_valid_filename
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
    
    # these next two methods are for serialization/deserialization of Accounts. this allows us to store them more easily.
    def to_dict(self):
        return {
            "service": self.service,
            "username": self.username,
            "password": self.password,
        }
    
    # this uses staticmethod because from_dict doesn't access object data
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

        return True



    def decrypt_vault(self):
        """
        Helper function to decrypt the vault

        returns True if successful
        """

        key_bytes = self.key.encode()

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
        try:
            root, ext = os.path.splitext(self.location)
            if ext != ".vault":
                return False
        except Exception as e:
            print(e)
            raise ValueError("Error: Vault file is invalid.")

        # check if the vault can be decrypted
        try:
            self.decrypt_vault()
        except:
            return False
        
        return True



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
                json.dump([new_account.to_dict()], f, indent=4)
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


        
    def list_accounts(self):
        """
        List all created accounts in the vault
        
        """

        try:
            self.decrypt_vault()
        except Exception as e:
            print(e)

        if os.path.getsize(self.location) == 0:
            print("Vault is empty.")
            self.encrypt_vault()
            return

        # open file and get all account data
        with open(self.location, "r") as f:
            data = json.load(f)
        accounts = [Account.from_dict(acc) for acc in data]

        if not accounts:
            print("No accounts stored.")
            return

        # print account data 
        for acc in accounts:
            print(f"Service: {acc.service}, Username: {acc.username}, Password: {acc.password}")

        # re-encrypt after reading
        try:
            self.encrypt_vault()
        except Exception as e:
            print(e)


    def search_accounts(self, query: str):
        """
        Search for a specific account in the vault

        prints the account entry matching the search query
        """

        query = query.lower()

        # the usual error-handling
        try:
            self.decrypt_vault()
        except Exception as e:
            print(e)

        if os.path.getsize(self.location) == 0:
            print("Vault is empty.")
            self.encrypt_vault()
            return

        # open file and get all account data
        with open(self.location, "r") as f:
            data = json.load(f)
        accounts = [Account.from_dict(acc) for acc in data]

        # find matches
        matches = [
            acc for acc in accounts
            if query in acc.service.lower() or query in acc.username.lower()
        ]

        if not matches:
            print("No matching accounts found.\n")
            self.encrypt_vault()
            return

        for acc in matches:
            print(f"Service: {acc.service}\nUsername: {acc.username}\n")

        # re-ecnrypt
        try:
            self.encrypt_vault()
        except Exception as e:
            print(e)


    def delete_account(self, service: str, username: str):
        """
        Delete a specified account from the vault
        """

        service = service.lower()
        username = username.lower()

        try:
            self.decrypt_vault()
        except Exception as e:
            print(e)

        if os.path.getsize(self.location) == 0:
            print("Vault is empty.")
            self.encrypt_vault()
            return

        with open(self.location, "r") as f:
            data = json.load(f)
        accounts = [Account.from_dict(acc) for acc in data]

        # filter out any matching entries
        new = [
            acc for acc in accounts
            if not (acc.service.lower() == service and acc.username.lower() == username)
        ]

        # check to see if anything was removed
        if len(new) == len(accounts):
            print("No matching account found.")
            self.encrypt_vault()
            return

        # write the updated list back to file
        data = [acc.to_dict() for acc in new]
        with open(self.location, "w") as f:
            json.dump(data, f, indent=4)

        print("Account successfully removed.\n")

        # encrypt the file once again
        try:
            self.encrypt_vault()
        except Exception as e:
            print(e)
        