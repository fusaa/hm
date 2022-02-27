#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import re
import numpy as np
from sys import exit

df = pd.read_csv('./hm_data.csv', dtype={'color_id': object, 'showcase_id': str}) # TODO ignore_index


# In[ ]:


df = df.drop('Unnamed: 0', axis=1)
df.insert(0, 'job2_datetime', pd.to_datetime('now').replace(microsecond=0))
# df.columns
# print(df.head())

df.loc[1,'job2_datetime']


# In[ ]:


# 2 FORMATTING COLUMNS ITEMS


# Drop NaN
# df.isna().sum()
# df.notnull()  # returns true if it is not null
# df = df.dropna( subset = ['availability'])
df['availability'] = df['availability'].apply(lambda x: x.replace(' ', '_').lower())
df['product_title'] = df['product_title'].apply(lambda x: x.replace(' ', '_').lower())
df['price_item'] = df['price_item'].apply(lambda x: x.replace('$', '').lower()).astype(float)
df['price_item_desc'] = df['price_item_desc'].apply(lambda x: x.replace('$', '').lower()).astype(float)

df['stars'] = df['stars'].apply(lambda x: 0 if x == 'NoStarsData' else x).astype(float)
df['job2_datetime'] = pd.to_datetime( df['job2_datetime'], format= '%Y-%m-%d %H:%M:%S')  # not necessary since used a function for creating it.
df['details_color'] = df['details_color'].apply(lambda x: str(x).replace("\'", "").replace(", ", ".").replace(" ", "_").replace("-","_").lower()[1:-1])
df['color'] = df['color'].apply(lambda x: x.replace(" ", "_").lower())
df['color'] = df['color'].apply(lambda x: x.replace("/", "_").lower())
df['length'] = df['length'].apply(lambda x: str(x)[2:-2].lower())
df['material'] = df['material'].apply(lambda x: str(x)[2:-2].replace('\', \'', "_").lower())

df['waist_rise'] = df['waist_rise'].apply(lambda x: str(x).replace(' ', '_')[2:-2].lower())

# df['stars'] = df['stars'].astype(float)
#create style_id column:
df['style_id'] = df['color_id'].apply(lambda x: str(x)[:-3]).astype(str)
df['fit'] = df['fit'].apply(lambda x: str(x)[2:-2].replace(' ', '_').lower()).astype(str)
df['details_color'].unique()

# df['material'].unique()


# df.iloc[3826]

df['color'] = df['color'].apply(lambda x: x.replace(' ', '_').lower()).astype(str)


# In[ ]:



# 3  FORMATTING COMPOSITION 

b = "\"[\'"
# df trim
# df = df.iloc[44:266]

df['composition'] = df['composition'].apply(lambda x: re.sub('\[', "", str(x)))
df['composition'] = df['composition'].apply(lambda x: re.sub('\]', "", str(x)))
df['composition'] = df['composition'].apply(lambda x: re.sub('\'', "", str(x)))


df['composition'] = df['composition'].apply(lambda x: x.replace(",",""))
df['composition'] = df['composition'].apply(lambda x: x.replace("Pocket lining:","pocket_lining"))
df['composition'] = df['composition'].apply(lambda x: x.replace("Shell:","shell"))
df['composition'] = df['composition'].apply(lambda x: x.replace("Lining:","lining"))

df['composition'] = df['composition'].apply(lambda x: x.replace("Cotton","cotton"))
df['composition'] = df['composition'].apply(lambda x: x.replace("Spandex","spandex"))
df['composition'] = df['composition'].apply(lambda x: x.replace("Polyester","polyester"))
df['composition'] = df['composition'].apply(lambda x: x.replace("Elasterell-P","elasterell_p"))
# df['composition'].unique()


# In[ ]:


# 4 COMPOSITION SEPARATE COLUMNS CREATION
df['shell_cotton'] = np.NaN  # NaN or 0 ?  like 0% in the composition
df['shell_spandex'] = np.NaN
df['shell_polyester'] = np.NaN
df['shell_elasterell_p'] = np.NaN

df['pocket_lining_cotton'] = np.NaN  # NaN or 0 ?
df['pocket_lining_spandex'] = np.NaN
df['pocket_lining_polyester'] = np.NaN
df['pocket_lining_elasterell_p'] = np.NaN

df['lining_cotton'] = np.NaN  # NaN or 0 ?
df['lining_spandex'] = np.NaN
df['lining_polyester'] = np.NaN
df['lining_elasterell_p'] = np.NaN


# 5 COMPOSITION FUNCTION FILTER_COMP

def filter_comp(data, aux_index):
    lis = data.split(" ")
    #print(lis)
    shell = []
    type_materials_list = ['cotton', 'spandex', 'polyester', 'elasterell_p' ]  # TODO -> list auto generation
    item_parts = ['shell', 'lining', 'pocket_lining']  # TODO -> list auto generation

    id_ed = False
    current_part = ''
    current_list = []
    to_100 = 0
    p_n = 0
    current_index = 0
    
    print("Doing index: "  + str(aux_index))
    for a in range(len(lis)):
        if (a > current_index) | (a == 0):  # so we resume classifying at the right part....
            if lis[a] in item_parts:  #this works with list start with an item part....
                print(" **** **** found part: " + str(lis[a]))
                
                current_part = str(lis[a])
                current_list = []
                
                p_n = a + 1
                to_100 = 0  # counter to 100% item, so it knows when that item part is finished
                
            if (lis[a] not in item_parts) & (a == 0):
                print(" *** *** assuming  part: shell ")
                
                current_part = 'shell'
                current_list = []
                
                p_n = a
                to_100 = 0  # counter to 100% item, so it knows when that item part is finished
                
            if (lis[a] not in item_parts) & (a != 0) & (to_100 >= 100):
                print(" ** assuming just got 100% of part: now doing this PART " + str(lis[a]) + 'as SHELL')
                
                current_part = 'shell'
                current_list = []
                
                p_n = a
                to_100 = 0  # counter to 100% item, so it knows when that item part is finished
                
                
            while (p_n < len(lis)):
                if bool(re.search("^[0-9]%", lis[p_n])) | bool(re.search("^[0-9][0-9]%", lis[p_n])) | bool(re.search("^[0-9][0-9][0-9]%", lis[p_n])):  # of course no value over 100%, could use the 100% on regex...
                    to_100 += int(lis[p_n][:-1])
                    print('100 count = ' + str(to_100))
                    # current_list.append(lis[p_n])  # put data in the list till ... 100% or another item is found. or end of list
                    if to_100 >= 100:
                        print('100% break')
                        # to_100 = 0 will get zero´ed on the tests at the beggining of func

                        # check if list continues
                        # dont think it is necessary - TODO check on results. 
                        # TODO:  WARNING - TODO - Case shell starts
                        # later w/ no title indicating it is shell from that point.
                        current_index = p_n  # so we know where to restart for
                        # p_n = 0 # doing on the if tests at beggining
                        current_list.append(lis[p_n]) #append current item since there´s a break after
                        break

                    if (lis[p_n] in item_parts) | (p_n == len(lis) - 1):  # so it stops counting when finds another item or end
                        current_index = p_n
                        p_n = 0
                        break
                        
                current_index = p_n
                current_list.append(lis[p_n])
                p_n +=1
                print(current_part + str(current_list))

            # print straitght to df new column values
            # TODO: Check if necessary more code for shell in the middle of list without announcement.
       
        # Let´s write data straight to dataframe: ( iloc?)
        # TODO ... a for loop w/ lists could make things better, though harder to understand...
        # necessary for these if´s statement to be inside the WHILE! loop (running multiple time with right result)
        # it could be made more efficient.
        
            if current_part == 'shell':
                print('I have at current part ' + str(current_part) + 'list '+ str(current_list))
                if 'cotton' in current_list:
                    df.loc[aux_index,'shell_cotton'] = current_list[(current_list.index('cotton')) + 1]  
                if 'spandex' in current_list:
                    df.loc[aux_index,'shell_spandex'] = current_list[(current_list.index('spandex')) + 1]
                if 'polyester' in current_list:
                    df.loc[aux_index,'shell_polyester'] = current_list[(current_list.index('polyester')) + 1]
                if 'elasterell_p' in current_list:
                    df.loc[aux_index,'shell_elasterell_p'] = current_list[(current_list.index('elasterell_p')) + 1]

            if current_part == 'pocket_lining':
                print('I have at current part ' + str(current_part) + 'list '+ str(current_list))
                if 'cotton' in current_list:
                    df.loc[aux_index,'pocket_lining_cotton'] = current_list[(current_list.index('cotton')) + 1]
                if 'spandex' in current_list:
                    df.loc[aux_index,'pocket_lining_spandex'] = current_list[(current_list.index('spandex')) + 1]
                if 'polyester' in current_list:
                    df.loc[aux_index,'pocket_lining_polyester'] = current_list[(current_list.index('polyester')) + 1]
                if 'elasterell_p' in current_list:
                    df.loc[aux_index,'pocket_lining_elasterell_p'] = current_list[(current_list.index('elasterell_p')) + 1]

            if current_part == 'lining':
                print('I have at current part ' + str(current_part) + 'list '+ str(current_list))
                if 'cotton' in current_list:
                    df.loc[aux_index,'lining_cotton'] = current_list[(current_list.index('cotton')) + 1]  
                if 'spandex' in current_list:
                    df.loc[aux_index,'lining_spandex'] = current_list[(current_list.index('spandex')) + 1]
                if 'polyester' in current_list:
                    df.loc[aux_index,'lining_polyester'] = current_list[(current_list.index('polyester')) + 1]
                if 'elasterell_p' in current_list:
                    df.loc[aux_index,'lining_elasterell_p'] = current_list[(current_list.index('elasterell_p')) + 1]
                    
df['aux_index'] = df.apply(lambda row: row.name, axis=1)
  
df[['composition','aux_index']].apply(lambda x: filter_comp(x['composition'],x['aux_index']), axis = 1)


# In[ ]:


# 6 SAVES PICKLE FILE
# save a pickefile - keeps python formats ; serialization

df.to_pickle('./hm_data - cleaned.pkl')


# In[ ]:




