#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os
import sqlite3
from sqlalchemy import create_engine

data = pd.read_pickle('./hm_data - cleaned.pkl')


# In[2]:


def main():
    if os.path.exists('./hm_db.sqlite'):
        print('File exists')
        update()
    else:
        create_scheme()
        update()

    


# In[3]:


# 1st create table / query

def create_scheme():
    query_showroom_schema = """
        CREATE TABLE showrooms (
            color_id            INTEGER,
            job2_datetime       TEXT,
            sizes               TEXT,
            availability        TEXT,
            product_title       TEXT,
            color               TEXT,
            details_color       TEXT,
            stars               FLOAT,
            reviews             INTEGER,
            fit                 TEXT,
            composition         TEXT,
            length              TEXT,
            waist_rise          TEXT,
            material            TEXT,
            showcase_id         INTEGER,
            price_item          REAL,
            price_item_desc     REAL,
            description         TEXT,
            style_id            INTEGER,
            shell_cotton        REAL,
            shell_spandex       REAL,
            shell_polyester     REAL,
            shell_elasterell_p  REAL,
            pocket_lining_cotton REAL,
            pocket_lining_spandex  REAL,
            pocket_lining_polyester REAL,
            pocket_lining_elasterell_p REAL,
            lining_cotton       REAL,
            lining_spandex      REAL,
            lining_polyester    REAL,
            lining_elasterell_p REAL,
            aux_index           INTEGER
            )

    """
    # conn.close()

    # Connecting to db (actually na prática usamos essa linha só pra criar o arquivo do db)
    conn = sqlite3.connect('hm_db.sqlite')  # connect returns a connection

    # poderia apagar esse trecho:
    cursor = conn.execute(query_showroom_schema) #returns a cursor...
    conn.commit()  # needs to commit conn to db itself after creating cursor....
    conn.close()  # closes the connection to db - so it wont stay open.


# In[5]:



def update():
    conn = create_engine('sqlite:///hm_db.sqlite', echo=False)

    query = '''
        SELECT * FROM showrooms
    '''

    df = pd.read_sql_query(query, conn)
    df.head()

    # loading data to table  -- using pandas to_sql method
    data.to_sql('showrooms', con=conn, if_exists='append', index=False)

    df = pd.read_sql_query(query, conn)
    conn = sqlite3.connect('hm_db.sqlite')
    cursor = conn.execute(query)
    conn.commit()
    conn.close()
    df.head()


# In[8]:


main()


# In[ ]:




