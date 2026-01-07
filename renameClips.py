import re #regular expressions
import os #to handle file paths for different operating systems
import fileinput

'''
WARNING: This code will rename all .wav files in the working directory and all subdirectories, so use carefully!
'''

os.chdir('./') # change functioning directory to the folder of this file

def bashPause():
    try:
        programPause = raw_input("Press the <ENTER> key to continue... (raw input)")
    except:
        programPause = input("Press the <ENTER> key to continue...")

layers = 1
print("How many sound layers are in each recording (such as _3)?")
try:
    layers = input()
except ValueError:
    print("That wasn't a valid integer. We'll just assume 1 layer.")
    layers = 1
    
layers = int(layers)

i = 1
renames = []

while i <= layers:
    print("What should we rename _" + str(i) + " files?")
    try:
        rename = str(input())
        #add underscore if there isn't one already
        #if rename[0] != "_":
        #   rename[0] = "_" + rename[0]
        renames.append(rename)
    except ValueError:
        print("That wasn't a valid string. We'll just keep it as is.")
    i += 1

directory = os.getcwd()

for path, folders, files in os.walk(directory):

    i = 0
    folder_name = ""

    for filename in files:

        if folder_name != path.split(os.path.sep)[-1]:
            # when hitting new folder, refresh the take count
            folder_name = path.split(os.path.sep)[-1]
            take = 1
            i = 0

        filename_arr = filename.split('.') # split off file extension
        
        if filename_arr[1] == "wav":
            if filename_arr[0][-2] == "_":
                layer = int(filename_arr[0][-1]) - 1 # get the layer number, which is the last character before .extension. Subtract 1 to get correct index from array
                filename_arr[0] = filename_arr[0][0:-1]
                
                # Finally, rename the file
                rename = ""
                if len(renames) > layer:
                    rename = renames[layer]

                new_file_name = os.path.join(folder_name, folder_name + '-T' + str(take) + '_' + rename + '.' + filename_arr[1])
                print(new_file_name)
                oldName = os.path.join(folder_name, filename)
                os.rename(oldName, new_file_name)
                if layer + 1 >= layers: # once we've cycled through all the layers, it's a new take
                    take += 1
            else:
                print("Cannot get layer number for " + filename)

        else:
            print(filename + " is not a wav file")

print("File renames complete!")
bashPause()

