import os 
def CompanyNameRecog(CompanyName):
    file = open("company2.txt","r")
    content = file.readlines()
    for var in content:
        if CompanyName in var:
            return True    
    return False