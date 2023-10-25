import random
import streamlit as st
import sqlite3
import datetime

# Create or connect to an SQLite database
conn = sqlite3.connect('planner.db')
cursor = conn.cursor()

# Create tables for tasks, notes, and subjects if they don't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        task TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS due_date (
        id INTEGER PRIMARY KEY,
        due_date_input TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY,
        note TEXT
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        subject TEXT
    )
''')
conn.commit()

# Title and introduction
st.title("High School Planner")
st.write("Welcome to your digital planner!")

st.subheader("To-Do List")
new_task_name = st.text_input("Add a new task:")
new_due_date = st.date_input("Due date:", value=None)

if st.button("Add Task"):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (new_task_name,))
    cursor.execute("INSERT INTO due_date (due_date_input) VALUES (?)", (new_due_date,))
    conn.commit()
    st.write(f"Task added: {new_task_name}")

# View all tasks
if st.button("View All Tasks"):
    st.subheader("All Tasks")
    #tasks = cursor.execute("SELECT new_task_name FROM tasks").fetchall()
    #due_dates = cursor.execute("SELECT new_due_date FROM due_date").fetchall()
    check_list = []
    task_list = []
    due_date_list = []

    df = pd.DataFrame(
        {
            "Check": check_list,
            "Task": task_list,
            "Due Date": due_date_list
        }
    )

    for i in task_list:
        new_task = [None, new_task_name, new_due_date]
        df.loc[len(df)] = new_task

    st.data_editor(
        df,
        column_config={
            "Check": st.column_config.CheckboxColumn(
                #"Check",
                #help="Check the box if you've completed the task",
                #=False,
            )
        },
        hide_index=True,
    )
    
# Notes and Resources
st.subheader("Notes and Resources")
note = st.text_area("Add a note or resource:")
if st.button("Save Note"):
    cursor.execute("INSERT INTO notes (note) VALUES (?)", (note,))
    conn.commit()
    st.write(f"Note saved: {note}")

# View all notes/resources
if st.button("View All Notes"):
    st.subheader("All Notes")
    notes = cursor.execute("SELECT note FROM notes").fetchall()
    due_date_db = cursor.execute("SELECT ")
    for i, note in enumerate(notes):
        st.write(f"{i + 1}. {note[0]}")

# Subjects and Courses
st.subheader("Subjects and Courses")
subject = st.text_input("Add a subject or course:")
if st.button("Add Subject"):
    cursor.execute("INSERT INTO subjects (subject) VALUES (?)", (subject,))
    conn.commit()
    st.write(f"Subject added: {subject}")

# View all subjects/courses
if st.button("View All Subjects"):
    st.subheader("All Subjects")
    subjects = cursor.execute("SELECT subject FROM subjects").fetchall()
    for i, subject in enumerate(subjects):
        st.write(f"{i + 1}. {subject[0]}")

# Close the database connection
conn.close()
