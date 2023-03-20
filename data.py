import sqlite3
import table

con = sqlite3.connect('tables.db')
cur = con.cursor()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

cur.execute("""CREATE TABLE IF NOT EXISTS RainbowTable(
    id INTEGER PRIMARY KEY, 
    chain_len INTEGER, 
    hashing_alg TEXT, 
    reduction_function TEXT, 
    password_length INTEGER, 
    name TEXT, 
    number_of_tries INTEGER, 
    successful_tries INTEGER,
    dict_text BLOB NOT NULL)""")

con.commit()


def add_table_to_database(RT: table.RainbowTable, RTname): 
    chain_len = RT.chain_len
    hash_alg = RT.alg
    rest = RT.rest
    length = RT.len
    table_text = convertToBinaryData(RTname)
    try:
        new_ID = cur.execute("SELECT MAX(id) FROM RainbowTable").fetchone()[0] + 1
    except:
        new_ID = 1
    cur.execute("INSERT INTO RainbowTable VALUES (?, ?, ?, ?, ?, ?, 0, 0, ?)", (new_ID, chain_len, hash_alg, rest, length, RTname, table_text))
    con.commit()
    
def get_tables(alg: str, rest: str, length: int):
    max_len = cur.execute("SELECT MAX(password_length) FROM RainbowTable WHERE hashing_alg = ? AND reduction_function = ?", (alg, rest)).fetchone()[0]
    if length > 8:
        cur.execute("SELECT name, number_of_tries, successful_tries, id, password_length FROM RainbowTable WHERE hashing_alg = ? AND reduction_function = ? AND password_length BETWEEN ? AND ?", (alg, rest, length, max_len))
    else:
        cur.execute("SELECT name, number_of_tries, successful_tries, id, password_length FROM RainbowTable WHERE hashing_alg = ? AND reduction_function = ? AND password_length = ?", (alg, rest, length))
    return cur.fetchall()

def update_table(success: bool, id: int):
    if success:
        con.execute("""UPDATE RainbowTable SET number_of_tries = number_of_tries + 1, successful_tries = successful_tries + 1 WHERE id = ?""", (id))
    else:
        con.execute("""UPDATE RainbowTable SET number_of_tries = number_of_tries + 1 WHERE id = ?""", (id))
    con.commit()
    
def fetch_table(id: int):
    cur.execute("SELECT dict_text, name FROM RainbowTable WHERE id = ?", (id,))
    return cur.fetchall()
    
    
