import os
from pathvalidate import validate_filename, is_valid_filename

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
    def createVault(self):
        f = open(self.location)
        

    def __init__(self, location):
        if is_valid_filename(location) and not os.path.exists(location):
            self.location = location
            Vault.createVault()
        else:
            raise ValueError("Error: file path/name is invalid or exists.")
        
