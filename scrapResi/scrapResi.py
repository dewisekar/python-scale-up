#import pytesseract
#from pdf2image import convert_from_path
import pytesseract
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
from os import path
import sys
#import database
import platform 
import time
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'logger'))

import database
import myLogger

from wand.image import Image
from PIL import Image as PI
import pyocr
import pyocr.builders
import io

from scrapTiktok import scrapTiktokData
from scrapShopee import scrapShopeeData

timeWait = 10
pathFolder = '' #'/home/projects/docs/'
pathFolderDone = '' #'/home/projects/docs/Done/'
tool = pyocr.get_available_tools()[0]
lang = tool.get_available_languages()[1]

def convert_pdf_to_img(pdf_file) :
    return convert_from_path(pdf_file, 500)
def convert_image_to_text(file):
    text = image_to_string (file)
    return text

def initialFunction():
    global pathFolder
    global pathFolderDone
    if(platform.system() == 'Linux'):
        pathFolder = '/home/projects/docs/'
        pathFolderDone = '/home/projects/docs/Done/'
    else :
        pathFolder = 'D:/APPLICATION/docs/'
        pathFolderDone = 'D:/APPLICATION/docs/Done/'
    
    myLogger.logging_info("scrapResi","Initialization, pathFolder: ",pathFolder,"pathFolderDone : " ,pathFolderDone)
    #print("Initialization, pathFolder: ",pathFolder,"pathFolderDone : ", pathFolderDone)

def move_file(oldPath,newPath):
    try:
        os.rename(oldPath,newPath)
    except Exception as e:
        myLogger.logging_error("scrapResi","Cannot move file:",oldPath,"to path:",newPath)

def main():
    global pathFolder
    global pathFolderDone
    initialFunction()

    while True :
        sql = """\
        EXEC [dbo].[SP_GetFileResiToScrap];
        """
        try:
            rows = database.fetchRowsFromDatabase(sql)
            loop = 0
            for row in rows:
                loop += 1
                fileId = row[0]
                fileName = row[1]
                filePath = pathFolder + fileName #+ extension
                channel = row[2]
                isMarketPlace = row[3]
                myLogger.logging_info("scrapResi","filePath:",filePath)
                
                #print("filePath:",filePath)
                if path.exists(filePath):
                    myLogger.logging_info("scrapResi","File '", filePath,"' is exists:",str(path.exists(filePath)))

                    isFileCanBeRead = True
                    try:
                        images = convert_pdf_to_img (filePath)
                    except Exception as e:
                        myLogger.logging_info("scrapResi","File '", filePath,"' can not be read")
                        isFileCanBeRead = False

                    if not isFileCanBeRead:
                        sqlUpdateString = ""
                        sqlUpdateString = "UPDATE [dbo].[DAILYFILERESI] SET STATUSFILE='4',"
                        sqlUpdateString += " FILENAME='" + fileName + "{ERROR}',"
                        sqlUpdateString += " ERRMSG='FILE CAN NOT BE READ', TOTALPAGESINSERTED='0'"
                        sqlUpdateString += " WHERE  ID =" + str(fileId) +";"
                        database.executeSqlQuery(sqlUpdateString)
                        move_file(pathFolder + fileName,pathFolder+"pathFolder" + fileName)
                        break
                    
                    final_text2 = ""
                    totalResiPageCanBeRead = 0
                    totalResiPageCanBeUpdate = 0
                    listOfErrowRow = []
                    iteratorPages = 0
                    for pg, img in enumerate (images) :
                        iteratorPages += 1
                        myLogger.logging_info("scrapResi","rows:",iteratorPages)
                        final_text = convert_image_to_text (img)
                        sqlUpdate = ''
                        if channel == 'Tiktok' :
                            sqlUpdate,x,y = scrapTiktokData(final_text,fileName)
                            #totalResiPageCanBeRead += x
                            #totalResiPageCanBeFound += y
                        elif channel == 'Shopee' :
                            sqlUpdate = scrapShopeeData(final_text,fileName)

                        if sqlUpdate != '' :
                            myLogger.logging_info("scrapResi","executing sql update")
                            #print("executing sql update")
                            try :
                                database.executeSqlQuery(sqlUpdate)
                                totalResiPageCanBeUpdate += 1
                            except  Exception as e:
                                myLogger.logging_error("scrapResi","got exception update:",e)
                                listOfErrowRow.append(iteratorPages)
                                #print("got exception:",e)
                        else:
                            listOfErrowRow.append(iteratorPages)

                        
                        final_text2 += final_text

                    totalResiPageCanBeRead = iteratorPages
                    strListOfErrorRows = ','.join(str(x +1) for x in listOfErrowRow)

                    #print(final_text2)
                    myLogger.logging_info("scrapResi","fileName:", fileName,",totalResiPageCanBeRead:",totalResiPageCanBeRead, ",totalResiPageCanBeUpdate:",totalResiPageCanBeUpdate)
                    #print("fileName:",fileName,",totalResiPageCanBeRead:",totalResiPageCanBeRead,",totalResiPageCanBeFound:",totalResiPageCanBeFound)
                    myLogger.logging_info("scrapResi","==========================")
                    updateString = " UPDATE [dbo].[DAILYFILERESI] SET STATUSFILE='1',"
                    updateString += " ERRMSG='" +"SUCCESS IMPORT; total halaman resi yang dapat di scrap:" + str(totalResiPageCanBeRead) + "; total resi yang dapat diupdate:" + str(totalResiPageCanBeUpdate) + "', "
                    updateString += " TOTALPAGESINSERTED = '" + str(totalResiPageCanBeUpdate) + "',"
                    updateString += " ERRORPAGES = '" + strListOfErrorRows + "'"
                    updateString += " WHERE  ID =" + str(fileId) +";"
                    myLogger.logging_info("scrapResi","update file status:", updateString)
                    #print("update file status:",updateString)
                    database.executeSqlQuery(updateString)
                if loop >=1 :
                    break
        except Exception as e:
            myLogger.logging_error("scrapResi","Exception:",e)
        
        time.sleep(timeWait)
    


if __name__== "__main__":
   main()