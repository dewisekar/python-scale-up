import pyodbc 
import pandas as pd
import os.path
from os import path
import statusFileEnum as StatusFile
from importShopee import readShopeeRow
import time
import platform 
import sys
sys.path.append(path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(path.join(os.path.dirname(__file__), '..', 'logger'))
import database
import myLogger



#pathFolder = 'D:/APPLICATION/docs/'
pathFolder = '' #'/home/projects/docs/'
pathFolderDone = '' #'/home/projects/docs/Done/'
driver = ''

def initialFunction():
    global pathFolder
    global pathFolderDone
    global driver
    if(platform.system() == 'Linux'):
        pathFolder = '/home/projects/docs/'
        pathFolderDone = '/home/projects/docs/Done/'
        driver = 'ODBC Driver 18 for SQL Server'
    else :
        pathFolder = 'D:/APPLICATION/docs/'
        pathFolderDone = 'D:/APPLICATION/docs/Done/'
        driver = 'SQL Server'
    
    myLogger.logging_info("readFileTrx","Initialization, pathFolder: ",pathFolder,"pathFolderDone : ", pathFolderDone,"driver:",driver)
    #print("Initialization, pathFolder: ",pathFolder,"pathFolderDone : ", pathFolderDone,"driver:",driver)


# server = 'localhost'
# database = 'WEB_CONFIG'
# username = 'sa'
# password = 'P@ssw0rd'
#pathFolderDone = 'D:/APPLICATION/docs/Done/'
#extension = '.xlsx'
#df = pd.read_excel (r'C:\Users\vadio\Documents\GitHub\Repo-Dio\tesexcel.xlsx')

def main():
    global pathFolder
    global pathFolderDone
    initialFunction()
    while True:
        sql = """\
        EXEC [dbo].[SP_GetFileToInsert];
        """

        fileName = ""
        fileId = ""
        
        try:
            rows = database.fetchRowsFromDatabase(sql)
            loop = 0
            for row in rows:
                loop += 1
                listOfErrowRow = []
                fileId = row[0]
                fileName = row[1]
                filePath = pathFolder + fileName #+ extension
                channel = row[2]
                isMarketPlace = row[3]
                myLogger.logging_info("readFileTrx","File '"+ filePath + "' is exists:"+str(path.exists(filePath)))
                if path.exists(filePath):
                    insertedRows = 0
                    canBeReadRows = 0
                    generatedSqlRows = 0
                    errorRows = 0 
                    iteratorRow = 0
                    rownum = 0
                    df = pd.read_excel (filePath,converters={'HP. PENERIMA (DEPAN 62)':str})
                    for index, row in df.iterrows():
                        iteratorRow += 1
                        if(str(row['INVOICE']) != 'nan' and  str(row['INVOICE']) != 'NaT'):
                            rownum+= 1
                            executeJournalJualString = readShopeeRow(row,fileName)
                            if( executeJournalJualString == ''):
                                listOfErrowRow.append(iteratorRow) 
                                myLogger.logging_info("readFileTrx","can not generate update jurnal jual string ",fileName," at row=", iteratorRow,", invoice :",str(row['INVOICE']))
                            else:
                                generatedSqlRows +=1 
                                try:
                                    database.executeSqlQuery(executeJournalJualString)
                                    insertedRows += 1
                                except Exception as e:
                                    listOfErrowRow.append(iteratorRow) 
                                    myLogger.logging_info("readFileTrx","can not execute update jurnal jual string ",fileName," at row=", iteratorRow,", invoice :",str(row['INVOICE']))
                                    myLogger.logging_info("readFileTrx",executeJournalJualString)
                                    
                        else:
                            listOfErrowRow.append(iteratorRow) 
                            errorRows += 1
                            myLogger.logging_info("readFileTrx","found rows error on file ",fileName," at row=", iteratorRow)
                    
                    errMsgFile = "total file rows :" + str(iteratorRow) 
                    errMsgFile += ",total rows can be read:" + str(canBeReadRows)
                    errMsgFile += ",total rows can be generated sql:" + str(generatedSqlRows)
                    errMsgFile += ",total rows can be inserted :" + str(insertedRows)
                    myLogger.logging_info("readFileTrx",fileName,": ",errMsgFile)
                    strListOfErrorRows = ','.join(str(x +1) for x in listOfErrowRow)
                    updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.SUCCESS) +"',@ERRMSG='"+ errMsgFile + "';"
                    database.executeSqlQuery(updateString)  
                    myLogger.logging_info("readFileTrx","strListOfErrorRows",": ",strListOfErrorRows)
                    updateString = " UPDATE [dbo].[DAILYFILETRX] SET ERRORROWS = '" + strListOfErrorRows + "' WHERE ID = " + str(fileId) + ";"
                    database.executeSqlQuery(updateString) 
                    updateString = " UPDATE [dbo].[DAILYFILETRX] SET TOTALROWSINSERTED = '" + str(insertedRows) + "' WHERE ID = " + str(fileId) + ";"
                    database.executeSqlQuery(updateString) 
                else:
                    updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.NOT_FOUND)+"',@ERRMSG='NOT FOUND';"
                    database.executeSqlQuery(updateString) 
        except Exception as e:
            errMsg = "An exception occurred :" + str(e)
            myLogger.logging_info("readFileTrx",errMsg)
            if(fileName != "" and fileId != ""):
                updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.UNDEFINED)+"',@ERRMSG='{}';".format(errMsg)
                database.executeSqlQuery(updateString)         
        #region old
        # with pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;') as conn:

        #     fileId = 0 
        #     try:
        #         sql = """\
        #             EXEC [dbo].[SP_GetFileToInsert];
        #             """

        #         cursor = conn.cursor()
        #         cursor.execute(sql)

        #         rows = cursor.fetchall()
        #         loop = 0

        #         for row in rows: #looping in all file will be imported
        #             loop += 1
        #             try:
        #                 fileId = row[0]
        #                 fileName = row[1]
        #                 filePath = pathFolder + fileName #+ extension
        #                 channel = row[2]
        #                 isMarketPlace = row[3]
        #                 print ("File '"+ filePath + "' is exists:"+str(path.exists(filePath)))
        #                 if path.exists(filePath):
        #                     # if (channel == "Shopee") :
        #                     #     df = pd.read_excel (filePath,converters={'Perkiraan Ongkos Kirim':str})
        #                     # else :
        #                     #     df = pd.read_excel (filePath)
        #                     # executeJournalJualString = ""

        #                     #print(df)
        #                     rownum = 0
        #                     df = pd.read_excel (filePath,converters={'HP. PENERIMA (DEPAN 62)':str})
        #                     for index, row in df.iterrows():
        #                         if(str(row['INVOICE']) != 'nan' and  str(row['INVOICE']) != 'NaT'):
        #                             rownum+= 1
        #                             try:
        #                                 executeJournalJualString = readShopeeRow(row,fileName)
        #                                 with pyodbc.connect('DRIVER={'+driver+'};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password+';TrustServerCertificate=yes;') as conn2:
        #                                     cursor2 = conn2.cursor()
        #                                     print(executeJournalJualString)
                            
        #                                     cursor2.execute(executeJournalJualString)
                                        
        #                                 #time.sleep(1)
        #                             except Exception as ex :
        #                                 print("err :",ex)
        #                     print("total rows : ",rownum)
        #                     updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.SUCCESS) +"',@ERRMSG='SUCCESS';"
        #                     cursor.execute(updateString)
        #                 else:
        #                     updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.NOT_FOUND)+"',@ERRMSG='NOT FOUND';"
        #                     #cursor.execute(updateString)
        #             except Exception as e:
        #                 errMsg = "An exception occurred :" + str(e)
        #                 print(errMsg) 
        #                 updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.UNDEFINED)+"',@ERRMSG='{}';".format(errMsg)
        #             if loop >=1 :
        #                 break
        #         #print(i,i[1])
        #     except Exception as e:
        #         errMsg = "An exception occurred :" + str(e)
        #         print(errMsg) 
        #         #if fileId ==0 :
        #         #updateString = "EXEC [dbo].[SP_UpdateStatusDailyFileTrx] @ID=" +str(fileId) + ",@STATUSFILE='" + str(StatusFile.UNDEFINED) +"',@ERRMSG='" +errMsg.replace("'","" )+"';"
        #         #print(updateString)
        #         #cursor.execute(updateString)
        #endregion
        time.sleep(60)


if __name__== "__main__":
   main()




