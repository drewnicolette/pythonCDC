import hashlib
import os
from pathlib import Path
import glob
from datetime import datetime

def checkPath(path):
    if not os.path.exists(path):
        print("Path does not exist")
        os._exit(1)

def checkPrevFileExists(path):
    filesInDir = [file for file in os.listdir(path)]   
 
    if 'prev.' not in str(filesInDir):
        print("\n'prev' file does not exist there")
        createFile = input("\nDo you want to create it? (yes/no): ")
        if createFile=='yes':
            createPrevFile = "".join([path,"prev.csv"])
            Path(createPrevFile).touch()
            print("\nPrev File Created")

def checkArchiveDirsExist(path):
    prevDir = "".join([path,'prev_archive'])
    resultDir = "".join([path,'resultDir'])
    filesInDir = [file for file in os.listdir(path)]

    if ('prev_' not in str(filesInDir)) and ('result' not in str(filesInDir)):
        print("\nBoth the 'prev' and 'result' folders do not exist")
        createThem = input("\nDo you want to create them both? (yes/no): ")
        if createThem == 'yes':
            os.mkdir(prevDir)
            os.mkdir(resultDir)
        else:
            print("\nThese are needed for process to work... please create")
            os._exit(1)
    elif ('prev_' not in str(filesInDir)) and ('result' in str(filesInDir)):
        print("\nThe 'prev' archive folder does not exist")
        createPrev = input("\nDo you want to create the 'prev' directory? (yes/no): ")
        if createPrev == 'yes':
            os.mkdir(prevDir)
        else:
            print("\nThis is needed for process to work... please create")
            os._exit(1)
    elif ('prev_' in str(filesInDir)) and ('result' not in str(filesInDir)):
        print("\nThe 'result' folder does not exist")
        createCurr = input("\nDo you want to create the 'result' directory? (yes/no): ")
        if createCurr == 'yes':
            os.mkdir(resultDir)
        else:
            print("\nThis is needed for process to work... please create") 
            os._exit(1)

def checkSum(path):
    csv_files = glob.glob("".join([path,'*.csv']))
    if len(csv_files) < 2:
        print("\nPlease check both the curr and prev file exist!")
        os._exit(0)

    digests = []
    for filename in csv_files:
        hasher = hashlib.md5()
        with open(filename, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
            get_hash = hasher.hexdigest()
            digests.append(get_hash)

    if digests[0] == digests[1]:
        return True
    else:
        return False 

def movePrevFile(path,file='prev.csv'):
    full_path = "".join([path,file])
    fileSplit = os.path.splitext(file)[0]
    dateTime = datetime.now()
    dateTimeStr = dateTime.strftime("%m_%d_%Y_%H:%M:%S")
    filename = "".join([fileSplit,dateTimeStr,".csv"])
    filenameAndPath = "".join([path,'prev_archive/',filename])
    os.rename(full_path,filenameAndPath)

def RenameCurrtoPrev(path,file='curr.csv'):
    fullCurrPath = "".join([path,file])
    fullPrevPath = "".join([path,'prev.csv'])
    os.rename(fullCurrPath,fullPrevPath)
    
