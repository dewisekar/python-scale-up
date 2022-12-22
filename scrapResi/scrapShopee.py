import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'database'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'logger'))
import database
import myLogger
import re

def scrapShopeeData(final_text,fileName):
    sqlUpdate = ''
    myLogger.logging_error("scrapResi",'text :', final_text)
    return sqlUpdate
