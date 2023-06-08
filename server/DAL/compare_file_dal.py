import os
import sys 
import numpy as np
import io
import openpyxl
import xlsxwriter as pd

from json.decoder import JSONDecodeError
import pandas as pd
#!/usr/bin/env python
# -*- coding: utf-8 -*-
class CompareFileDal:
    def __init__(self):
        self.__path = os.path.join(sys.path[0],'data/users.json')

    def read_file(self,link_to_file):
        link = link_to_file["link"]
        try:
            workbook = pd.read_excel(link, engine = 'openpyxl')
            return workbook
        except:
            return({"Error":"The system does not find the link: {}".format(link)})
            
    
    def write_file(self,link_to_file,basic_data,data_from_web):
        link = link_to_file["link"]
        try:
            df = pd.DataFrame(data_from_web,columns=basic_data.columns)
            output = io.BytesIO()
            writer = pd.ExcelWriter(link, engine='xlsxwriter')

            df.to_excel(writer, sheet_name='Sheet1',index=False)
            workbook  = writer.book
            worksheet = writer.sheets['Sheet1']
            green = workbook.add_format({'bg_color': '#008000'})
            red = workbook.add_format({'bg_color': '#FF0000'})

            for row in range(1, df.shape[0]+1):
                value1 = df.at[row-1,basic_data.columns[len(basic_data.columns)-2]]
                value2 = df.at[row-1,basic_data.columns[len(basic_data.columns)-1]]
                if str(value1) == str(value2):
                    worksheet.set_row(row, cell_format=green)
                else:
                    worksheet.set_row(row, cell_format=red)
            writer.close()
            xlsx_data = output.getvalue()
        except:
            return({"Error":"The system failed to save the data to the file : {}".format(link)})