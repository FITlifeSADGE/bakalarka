import hashlib
import random
import string
from parse import get_args
from table import RainbowTable
import data
import pathlib

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored rainbow table data into: ", filename)
    
# Estimate time to generate a table
def estimate_gen_time(chain_len, chain_num):
    hashes_per_sec = 300000
    return((chain_len * chain_num) / hashes_per_sec)

# Check if given arguments are valid
def check_args_gen(args):
    if args.length_max < 1:
        print("Length must be greater than 0")
        exit(1)
    if args.length_min < 1:
        print("Length must be greater than 0")
        exit(1)
    if args.length_max > 30:
        print("Plaintext length is capped at 30")
        exit(1)
    if args.length_min > 30:
        print("Plaintext length is capped at 30")
    if args.columns < 1:
        print("Number of columns must be greater than 0")
        exit(1)
    if args.rows < 1:
        print("Number of rows must be greater than 0")
        exit(1)
    if args.length_min > args.length_max:
        print("Minimum length must be less or equal to maximum length")
        exit(1)
        
def check_args_search(args):
    if args.length_max < 1:
        print("Length must be greater than 0")
        exit(1)
    if args.length_min < 1:
        print("Length must be greater than 0")
        exit(1)
    if args.length_max > 30:
        print("Plaintext length is capped at 30")
        exit(1)
    if args.length_min > 30:
        print("Plaintext length is capped at 30")
    if args.length_min > args.length_max:
        print("Minimum length must be less or equal to maximum length")
        exit(1)

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
def reduce_lower(lower, upper):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (26 ** lower) # Conver hash to number
        plaintext = ""
        diff = upper - lower
        rang = plaintextKey % (diff + 1) + lower # Get Random length
        for _ in range(rang):
            plaintext += string.ascii_lowercase[plaintextKey % 26]
            plaintextKey //= 26
        return plaintext
    return result

def reduce_upper(lower, upper):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (26 ** lower)
        plaintext = ""
        diff = upper - lower
        rang = plaintextKey % (diff + 1) + lower
        for _ in range(rang):
            plaintext += string.ascii_uppercase[plaintextKey % 26]
            plaintextKey //= 26
        return plaintext
    return result

def reduce_letters(lower, upper):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (52 ** lower)
        plaintext = ""
        diff = upper - lower
        rang = plaintextKey % (diff + 1) + lower
        for _ in range(rang):
            plaintext += string.ascii_letters[plaintextKey % 52]
            plaintextKey //= 52
        return plaintext
    return result

def reduce_special_chars(lower, upper):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (100 ** lower)
        plaintext = ""
        diff = upper - lower
        rang = plaintextKey % (diff + 1) + lower
        for _ in range(rang):
            plaintext += string.printable[plaintextKey % 100]
            plaintextKey //= 100
        return plaintext
    return result

def reduce_alphanumeric(lower, upper):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (62 ** lower)
        plaintext = ""
        diff = upper - lower
        rang = plaintextKey % (diff + 1) + lower
        for _ in range(rang):
            plaintext += (string.ascii_letters + string.digits)[plaintextKey % 62]
            plaintextKey //= 62
        return plaintext
    return result

def reduce_all(lower, upper):
    def result(hash, col):
        plaintextKey = (int(hash, 16) ^ col) % (110 ** lower)
        plaintext = ""
        diff = upper - lower
        rang = plaintextKey % (diff + 1) + lower
        for _ in range(rang):
            plaintext += (string.printable + string.digits)[plaintextKey % 110]
            plaintextKey //= 110
        return plaintext
    return result

# Select hashing algorithm
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

# Select reduction function
def get_reduction_func(input: str, lower: int, upper: int):
    if input == 'lowercase':
        return reduce_lower(lower, upper), gen_lower(lower), string.ascii_lowercase
    elif input == 'uppercase':
        return reduce_upper(lower, upper), gen_upper(lower), string.ascii_uppercase
    elif input == 'letters':
        return reduce_letters(lower, upper), gen_letters(lower), string.ascii_letters
    elif input == 'special':
        return reduce_special_chars(lower, upper), gen_special_chars(lower), string.printable
    elif input == 'alphanum':
        return reduce_alphanumeric(lower, upper), gen_alphanumeric(lower), string.ascii_letters + string.digits
    elif input == 'all':
        return reduce_all(lower, upper), gen_all(lower), string.printable + string.digits
    else:
        print("This reduction function is not supported")
        exit(1)
    
    
args = get_args()
if args.mode == "crack":
    plaintext = data.search_password(args.hash) # Search for password in database
    if plaintext:
        print("Password found in database: {0}".format(plaintext[0]))
        exit(0)
    try: 
        int(args.hash, 16)
    except:
        print("Hash is not in hexadecimal format")
        exit(1)
    table = RainbowTable(hashlib.md5, 10, reduce_lower(5, 10), gen_lower(5), "md5", "lowercase", 5, 6) # Create empty table
    if not args.path.endswith("/"): # Add / to path if not present
        args.path += "/"
    table.load_from_cvs(filename= args.path + args.table) # Load table from file
    hashing_alg = get_hashing_alg(table.table['alg'])
    reduction_func, _, _ = get_reduction_func(table.table['rest'], int(table.table['len']), int(table.table['len_max']))
    table.hash_func = hashing_alg
    table.chain_len = int(table.table['chain_len'])
    table.reduction_func = reduction_func
    result = table.crack(args.hash)
    
    id = data.get_table_id(args.table) # Get id of table for later update of values
    
    if result is not None:
        #clear()
        print("Succes, the password is {0}".format(result))
        data.update_table(True, id)
        data.add_password_to_database(args.hash, result)
    else:
        #clear()
        print("Password not found")
        data.update_table(False, id) 
    
elif args.mode == "gen":
    check_args_gen(args)
    if args.length_min < 5:
        print("Minimum length of less than 5 results in many collisions, which can cause the table to be unusable")
        print("do you wish to continue? (y/n)")
        inp = input()
        if inp != "y":
            exit(1)
    hashing_alg = get_hashing_alg(args.algorithm)
    reduction_func, gen_func, charset = get_reduction_func(args.restrictions, args.length_min, args.length_max)
    
    table = RainbowTable(hashing_alg, args.columns, reduction_func, gen_func, args.algorithm, args.restrictions, args.length_min, args.length_max)
    if args.filename[-4:] != ".csv": # Add .csv to filename if not present
        args.filename += ".csv"
    estimate = estimate_gen_time(args.rows, args.columns)
    print("Estimated time to generate table assuming average CPU : {0} mins, {1} seconds".format(int(estimate/60), int(estimate % 60)))
    print("Do you wish to continue? (y/n)")
    inp = input()
    if inp == "n":
        print("Exiting...")
        exit(0)
    elif inp == "y":
        pass
    else: 
        print("Invalid input, exiting...")
        exit(0)
    table.gen_table(rows=args.rows, file=args.filename)
    
    data.add_table_to_database(table, args.filename)
    
    print("""rainbow table {3} parameters:
          hash algorithm:   {0}
          charset name:     {1}
          charset length:   {2}
          charset data:     {4}
        """.format(args.algorithm, args.restrictions, len(charset), args.filename, charset))
    
elif args.mode == "search":
    check_args_search(args)
    res = data.get_tables(args.algorithm, args.restrictions, args.length_min, args.length_max)
    print("Found {0} tables".format(len(res)))
    for table in res:
        print("""
              name :                    {0}
              number of tries:          {1}
              successful tries:         {2}
              password length range:    {3} to {4} characters
              ID:                       {5}""".format(table[0], table[1], table[2], table[4], table[5], table[3]))
        print("Select a table using load path ID")
    
elif args.mode == "load":
    name = data.fetch_table(args.ID)
    if not name: # Check if table exists
        print("No table with this ID")
        exit(1)
    if not pathlib.Path(args.path).exists(): # Check if path exists
        print("Path does not exist")
        exit(0)
    path = args.path + "/" + name[0][1] # Create path to file
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