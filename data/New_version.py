#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import pylab as plt
import seaborn as sns
import statistics

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


pd.set_option('display.max_columns', None)  # es para enseñar todas las columnas del df

import warnings
warnings.simplefilter('ignore')


# In[3]:


shark=pd.read_csv('../data/attacks.csv',encoding="latin1")


# In[4]:


shark.head()


# In[5]:


nan_cols=shark.isna().sum()
nan_cols[nan_cols>0]


# In[6]:


def check_nan(df):
    
    nan_cols=shark.isna().mean() * 100
    
    display(f'N nan cols: {len(nan_cols[nan_cols>0])}')
    display(nan_cols[nan_cols>0])
    
    plt.figure(figsize=(10, 6))

    sns.heatmap(df.isna(),  # mapa de calor
                yticklabels=False,
                cmap='viridis',
                cbar=False)
    
    plt.show();


# In[7]:


check_nan(shark)


# In[8]:


#lista de filas en las que todos los valores son nulos

nan_rows=shark.index[shark.isnull().all(1)] 
nan_rows


# Podemos eliminar 5145 filas (hasta el 20%) 

# In[9]:


rows_eliminate=[]

for i in range(5145):
    
    rows_eliminate.append(nan_rows[i])
    


# In[10]:


len(rows_eliminate)


# In[11]:


shark.drop(rows_eliminate,axis=0,inplace=True)


# In[12]:


shark.shape


# Ya hemos eliminado el mayor numero de filas con todo nulos que podemos

# # ELIMINANDO NULOS

# In[13]:


shark.info()


# ### Columnas "Unnamed"

# Ambas columnas están completamente vacias por lo que las vamos a rellenar de ceros

# In[14]:


shark["Unnamed: 22"]=0
shark["Unnamed: 23"]=0


# ### Columnas con categorias  

# Las columnas que son categorias como (type, country, Area, location, Activity, Name, Sex, Age, Injury, Fatal...) las vamos a rellenar sus NAN con unknown por el momento ya que si no hay valor es que en principio no tenemos información.

# In[15]:


shark[["Type","Country","Area","Location","Activity","Name","Sex ","Age","Injury","Fatal (Y/N)","Time","Species ","Investigator or Source","pdf","href formula","href"]]=shark[["Type","Country","Area","Location","Activity","Name","Sex ","Age","Injury","Fatal (Y/N)","Time","Species ","Investigator or Source","pdf","href formula","href"]].fillna("Unknown")


# In[16]:


check_nan(shark)


# ### Columnas Case Number

# La columna Case number son fechas, por lo que finalmente vamos a querer tenerla como date type. Antes de eliminar los nulos vamos a limpiarla de manera que solo nos queden fechas

# In[17]:


shark["Case Number"]=shark["Case Number"].str.extract(r'(\d\d\d\d.\d\d.\d\d)') 


# He usado Regex para seleccionar las fechas en formato yyyy.mm.dd, de esta manera los elementos del final que son i.e ND-0154 se eliminan ya que no sabemos si esos números hace referencia al año, dia, mes....
# 
# Rellenamos los nan con la última fecha disponible ya que es la mas cercana

# In[18]:


shark["Case Number"]=shark["Case Number"].str.replace('.', '-')


# In[19]:


shark["Case Number"].tail()


# In[20]:


shark.replace({"Case Number":{"00":"01","/":"-",",":"-","2014-17-28":"2014-12-28"}},inplace=True)


# Cambiamos el tipo de dato da "datetime" con "errors=corerce"

# In[21]:


shark["Case Number"]=pd.to_datetime(shark["Case Number"], format='%Y-%m-%d',errors = 'coerce')


# Rellenamos los valores nulos con la última fecha disponible ya que será la más cercana de las que tenemos

# In[22]:


shark["Case Number"].fillna(method="ffill",inplace=True)


# Sobreescribimos columna Case Number.1 y 2 ya que hemos hecho:
# len(shark.drop_duplicates(subset=["Case Number.1","Case Number.2"]))==len(shark) 
# y hemos visto que son exactamente iguales a "Case Number"

# In[23]:


shark["Case Number.1"]=shark["Case Number"]


# In[24]:


shark["Case Number.2"]=shark["Case Number"]


# Hacemos lo mismo con la columna "Date"

# In[25]:


shark["Date"]=shark["Case Number"]


# In[26]:


check_nan(shark)


# ### Columna "Year"

# In[27]:


pd.set_option("display.max_rows",None)


# Como los años van en orden, vamos a rellenar los nulos con el año equivalente a su índice en la columa Date

# In[28]:


shark.Year.head()


# In[29]:


nan_rows=shark[shark['Year'].isna()].index
nan_rows


# Como la columna Date tiene formato yyyy-mm-dd, queremos que solo se queden los 4 primeros números. Es decir, el año

# In[30]:


shark["años_date"]=shark["Date"]


# In[31]:


shark["años_date"]=shark["años_date"].astype(dtype="str")


# In[32]:


shark["años_date"]=shark["años_date"][nan_rows].str.extract('(\d\d\d\d)')


# In[33]:


shark.Year[nan_rows]=shark["años_date"][nan_rows]


# Eliminamos la columna "años_date" ya que no la necesitamos más

# In[34]:


shark.drop("años_date",axis=1,inplace=True)


# ### Columna original order

# In[35]:


shark["original order"].head()


# In[36]:


nan_rows=shark[shark['original order'].isna()].index
nan_rows


# In[37]:


for i in nan_rows:
    
    shark["original order"][nan_rows]=i+2


# In[38]:


check_nan(shark)


# Ya hemos eliminado todos los nulos

# # LIMPIEZA DE COLUMNAS

# ### Columna "Age"

# In[39]:


shark.Age.head()


# 
# Vamos a rellenar los nulos de la columna age con la media de edad de los datos que tenemos ya que nos conviene mantener en la columna todo valores numéricos en lugar de añadir alguna categoría como "unknown", por lo que vamos a sustituir los "unknown" que habiamos puesto antes por la media

# Hay valores que tienen letras, por lo que cogemos solo los valores numéricos

# In[40]:


shark["Age"]=shark.Age.str.extract(r'(\d\d)')


# In[41]:


shark.Age.fillna(0,inplace=True)


# In[42]:


shark.Age=shark.Age.astype(dtype="int8")


# In[43]:


shark.Age.replace(0, shark.Age.mean(),inplace=True) #sustituimos los 0 por la media 


# ### Columna "Sex"

# In[44]:


shark.rename(columns={"Sex ":"Sex"},inplace=True) #renombramos la columna para quitar el espacio


# In[45]:


shark.Sex.unique()


# Queremos dejar solo 3 categorias: F, M, Unknown, por lo que vamos a sustituir las otras

# In[46]:


shark.replace({"Sex":{"M ":"M","lli":"Unknown","N":"M",".":"Unknown","Afternoon":"Unknown","Morning":"Unknown","Late Afternoon":"Unknown"}},inplace=True)


# In[47]:


shark.Sex.unique()


# ### Columna "Name"

# En esta columna quiero dejar el contenido de cada elemento limpio, pero no voy a decidir yo si es un nombre o no, por lo que voy a quitar signos de puntuación,números...

# In[48]:


shark.replace({"Name":{"male":"Unknown",".":"",":":"","Occupant":"","occupants":""}},inplace=True)


# Luego quizás intente limpiar más la columna, pero por el momento avanzamos

# ### Columna "Species"

# Esta columna está hecha un desastre, solo me van a interesar aquellas que especifiquen el tipo de tiburón por lo que voy a coger solo la primera palabra antes de "shark" i.e. the white shark cojo "white" >> luego podemos seguir limpiando

# In[49]:


shark.rename(columns={"Species ":"Species"},inplace=True) #Renombramos para quitar el espacio


# In[50]:


shark.Species=shark.Species.str.extract(r'(\w+)\s+shark')


# In[51]:


shark.Species.fillna("Unknown",inplace=True)


# In[52]:


shark.Species.unique()


# In[53]:


shark.replace({"Species":{" m ":"Unknown","\d":"Unknown","same":"","Unknown":"","as":"Unknown","the":"unknown"}},inplace=True)


# In[54]:


shark.Species.unique()


# ### Columna Time

# In[55]:


shark.Time.head()


# Vamos a crear una nueva columna "nuevo_time" que nos coja la hora a la que ha sido el ataque

# In[56]:


shark["nuevo_time"]=shark.Time.str.extract(r'(\d\d)')


# In[57]:


shark["nuevo_time"].fillna("0",inplace=True)


# In[58]:


shark["nuevo_time"]=shark["nuevo_time"].astype(dtype="int16")


# Vamos a categorizar la columna Time de manera que tengamos tres opciones: "Morning", "Afternoon", "Late Afternoon"

# In[59]:


shark["nuevo_time"][(shark["nuevo_time"]>0) & (shark["nuevo_time"]<13)]=-1


# In[60]:


shark["nuevo_time"][(shark["nuevo_time"]<20) & (shark["nuevo_time"]>=13)]=-2


# In[61]:


shark["nuevo_time"][shark["nuevo_time"]>20]=-3


# In[62]:


shark.nuevo_time.head()


# In[63]:


shark["nuevo_time"][shark["nuevo_time"]==-1]="Morning"
shark["nuevo_time"][shark["nuevo_time"]==-2]="Afternoon"
shark["nuevo_time"][shark["nuevo_time"]==-3]="Late Afternoon"


# Vamos a añadir en la columna "nuevo_time" donde hay ceros queremos meter los valores de la columna Time correspondientes, de manera que solo tengamos strings

# In[64]:


index1=shark[shark["nuevo_time"]==0].index


# In[65]:


shark["nuevo_time"][index1]=shark.Time[index1]


# In[66]:


shark.nuevo_time.unique()


# Queremos reducir estas características a la siguientes: Morning, Afternoon y Late Afternoon

# In[67]:


shark.replace({"Time":{"Midday":"Afternoon","9h00":"Morning","Early morning":"Morning","Just before noon":"Morning","Sunset":"Late Afternoon","Evening":"Afternoon","--":"unknown","Early morning":"Morning","Morning ":"Morning","Early Morning":"Morning","Mid afternoon":"Afternoon","Mid morning":"Morning","AM":"Morning","Mid-morning":"Morning","Daytime":"unknown","After lunch":"Afternoon","Dawn":"Late Afternoon","morning":"Morning","Daybreak":"unknown","After lunch":"Afternoon","night":"Late Afternoon",'"Early evening"':"Afternoon","Before daybreak":"Afternoon","Dusk":"Afternoon","After Dusk":"Late Afternoon",'"After lunch"':"Afternoon","A.M.":"Morning","P.M.":"Afternoon","Midday.":"Afternoon",'"After dark"':"Late Afternoon"," ":"unknown","Late afternon":"Late Afternoon","dusk":"Afternoon",0:"unknown",'"Evening"':"Afternoon","2 hours after Opperman":"unknown"}},inplace=True)


# In[68]:


shark.nuevo_time.unique()


# #### Luego continuamos quitando categorias

# ### Columna "Fatal (Y/N)"
# 

# In[69]:


shark["Fatal (Y/N)"].unique()


# Queremos que solo estén las categorias Y y N

# In[70]:


shark.replace({"Fatal (Y/N)":{"Afternoon":"Unknown","Morning":"Unknown","Late Afternoon":"Unknown","M":"Unknown","UNKNOWN":"Unknown","2017":"Unknown"," N":"Unknown","N ":"Unknown","y":"Unknown","unknown":"Unknown"}},inplace=True)


# In[71]:


shark["Fatal (Y/N)"].unique()


# In[72]:


shark.columns


# In[73]:


shark.head()


# In[74]:


shark_final_otro=shark.copy(deep=True)


# In[75]:


shark_final_otro.to_csv('../data/shark_final_otro.csv', index=False)


# In[ ]:




