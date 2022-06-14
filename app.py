#Read json file
import json
#Install Library
import streamlit as st
import numpy as np
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

import google_auth_httplib2
import httplib2

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import HttpRequest

GSHEET_URL = "https://docs.google.com/spreadsheets/d/1HePfPJzuBKAvffu9K5zf2XSXlN92PIfGWaz5WQesn3k/edit#gid=0"

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/spreadsheets']


#credentials to the account
cred = ServiceAccountCredentials.from_json_keyfile_name('warm-practice-348819-7b2f3a467d90.json',scope) 

# authorize the clientsheet 
client = gspread.authorize(cred)

# get the sample of the Spreadsheet
sheet = client.open('Bug_Report')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

st.set_page_config(page_title="Bug report", page_icon="🐞", layout="centered")

st.title("Customer Management Sysytem 2.0")

st.sidebar.write(
    f"This app shows how a Streamlit app can interact easily with a [Google Sheet]({GSHEET_URL}) to read or store data."
)

st.sidebar.write(
    f"[Read more](https://docs.streamlit.io/knowledge-base/tutorials/databases/public-gsheet) about connecting your Streamlit app to Google Sheets."
)

form = st.form(key="annotation")

form = st.form("checkboxes", clear_on_submit = True)
with form:
    cols = st.columns((1, 1))
    author = cols[0].text_input("Report author:")
    bug_type = cols[1].selectbox(
        "Bug type:", ["Front-end", "Back-end", "Data related", "404"], index=2
    )
    comment = st.text_area("Comment:")
    cols = st.columns(2)
    date = cols[0].date_input("Bug date occurrence:")
    bug_severity = cols[1].slider("Bug severity:", 1, 5, 2)
    submitted = st.form_submit_button(label="Submit")
    
if submitted:
    row = [author, bug_type, comment, str(date), bug_severity]
    index = 2
    sheet_instance.insert_row(row, index)
    
    st.success("Thanks! Your bug was recorded.")
    st.balloons()
    
expander = st.expander("See all records")    
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    # get all the records of the data
    records = sheet_instance.get_all_records()

    # convert the json to dataframe
    records_df = pd.DataFrame.from_dict(records)

    df = records_df.astype(str)
    st.dataframe(df)
    
st.subheader("🐞 Delete Record")

form2 = st.form(key="annotation1")
with form2:
    #del_index = cols[0].text_input("Index of the record:")
    del_index = st.number_input("Index of the record:", 0)
    del_index = del_index + 2
    deleted = st.form_submit_button(label="Delete")
if deleted:
    sheet_instance.delete_row(index=del_index)
    
    st.success("Thanks! Your record was deleted. Please refresh the page to see the updated records")
    st.balloons()
    
expander = st.expander("See all records")    
with expander:
    st.write(f"Open original [Google Sheet]({GSHEET_URL})")
    # get all the records of the data
    records = sheet_instance.get_all_records()

    # convert the json to dataframe
    records_df = pd.DataFrame.from_dict(records)

    df = records_df.astype(str)
    st.dataframe(df)