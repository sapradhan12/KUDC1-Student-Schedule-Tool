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

# To-Do List
st.subheader("To-Do List")
task = st.text_input("Add a new task:")
due_date_input = st.date_input("Due date:", value=None)
if st.button("Add Task"):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    cursor.execute("INSERT INTO due_date (due_date_input) VALUES (?)", (due_date_input,))
    conn.commit()
    st.write(f"Task added: {task}")

# View all tasks
#if st.button("View All Tasks"):
st.subheader("All Tasks")
tasks = cursor.execute("SELECT task FROM tasks").fetchall()
due_dates = cursor.execute("SELECT due_date_input FROM due_date").fetchall()
for i, task, due_date_input in range(enumerate(enumerate(tasks), enumerate(due_dates))):
    st.write(f"{i + 1}. {int(task)}, due {int(due_date_input)}.")

'''
for i, due_date_input in enumerate(due_dates):
    st.write(f"Due {due_date_input}.")
    st.checkbox("Done?", key=i)
'''
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
