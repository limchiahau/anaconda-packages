#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import urllib.request as request
import pathlib


# In[2]:


package_list_url = 'https://docs.anaconda.com/anaconda/packages/py3.7_linux-64/'
output_file = pathlib.Path('anaconda-packages')


# In[3]:


# get the raw html for package_list_url
req = request.Request(package_list_url)
resp = request.urlopen(req)
html = resp.read().decode('utf-8')


# In[4]:


# replace check marks in the "In Installer column with the word True."
html = html.replace('<i class="fa fa-check"></i>', 'True')


# In[5]:


# create dataframe from the html
df = pd.read_html(html)[0]


# In[6]:


# keep packages that are included in the installer
df = df[df['In Installer'].notna()]


# In[7]:


df


# In[8]:


# remove packages starting with "_".
# The assumption is packages starting with "_"
# is not meant to be used by end-users.
df = df[~df['Name'].str.startswith('_')]


# In[9]:


# create a list of strings in the format:
# package==version
# 
# this makes it easier to pass into pip.
package_list = "'" + df['Name'] + "==" + df['Version'] + "'"
package_list


# In[10]:


#remove the output file if it already exists
try:
    output_file.unlink()
except:
    pass


# In[11]:


#save the package_list to a file
output_file.write_text('\n'.join(package_list))


# In[ ]:




