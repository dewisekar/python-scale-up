import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'logger'))
import database
import myLogger

def scrapTiktokData(final_text,fileName):
    sqlUpdate = ''
    totalResiPageCanBeRead = 0
    totalResiPageCanBeFound = 0
    try :
        splitedText = final_text.split("\n\n")
        while("" in splitedText) :
            splitedText.remove("")

        #print(splitedText)
        getPenerima = splitedText[3].split("\n")
        getAlamat = getPenerima[1]
        getNamaNoHp = getPenerima[0].split(",")
        getNama = getNamaNoHp[0].replace("Penerima : ", "")
        getNoHp = getNamaNoHp[1].replace(")","").replace("+","").replace("(","")

        getResi = [splitedText[7],splitedText[8],splitedText[9]]
        
        if getNama != "" and getAlamat != "" and getNoHp != "" :
            totalResiPageCanBeRead += 1

        myLogger.logging_info("scrapResi","Resi : ",getResi)
        myLogger.logging_info("scrapResi","Nama : ",getNama)
        myLogger.logging_info("scrapResi","Alamat : ",getAlamat)
        myLogger.logging_info("scrapResi","No. Hp : ",getNoHp)
        # print("Resi : ",getResi)
        # print("Nama : ",getNama)
        # print("Alamat : ",getAlamat)
        # print("No. Hp : ",getNoHp)
        
        isExistResi = 0
        for possibleResi in getResi:
            if(possibleResi != ""):
                sqlSelect = "EXEC [dbo].[SP_CheckIsExistKodeBooking] @KODERESI='" +possibleResi.replace("'","")  + "';"
                possibleResiRows = database.fetchRowsFromDatabase(sqlSelect)
                myLogger.logging_info("scrapResi","is exist kode booking:",possibleResi,",result:",len(possibleResiRows))
                # print("is exist kode booking:",possibleResi,",result:",len(possibleResiRows))
                if len(possibleResiRows) == 1 :
                    isExistResi = 1
                    myLogger.logging_info("scrapResi","resi is found")
                    # print("resi is found")
                    totalResiPageCanBeFound += 1
                    if getNama != "" and getAlamat != "" and getNoHp != "" :
                        sqlUpdate += " EXEC [dbo].[SP_UpdateJurnalJualFromResi] " 
                        sqlUpdate += " @RESI='" +possibleResi.replace("'","''") + "', " 
                        sqlUpdate += " @NAMA_PENERIMA='" + getNama.replace("'","''") + "', " 
                        sqlUpdate += " @HP_PENERIMA='" + getNoHp.replace("'","''") + "', " 
                        sqlUpdate += " @ALAMAT='" + getAlamat.replace("'","''")  + "', " 
                        sqlUpdate += " @FILE_TRX_NAME='" + fileName.replace("'","''") + "' ; " 
                        myLogger.logging_info("scrapResi",sqlUpdate)
                    break

        if isExistResi == 0 :
            myLogger.logging_info("scrapResi","resi is not found")
            myLogger.logging_error("scrapResi",'text true :', final_text)
            #print("resi is not found")  
    except  Exception as e:
        sqlUpdate = '' 
        myLogger.logging_error("scrapResi",'Failed to parse text :', e)
        myLogger.logging_error("scrapResi",'text :', final_text)

    #print("totalResiPageCanBeRead:",totalResiPageCanBeRead,",totalResiPageCanBeFound:",totalResiPageCanBeFound)
    return sqlUpdate,totalResiPageCanBeRead,totalResiPageCanBeFound
