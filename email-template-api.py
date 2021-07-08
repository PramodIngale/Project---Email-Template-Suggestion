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
def home_button():
    keywords = st.text_input("Enter the Keywords and Click on Search") #Input from user
    keyword_button = st.button("Search")
    if  keyword_button == True:  
        
        if keywords == "": 
            st.subheader("Template")
            st.error("Please enter some keywords and click on search")
        else:
            my_bar = st.progress(0) #Progress bar
            for p in range(100):
                time.sleep(0.001)
                my_bar.progress(p + 1)
            #Vectorization and class prediction
            array = vectorizer_model.transform(pd.Series(keywords))
            class_probability = classification_model.predict_proba(array)
            
            probability = "bad"
            for prob_val in class_probability[0]:
                if prob_val > 0.30:
                    probability = "Good"
                    pass
                
            if probability != "Good":
                st.error("Keywords are not suffiecient, please try adding few more and click on search")
            else:   
                email_class = classification_model.predict(array)
                teamplate_name = class_dict.get(email_class[0])

                st.subheader("Template")    
                st.write("Subject: ",teamplate_name)

                #Output template display
                st.markdown("# ------------------------------------------------", True)
                template_conetnt = docx.Document(teamplate_name+".docx")
                for para in template_conetnt.paragraphs:
                    st.markdown(para.text)
                st.markdown("# ------------------------------------------------", True)
                
                #Copy button
                firstb,secondb,thirdb = st.beta_columns([1.8,1,1])
                copy_button = secondb.button("Copy")
       
    if keyword_button == False:
        copy_button = False
        st.write("Waiting for user to enter the Keywords...............!!!!")
    return keyword_button

def appdes_button():
#-------------Navigation - Application Description------------------       
# if rad == "Application Description":
    st.header("Purpose")
    st.markdown("> Email Template Suggestion API is developed to suggest email template to the user based on the keywords provided by them.", True)
    st.header("Adavantages")
    st.markdown("> Content will be updated soon....", True)
    st.header("How to Use")
    st.markdown("> Content will be updated soon....", True)
    return

#Condiitons
if rad == "Home":
    keyword_status = home_button()
if rad == "Application Description":
    appdes_button()
