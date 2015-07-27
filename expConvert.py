import sys
import argparse
import csv

#set commandline args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Specify file location")
parser.add_argument("-d", "--debug", help="Debug Info", action="store_true") 

#Set file path manually, commandline overrides
#example file_path = r""
file_path = None
global debug
list_items = []
list_mods = []
menu_group = {}
menu_category = {}

def parse_file():
    with open(file_path, 'r') as fileRead:
        x=0
        for line in csv.reader(fileRead, delimiter=',',  skipinitialspace=True):
            if(debug): print(line[0])
            if(line[0] == 'MenuCategories'):
                cat_key = ''
                cat_name = ''
                for item in line:
                    if ('MenuCategoryID' in item):
                        if(debug): print(item)
                        cat_key = int(item.split('<=>')[1])
                    if ('MenuCategoryText' in item):
                        cat_name = item.split('<=>')[1]
                menu_category[cat_key] = cat_name;
            if(line[0] == 'MenuGroups'):
                group_key = ''
                group_name = ''
                for item in line:
                    if ('MenuGroupID' in item):
                        group_key = int(item.split('<=>')[1])
                    if ('MenuGroupText' in item and not 'SecLangMenuGroupText' in item):
                        if(debug): print(item)
                        group_name = item.split('<=>')[1]
                menu_group[group_key] = group_name;
            if(line[0] == 'MenuItems'):
                newItem = MenuItem();
                for item in line:
                    if( item.split('<=>')[0] == "MenuCategoryID"):
                        key = int(item.split('<=>')[1])
                        newItem.category = menu_category[key]
                    if( item.split('<=>')[0] == "MenuGroupID"):
                        key = int(item.split('<=>')[1])
                        newItem.group = menu_group[key]
                    if( item.split('<=>')[0] == "MenuItemText"):
                        newItem.name = item.split('<=>')[1]
                    if( item.split('<=>')[0] == "DefaultUnitPrice"):
                        newItem.price = item.split('<=>')[1]
                list_items.append(newItem)
            if(line[0] == 'MenuModifiers'):
                newMod = Modifier();
                for item in line:
                    if( item.split('<=>')[0] == "SecLangModifierText"):
                        newMod.sec_name = item.split('<=>')[1]
                    if( item.split('<=>')[0] == "MenuModifierText"):
                        newMod.name = item.split('<=>')[1]
                    if( item.split('<=>')[0] == "AdditionalCost"):
                        newMod.price = item.split('<=>')[1]
                list_mods.append(newMod)

        fileRead.close()
        with open("parsedDocument.txt", 'w') as file_write:
            file_write.write("--------------------------------------Menu Items----------------------------------------\n")
            for item in list_items:
                file_write.write("Item Name: " + item.name + "| Price: $" + item.price + "| Category: " + item.category + "| Group: " + item.group+"\n")
            file_write.write("---------------------------------------------------------------------------------------\n")
            file_write.write("--------------------------------------Modifiers----------------------------------------\n")
            for item in list_mods:
                file_write.write("Modifier: " + item.name + " | Addtional Price: $" + item.price + "| Spanish: " + item.sec_name + "\n")
            file_write.close()

class MenuItem:
    """Object to Store Menu Items Information"""
    def __init__(self):
        self.name = ""
        self.price = ""
        self.group = ""
        self.category = ""


class Modifier:
    def __init__(self):
        self.name = ""
        self.sec_name = ""
        self.cost = ""
        



#Main entry point
def main():
    global file_path
    global debug
    args = parser.parse_args()
    debug = args.debug
    #just commandline arg handling
    if (args.file != None):
        file_path = args.file
    elif(file_path is None):
        raise ValueError("File path not defined, Type -h for help")
        
    #debug print
    if(debug):
        print(file_path)

    #begin parsing file
    parse_file()

if __name__ == "__main__":
    main()

