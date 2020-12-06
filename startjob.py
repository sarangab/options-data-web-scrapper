from util import get_option_chain_table
from datetime import date
import time
import datetime
import os 
import pandas as pd
os.makedirs("data", exist_ok=True)
from os import system, name


prev_datetime = None
index = 0
while True:
    dataFrame, index_val, index_datetime = get_option_chain_table("NIFTY", instrument="OPTIDX", expiry=date(2020, 12, 10))
    if index_datetime != prev_datetime:
        prev_datetime = index_datetime
        file_name = index_datetime.strftime("%Y-%m-%d_%H:%M:%S") + "_" + str(index_val)
        dataFrame.to_csv(os.path.join(os.getcwd(), "data", file_name + ".csv"))        
        print(index_datetime, " ", index_val)
    else:
        print("running...")
    time.sleep(5)
    index += 1
    if index >= 10:
        index = 0
        if name == 'nt':
            system('cls')
        else:
            system('clear')
    

