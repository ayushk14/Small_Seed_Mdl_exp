
# coding: utf-8

# In[1]:


import smtplib
import sys


# In[2]:

start_time = sys.argv[1]
end_time = sys.argv[2]
exp_description = sys.argv[3]

receiver_list = []
receiver_list.append('RECEIVER EMAIL ID')


# In[3]:


sender = 'SENDER EMAIL ID'


# In[4]:


subject = 'Kaldi Results Update'


# In[5]:


file = open('res.txt','r')


# In[6]:


f_content = file.read()


# In[8]:


for receiver in receiver_list:
    message = """From: SENDER EMAIL ID
To: """+receiver+"""
Subject: """+subject+"""-"""+exp_description+"""

Experiment Description: """+exp_description+"""\n
Start Time: """+start_time+"""
End Time: """+end_time+"""
The results are as follows:-\n
"""+f_content

    try:
        smtpObj = smtplib.SMTP('smtp.gmail.com',587)
        smtpObj.starttls()
        smtpObj.login("SENDER EMAIL ID","SENDER PASSWORD")
        smtpObj.sendmail(sender,receiver,message)
        print('Successfully sent')
    except smtplib.SMTPException as e:
        print(e)
