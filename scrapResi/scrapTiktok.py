import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'logger'))
import database
import myLogger
import re

def scrapTiktokData(final_text,fileName):
    sqlUpdate = ''
    totalResiPageCanBeRead = 0
    totalResiPageCanBeFound = 0
    try :
        splitedText = final_text.split("\n\n")
        while("" in splitedText) :
            splitedText.remove("")
        
        w = "JX"
        g = "Penerima : "

        resi = ''
        penerima = ''
        namaNoHpPenerima = ''
        namaPenerima = ''
        noHpPenerima = ''
        alamatPenerima = ''
        
        IsValidResi = re.search('({0})((.)*)\n'.format(w),final_text)
        #IsValidResi = re.search('({0})\d+'.format(w),final_text)
        if IsValidResi:
            resi = IsValidResi[0]
            resi = resi.replace("\n","").replace(" ","")

        sqlSelect = "EXEC [dbo].[SP_CheckIsExistKodeBooking] @KODERESI='" + resi + "';"
        
        possibleResiRows = database.fetchRowsFromDatabase(sqlSelect)
        myLogger.logging_info("scrapResi","is exist kode booking:",resi,",result:",len(possibleResiRows))
                
        if len(possibleResiRows) == 1 :
            isValidPenerima = re.search('({0})((.|\n)*)(TOTAL)'.format(g),final_text)
            if isValidPenerima:
                penerima = isValidPenerima[0]

            arrPenerima = penerima.split("\n")

            if len(arrPenerima) >= 2:
                namaNoHpPenerima = arrPenerima[0]
                if namaNoHpPenerima != "":
                    arrNamaNoHpPenerima = namaNoHpPenerima.split(",")
                    if len(arrNamaNoHpPenerima) >= 2:
                        if arrNamaNoHpPenerima[0] != "":
                            namaPenerima = arrNamaNoHpPenerima[0].replace("Penerima : ", "")
                        if arrNamaNoHpPenerima[1] != "":
                            noHpPenerima = arrNamaNoHpPenerima[1].replace(")","").replace("+62","").replace("(","")
                            noHpPenerima = noHpPenerima.replace(" ","")
                            if noHpPenerima[0] != "0":
                                noHpPenerima = "0" + noHpPenerima
                # alamatPenerima = arrPenerima[1]
                # alamatPenerima = alamatPenerima.replace("\n"," ")
                for x in range(1,len(arrPenerima)):
                    if arrPenerima[x] != "" and (not ("COD" in arrPenerima[x])) and (not ("TOTAL" in arrPenerima[x])):
                        alamatPenerima += arrPenerima[x].replace("\n"," ")
                
                myLogger.logging_info("scrapResi","Resi is found")
                myLogger.logging_info("scrapResi","Resi : ",resi)
                myLogger.logging_info("scrapResi","Nama : ",namaPenerima)
                myLogger.logging_info("scrapResi","Alamat : ",alamatPenerima)
                myLogger.logging_info("scrapResi","No. Hp : ",noHpPenerima)

                if namaPenerima != "" and alamatPenerima != "" and noHpPenerima != "" :
                    sqlUpdate += " EXEC [dbo].[SP_UpdateJurnalJualFromResi] " 
                    sqlUpdate += " @RESI='" +resi.replace("'","''") + "', " 
                    sqlUpdate += " @NAMA_PENERIMA='" + namaPenerima.replace("'","''") + "', " 
                    sqlUpdate += " @HP_PENERIMA='" + noHpPenerima.replace("'","''") + "', " 
                    sqlUpdate += " @ALAMAT='" + alamatPenerima.replace("'","''")  + "', " 
                    sqlUpdate += " @FILE_TRX_NAME='" + fileName.replace("'","''") + "' ; " 
                    myLogger.logging_info("scrapResi",sqlUpdate)
                
                #myLogger.logging_info("scrapResi",'text :', final_text)
        else :
            myLogger.logging_error("scrapResi","Resi is not found,",resi)
            myLogger.logging_error("scrapResi",'text :', final_text)
        
        #region old
        #print(splitedText)
        # getPenerima = splitedText[3].split("\n")
        # getAlamat = getPenerima[1]
        # getNamaNoHp = getPenerima[0].split(",")
        # getNama = getNamaNoHp[0].replace("Penerima : ", "")
        # getNoHp = getNamaNoHp[1].replace(")","").replace("+","").replace("(","")

        # getResi = [splitedText[7],splitedText[8],splitedText[9]]
        
        # if getNama != "" and getAlamat != "" and getNoHp != "" :
        #     totalResiPageCanBeRead += 1

        # myLogger.logging_info("scrapResi","Resi : ",getResi)
        # myLogger.logging_info("scrapResi","Nama : ",getNama)
        # myLogger.logging_info("scrapResi","Alamat : ",getAlamat)
        # myLogger.logging_info("scrapResi","No. Hp : ",getNoHp)
        # print("Resi : ",getResi)
        # print("Nama : ",getNama)
        # print("Alamat : ",getAlamat)
        # print("No. Hp : ",getNoHp)
        

        # isExistResi = 0
        # for possibleResi in getResi:
        #     if(possibleResi != ""):
        #         sqlSelect = "EXEC [dbo].[SP_CheckIsExistKodeBooking] @KODERESI='" +possibleResi.replace("'","")  + "';"
        #         possibleResiRows = database.fetchRowsFromDatabase(sqlSelect)
        #         myLogger.logging_info("scrapResi","is exist kode booking:",possibleResi,",result:",len(possibleResiRows))
        #         # print("is exist kode booking:",possibleResi,",result:",len(possibleResiRows))
        #         if len(possibleResiRows) == 1 :
        #             isExistResi = 1
        #             myLogger.logging_info("scrapResi","resi is found")
        #             # print("resi is found")
        #             totalResiPageCanBeFound += 1
        #             if getNama != "" and getAlamat != "" and getNoHp != "" :
        #                 sqlUpdate += " EXEC [dbo].[SP_UpdateJurnalJualFromResi] " 
        #                 sqlUpdate += " @RESI='" +possibleResi.replace("'","''") + "', " 
        #                 sqlUpdate += " @NAMA_PENERIMA='" + getNama.replace("'","''") + "', " 
        #                 sqlUpdate += " @HP_PENERIMA='" + getNoHp.replace("'","''") + "', " 
        #                 sqlUpdate += " @ALAMAT='" + getAlamat.replace("'","''")  + "', " 
        #                 sqlUpdate += " @FILE_TRX_NAME='" + fileName.replace("'","''") + "' ; " 
        #                 myLogger.logging_info("scrapResi",sqlUpdate)
        #             break

        # if isExistResi == 0 :
        #     myLogger.logging_info("scrapResi","resi is not found")
        #     myLogger.logging_error("scrapResi",'text true :', final_text)
            #print("resi is not found")
        #endregion  
    except  Exception as e:
        sqlUpdate = '' 
        myLogger.logging_error("scrapResi",'Failed to parse text :', e)
        myLogger.logging_error("scrapResi",'text :', final_text)

    #print("totalResiPageCanBeRead:",totalResiPageCanBeRead,",totalResiPageCanBeFound:",totalResiPageCanBeFound)
    return sqlUpdate,totalResiPageCanBeRead,totalResiPageCanBeFound
