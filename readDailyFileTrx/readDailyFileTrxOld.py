import pyodbc 
import pandas as pd
import os.path
from os import path
import statusFileEnum as StatusFile

pathFolder = 'D:/APPLICATION/docs/'
pathFolderDone = 'D:/APPLICATION/docs/Done/'
#extension = '.xlsx'
#df = pd.read_excel (r'C:\Users\vadio\Documents\GitHub\Repo-Dio\tesexcel.xlsx')

def main():
    
    #connect to sql server localhost
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=localhost;'
                      'Database=WEB_CONFIG;'
                      'Trusted_Connection=yes;')

    try:
        sql = """\
            EXEC [dbo].[SP_GetFileToInsert];
            """

        cursor = conn.cursor()
        cursor.execute(sql)
        loop = 0
        for i in cursor:
            loop += 1
            fileId = i[0]
            fileName = i[1]
            filePath = pathFolder + fileName #+ extension
            channel = i[2]
            isMarketPlace = i[3]
            if path.exists(filePath):
                df = pd.read_excel (filePath)
                print(df)
            else:
                updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.NOT_FOUND) +"';"
                cursor.execute(updateString)
            print('filePath:',filePath)
            print ("File exists:"+str(path.exists(filePath)))
            if loop >=1 :
                break
            #print(i,i[1])
    except Exception as e:
        print("An exception occurred :",e) 
    
    conn.close()


if __name__== "__main__":
   main()




