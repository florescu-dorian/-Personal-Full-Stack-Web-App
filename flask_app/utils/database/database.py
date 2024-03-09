import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['users', 'nft']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        ''' FILL ME IN WITH CODE THAT CREATES YOUR DATABASE TABLES.'''

        #should be in order or creation - this matters if you are using forign keys.
         
        if purge:
            for table in self.tables[::-1]:
                self.query(f"""DROP TABLE IF EXISTS {table}""")
            
        # Execute all SQL queries in the /database/create_tables directory.
        for table in self.tables:
            
            #Create each table using the .sql file in /database/create_tables directory.
            with open(data_path + f"create_tables/{table}.sql") as read_file:
                create_statement = read_file.read()
            self.query(create_statement)

            # Import the initial data
            try:
                params = []
                with open(data_path + f"initial_data/{table}.csv") as read_file:
                    scsv = read_file.read()            
                for row in csv.reader(StringIO(scsv), delimiter=','):
                    params.append(row)
            
                # Insert the data
                cols = params[0]; params = params[1:] 
                self.insertRows(table = table,  columns = cols, parameters = params)
            except:
                print('no initial data')

    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        
        # Check if there are multiple rows present in the parameters
        has_multiple_rows = any(isinstance(el, list) for el in parameters)
        keys, values      = ','.join(columns), ','.join(['%s' for x in columns])
        
        # Construct the query we will execute to insert the row(s)
        query = f"""INSERT IGNORE INTO {table} ({keys}) VALUES """
        if has_multiple_rows:
            for p in parameters:
                query += f"""({values}),"""
            query     = query[:-1] 
            parameters = list(itertools.chain(*parameters))
        else:
            query += f"""({values}) """                      
        
        insert_id = self.query(query,parameters)[0]['LAST_INSERT_ID()']         
        return insert_id


        # Return the formatted date string in mm/yy format
    def date(self, date, end=False):
        if end and date is None:
            return "Present"
        return date.strftime("%B %Y") if date else ""


    def getResumeData(self):
        resume_data = {}
        # get all institutions and positions, experience and skills into a single query
        inst_pos_rows = self.query("SELECT * FROM institutions i JOIN positions p ON i.inst_id = p.inst_id")
        exp_skill_rows = self.query("SELECT * FROM experiences e JOIN skills s ON e.experience_id = s.experience_id")
        for row in inst_pos_rows:
            inst_id = row['inst_id']
            # if an inst does not exist create one
            if inst_id not in resume_data:
                resume_data[inst_id] = {
                    'address': row['address'],
                    'city': row['city'],
                    'state': row['state'],
                    'type': row['type'],
                    'zip': row['zip'],
                    'department': row['department'],
                    'name': row['name'],
                    'positions': {},
                }
            pos_id = row['position_id']
            # if a pos does not exist create one
            if pos_id not in resume_data[inst_id]['positions']:
                resume_data[inst_id]['positions'][pos_id] = {
                    'end_date': self.date(row['end_date'], True),
                    'start_date': self.date(row['start_date']),
                    'responsibilities': row['responsibilities'],
                    'title': row['title'],
                    'experiences': {},
                }
            exp_id = None
            # match the experience with the current pos
            for exp_row in exp_skill_rows:
                if exp_row['position_id'] == pos_id:
                    if exp_id != exp_row['experience_id']:
                        exp_id = exp_row['experience_id']
                        # create a new experience if it doesn't exist
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id] = {
                            'name': exp_row['name'],
                            'description': exp_row['description'],
                            'end_date': self.date(exp_row['end_date'], True),
                            'start_date': self.date(exp_row['start_date']),
                            'hyperlink': exp_row['hyperlink'],
                            'skills': {},
                        }
                    skill_id = exp_row['skill_id']
                    # if a skill does not exists create one
                    if skill_id not in resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills']:
                        resume_data[inst_id]['positions'][pos_id]['experiences'][exp_id]['skills'][skill_id] = {
                            'name': exp_row['name'],
                            'skill_level': exp_row['skill_level'],
                        }
        return resume_data
#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    # def createUser(self, email='me@email.com', password='password', role='user'):
    #     return {'success': 1}

    # def authenticate(self, email='me@email.com', password='password'):
    #     return {'success': 1}

    

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message




    def createUser(self, email='me@email.com', password='password', role='user'):
        user_row = self.query("SELECT 1 FROM `users` WHERE email=%s", parameters=[email])
        if (user_row): # user exists already
            return {'success': 0}

        self.insertRows('users', ['role', 'email', 'password'], [[role, email, self.onewayEncrypt(password)]])
        return {'success': 1}

    def authenticate(self, email='me@email.com', password='password'):
        user_row = self.query("SELECT 1 FROM `users` WHERE email=%s AND password=%s", parameters=[email, self.onewayEncrypt(password)])
        if (user_row):
            return {'success': 1}

        return {'success': 0}
    

    
    def getUserIdfromEmail(self, email="me@gmail.com"):
        query = "SELECT user_id from users WHERE email = %s;"
        result = self.query(query, parameters=[email])
        return result[0]['user_id'] if result else None
    


    def getUserNFTs(self, userId):
        query = "SELECT nft_id, description, token, file_data FROM nft WHERE user_id = %s;"
        result = self.query(query, parameters=[userId])
        return [row for row in result]
    

    def getAllNFTs(self):
        query = "SELECT * from nft;"
        result = self.query(query)

        allNFTs = [{'nft_id': row['nft_id'],
                    'user_id': row['user_id'],
                    'description': row['description'],
                    'token': row['token'],
                    'file_data': row['file_data']}
                for row in result]

        return allNFTs
    


    def getUserTokens(self, userId):
        query = "SELECT tokens FROM users WHERE user_id = %s;"
        result = self.query(query, parameters=[userId])
        return result[0]['tokens'] if result else None
    

    def userMAFAMATICS(self, userId, nftId):
        query = "SELECT token FROM nft WHERE nft_id = %s;"
        result = self.query(query, parameters=[nftId])
        nft_val = result[0]['token'] if result else None
        user_val = self.getUserTokens(userId)
        return user_val - nft_val if nft_val and user_val else None
