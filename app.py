from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3
import google.generativeai as genai
import pandas as pd  # Import pandas for DataFrame support
import re

# Load environment variables
load_dotenv()

# Configure our API key (https://aistudio.google.com/app/apikey)
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def clean_sql_query(query):
    # Remove backticks and 'sql' labels, and ensure it's a single line
    return re.sub(r'```sql\s*|\s*```', '', query).strip()

def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + question)
    return clean_sql_query(response.text)  # Clean the SQL query

# Function to retrieve query results from the SQLite database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    
    try:
        cur.execute(sql)  # Execute the provided SQL query
        rows = cur.fetchall()  # Fetch all the results
        columns = [column[0] for column in cur.description]  # Get column names
    except sqlite3.OperationalError as e:
        rows = []  # Return an empty result in case of an error
        st.error(f"SQL Error: {e}")
    finally:
        conn.close()
    
    return rows, columns  # Return both rows and columns

# Define the prompt for SQL generation
prompt = '''You are an expert in converting English questions into SQL queries! 
The following table "STUDENT" contains the columns: NAME, CLASS (course), SECTION, and MARKS. 
Use this data to generate SQL queries for various tasks.

Here are some example questions:

1. Retrieve the names of all students who are enrolled in the "Data Science" course.
2. Find the average marks of students in Section "B".
3. List all students who have scored more than 70 marks in the "DevOps" course.
4. Get the total number of students enrolled in each course.
5. Retrieve students who are in Section "A" and have marks greater than 80.
6. Find the highest marks scored by any student in the "Data Engineer" course.

Generate the corresponding SQL queries to answer these questions.
'''

# Streamlit App setup
st.set_page_config(page_title='SQL Query Retriever with Gemini AI')
st.header('Gemini App to Retrieve SQL Data')

# Input text box for user question
question = st.text_input('Enter your natural language question:', key='input')

# Button to submit the question
submit = st.button('Submit Question')

# If submit is clicked
if submit:
    # Get the SQL query from the Gemini AI model
    sql_query = get_gemini_response(question, prompt)
    
    # Display the generated SQL query for transparency
    st.subheader('Generated SQL Query:')
    st.code(sql_query, language='sql')

    # Retrieve data from the SQLite database using the generated query
    data, columns = read_sql_query(sql_query, 'student.db')

    # Display the results or an error if the query fails
    st.subheader('Query Results:')
    if data:
        # Convert the results to a DataFrame
        df = pd.DataFrame(data, columns=columns)  # Create a DataFrame with the column names
        st.dataframe(df)  # Display the DataFrame in Streamlit
    else:
        st.write("No data returned or invalid query.")
