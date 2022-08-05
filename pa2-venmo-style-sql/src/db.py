import os
import sqlite3

# From: https://goo.gl/YzypOI
def singleton(cls):
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


class DatabaseDriver(object):
    """
    Database driver for the transaction app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Initializes database connection and create SQL table.
        """
        self.conn = sqlite3.connect("venmo.db", check_same_thread = False)
        self.create_users_table()
    
    def create_users_table(self):
        """
        Using SQL, creates a user database that tracks id, name, username, and
        balance.
        """
        try:
            self.conn.execute(
                """
                CREATE TABLE users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    username TEXT NOT NULL,
                    balance INTEGER NOT NULL
                );
                """
            )
        except Exception as e:
            print(e)
        
    def delete_users_table(self):
        """
        Using SQL, delete entire table
        """
        self.conn.execute("DROP TABLE IF EXISTS users;")

    def select_users(self):
        """
        Using SQL, return a list with dictionary of each user's id, name and
        username.
        """
        cursor = self.conn.execute("SELECT * FROM users")
        users = []
        for row in cursor:
            users.append({"id": row[0], "name": row[1], "username": row[2]})
        return users
    
    def insert_user(self, name, username, balance):
        """
        Using SQL, insert new user into the table 

        Parameter name, username, balance are parameter that accepts the 
        user's information.
        """
        cursor = self.conn.execute(
            """
            INSERT INTO users (name, username, balance) 
            VALUES (?, ?, ?);
            """, (name, username, balance))
        # commit the sql insertion
        self.conn.commit()
        # return last inserted row
        return cursor.lastrowid
    
    def select_user_id(self, id):
        """
        Using SQL, return list containing information about user of specified id

        Parameter id refers to user's id. 
        Precondition id should exist in users table. 
        """
        cursor = self.conn.execute("SELECT * FROM users WHERE id = ?;", (id,))
        user = []
        for row in cursor:
            user.append({"id": row[0], "name": row[1], "username": row[2], "balance": row[3]})
        return user
    
    def delete_user(self, id):
        """
        Using SQL, delete user with specified id
        """
        self.conn.execute("DELETE FROM users WHERE id = ?;", (id,))
        self.conn.commit()

    def update_bal(self, id, new_bal):
        """
        Using SQL, update the specified user's balance with the new balance

        Parameter id refers to user's id. 
        Precondition id should exist in users table. 

        Parameter new_bal refers to the new updated balance of user.
        """
        self.conn.execute("UPDATE users SET balance = ? WHERE id = ?;", (new_bal, id))
        self.conn.commit()