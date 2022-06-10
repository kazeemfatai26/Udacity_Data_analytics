#!/usr/bin/env python
# coding: utf-8

# ## Gather

# In[2]:


import pandas as pd
import re as re


# In[3]:


patients = pd.read_csv('patients.csv')
treatments = pd.read_csv('treatments.csv')
adverse_reactions = pd.read_csv('adverse_reactions.csv')


# ## Assess

# In[4]:


patients.head()


# In[5]:


treatments.head()


# In[6]:


adverse_reactions.head()


# In[7]:


patients.info()


# In[8]:


treatments.info()


# In[9]:


adverse_reactions.info()


# In[10]:


all_columns = pd.Series(list(patients) + list(treatments) + list(adverse_reactions))
all_columns[all_columns.duplicated()]


# In[11]:


list(patients)


# In[12]:


patients[patients['address'].isnull()]


# In[13]:


patients.describe()


# In[14]:


treatments.describe()


# In[15]:


patients.sample(5)


# In[16]:


patients.surname.value_counts()


# In[17]:


patients.address.value_counts()


# In[18]:


patients[patients.address.duplicated()]


# In[19]:


patients.weight.sort_values()


# In[20]:


weight_lbs = patients[patients.surname == 'Zaitseva'].weight * 2.20462
height_in = patients[patients.surname == 'Zaitseva'].height
bmi_check = 703 * weight_lbs / (height_in * height_in)
bmi_check


# In[21]:


patients[patients.surname == 'Zaitseva'].bmi


# In[22]:


sum(treatments.auralin.isnull())


# In[23]:


sum(treatments.novodra.isnull())


# #### Quality
# ##### `patients` table
# - Zip code is a float not a string
# - Zip code has four digits sometimes
# - Tim Neudorf height is 27 in instead of 72 in
# - Full state names sometimes, abbreviations other times
# - Dsvid Gustafsson
# - Missing demographic information (address - contact columns) ***(can't clean)***
# - Erroneous datatypes (assigned sex, state, zip_code, and birthdate columns)
# - Multiple phone number formats
# - Default John Doe data
# - Multiple records for Jakobsen, Gersten, Taylor
# - kgs instead of lbs for Zaitseva weight
# 
# ##### `treatments` table
# - Missing HbA1c changes
# - The letter 'u' in starting and ending doses for Auralin and Novodra
# - Lowercase given names and surnames
# - Missing records (280 instead of 350)
# - Erroneous datatypes (auralin and novodra columns)
# - Inaccurate HbA1c changes (leading 4s mistaken as 9s)
# - Nulls represented as dashes (-) in auralin and novodra columns
# 
# ##### `adverse_reactions` table
# - Lowercase given names and surnames

# #### Tidiness
# - Contact column in `patients` table should be split into phone number and email
# - Three variables in two columns in `treatments` table (treatment, start dose and end dose)
# - Adverse reaction should be part of the `treatments` table
# - Given name and surname columns in `patients` table duplicated in `treatments` and `adverse_reactions` tables

# ## Clean

# In[24]:


patients_clean = patients.copy()
treatments_clean = treatments.copy()
adverse_reactions_clean = adverse_reactions.copy()


# ### Missing Data

# <font color='red'>Complete the following two "Missing Data" **Define, Code, and Test** sequences after watching the *"Address Missing Data First"* video.</font>

# #### `treatments`: Missing records (280 instead of 350)

# ##### Define
# *Your definition here. Note: the missing `treatments` records are stored in a file named `treatments_cut.csv`, which you can see in this Jupyter Notebook's dashboard (click the **jupyter** logo in the top lefthand corner of this Notebook). Hint: [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.concat.html) for the function used in the solution.*

# In[25]:


df = pd.read_csv('treatments_cut.csv')


# In[26]:


df.shape


# ##### Code

# In[27]:


# Your cleaning code here
#here, i try to join my missing data to the original dataset

df_join = pd.concat([treatments_clean, df], join = 'inner', ignore_index = True, verify_integrity=True)


# ##### Test

# In[28]:


# Your testing code here
#now i will check the info of my newly joined table
df_join.info()


# In[29]:


df_join.tail()


# #### `treatments`: Missing HbA1c changes and Inaccurate HbA1c changes (leading 4s mistaken as 9s)
# *Note: the "Inaccurate HbA1c changes (leading 4s mistaken as 9s)" observation, which is an accuracy issue and not a completeness issue, is included in this header because it is also fixed by the cleaning operation that fixes the missing "Missing HbA1c changes" observation. Multiple observations in one **Define, Code, and Test** header occurs multiple times in this notebook.*

# ##### Define
# *Your definition here.*
# - here, i will be calculating the hba1c change and refilling the change column with my results
# - thus, accounting for the missing and innacurate data

# ##### Code

# In[30]:


# Your cleaning code here
#i will subtract the start level from the end level
#here, i will load my data

df_join.head()


# In[31]:


#here, i will do the calculation
df_join['hba1c_change'] = df_join['hba1c_start'] - df_join['hba1c_end']


# ##### Test

# In[32]:


# Your testing code here
#this code checks for null values in the hba1c_change column
df_join.hba1c_change.isnull().sum()


# In[33]:


#for inaccurate values, this code confirms that all calculations is correct

df_join.sample(5)


# In[34]:


treatments_clean = df_join


# In[35]:


treatments_clean.sample(4)


# ### Tidiness

# <font color='red'>Complete the following four "Tidiness" **Define, Code, and Test** sequences after watching the *"Cleaning for Tidiness"* video.</font>

# #### Contact column in `patients` table contains two variables: phone number and email

# ##### Define
# *Your definition here. Hint 1: use regular expressions with pandas' [`str.extract` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.extract.html). Here is an amazing [regex tutorial](https://regexone.com/). Hint 2: [various phone number regex patterns](https://stackoverflow.com/questions/16699007/regular-expression-to-match-standard-10-digit-phone-number). Hint 3: [email address regex pattern](http://emailregex.com/), which you might need to modify to distinguish the email from the phone number.*

# ##### Code

# In[36]:


# Your cleaning code here
#displaying the contact column to be worked on
patients_clean.contact


# In[37]:


#tried to create a pattern of regular expresions
email_pattern = r'([^0-9-._/|,\s][a-zA-Z0-9_.+-]+@[a-zA-Z-]+\.[a-zA-Z-.]+)'

phone_pattern = r'(((\+?\d+)?[\s.-]?)?\(?[2-9]?(?!11)\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4})'


# In[38]:


#this code extracts the email from the contact column
patients_clean['Email'] = patients_clean.contact.str.extract(email_pattern, flags = 0)


# In[39]:


#here, i extracted the phone numbers from the contact column
#the p1 and p2 were created temporarily to store for irrelevant values returned by the regex pattern
patients_clean[['phone_number', 'p1', 'p2']] = patients_clean.contact.str.extract(phone_pattern, flags = 0)


# In[40]:


#next i will drop irrellevant columns created for the sake of analysis
patients_clean.drop(columns = ['p1', 'p2', 'contact'], inplace = True)


# ##### Test

# In[41]:


# Your testing code here
#this code shows the columns created 
patients_clean.head()


# #### Three variables in two columns in `treatments` table (treatment, start dose and end dose)

# ##### Define
# *Your definition here. Hint: use pandas' [melt function](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.melt.html) and [`str.split()` method](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.split.html). Here is an excellent [`melt` tutorial](https://deparkes.co.uk/2016/10/28/reshape-pandas-data-with-melt/).*

# In[42]:


treatments_clean.head()


# ##### Code

# In[43]:


# Your cleaning code here
#here, i try to write a code that transforms the column names, auralin and novodra into value in a new column 'treatments' 
#and then set it values
treatments_clean = pd.melt(treatments_clean, id_vars=["given_name", 'surname', 'hba1c_start', 'hba1c_end', 'hba1c_change'], 
                 var_name="Treatment", value_name="Dosage")


# In[44]:


#this code shows that the above task is confirmed
treatments_clean.head(5)


# In[45]:


#this code is used to drop rows where there is no dosage values, represented as '-'
treatments_clean.drop(treatments_clean[treatments_clean.Dosage.str.contains(r'^[\W-]+$')].index, inplace = True)

#this code confirms the above results
treatments_clean.shape


# In[46]:


#here, i split the dosage column to get the start and end dose respectively
treatments_clean[['start_dose', 'end_dose']] = treatments_clean.Dosage.str.split("-", n=1, expand=True)


# In[47]:


#this code confirms the above operation
treatments_clean.head()


# In[48]:


#this line of code removes the non-number characters in the dosage column
treatments_clean['start_dose'] = treatments_clean['start_dose'].str.strip('u ')
treatments_clean['end_dose'] = treatments_clean['end_dose'].str.strip('u ')

#this line of code drops the irrelevant columns
treatments_clean.drop(columns = ['Dosage'], inplace = True)

#this line of code aims to reset index of the dataframe
treatments_clean = treatments_clean.reset_index(drop = True)


# ##### Test

# In[49]:


# Your testing code here
#this code checks that all operations performed above are effected
treatments_clean.sample(5)


# In[50]:


#this code also helps to check that the number of samples still remains 350
treatments_clean[treatments_clean['given_name'].duplicated()]


# #### Adverse reaction should be part of the `treatments` table

# ##### Define
# *Your definition here: here, i am to merge my adverse reaction samples to their respective sample on the treatments table
# 
# Hint: [tutorial](https://chrisalbon.com/python/pandas_join_merge_dataframe.html) for the function used in the solution.*

# In[51]:


#checks the number of samples to be merged
adverse_reactions_clean.shape


# ##### Code

# In[52]:


# Your cleaning code here
#here i want to try to merge the adverse reactions table to my treatments table on patients with given names and surnames

treatments_clean = pd.merge(treatments_clean, adverse_reactions_clean, on=['given_name', 'surname'], how='left')


# ##### Test

# In[53]:


# Your testing code here
#to confirm the above operation
treatments_clean.head(10)


# #### Given name and surname columns in `patients` table duplicated in `treatments` and `adverse_reactions` tables  and Lowercase given names and surnames

# ##### Define
# *Your definition here. Hint: [tutorial](https://chrisalbon.com/python/pandas_join_merge_dataframe.html) for one function used in the solution and [tutorial](http://erikrood.com/Python_References/dropping_rows_cols_pandas.html) for another function used in the solution.*

# ##### Code

# In[54]:


# Your cleaning code here
#here i will try to create a dataframe to store my required columns from patients
names_rep = patients_clean[['given_name', 'surname', 'patient_id']]


# In[55]:


#to turn all entries of names to lower letters for consistency
names_rep.given_name = names_rep.given_name.str.lower()
names_rep.surname = names_rep.surname.str.lower()


# In[56]:


#merge the new index columns to the treatments_clean so as to eliminate names in the table and replace with patients_id
treatments_clean = pd.merge(treatments_clean, names_rep, on = ['given_name', 'surname'])


# In[57]:


#dropping irrelevant columns
treatments_clean.drop(columns = ['given_name', 'surname'], inplace = True)


# ##### Test

# In[58]:


# Your testing code here
treatments_clean.head()


# ### Quality

# <font color='red'>Complete the remaining "Quality" **Define, Code, and Test** sequences after watching the *"Cleaning for Quality"* video.</font>

# #### Zip code is a float not a string and Zip code has four digits sometimes

# ##### Define
# *Your definition here: i will change the data type of the zip code and also remove all '.0' with string slicing after which i will fill the zipcode to make sure all length id 5 characters length.*
# 
# *Hint: see the "Data Cleaning Process" page.*

# ##### Code

# In[59]:


# Your cleaning code here
#this line of code converts data type to string, removes the decimal points and makes sure all zipcodes are 5 characters long
patients_clean.zip_code = patients_clean.zip_code.astype(str).str[:-2].str.pad(5, fillchar = '0')


# In[60]:


import numpy as np
#this line of code replaces all '0000n' with NAN 
patients_clean.zip_code = patients_clean.zip_code.replace('0000n', np.nan)


# ##### Test

# In[61]:


# Your testing code here
patients_clean.head()


# #### Tim Neudorf height is 27 in instead of 72 in

# ##### Define
# *Your definition here: i want to replace the value of Tim Neudorf height*

# ##### Code

# In[62]:


# Your cleaning code here
#here, i show the exact height of tim and discovered he is the only outlier with 27
patients_clean[patients_clean.given_name == 'Tim']


# In[63]:


#this code replaces the only outlier in our height column
patients_clean['height'] = patients_clean['height'].replace([27],72)


# ##### Test

# In[64]:


# Your testing code here
patients_clean[patients_clean.given_name == 'Tim']


# - **Now, the above output confirms that my change has been effected and in place**

# #### Full state names sometimes, abbreviations other times

# ##### Define
# *Your definition here. Hint: [tutorial](https://chrisalbon.com/python/pandas_apply_operations_to_dataframes.html) for method used in solution.*

# ##### Code

# In[65]:


# Your cleaning code here
patients_clean.state.unique()


# In[66]:


#this is a dictionary containg full names of abreviations in the state column
us_state_abbrev = {
            'AL': 'Alabama',
            'AK': 'Alaska',
            'AZ': 'Arizona',
            'AR': 'Arkansas',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'HI': 'Hawaii',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'IA': 'Iowa',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'ME': 'Maine',
            'MD': 'Maryland',
            'MA': 'Massachusetts',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MS': 'Mississippi',
            'MO': 'Missouri',
            'MT': 'Montana',
            'NE': 'Nebraska',
            'NV': 'Nevada',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NY': 'New York',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VT': 'Vermont',
            'VA': 'Virginia',
            'WA': 'Washington',
            'WV': 'West Virginia',
            'WI': 'Wisconsin',
            'WY': 'Wyoming',
            'DC': 'District of Columbia',
            'MP': 'Northern Mariana Islands',
            'PW': 'Palau',
            'PR': 'Puerto Rico',
            'VI': 'Virgin Islands',
            'AA': 'Armed Forces Americas (Except Canada)',
            'AE': 'Armed Forces Africa/Canada/Europe/Middle East',
            'AP': 'Armed Forces Pacific'
        }


# In[67]:


#here, this line of code maps the dictionary to the state column and also fill values not found in the dict with previous values
patients_clean.state = patients_clean.state.map(us_state_abbrev).fillna(patients_clean['state'])


# ##### Test

# In[68]:


patients_clean.head()


# In[69]:


#confirms that samples quantity not tampered with
patients_clean.shape


# #### Dsvid Gustafsson

# ##### Define
# *Your definition here: i will correct the typographical error noted in the name above*

# ##### Code

# In[70]:


#this line of code replaces the typographical error with the correct spelliing
patients_clean.given_name = patients_clean.given_name.replace(['Dsvid'], 'David')


# ##### Test

# In[71]:


# Your testing code here
#this code should return no value since the error has been corrected
patients_clean[patients_clean.given_name == 'Dsvid']


# #### Erroneous datatypes (assigned sex, state, zip_code, and birthdate columns) and Erroneous datatypes (auralin and novodra columns) and The letter 'u' in starting and ending doses for Auralin and Novodra

# ##### Define
# *Your definition here. Hint: [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.astype.html) for one method used in solution, [documentation page](http://pandas.pydata.org/pandas-docs/version/0.20/generated/pandas.to_datetime.html) for one function used in the solution, and [documentation page](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.str.strip.html) for another method used in the solution.*

# ##### Code

# In[72]:


# Your cleaning code here
#this line of code converts assigned_sex, and state column to  category datatypes
patients_clean = patients_clean.astype({'assigned_sex': 'category','state': 'category'})



# In[73]:


#this code converts birthdate column to datetime data type
patients_clean['birthdate'] = pd.to_datetime(patients_clean['birthdate'])


# ##### Test

# In[74]:


# Your testing code here
patients_clean.dtypes


# #### Multiple phone number formats

# ##### Define
# *Your definition here. Hint:remove all non digit characters. helpful [Stack Overflow answer](https://stackoverflow.com/a/123681).*

# ##### Code

# In[75]:


# Your cleaning code here
#this line of code replaces all non didgit characters with nothing and then pads the remaining with a 1 to have country code

patients_clean.phone_number = patients_clean.phone_number.str.replace(r'\D+', '').str.pad(11, fillchar='1')


# ##### Test

# In[76]:


# Your testing code here
patients_clean.phone_number.head()


# #### Default John Doe data

# ##### Define
# *Your definition here. Recall that it is assumed that the data that this John Doe data displaced is not recoverable.since  this data is non revoverable, i will be removing it from my dataset*

# ##### Code

# In[78]:


# Your cleaning code here
patients_clean = patients_clean[patients_clean.surname != 'Doe']


# ##### Test

# In[80]:


# Your testing code here
#should be empty
patients_clean[patients_clean.surname == 'Doe']


# #### Multiple records for Jakobsen, Gersten, Taylor

# ##### Define
# *Your definition here: it was discovered that some records are that of nicknames, hence, i eill be dropping the records belonging to nicknames, in order to conform with the records on treatments table*

# ##### Code

# In[81]:


#this code filters out the first occurence of duplicate values , which happens to be that of the reaal names and not nicknames
# Your cleaning code here
patients_clean = patients_clean[~((patients_clean.address.duplicated()) & patients_clean.address.notnull())]


# ##### Test

# In[82]:


# Your testing code here
patients_clean[patients_clean.surname == 'Jakobsen']


# In[84]:


#there should be no nick
patients_clean[patients_clean.surname == 'Gersten']


# In[83]:


#there should be nickname, sandy
patients_clean[patients_clean.surname == 'Taylor']


# #### kgs instead of lbs for Zaitseva weight

# ##### Define
# *Your definition here: it was discovered that Zaitseva's weight was miscalculated and recorded in kg instead of pounds.This record will be recalculated and replaced*

# ##### Code

# In[89]:


# Your cleaning code here
patients_clean[patients_clean.surname == 'Zaitseva']


# In[88]:


patients_clean['weight'] = patients_clean['weight'].replace([48.8],48.8 * 2.20462)


# ##### Test

# In[91]:


# Your testing code here
#notice the change in weight for Zaitseva
patients_clean[patients_clean.surname == 'Zaitseva']

