import os
import sqlite3

class DatabaseDriver(object):
    """
    Database driver for the Venmo (Full) app.
    Handles with reading and writing data with the database.
    """

    def __init__(self):
        """
        Initializes database connection, create SQL table and set to instance
        variable 'conn'
        """
        self.conn = sqlite3.connect("venmo.db", check_same_thread = False)
        # self.delete_users_table()
        # self.delete_txns_table()
        self.create_users_table()
        self.create_txns_table()
    
    # -- USERS -----------------------------------------------------------

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
        user_txns = self.select_txn_by_user(id)
        for row in cursor:
            user.append({"id": row[0], "name": row[1], "username": row[2], "balance": row[3], "transactions": user_txns})
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
    
    #-- TRANSACTIONS --------------------------------------------------------

    def create_txns_table(self):
        """
        Using SQL, create txns relational table to track transactions between different users.
        Sender_id and reciever_id refers to user's id from users table. 
        """
        try:
            cursor = self.conn.execute(
                """
                CREATE TABLE txns (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL, 
                    sender_id INTEGER SECONDARY KEY NOT NULL,
                    receiver_id INTEGER SECONDARY KEY NOT NULL,
                    amount INTEGER NOT NULL,
                    message TEXT NOT NULL,
                    accepted BOOL
                )
                """
            )
        except Exception as e:
            print(e)
    
    def delete_txns_table(self):
        """
        Using SQL, delete txns table
        """
        self.conn.execute("DROP TABLE IF EXISTS txns;")

    def insert_txn(self, timestamp, sender_id, receiver_id, amount, message, accepted):
        """
        Using SQL, create a new transaction within txns table given parameters. Returns the id 
        of the last generated (newest) transaction. 
        """
        cursor = self.conn.execute(
            """
            INSERT INTO txns (timestamp, sender_id, receiver_id, amount, message, accepted)
            VALUES (?, ?, ?, ?, ?, ?);
            """, (timestamp, sender_id, receiver_id, amount, message, accepted)
        )
        self.conn.commit()
        return cursor.lastrowid

    def select_txn_by_user(self, user_id):
        """
        Using SQL, returns a list of dictionaries of all of the user's transaction given
        user's id. 
        """
        cursor = self.conn.execute(
            """
            SELECT * FROM txns
            WHERE sender_id = ? 
            OR receiver_id = ?;
            """, (user_id, user_id)
        )
        txns = []
        for row in cursor:
            txns.append({ 
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": bool(row[6])
                })
        return txns        
    
    def select_txn_by_id(self, txn_id):
        """
        Using SQL, return a list of dictionary of details on one transaction given 
        transaction id.
        """
        cursor = self.conn.execute("SELECT * FROM txns WHERE id = ?;", (txn_id,))
        txn = []
        for row in cursor:
            txn.append({ 
                "id": row[0],
                "timestamp": row[1],
                "sender_id": row[2],
                "receiver_id": row[3],
                "amount": row[4],
                "message": row[5],
                "accepted": bool(row[6])
                })
        return txn