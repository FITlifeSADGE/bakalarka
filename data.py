import sqlite3
import table

con = sqlite3.connect('/usr/share/collections/RTables/tables.db')
cur = con.cursor()


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open("/usr/share/collections/RTables/" + filename, 'rb') as file:
        blobData = file.read()
    return blobData

cur.execute("""CREATE TABLE IF NOT EXISTS RainbowTable(
    id INTEGER PRIMARY KEY, 
    chain_len INTEGER, 
    hashing_alg TEXT, 
    reduction_function TEXT, 
    password_length_min INTEGER, 
    password_length_max INTEGER,
    name TEXT, 
    number_of_tries INTEGER, 
    successful_tries INTEGER,
    dict_text BLOB NOT NULL)""")

cur.execute("""CREATE TABLE IF NOT EXISTS Password(
    hash TEXT PRIMARY KEY,
    plaintext TEXT
    )""")

con.commit()


def add_table_to_database(RT: table.RainbowTable, RTname): 
    chain_len = RT.chain_len
    hash_alg = RT.alg
    rest = RT.rest
    min_length = RT.len
    max_length = RT.len_max
    table_text = convertToBinaryData(RTname)
    try:
        new_ID = cur.execute("SELECT MAX(id) FROM RainbowTable").fetchone()[0] + 1
    except:
        new_ID = 1
    cur.execute("INSERT INTO RainbowTable VALUES (?, ?, ?, ?, ?, ?, ?, 0, 0, ?)", (new_ID, chain_len, hash_alg, rest, min_length, max_length, RTname, table_text))
    con.commit()
    
def get_tables(alg: str, rest: str, length_min: int, length_max: int):
    cur.execute("SELECT name, number_of_tries, successful_tries, id, password_length_min, password_length_max FROM RainbowTable WHERE hashing_alg = ? AND reduction_function = ? AND password_length_min <= ? AND password_length_max >= ?", (alg, rest, length_min, length_max))
    return cur.fetchall()

def update_table(success: bool, id: int):
    if success:
        con.execute("""UPDATE RainbowTable SET number_of_tries = number_of_tries + 1, successful_tries = successful_tries + 1 WHERE id = ?""", (id,))
    else:
        con.execute("""UPDATE RainbowTable SET number_of_tries = number_of_tries + 1 WHERE id = ?""", (id,))
    con.commit()
    
def fetch_table(id: int):
    cur.execute("SELECT dict_text, name FROM RainbowTable WHERE id = ?", (id,))
    return cur.fetchall()

def get_table_id(RT_name: str):
    cur.execute("SELECT id FROM RainbowTable WHERE name = ? AND dict_text = ?", (RT_name, convertToBinaryData(RT_name)))
    return cur.fetchone()[0]
    
def add_password_to_database(hash: str, plaintext: str):
    cur.execute("INSERT INTO Password VALUES (?, ?)", (hash, plaintext))
    con.commit()
    
def search_password(hash: str):
    cur.execute("SELECT plaintext FROM Password WHERE hash = ?", (hash,))
    return cur.fetchone()
    
