import pandas as pd
import glob

path = '/home/drewnicolette/Desktop/compare/'
column_names = ['id','first','last','salary'] 
csv_files = glob.glob("".join([path,'*.csv']))

old = pd.read_csv(csv_files[1],header=None,names=column_names,dtype={'id':str})
new = pd.read_csv(csv_files[0],header=None,names=column_names,dtype={'id':str})

#Adding column with old and new
old['version'] = 'old'
new['version'] = 'new'

full_set = pd.concat([old,new], ignore_index=True)
changes = full_set.drop_duplicates(subset=column_names,keep='last')

set_ind = changes.set_index('id')
def getDuplicatedIndexes(df):
    dict1 = {}
    for row in df.index:
        if row not in dict1:
            dict1[row] = 1
        else:
            dict1[row] += 1
    
    final_list = []

    for key,value in dict1.items():
        if value > 1:
            final_list.append(key)

    return final_list
            
dupe_names = getDuplicatedIndexes(set_ind)
dupes = changes[changes['id'].isin(dupe_names)]

change_new = dupes[(dupes['version'] == 'new')]
change_old = dupes[(dupes['version'] == 'old')]

change_new.set_index('id',inplace=True)
change_new['statement'] = 'update'
change_old.set_index('id',inplace=True)

#diff_panel = pd.Panel(dict(df1=change_old,df2=change_new))
#diff_output = diff_panel.apply(report_diff,axis=0)
removal = changes
removal['duplicate'] = removal['id'].isin(dupe_names)
removed_rows = removal[(removal['duplicate'] == False) & (removal['version'] =='old')]
removed_rows.set_index('id',inplace=True)
removed_rows['statement'] = 'delete'

added_rows = full_set.drop_duplicates(subset=column_names)
added_rows['duplicate'] = added_rows['id'].isin(dupe_names)
added_rows_final = added_rows[(added_rows['duplicate'] == False) & (added_rows['version'] == 'new')]
added_rows_final.set_index('id',inplace=True)
added_rows_final['statement'] = 'insert'

df1 = pd.concat([change_new,added_rows_final,removed_rows])
df1 = df1.reset_index()
df1 = df1.drop(columns=['version','duplicate'])
df1.to_csv("".join([path,'results.csv']),index=False,header=True)
