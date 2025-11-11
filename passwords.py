

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
    