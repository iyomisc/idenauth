import sqlite3
import uuid
import time
import datetime
from idena_auth.config import CONFIG
import urllib.request
from json import loads as json_loads


class Requests:
    create_tables = ("CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY, address TEXT DEFAULT '', authenticated BOOL DEFAULT 0, status TEXT DEFAULT '')", )

    add_new_token = "REPLACE INTO sessions(token) VALUES(?)"
    remove_token = "DELETE FROM sessions WHERE token=?"
    
    link_address = "UPDATE sessions SET address=? WHERE token=?"
    get_address = "SELECT address FROM sessions WHERE token=?"
    set_auth = "UPDATE sessions SET authenticated=? WHERE token=?"
    is_auth = "SELECT sum(authenticated) FROM sessions WHERE token=?"
    is_address_auth = "SELECT sum(authenticated) FROM sessions WHERE address=?"
    
    get_token_status = "SELECT status FROM sessions WHERE token=? AND authenticated=1"
    get_address_status = "SELECT status FROM sessions WHERE address=?"
    set_address_status = "UPDATE sessions SET status=? WHERE address=?"
    get_all_status = "SELECT token, address, status FROM sessions WHERE authenticated=1"
    
    is_registered = "SELECT COUNT(*) FROM sessions WHERE token=?"


class AuthDb:
    def __init__(self):
        self.db = sqlite3.connect(CONFIG["db_path"], check_same_thread=False)
        cursor = self.db.cursor()
        for table in Requests.create_tables:
            cursor.execute(table)
        self.db.commit()

    def get_address_status(self, address):
        cursor = self.db.cursor()
        cursor.execute(Requests.get_address_status, (address,))
        result = cursor.fetchall()
        if len(result) and len(result[0]):
            return result[0][0]
        return ""
    
    def get_token_status(self, token):
        cursor = self.db.cursor()
        cursor.execute(Requests.get_token_status, (token,))
        result = cursor.fetchall()
        if len(result) and len(result[0]):
            return result[0][0]
        return None

    def new_token(self, token=None):
        if not token:
            token = uuid.uuid4().hex

        cursor = self.db.cursor()
        cursor.execute(Requests.add_new_token, (token, ))
        self.db.commit()

        return token

    def link_address(self, token, address):
        cursor = self.db.cursor()
        cursor.execute(Requests.link_address, (address, token))
        self.db.commit()

    def get_address(self, token):
        cursor = self.db.cursor()
        cursor.execute(Requests.get_address, (token, ))
        result = cursor.fetchall()
        if len(result) and len(result[0]):
            return result[0][0]
        return ""

    def auth(self, token, authenticated=True):
        cursor = self.db.cursor()
        cursor.execute(Requests.set_auth, (authenticated, token))
        self.db.commit()
        return authenticated

    def set_address_status(self, address, status=""):
        cursor = self.db.cursor()
        cursor.execute(Requests.set_address_status, (status, address))
        self.db.commit()
        return True
    
    def get_all_status(self):
        cursor = self.db.cursor()
        cursor.execute(Requests.get_all_status)
        result = cursor.fetchall()
        return result
        
    def is_token_registered(self, token):
        cursor = self.db.cursor()
        cursor.execute(Requests.is_registered, (token,))
        result = cursor.fetchall()

        return result[0][0]
        
    def is_token_auth(self, token):
        cursor = self.db.cursor()
        cursor.execute(Requests.is_auth, (token,))
        result = cursor.fetchall()

        return result[0][0]
        
    def is_address_auth(self, address):
        cursor = self.db.cursor()
        cursor.execute(Requests.is_address_auth, (address,))
        result = cursor.fetchall()

        return result[0][0]
    
    def remove_token(self, token):
        cursor = self.db.cursor()
        cursor.execute(Requests.remove_token, (token, ))
        self.db.commit()
        return True
    
    def stop(self):
        self.db.close()


if __name__ == '__main__':
    print("I'm a module, I can't run!")
