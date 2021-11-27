import os 

def find_data():
    if not os.listdir('../data/new'):
        print("Directory is empty")
    else:    
        print("Directory is not empty")

find_data()