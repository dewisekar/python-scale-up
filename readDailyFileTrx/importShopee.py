from datetime import datetime
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'logger'))
import myLogger

importerShopeeVarchar = [ ['TGL ORDER','TGL_ORDER'],
['ORDER VIA','ORDER_VIA'],
['KET LAIN','KET_LAIN'],
['USERNAME','USERNAME'],
['NAMA PENERIMA','NAMA_PENERIMA'],
['HP. PENERIMA (DEPAN 62)','HP_PENERIMA'],
['ALAMAT','ALAMAT'],
['KOTA','KOTA'],
['PROVINSI','PROVINSI'],
#['PULAU','PULAU'],
#['STATUS TRX','STATUS_TRX'],
['Nama Produk','Nama_Produk'],
#['Nama Produk 2','Nama_Produk_2'],
#['Nama Produk 3','Nama_Produk_3'],
#['Nama Produk 4','Nama_Produk_4'],
#['Nama Produk 5','Nama_Produk_5'],
['KURIR','KURIR'],
['INVOICE','INVOICE'],
['RESI / KODE BOOKING','RESI']]

importerShopeeFloat = [ ['DISKON DARI PENJUAL','DISKON_DARI_PENJUAL'],
['DISKON DARI MP','DISKON_DARI_MP'],
#['DITERIMA','DITERIMA'],
['Jml Produk','Jml_Produk'],
#['Jml Produk 2','Jml_Produk_2'],
#['Jml Produk 3','Jml_Produk_3'],
#['Jml Produk 4','Jml_Produk_4'],
#['Jml Produk 5','Jml_Produk_5'],
['ONGKIR DIBAYAR OLEH CUSTOMER','ONGKIR_DIBAYAR_OLEH_CUSTOMER'],
['DISC ONGKIR SELLER','DISC_ONGKIR_SELLER'],
['DISC ONGKIR PLATFORM','DISC_ONGKIR_PLATFORM'],
['ONGKIR DIBAYAR OLEH JIERA','ONGKIR_DIBAYAR_OLEH_JIERA']]

strJenisOrderan = 'S'

def readShopeeRow(row,filename):
    strSql = ""
    strNomorInovice = ""
    try:
        strNomorInovice = row['INVOICE']
        strSql = "EXEC [dbo].[SP_InsertJournalJualMaster] "
        #print(row['Waktu Pembayaran Dilakukan'])
        for item in importerShopeeVarchar:
            key_xlsx = item[0]
            key_table = item[1]
            #strSql = strSql + "@" + key_table + "='" + str(row[key_xlsx]).replace("'","") + "',"
            if(str(row[key_xlsx]) == 'nan'):
                strSql = strSql + "@" + key_table + "= NULL "+ ","
            else :
                strSql = strSql + "@" + key_table + "='" + str(row[key_xlsx]) + "',"
        
        for item in importerShopeeFloat:
            key_xlsx = item[0]
            key_table = item[1]
            #strSql = strSql + "@" + key_table + "='" + str(row[key_xlsx]).replace("'","") + "',"
            if(str(row[key_xlsx]) == 'nan'):
                strSql = strSql + "@" + key_table + "= NULL "+ ","
            else :
                strSql = strSql + "@" + key_table + "=" + str(row[key_xlsx])+ ","
        #SET TANGGAL
        # datetimeWaktuPesanan = datetime.strptime(row['Waktu Pesanan Dibuat'], '%Y-%m-%d')
        # strWaktuPesanan = datetimeWaktuPesanan.strftime('%Y%m%d')
        # strSql = strSql + "@TANGGAL_PESAN='"+ strWaktuPesanan + "',"

        #SET JENIS ORDERAN 
        # strSql = strSql + "@JENIS_ORDERAN='"+ strJenisOrderan + "',"

        #SET ONGKIR
        # objOngkir = row['Perkiraan Ongkos Kirim']
        # objOngkir = objOngkir.replace('.','') + '.00'
        # strSql = strSql + "@ONGKIR="+ objOngkir + ","
        
        #SET JUMLAH
        # objJumlah = row['Jumlah']
        # strSql = strSql + "@JML_PRODUK="+ str(objJumlah) + ","

        #SET FiletrxName
        strSql = strSql + "@FILE_TRX_NAME='"+ filename.replace("'","") + "',"

        strSql = strSql[:-1]
    #print("Sql Exec:", sql)
    except Exception as e:
        myLogger.logging_info("readFileTrx","Create execute sql Journal Error gagal, No. Invoice : ",strNomorInovice, ",filename:", filename,",exc:", e)
        #print("Create execute sql Journal Error gagal, No. Invoice : ",strNomorInovice, ",filename:", filename,",exc:", e)
    

    return strSql
