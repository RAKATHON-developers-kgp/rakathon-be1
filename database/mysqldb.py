import mysql.connector

def db_connect():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="testing_db"   
    )
    return mydb

def get_data():
    mydb = db_connect()
    cursor = mydb.cursor()
    myresult = cursor.execute("SELECT * FROM Persons")
    myresult = cursor.fetchall()
    listt = list(sum(myresult,()))
    cursor.close()
    return listt

def input_data(name):
    mydb = db_connect()
    cursor = mydb.cursor()
    sql = "INSERT INTO Persons (name) VALUES (%s)"
    val = [name]
    cursor.execute(sql, val)
    mydb.commit()
    cursor.close()
    mydb.close()


def delete_data(name):
    mydb = db_connect()
    cursor = mydb.cursor()
    sql = "DELETE FROM Persons WHERE name = %s"
    adr = [name]
    cursor.execute(sql, adr)
    mydb.commit()
    cursor.close()
    mydb.close()








# list = get_data()

# print(list)
# print(list)
# print(list)
