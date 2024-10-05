import sqlite3

# Connect to an SQLite database (or create one)
conn = sqlite3.connect('student.db')  # Using in-memory database for this example
cursor = conn.cursor()

# SQL statement to create the STUDENT table
table_info = '''
CREATE TABLE STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
'''

# Execute the table creation
cursor.execute(table_info)

# Sample data to populate the STUDENT table
sample_data = [
    ('John Doe', 'Data Science', 'A', 85),
    ('Jane Smith', 'Data Science', 'B', 92),
    ('Alice Johnson', 'DEVOPS', 'A', 88),
    ('Bob Brown', 'DEVOPS', 'B', 76)
]

# Insert the sample data into the STUDENT table
cursor.executemany("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES (?, ?, ?, ?)", sample_data)

## Display all records
print("The inserted records are")

# Retrieve and display the data to verify insertion
data = cursor.execute('''SELECT * FROM STUDENT''')

for row in data:
    print(row)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
