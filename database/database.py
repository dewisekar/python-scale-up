import pyodbc
import platform 

server = 'localhost'
database = 'WEB_CONFIG'
username = 'sa'
password = 'P@ssw0rd'
driver = ''

def initialFunction():
    global driver
    if(platform.system() == 'Linux'):
        driver = 'ODBC Driver 18 for SQL Server'
    else :
        driver = 'SQL Server'
    
    #print("driver:",driver)

def fetchRowsFromDatabase(strSql):
    initialFunction()
    with pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;') as conn:
        cursor = conn.cursor()
        cursor.execute(strSql)
        rows = cursor.fetchall()
        return rows

def executeSqlQuery(strSql):
    initialFunction()
    with pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;') as conn:
        cursor = conn.cursor()
        return cursor.execute(strSql)
        #rows = cursor.fetchall()
        #return rows

