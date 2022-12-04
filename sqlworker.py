import mysql.connector
import random
import string

def Create_User(username):
    dbconfig = {'host':'127.0.0.1','user':'root','password':'example','database':'example',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """ insert into users (user)
    value (%s)"""
    cursor.execute(_SQL,username.split())
    conn.commit()
    cursor.close()
    conn.close()
    dbconfig = {'host':'127.0.0.1','user':'root','password':'example','database':'example',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = "CREATE TABLE "+username+"(id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(32), description varchar(64), event_time varchar(16), reminder_time varchar(16));"
    cursor.execute(_SQL)
    conn.commit()
    cursor.close()
    conn.close()

def Print_Users(id):
    dbconfig = {'host':'127.0.0.1','user':'root','password':'example','database':'example',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    cursor.execute("select * from "+id+";")
    x = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return x

def Checker(username):
    dbconfig = {'host':'127.0.0.1','user':'root','password':'example','database':'example',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """select * from users where user = %s"""
    cursor.execute(_SQL,(username))
    s=cursor.fetchall()
    cursor.close()
    conn.close()
    return s

def New_event(table, name, description, event_time, reminder_time):
    dbconfig = {'host':'127.0.0.1','user':'root','password':'example','database':'example',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = f""" insert into {table} (name, description, event_time, reminder_time)
    values (%s, %s, %s, %s)"""
    cursor.execute(_SQL, (name, description, event_time, reminder_time))
    conn.commit()
    cursor.close()
    conn.close() 

def Delete_event(id, name):
    dbconfig = {'host':'127.0.0.1','user':'root','password':'example','database':'example',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = f"""DELETE FROM {id} WHERE name = %s"""
    cursor.execute(_SQL,(name.split()))
    conn.commit()
    cursor.close()
    conn.close() 

