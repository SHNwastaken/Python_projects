import os
from collections import Counter
import argparse
from openpyxl import Workbook
def file_ext_finder(path):
    o=os.path.join(path, "file_extensions.xlsx")
    file_ext=Counter()
    file_ext2=Counter()
    rows=[]
    for current,subdir,files in os.walk(path):
        print("")
        rel_path=os.path.relpath(current,path)
        if rel_path == ".":
            print(f'Inside {os.path.basename(path)}')
        else:
            print(f'Inside {rel_path}')
        for file in files:
            ext=file.rsplit('.',1)[-1]
            file_ext[ext]+=1
            file_ext2[ext]+=1
        for extname,count in file_ext.items():
         print("No of",extname," in folder:",count)
        for ext,count in file_ext.items():
            rows.append([os.path.normpath(current),ext,count]) 
        file_ext.clear()  
    print(" ")
    print("Total Unique No of Extensions in given directory")    
    for extname2,count2 in file_ext2.items():
        print("Total No of",extname2," in directory:",count2)
    save_to_excel(rows,o,file_ext2) 


def save_to_excel(rows,output,file_ext2):
    sum=0
    workbook=Workbook()
    sheet=workbook.active
    sheet.title='File Extensions'
    sheet.append(['Path','Extension Type','Count'])
    for row in rows:
        sheet.append(row)
    for row in range(2,sheet.max_row+1):
        sum+=sheet[f'C{row}'].value
    sheet.append([''])    
    for extname2,count2 in file_ext2.items():
        sheet.append([f'Total .{extname2}','',count2]) 
    sheet.append(['']) 
    sheet.append(['Total no of files: ',' ',sum ]) 
    workbook.save(output)
    print(f'Data saved to {output}')  

def main():
    parser = argparse.ArgumentParser(description='Count file extensions in a directory.')
    parser.add_argument('--path', type=str,default=os.getcwd() ,help='Path to the folder to scan')
    args=parser.parse_args()

    file_ext_finder(args.path)
if __name__ == "__main__":
    main()    