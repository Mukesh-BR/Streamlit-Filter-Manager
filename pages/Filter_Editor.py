import os
import numpy as np
import pandas as pd
import streamlit as st
import time
import datetime

st.set_page_config(layout="centered", page_title="Data Editor")
st.title("Filters Editor")
st.caption("This web page can be used to edit the filters we use on production")

#Define path constants
base_filename = "data/"
archival_path= base_filename + "archives/filter_archives/"

if not os.path.exists(archival_path):
    os.makedirs(archival_path)

# Get list of filters, we sort the list of filters to improve user experience
filters = os.listdir(base_filename)
filters.sort()
if "archives" in filters:
    filters.remove("archives")
if "dev_meta.csv" in filters:
    filters.remove("dev_meta.csv")
choice = st.selectbox('Select the filter to edit: ',filters)

filename = base_filename+choice

#Get table of questions
meta_table_filepath = base_filename + "dev_meta.csv"
meta_table = pd.read_csv(meta_table_filepath)

def get_data(filename):
    return pd.read_csv(filename)

def get_current_timestamp():
    current_time = datetime.datetime.now()
    time_stamp = current_time.timestamp()
    dt_object = datetime.datetime.fromtimestamp(time_stamp)
    formatted_ts = dt_object.strftime("%Y-%m-%d %H:%M:%S")  
    return formatted_ts

# Sanity checks
def sanity_checks(edited, meta_table):
    questions_answer_pairs = meta_table[["questionid","answerid"]]
    questions = meta_table.questionid
    answers = meta_table.answerid

    # Sanity checks on question ids
    # 1. Question IDs cannot be NULL
    # 2. Question IDs for which we define filters must exist in the questions database
    # 3. For filters with questionid is the Primary Key, they must be unique
    if "questionid" in edited.columns:
        filter_questions = edited.questionid
        if filter_questions.isnull().any()==True:
            return True, "Question ID cannot be null"
        if filter_questions.isin(questions).all()==False:
            return True, "One or more question ids in edited filter does not exist in the meta table"
        if (filter_questions.nunique() != len(filter_questions)) and (choice== "dev_nps_category_override.csv" or choice== "dev_nps_brand_override.csv"):
            return True, "Question ids must be unique"

    # Sanity checks on Answer ids
    # 1. Answer IDs cannot be NULL
    # 2. Answer IDs for which we define filters must exist in the answers database
    if "answerid" in edited.columns:
        filter_answers = edited.answerid
        if filter_answers.isnull().any()==True:
            return True, "Answer ID cannot be null"
        if filter_answers.isin(answers).all()==False:
            return True, "One or more answer ids in edited filter does not exist in the meta table"
    
    # Sanity checks for question answer pairs
    # 1. The question answer pair must be unique
    # 2. The question answer pair in the edits table must also exist in the meta database
    if "answerid" in edited.columns and "questionid" in edited.columns:
        edited_questions_answer_pairs = edited[["questionid","answerid"]]
        if edited_questions_answer_pairs.drop_duplicates().shape[0] != len(edited_questions_answer_pairs):
            return True, "Question, Answer pairs must be unique"
        if len(pd.merge(edited_questions_answer_pairs, questions_answer_pairs))!=len(edited_questions_answer_pairs):
            return True, "The edited question answer pairs do not exist in the meta table."
    
    # Sanity checks on alpharoc_orders
    # 1. Order field cannot be null
    # 2. There cannot be more than ordering value for a (question, answer) pair
    if "alpharoc_order" in edited.columns:
        alpharoc_order= edited.alpharoc_order
        if alpharoc_order.isnull().any()==True:
            return True, "Order field cannot be null"
        if edited.groupby(['questionid', 'answerid'])['alpharoc_order'].transform('nunique').gt(1).any():
            return True, "A question answer pair has more than one ordering"
    
    # Sanity checks on dates
    # 1. Start date must be on or before current date
    # 2. End date must be on or before current date
    # 3. Start date must on or be before end date
    if "start_date" in edited.columns and "end_date" in edited.columns:
        if ((pd.to_datetime(edited['start_date']) <= pd.to_datetime('today')) & (pd.to_datetime(edited['end_date']) <= pd.to_datetime('today')) & (pd.to_datetime(edited['start_date']) <= pd.to_datetime(edited['end_date']))).all() == False:
            return True, "Start date must be before than end date and both should be before today"
        
    return False, None


with st.form("data_editor_form"):
    st.caption("Edit the dataframe below")
    dataset = get_data(base_filename+choice)
    edited = st.data_editor(dataset, use_container_width=True, num_rows="dynamic")
    submit_button = st.form_submit_button("Submit")

if submit_button:
    has_error, message = sanity_checks(edited, meta_table)
    if has_error:
        st.error('No updates performed! ' + message + ' Page will automatically refresh in a few seconds', icon="🚨")
        time.sleep(4)
        st.rerun()
    else:
        ts = get_current_timestamp()
        split_filename = choice.split(".")[0]
        archived = archival_path + split_filename + '_' + ts + ".csv"
        
        # Read previous values in order to archive them
        previous = get_data(base_filename+choice)

        if previous.equals(edited):
            st.error('No updates performed as no edits found! Page will automatically refresh in a few seconds', icon="🚨")
            time.sleep(4)
            st.rerun()
        
        else:
            previous.to_csv(archived, index=False)
            edited.to_csv(filename, index=False)
            st.success('Updated Successfully! Page will automatically refresh in a few seconds', icon="✅")
            time.sleep(2)
            st.rerun()