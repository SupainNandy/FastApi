# python have Dynamic typing support,not support static typing like c,c++,cnad java
# python dont support type validation

#problem
# def insert_patent_data(name,age):
#     print(name)
#     print(age)
#     print('Insert into database')

# insert_patent_data('ram','rupam')

# ----------------------------------------------------------------------------------------------------------------------------------------------------

#problem two -> if i give type hinting that also not give error becouse this typehint give suggestion while coding not error ditect
# def insert_patent_data(name:str,age:int): 
#     print(name)
#     print(age)
#     print('Insert into database')

# insert_patent_data('ram','rupam')

#-------------------------------------------------------------------------------------------------------------------------------------------------
#problem 3: this way we can create type error validation 
# def insert_patent_data(name:str,age:int): 
#    if type(name)==str and type(age)== int:
#      print(name)
#      print(age)
#      print('Insert into database')
#    else:
#       raise TypeError("Incorrect DataType")

# insert_patent_data('ram','rupam')

#--------------------------------------------------------------------------------------------------------------------------------
# problem 4: data validation, i want age is not go to negative number
def insert_patent_data(name:str,age:int): 
   if type(name)==str and type(age)== int:
     if(age<0):
        raise ValueError('Age cant go negative')
     print(name)
     print(age)
     print('Insert into database')
   else:
      raise TypeError("Incorrect DataType")

insert_patent_data('ram',-9)

