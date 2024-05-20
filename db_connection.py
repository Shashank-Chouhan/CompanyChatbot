import sqlite3
conn = sqlite3.connect('example.db')
cursor = conn.cursor()

def create_connection():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    return cursor, conn

def load_tables(cursor= cursor, conn= conn):
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS qadb (
        question_number INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer INTEGER NOT NULL
    )
    ''')

    question = 'This is the question?'
    answer = 'This is the answer.'
    cursor.execute('INSERT INTO qadb (question, answer) VALUES (?, ?)', (question, answer))
    conn.commit()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS admin_list (
        admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_name TEXT NOT NULL,
        admin_password TEXT NOT NULL
    )
    ''')
    admin_name = "admin"
    admin_password = "admin123"
    cursor.execute('INSERT INTO admin_list (admin_name, admin_password) VALUES (?, ?)', (admin_name, admin_password))
    conn.commit()


def add_qa_tuple_in_table(qa_tuple, cursor= cursor, conn= conn):
    new_question, new_answer = qa_tuple
    cursor.execute('INSERT INTO qadb (question, answer) VALUES (?, ?)', (new_question, new_answer))
    conn.commit()
    return 200

def delete_qa_tuple_from_table( question_number,cursor= cursor, conn= conn):    
    cursor.execute('DELETE FROM qadb WHERE question_number = ?', (question_number,))
    conn.commit()
    # cursor.execute('SELECT * FROM qadb ')
    # rows = cursor.fetchall()
    # print(rows)
    return f"Question number {question_number} deleted successfully."

def update_qa_tuple_from_table(question_number, new_question, new_answer,cursor= cursor, conn= conn):
    cursor.execute('UPDATE qadb SET question = ?, answer = ? WHERE question_number = ?', (new_question, new_answer, question_number))
    conn.commit()
    # cursor.execute('SELECT * FROM qadb ')
    # rows = cursor.fetchall()
    # print(rows)
    return 200

def show_qadb(cursor= cursor, conn= conn):
    cursor.execute('SELECT question_number, question, answer FROM qadb ' )
    rows = cursor.fetchall()
    print(rows)
    # print(type(rows))
    return rows

def delete_whole_table( cursor= cursor, conn= conn):    
    cursor.execute('DELETE FROM qadb')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name=?', ('qadb',))
    conn.commit()
    # cursor.execute('SELECT * FROM qadb ')
    # rows = cursor.fetchall()
    # print(rows)
    return f"Whole database deleted successfully."
    
def close_connection(cursor, conn):  
    cursor.close()
    conn.close()


# FORMAT TO USE THESE FUNCTIONS IN OTHER FILES

# cursor, conn = create_connection()
# cursor.execute('DROP TABLE IF EXISTS qadb')
# conn.commit()
# print(show_qadb(cursor))
# perform these functions

# close_connection(cursor, conn)


