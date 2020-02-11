import functions as f
import cdc as c
import os
import time

def main():
    path = '/home/drewnicolette/Desktop/compare/'
    column_names = ['id','first','last','salary']

    f.checkPath(path)
    f.checkPrevFileExists(path)
    f.checkArchiveDirsExist(path)
    if f.checkSum(path) == True:
        print("\nNo change in files")
        f.movePrevFile(path)
        time.sleep(1)
        f.RenameCurrtoPrev(path)
        os._exit(0)
   
    c.addResultsFile(path,column_names)
    #Check if results file has zero or one file in it
    #NiFi should be running and consuming those files so there should be more than one
    f.movePrevFile(path)
    time.sleep(1)
    f.RenameCurrtoPrev(path)

if __name__ == "__main__":
    main()
