import os
import numpy as np
import pandas as pd
import streamlit as st
import time
import datetime

st.set_page_config(layout="centered", page_title="Data Editor")
st.title("Filters Editor")
st.caption("This web page can be used to edit the filters we use on production")

def get_data(filename):
    return pd.read_csv(filename)

base_filename = "data/"
archival_path= base_filename + "archives/filter_archives/"
print(os.curdir)

filters = os.listdir(base_filename)
if "archives" in filters:
    filters.remove("archives")
if "dev_meta.csv" in filters:
    filters.remove("dev_meta.csv")
meta_table_filepath = base_filename + "dev_meta.csv"
meta_table = pd.read_csv(meta_table_filepath)

def check_error(edited, meta_table):
    questions = meta_table.questionid
    answers = meta_table.answerid
    print(questions)
    print(answers)
    if "questionid" in edited.columns:
        filter_questions = edited.questionid
        print(filter_questions)
        print(filter_questions.isin(questions))
        if filter_questions.isnull().any()==True:
            return True, "Question ID cannot be null"
        if filter_questions.isin(questions).all()==False:
            return True, "One or more question ids in edited filter does not exist in the meta table"
        if (filter_questions.nunique() != len(filter_questions)) and (choice== "dev_nps_category_override.csv" or choice== "dev_nps_brand_override.csv"):
            return True, "Question ids must be unique"
    if "answerid" in edited.columns:
        filter_answers= edited.answerid
        print(filter_answers)
        print(filter_answers.isin(answers))
        if filter_answers.isnull().any()==True:
            return True, "Answer ID cannot be null"
        if filter_answers.isin(answers).all()==False:
            return True, "One or more answer ids in edited filter does not exist in the meta table"
        
    if "alpharoc_order" in edited.columns:
        alpharoc_order= edited.alpharoc_order
        if alpharoc_order.isnull().any()==True:
            return True, "Alpharoc cannot be null"
        print(edited.groupby(['questionid', 'answerid'])['alpharoc_order'].transform('nunique'))
        if edited.groupby(['questionid', 'answerid'])['alpharoc_order'].transform('nunique').gt(1).any():
            return True, "A question answer pair has more than one ordering"
    
    if "start_date" in edited.columns and "end_date" in edited.columns:
        if ((pd.to_datetime(edited['start_date']) <= pd.to_datetime('today')) & (pd.to_datetime(edited['end_date']) <= pd.to_datetime('today')) & (pd.to_datetime(edited['start_date']) <= pd.to_datetime(edited['end_date']))).all() == False:
            return True, "Start date must be before than end date and both should be before today"
        
    return False, None


choice = st.selectbox('Select the filter to edit: ',filters)
filename = base_filename+choice

with st.form("data_editor_form"):
    st.caption("Edit the dataframe below")
    dataset = get_data(base_filename+choice)
    edited = st.data_editor(dataset, use_container_width=True, num_rows="dynamic")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    has_error, message = check_error(edited, meta_table)
    if has_error:
        st.error('No updates performed! ' + message, icon="🚨")
        time.sleep(2)
        st.rerun()

    current_time = datetime.datetime.now()
    time_stamp = current_time.timestamp()
    dt_object = datetime.datetime.fromtimestamp(time_stamp)
    formatted_string = dt_object.strftime("%Y-%m-%d %H:%M:%S")  
    split_filename = choice.split(".")[0]
    timestamped_filename = split_filename + '_' + str(formatted_string) + ".csv"
    
    archived = archival_path + timestamped_filename
    previous = get_data(base_filename+choice)
    test = edited.iloc[:, ~edited.columns.str.contains('Unnamed', case=False)]
    previous.to_csv(archived, index=False)
    test.to_csv(filename, index=False)
    st.write("Base dataset updated")
    st.success('Updated Successfully! Page will automatically refresh in a few seconds', icon="✅")
    time.sleep(2)
    st.rerun()