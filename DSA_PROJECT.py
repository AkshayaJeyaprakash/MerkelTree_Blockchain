#!/usr/bin/env python
# coding: utf-8

# In[1]:


import hashlib
from datetime import datetime
import re
from typing import List
import typing
import itertools
from tqdm import tqdm
import mysql.connector
from PIL import Image
from tabulate import tabulate
import json


# In[2]:


def check_space(string):
    flag = False
    for i in (string):
        if i.isspace():
            flag = True
    return flag


# In[3]:


def new_login():
    username = input("USERNAME: ").lower()
    if check_space(username):
        print("USERNAME MUST NOT HAVE ANY SPACES")
        return new_login()
    password = input("PASSWORD: ").lower()
    mydb = mysql.connector.connect(host = "b3p5jdtawewglsidbrcd-mysql.services.clever-cloud.com",
                               user = "ufsqzaamugycov4i",
                               passwd = "m91jSulGNAK8WjDAY6HC",
                               database = "b3p5jdtawewglsidbrcd")
    mycurzor = mydb.cursor()
    mycurzor.execute("SELECT * FROM ADMIN")
    myresult = mycurzor.fetchall()
    list_users = []
    list_password = []
    for x in myresult:
        list_users.append(x[0])
        list_password.append(x[1])
    if list_users.count(username)!=0:
        print("USERNAME ALREADY EXISTS !!! TRY AGAIN\n")
        return new_login()
    elif list_password.count(password)!=0:
        print("PASSWORD ALREADY EXISTS !!! TRY AGAIN\n")
        return new_login()
    else:
        sql = "INSERT INTO ADMIN (username, password) VALUES (%s,%s)"
        val = (username,password)
        mycurzor.execute(sql, val)
        mydb.commit()
    mydb2 = mysql.connector.connect(host = "bui9n0ezfg4skkatjufr-mysql.services.clever-cloud.com",
                                    user = "ugczznfsxgqf2bpf",
                                    passwd = "aQY7gbVOr3pBGPT7BJVZ",
                                    database = "bui9n0ezfg4skkatjufr")
    mycurzor2 = mydb2.cursor()
    mycurzor2.execute("create table "+username+" (b_no int(3),transactions varchar(5000), hash varchar(70), prev_hash varchar(70), merkel_root varchar(70), nonce int(9),difficulty int(2), timestamp varchar(200))")
    return username


# In[4]:


def sign_in():
    username = input("USERNAME: ").lower()
    password = input("PASSWORD: ").lower()
    mydb = mysql.connector.connect(host = "b3p5jdtawewglsidbrcd-mysql.services.clever-cloud.com",
                               user = "ufsqzaamugycov4i",
                               passwd = "m91jSulGNAK8WjDAY6HC",
                               database = "b3p5jdtawewglsidbrcd")
    mycurzor = mydb.cursor()
    mycurzor.execute("SELECT * FROM ADMIN")
    myresult = mycurzor.fetchall()
    my = (username,password)
    flag=False
    for x in myresult:
        if my==x:
            flag=True
            break
    if flag == True:
        return username
    else:
        print("INVALID USER-ID & PASSWORD")
        return sign_in()


# In[5]:


def update_all(b_no, trans, hash1, p_hash, mer_root, nonce, diff, timestamp):
    mydb2 = mysql.connector.connect(host = "bui9n0ezfg4skkatjufr-mysql.services.clever-cloud.com",
                                    user = "ugczznfsxgqf2bpf",
                                    passwd = "aQY7gbVOr3pBGPT7BJVZ",
                                    database = "bui9n0ezfg4skkatjufr")
    mycurzor2 = mydb2.cursor()
    mycurzor2.execute("SHOW TABLES")
    list_table = []
    for x in mycurzor2:
        list_table.append(x[0])
    for i in list_table:
        sql = "INSERT INTO "+str(i)+" (b_no,transactions,hash,prev_hash,merkel_root,nonce,difficulty,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val1 = (b_no, trans, hash1, p_hash, mer_root, nonce, diff, timestamp)
        mycurzor2.execute(sql, val1)
        mydb2.commit()


# In[6]:


def hash_of_this(val):
    return hashlib.sha256(val.encode('utf-8')).hexdigest()


# In[7]:


def MerkleTree(txns):
    if (len(txns)==1):
        return hash_of_this(txns[0])
       
    if (len(txns)%2==1):
        txns.append(txns[-1])
    trans_hash = []
    for i in range(0,len(txns),2):
        data=hash_of_this(txns[i])+hash_of_this(txns[i+1])
        trans_hash.append((data))
    return MerkleTree(trans_hash)


# In[8]:


class transaction:
    
    def __init__(self,sender,receiver,amount):
        statement = "["+sender +" sent Rs."+ amount +" to "+ receiver+"]\n"
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.statement = statement
        
    def block_transaction(self):
        return self.trans
    
    def block_transaction(n):
        n = int(n)
        if n<10:
            transactions = []
            for i in range(n):
                print("*")
                print("TRANSACTION ",i+1)
                sender = input("Enter sender's name: ")
                receiver = input("Enter receiver's name: ")
                amount = input("Enter the amount involved in transaction: ")
                t = transaction(sender,receiver,amount)
                print("\033[1m",t.statement,"\033[0m")
                transactions.append(t.statement)
            return transactions
        else:
            print("These many transactions not permitted...\nThe maximum permitted transaction is 10")


# In[9]:


class block:
    
    def __init__(self,Transactions,Data,Previous_hash,nonce,difficulty,hash1,timestamp):
        self.transactions = Transactions
        self.timestamp  = timestamp
        self.data = Data
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = hash1
        self.previous_hash=Previous_hash
    
    def genesis(minerate,username):
        date = datetime.now()
        b = block('null','GENESIS BLOCK','null' ,1,1,'nullhashnow',date)
        mydb2 = mysql.connector.connect(host = "bui9n0ezfg4skkatjufr-mysql.services.clever-cloud.com",
                                    user = "ugczznfsxgqf2bpf",
                                    passwd = "aQY7gbVOr3pBGPT7BJVZ",
                                    database = "bui9n0ezfg4skkatjufr")
        mycurzor2 = mydb2.cursor()
        sql = "INSERT INTO "+username+" (b_no,transactions,hash,prev_hash,merkel_root,nonce,difficulty,timestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val1 = (1, 'null', 'nullhashnow', 'null','null', 1, 1, str(date))
        mycurzor2.execute(sql, val1)
        mydb2.commit()
        
        global mine_rate
        mine_rate = minerate
        return b
    
    def genesis2(minerate,date):
        b = block('null','GENESIS BLOCK','null' ,1,1,'nullhashnow',date)
        global mine_rate
        mine_rate = minerate
        return b
    
    def mine_block1(prev_block,n):
        data,transaction = block.add_transactions1(n)
        nonce = 0
        found = False
        while(found==False):
            nonce = nonce+1
            timestamp = datetime.now()
            difficulty = block.setDifficulty(prev_block,timestamp)
            if difficulty<1:
                difficulty = 1
            textdata = str(timestamp) + str(prev_block.hash) + str(difficulty) + str(data) + str(nonce)
            hash1 = hashlib.sha256(textdata.encode()).hexdigest()
            if hash1[:difficulty]=="0"*difficulty:
                found = True
                b = block(transaction, data, prev_block.hash, nonce, difficulty, hash1, timestamp)
        return b
    
    def mine_block2(prev_block,n):
        data,transaction = block.add_transactions2(n)
        nonce = 0
        found = False
        while(found==False):
            nonce = nonce+1
            timestamp = datetime.now()
            difficulty = block.setDifficulty(prev_block,timestamp)
            if difficulty<1:
                difficulty = 1
            textdata = str(timestamp) + str(prev_block.hash) + str(difficulty) + str(data) + str(nonce)
            hash1 = hashlib.sha256(textdata.encode()).hexdigest()
            if hash1[:difficulty]=="0"*difficulty:
                found = True
                b = block(transaction, data, prev_block.hash, nonce, difficulty, hash1, timestamp)
        return b
    
    def setDifficulty(prevBlock,timestamp):
        global mine_rate
        difficulty = prevBlock.difficulty
        if difficulty<1:
            diff = 1
        ts = int(str(timestamp)[17:19])
        p_ts = int(str(prevBlock.timestamp)[17:19])
        if (ts-p_ts) > mine_rate:
            diff = difficulty-1
        else:
            diff = difficulty+1
        return diff
    
    def add_transactions1(n: int):
        trans = transaction.block_transaction(n)
        data_hash = MerkleTree(trans)
        return data_hash,trans
    
    def add_transactions2(trans_list: list):
        trans = trans_list
        data_hash = MerkleTree(trans)
        return data_hash,trans


# In[10]:


class bc_node:
    
    def __init__(self, p_hash, block):
        self.previous_hash = p_hash
        self.block = block


# In[11]:


class blockchain:
    
    def __init__(self,minerate,username='null',date='null'):
        global mine_rate
        mine_rate = minerate
        self.chain = []
        if username == 'null':
            b = block.genesis2(minerate,date)
        else:
            b = block.genesis(minerate,username)
        self.chain.append(bc_node('null',b))
        b_inf = {}
        b_inf["Hash"]=b.hash
        b_inf["Merkel Root"]=b.data
        b_inf["Nonce"]=b.nonce
        b_inf["timestamp"]=f"{b.timestamp}"
        b_inf["Difficulty"]=b.difficulty
        b_inf["Previous Hash"]=b.previous_hash
        b_inf["Transactions"]=b.transactions
        b_inf["Block Number"]=len(self.chain)
        self.b_info=[]
        self.b_info.append(b_inf)
    
    def add_block_n(self, Transactions, Data, Previous_hash, nonce, difficulty, hash1, timestamp):
        b = block(Transactions,Data,Previous_hash,nonce,difficulty,hash1,timestamp)
        h = Previous_hash
        self.chain.append(bc_node(h,b))
        b_inf = {}
        b_inf["Hash"]=b.hash
        b_inf["Merkel Root"]=b.data
        b_inf["Nonce"]=b.nonce
        b_inf["timestamp"]=f"{b.timestamp}"
        b_inf["Difficulty"]=b.difficulty
        b_inf["Previous Hash"]=b.previous_hash
        b_inf["Transactions"]=b.transactions
        b_inf["Block Number"]=len(self.chain)
        trans = "".join(b.transactions)
        self.b_info.append(b_inf)
        return b_inf
    
    def add_block1(self,n):
        b = block.mine_block1(self.chain[len(self.chain)-1].block,n)
        h = self.chain[len(self.chain)-1].block.hash
        self.chain.append(bc_node(h,b))
        b_inf = {}
        b_inf["Hash"]=b.hash
        b_inf["Merkel Root"]=b.data
        b_inf["Nonce"]=b.nonce
        b_inf["timestamp"]=f"{b.timestamp}"
        b_inf["Difficulty"]=b.difficulty
        b_inf["Previous Hash"]=b.previous_hash
        b_inf["Transactions"]=b.transactions
        b_inf["Block Number"]=len(self.chain)
        trans = "".join(b.transactions)
        update_all(len(self.chain), trans, b.hash, b.previous_hash, b.data, b.nonce, b.difficulty, str(b.timestamp))
        self.b_info.append(b_inf)
        return b_inf
    
    def add_block2(self,n):
        b = block.mine_block2(self.chain[len(self.chain)-1].block,n)
        h = self.chain[len(self.chain)-1].block.hash
        self.chain.append(bc_node(h,b))
        b_inf = {}
        b_inf["Hash"]=b.hash
        b_inf["Merkel Root"]=b.data
        b_inf["Nonce"]=b.nonce
        b_inf["timestamp"]=f"{b.timestamp}"
        b_inf["Difficulty"]=b.difficulty
        b_inf["Previous Hash"]=b.previous_hash
        b_inf["Transactions"]=b.transactions
        b_inf["Block Number"]=len(self.chain)
        self.b_info.append(b_inf)
        return b_inf
    
    def is_valid_chain(chain):
        for k in range(1,len(chain)):
            b = chain[k].block
            pb = chain[k-1].block
            text = str(b.timestamp) + str(b.previous_hash) + str(b.difficulty) + str(b.data) + str(b.nonce)
            
            hash1 = hashlib.sha256(text.encode()).hexdigest()
            hash2 = b.hash
            if hash1!=hash2:
                print("DATA TAMPERED !!! HASH VALUES DON'T MATCH")
            h1 = b.previous_hash
            h2 = pb.hash
            if h1!=h2:
                print("PREVIOUS BLOCK OUT OF SYNC")


# In[12]:


def signin_chain(username):
    mydb2 = mysql.connector.connect(host = "bui9n0ezfg4skkatjufr-mysql.services.clever-cloud.com",
                               user = "ugczznfsxgqf2bpf",
                               passwd = "aQY7gbVOr3pBGPT7BJVZ",
                               database = "bui9n0ezfg4skkatjufr")
    mycurzor2 = mydb2.cursor()
    mycurzor2.execute("SELECT * FROM "+username)
    myresult = mycurzor2.fetchall()
    for i in range(len(myresult)):
        if i==0:
            x = myresult[i]
            gen_date = x[7]
            b = blockchain(5,username='null',date=gen_date)
        else:
            trans = x[1]
            c_hash = x[2]
            p_hash = x[3]
            data = x[4]
            nonce = x[5]
            diff = x[6]
            ts = x[7]
            b.add_block_n(trans, data, p_hash, nonce, diff, c_hash, ts)
    return(b)


# In[13]:


def view_db(username):
    mydb2 = mysql.connector.connect(host = "bui9n0ezfg4skkatjufr-mysql.services.clever-cloud.com",
                               user = "ugczznfsxgqf2bpf",
                               passwd = "aQY7gbVOr3pBGPT7BJVZ",
                               database = "bui9n0ezfg4skkatjufr")
    mycurzor2 = mydb2.cursor()
    mycurzor2.execute("SELECT b_no,transactions FROM "+username)
    myresult = mycurzor2.fetchall()
    list1 = []
    head = ("block no","transactions")
    for x in myresult:
        list1.append(x)
    print(tabulate(list1, headers=head, tablefmt="grid"))


# In[14]:


def view_json(b_chain):
    json_list = b_chain.b_info
    print("-----------------------------")
    for i in range(len(json_list)):
        print("BLOCK["+str(i+1)+"]")
        j = json_list[i]
        for key in j:
            print(key,': ',j[key])
        print(" ")
    print("-----------------------------")


# In[17]:


def my_main():
    from IPython.display import display,Image
    display(Image('zollor.png',width = 200, height = 100))
    while True:
        print("\n\033[1m***WELCOME TO ZOLLORS***\033[0m")
        print("------------------------------------")
        print("SIGN-UP/LOGIN")
        print("1👉Sign-up for new account")
        print("2👉Login to your existing account")
        print("------------------------------------")
        c = input("Enter your choice...")
        if c.isnumeric():
            if int(c)==1:
                username = new_login()
                print("hi ",username)
                print("\nU HAVE SUCCESSFULLY CREATED UR NEW ACCOUNT👍\n")
                b = blockchain(5,username)
                break
            elif int(c)==2:
                username = sign_in()
                b = signin_chain(username)
                print("\nhi ",username)
                print("U HAVE SUCCESSFULLY SIGNED IN👍\n")
                break
            else:
                print("\n***PLEASE ENTER A VALID OPTION***")
                print("***THE VALID OPTIONS ARE '1' AND '2'***")
        else:
            print("PLEASE ENTER A NUMERIC CHARACTER")       
    while True:
        print("\n\033[1m***WHAT WOULD YOU WISH TO DO🤔***\033[0m")
        print("1👉Mine a new block")
        print("2👉View my transactions list")
        print("3👉View entire blockchain")
        print("4👉Exit Application")
        choice = input("Enter your choice...")
        if int(choice)==1:
            while True:
                n = input("\nEnter the number of transactions...")
                if n.isnumeric():
                    if int(n)>0:
                        b.add_block1(n)
                        print("BLOCK SUCCESFULLY MINED...\n")
                        break
                    else:
                        print("INVALID INPUT...PLEASE ENTER WHOLE NUMBERS\n")
                else:
                    print("INVALID INPUT...PLEASE ENTER NUMERIC CHARACTERS\n")
        elif int(choice)==2:
            view_db(username)
        elif int(choice)==3:
            view_json(b)
        elif int(choice)==4:
            print("\n\n\033[1mTHANK YOU FOR USING ZOLLORS\033[0m")
            display(Image('hand.png',width = 200, height = 100))
            break
        else:
            print("\n***PLEASE ENTER A VALID OPTION***")
            print("***THE VALID OPTIONS ARE '1', '2', '3' and '4'***")


# In[18]:


my_main()

