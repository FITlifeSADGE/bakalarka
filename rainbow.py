import hashlib
import random
import string
from parse import get_args
from table import RainbowTable, clear
import data
import pathlib

usual_password_len = 8

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored rainbow table data into: ", filename)

# Word generator functions
def gen_lower(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_lowercase)
        return password
    return result

def gen_upper(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_uppercase)
        return password
    return result

def gen_letters(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_letters)
        return password
    return result

def gen_special_chars(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.printable)
        return password
    return result

def gen_alphanumeric(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.ascii_letters + string.digits)
        return password
    return result

def gen_all(n):
    def result():
        password = ""
        for _ in range(n):
            password += random.choice(string.digits + string.printable)
        return password
    return result


# Reduction functions
def reduce_lower(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (26 ** n)
        plaintext = ""
        if n > usual_password_len:
            rang = plaintextKey % (n - usual_password_len + 1) + usual_password_len
            for _ in range(rang):
                plaintext += string.ascii_lowercase[plaintextKey % 26]
                plaintextKey //= 26
        else:
            for _ in range(n):
                plaintext += string.ascii_lowercase[plaintextKey % 26]
                plaintextKey //= 26
        return plaintext
    return result

def reduce_upper(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (26 ** n)
        plaintext = ""
        if n > usual_password_len:
            rang = plaintextKey % (n - usual_password_len + 1) + usual_password_len
            for _ in range(rang):
                plaintext += string.ascii_uppercase[plaintextKey % 26]
                plaintextKey //= 26
        else:
            for _ in range(n):
                plaintext += string.ascii_uppercase[plaintextKey % 26]
                plaintextKey //= 26
        return plaintext
    return result

def reduce_letters(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (52 ** n)
        plaintext = ""
        if n > usual_password_len:
            rang = plaintextKey % (n - usual_password_len + 1) + usual_password_len
            for _ in range(rang):
                plaintext += string.ascii_letters[plaintextKey % 52]
                plaintextKey //= 52
        else:
            for _ in range(n):
                plaintext += string.ascii_letters[plaintextKey % 52]
                plaintextKey //= 52
        return plaintext
    return result

def reduce_special_chars(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (100 ** n)
        plaintext = ""
        if n > usual_password_len:
            rang = plaintextKey % (n - usual_password_len + 1) + usual_password_len
            for _ in range(rang):
                plaintext += string.printable[plaintextKey % 100]
                plaintextKey //= 100
        else:
            for _ in range(n):
                plaintext += string.printable[plaintextKey % 100]
                plaintextKey //= 100
        return plaintext
    return result

def reduce_alphanumeric(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (62 ** n)
        plaintext = ""
        if n > usual_password_len:
            rang = plaintextKey % (n - usual_password_len + 1) + usual_password_len
            for _ in range(rang):
                plaintext += (string.ascii_letters + string.digits)[plaintextKey % 62]
                plaintextKey //= 62
        else:
            for _ in range(n):
                plaintext += (string.ascii_letters + string.digits)[plaintextKey % 62]
                plaintextKey //= 62
        return plaintext
    return result

def reduce_all(n):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (110 ** n)
        plaintext = ""
        if n > usual_password_len:
            rang = plaintextKey % (n - usual_password_len + 1) + usual_password_len
            for _ in range(rang):
                plaintext += (string.printable + string.digits)[plaintextKey % 110]
                plaintextKey //= 110
        else:
            for _ in range(n):
                plaintext += (string.printable + string.digits)[plaintextKey % 110]
                plaintextKey //= 110
        return plaintext
    return result

def get_hashing_alg(input: str):
    if input == 'md5':
        return hashlib.md5
    elif input == 'sha1':
        return hashlib.sha1
    elif input == 'sha256':
        return hashlib.sha256
    elif input == 'sha512':
        return hashlib.sha512
    else:
        print("This hashing algorithm is not supported")
        exit(1)
        
def get_reduction_func(input: str, n: int):
    if input == 'lowercase':
        return reduce_lower(n), gen_lower(n)
    elif input == 'uppercase':
        return reduce_upper(n), gen_upper(n)
    elif input == 'letters':
        return reduce_letters(n), gen_letters(n)
    elif input == 'special':
        return reduce_special_chars(n), gen_special_chars(n)
    elif input == 'alphanum':
        return reduce_alphanumeric(n), gen_alphanumeric(n)
    elif input == 'all':
        return reduce_all(n), gen_all(n)
    else:
        print("This reduction function is not supported")
        exit(1)
    
    
args = get_args()
if args.mode == "crack":
    table = RainbowTable(hashlib.md5, 10, reduce_lower(5), gen_lower(5), "md5", "lowercase", 5)
    table.load_from_cvs(filename=args.table)
    hashing_alg = get_hashing_alg(table.table['alg'])
    reduction_func, _ = get_reduction_func(table.table['rest'], int(table.table['len']))
    table.hash_func = hashing_alg
    table.chain_len = int(table.table['chain_len'])
    table.reduction_func = reduction_func
    result = table.crack(args.hash)
    if result is not None:
        #clear()
        print("Succes, the password is {0}".format(result))
    else:
        #clear()
        print("Password not found")
    
    
elif args.mode == "gen":
    if args.length < 1:
        print("Length must be greater than 0")
        exit(1)
    if args.columns < 1:
        print("Number of columns must be greater than 0")
        exit(1)
    if args.rows < 1:
        print("Number of rows must be greater than 0")
        exit(1)
    hashing_alg = get_hashing_alg(args.algorithm)
    reduction_func, gen_func = get_reduction_func(args.restrictions, args.length)
    
    table = RainbowTable(hashing_alg, args.columns, reduction_func, gen_func, args.algorithm, args.restrictions, args.length)
    table.gen_table(rows=args.rows, file=args.filename)
    
    data.add_table_to_database(table, args.filename)
    
elif args.mode == "search":
    res = data.get_tables(args.algorithm, args.restrictions, args.length)
    print("Found {0} tables".format(len(res)))
    for table in res:
        print("name : {0}, number of tries: {1}, successful tries: {2}, password length up to {3} characters, ID: {4}".format(table[0], table[1], table[2], table[4], table[3]))
        print("Select a table using load path ID")
    
elif args.mode == "load":
    name = data.fetch_table(args.ID)
    path = args.path + "/" + name[0][1]
    if pathlib.Path(path).is_file():
        print("File already exists, are you sure you want to rewrite it? (y/n)")
        inp = input()
        if inp == "y":
            writeTofile(name[0][0], path)
        elif inp == "n":
            print("Exiting...")
            exit(0)
        else: 
            print("Invalid input, exiting...")
            exit(0)
    else:
        print("Downloading file...")
        writeTofile(name[0][0], path)
        print("Done")
    