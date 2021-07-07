#!/usr/bin/env python
# coding: utf-8

# Libraries
import pandas as pd
from pickle import load
import streamlit as st
import docx
import time
import clipboard

#Trained models

vectorizer_model = load(open("Vectorizer_model_BOW.sav", "rb"))
classification_model = load(open("Classification_model.sav", "rb"))

#Email class dictionary
class_dict = {0: "Bank Services application", 1: 'Bank loan application', 2: 'Cancellation of services',
              3: 'College admission application',4: 'Compliants of defective products', 5: 'Job application',
                6: 'Leave application',7: 'Refund query',8: 'Resignation'}


#---------------Header---------------------------------------------------------------------------------

st.title('''**Email Template Suggestion**''')
st.image("header_image.jpg", width=500)

#---------------Navigation Buttons---------------------------------------------------------------------------------

rad = st.sidebar.radio("Select", ["Home", "Application Description"])

##-------------Navigation - Home------------------
if rad == "Home":
    keywords = st.text_input("Enter the Keywords and Click on Search") #Input from user
    if st.button("Search"):
        
        if keywords == "" or len(keywords.split()) < 2:
            st.subheader("Template")
            st.error("Please enter minimum two keywords and click on search")
        else:
            #Vectorization and class prediction
            email_class = classification_model.predict(vectorizer_model.transform(pd.Series(keywords)))
            
            my_bar = st.progress(0) #Progress bar
            for p in range(100):
                time.sleep(0.005)
                my_bar.progress(p + 1)

#             with st.spinner("Waiting .."): # Spinner
#                 time.sleep(0.1)
# #                 st.success("Finished!")
                
                
            st.subheader("Template")    
            teamplate_name = class_dict.get(email_class[0])
            st.write("Subject: ",teamplate_name)
            
            st.markdown("# ------------------------------------------------", True)
            template_conetnt = docx.Document(teamplate_name+".docx")
            for para in template_conetnt.paragraphs:
                st.markdown(para.text)
#                 clipboard.copy("Work is done")
            st.markdown("# ------------------------------------------------", True)
            
            firstb,secondb,thirdb = st.beta_columns([1.8,1,1])
            copy_button = secondb.button("Copy")
#             st.write(copy_button)
#             time.sleep(10)
#             st.write(copy_button)
#             if copy_button == True:
#                 clipboard.copy("Work is done")       
    else:
        st.write("Waiting for user to enter the Keywords...............!!!!")
                       
#-------------Navigation - Application Description------------------       
if rad == "Application Description":
    st.header("Purpose")
    st.markdown("> Email Template Suggestion API is developed to suggest email template to the user based on the keywords provided by them.", True)
    st.header("Adavantages")
    st.markdown("> Content will be updated soon....", True)
    st.header("How to Use")
    st.markdown("> Content will be updated soon....", True)
    
    
    