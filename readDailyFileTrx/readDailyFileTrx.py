import pyodbc 
import pandas as pd
import os.path
from os import path
import statusFileEnum as StatusFile
from importShopee import readShopeeRow
import time

#pathFolder = 'D:/APPLICATION/docs/'
pathFolder = '/home/projects/docs/'
pathFolderDone = '/home/projects/docs/Done/'

server = 'localhost'
database = 'WEB_CONFIG'
username = 'sa'
password = 'P@ssw0rd'
#pathFolderDone = 'D:/APPLICATION/docs/Done/'
#extension = '.xlsx'
#df = pd.read_excel (r'C:\Users\vadio\Documents\GitHub\Repo-Dio\tesexcel.xlsx')

def main():
    
    while True:
        with pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;') as conn:

            fileId = 0 
            try:
                sql = """\
                    EXEC [dbo].[SP_GetFileToInsert];
                    """

                cursor = conn.cursor()
                cursor.execute(sql)

                rows = cursor.fetchall()
                loop = 0

                for row in rows:
                    loop += 1
                    fileId = row[0]
                    fileName = row[1]
                    filePath = pathFolder + fileName #+ extension
                    channel = row[2]
                    isMarketPlace = row[3]
                    print ("File '"+ filePath + "' is exists:"+str(path.exists(filePath)))
                    if path.exists(filePath):
                        # if (channel == "Shopee") :
                        #     df = pd.read_excel (filePath,converters={'Perkiraan Ongkos Kirim':str})
                        # else :
                        #     df = pd.read_excel (filePath)
                        # executeJournalJualString = ""

                        #print(df)
                        df = pd.read_excel (filePath,converters={'HP. PENERIMA (DEPAN 62)':str})
                        for index, row in df.iterrows():
                            if(str(row['INVOICE']) != 'nan' and  str(row['INVOICE']) != 'NaT'):
                                executeJournalJualString = readShopeeRow(row,fileName)
                                print(executeJournalJualString)
                        
                                cursor.execute(executeJournalJualString)
                        
                        updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.SUCCESS) +"',@ERRMSG='SUCCESS';"
                        cursor.execute(updateString)
                    else:
                        updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.NOT_FOUND)+"',@ERRMSG='NOT FOUND';"
                        #cursor.execute(updateString)
                    if loop >=1 :
                        break
                #print(i,i[1])
            except Exception as e:
                errMsg = "An exception occurred :" + str(e)
                print(errMsg) 
                #if fileId ==0 :
                #updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.UNDEFINED) +"',@ERRMSG='" +errMsg.replace("'","" )+"';"
                #print(updateString)
                #cursor.execute(updateString)
        time.sleep(60)


if __name__== "__main__":
   main()




