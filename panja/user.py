from passlib.hash import pbkdf2_sha256 as sha

from panja import common


class User():
    
    def __init__(self, name, nick, email, password, online_acess=False):
        self.name = name
        self.nick = nick
        self.email = email
        self.password = sha.hash(password)
        self.online_acess = online_acess
        common.users.append(self)

    def authenticate(self, password):
        return sha.verify(password, self.password)