## Modified from https://medium.com/mlearning-ai/how-to-start-learning-sql-with-streamlit-d3edad7494cd

from operator import index
import sqlite3
import streamlit as st
import pandas as pd
import os
from PIL import Image

## ERD form the sample case
sample_erd = Image.open("OnlineMediaSubscription.png")


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.write(e)

    return conn


def create_database():
    st.markdown("# Create Database")

    st.write(
        """A database in SQLite is just a file on same server. 
    By convention their names always end in .db"""
    )

    db_filename = st.text_input("DB Filename")
    create_db = st.button("Create Database")

    if create_db:
        if db_filename.endswith(".db"):
            conn = create_connection(db_filename)
            st.write(db_filename + " created successfully!")
        else:
            st.write("DB filename must end with .db, please retry.")

    st.sidebar.markdown("# Create a database")


def upload_data():
    st.markdown("# Upload Data")
    # https://discuss.streamlit.io/t/uploading-csv-and-excel-files/10866/2
    sqlite_dbs = [file for file in os.listdir(".") if file.endswith(".db")]

    if not sqlite_dbs:
        st.write("No databases created.")
    else:
        db_filename = st.selectbox("DB Filename", sqlite_dbs)
        table_name = st.text_input("Table Name to Insert")
        conn = create_connection(db_filename)
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            # read csv
            try:
                df = pd.read_csv(uploaded_file)
                df.to_sql(name=table_name, con=conn, index=False, if_exists="replace")
                st.write("Data uploaded successfully. These are the first 10 rows.")
                st.dataframe(df.head(10))

            except Exception as e:
                st.write(e)
    st.sidebar.markdown("# Upload data")


def run_query():
    st.markdown("# Run Query")
    sqlite_dbs = [file for file in os.listdir(".") if file.endswith(".db")]

    if not sqlite_dbs:
        st.write("No databases created.")
    else:

        db_filename = st.selectbox("DB Filename", sqlite_dbs)

        query = st.text_area("SQL Query", height=100)
        conn = create_connection(db_filename)

        submitted = st.button("Run Query")

        if submitted:
            try:
                query = conn.execute(query)
                cols = [column[0] for column in query.description]
                results_df = pd.DataFrame.from_records(
                    data=query.fetchall(), columns=cols
                )
                st.dataframe(results_df)
            except Exception as e:
                st.write(e)

        # Option to show tables
        show_tables = st.button("Show Tables")

        if show_tables:
            tables = pd.read_sql_query(
                "SELECT name FROM sqlite_master WHERE type='table';", conn
            )
            st.dataframe(tables)

    st.sidebar.markdown("# Run Query")


def sample_case():
    st.markdown("# Sample Case: Online Media Subscription")
    st.markdown("## ERD for sample case")
    st.image(sample_erd, caption="Online Media Subscription")

    ## Connecting to example db.
    ## Located in assets/stream.db
    ## Details on example db can be found in https://github.com/BrunoBVR/ICT-128-A2
    conn = create_connection("assets/stream.db")

    # Option to show tables
    show_tables = st.button("Show Tables")

    if show_tables:
        tables = pd.read_sql_query(
            "SELECT name FROM sqlite_master WHERE type='table';", conn
        )
        st.dataframe(tables)

    # Sample questions

    st.markdown("### Sample questions:")
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Q1", "Q2", "Q3", "Q4", "Q5"])

    with tab1:
        st.header("Question 1")
        st.warning("How many unique content itens are there per type?", icon="💭")

    with tab2:
        st.header("Question 2")
        st.warning("What genre of content has the highest star rating?", icon="💭")

    with tab3:
        st.header("Question 3")
        st.warning("What are the top 10 accounts with more streamed content?")

    with tab4:
        st.header("Question 4")
        st.warning("What are the top 3 most streamed content in Canada?")

    with tab5:
        st.header("Question 5")
        st.warning(
            "What is the average star rate of horror movies watched on Fridays in Asia?",
            icon="💭",
        )

    query = st.text_area("SQL Query", height=100)
    submitted = st.button("Run Query")

    if submitted:
        try:
            query = conn.execute(query)
            cols = [column[0] for column in query.description]
            results_df = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            st.dataframe(results_df)
        except Exception as e:
            st.write(e)

    st.sidebar.markdown("# Sample Case")


page_names_to_funcs = {
    "Create Database": create_database,
    "Upload Data": upload_data,
    "Run Query": run_query,
    "Try sample case": sample_case,
}


# selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
selected_page = st.sidebar.radio("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()
