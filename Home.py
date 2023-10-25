import streamlit as st
import sqlite3
from streamlit_calendar import calendar

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

# Main Planner
st.header("Your Planner")

calendar_options = {
    "headerToolbar": {
        "left": "today prev,next",
        "center": "title",
        "right": "resourceTimelineDay,resourceTimelineWeek,resourceTimelineMonth",
    },
    "slotMinTime": "06:00:00",
    "slotMaxTime": "18:00:00",
    "initialView": "resourceTimelineDay",
    "resourceGroupField": "building",
    "resources": [
        {"id": "a", "building": "Building A", "title": "Building A"},
        {"id": "b", "building": "Building A", "title": "Building B"},
        {"id": "c", "building": "Building B", "title": "Building C"},
        {"id": "d", "building": "Building B", "title": "Building D"},
        {"id": "e", "building": "Building C", "title": "Building E"},
        {"id": "f", "building": "Building C", "title": "Building F"},
    ],
}
calendar_events = [
    {
        "title": "Event 1",
        "start": "2023-07-31T08:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "a",
    },
    {
        "title": "Event 2",
        "start": "2023-07-31T07:30:00",
        "end": "2023-07-31T10:30:00",
        "resourceId": "b",
    },
    {
        "title": "Event 3",
        "start": "2023-07-31T10:40:00",
        "end": "2023-07-31T12:30:00",
        "resourceId": "a",
    }
]
custom_css="""
    .fc-event-past {
        opacity: 0.8;
    }
    .fc-event-time {
        font-style: italic;
    }
    .fc-event-title {
        font-weight: 700;
    }
    .fc-toolbar-title {
        font-size: 2rem;
    }
"""

calendar = calendar(events=calendar_events, options=calendar_options, custom_css=custom_css)

# To-Do List
st.subheader("To-Do List")
task = st.text_input("Add a new task:")
if st.button("Add Task"):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()
    st.write(f"Task added: {task}")

# View all tasks
if st.button("View All Tasks"):
    st.subheader("All Tasks")
    tasks = cursor.execute("SELECT task FROM tasks").fetchall()
    for i, task in enumerate(tasks):
        st.write(f"{i + 1}. {task[0]}    {st.checkbox("Done")}")

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
