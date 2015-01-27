'''
Created on 12.08.2013

@author: Clemens
'''


folder_name='\QT_Trial'

import os
import sys
#os.chdir(os.getcwd()+folder_name)


def convert_ui_files(folder='/UIFiles'):
    old_path=os.getcwd()
    new_path=os.getcwd()+folder
    os.chdir(new_path)
    for file in os.listdir('.'):
        if file.endswith(".ui"):
            filename=str(file).split('.')[0]
            if sys.platform == 'darwin':
                cmd='pyuic4-2.7 '+file +' > '+filename+'.py'
            else:
                cmd='pyuic4-2.7 '+file +' > '+filename+'.py'
            print cmd
            os.system(cmd)
    os.chdir(old_path)

if __name__=="__main__":
    convert_ui_files()