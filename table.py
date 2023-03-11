import time
import pickle
import csv

CSV_FIELDNAMES = ['start_point', 'endpoint_hash']

class RainbowTable:
    def __init__(self, hash_func, chain_len, reduction_func, gen_func):
        self.table = {}
        self.hash_func = hash_func
        self.chain_len = chain_len
        self.gen_func = gen_func
        self.reduction_func = reduction_func
        
    def gen_table(self, pickle_file="RainbowTable.pickle", rows=3*10**6, extend=False):
        startTime = time.time()
        if not extend:
            self.table = {}
        for i in range(rows):
            if i % 1000 == 0:
                print(i)
            
            start = self.gen_func()
            
            plainText = start
            for col in range(self.chain_len):
                hashcode = self.hash_func(plainText.encode('utf-8')).hexdigest()
                plainText = self.reduction_func(hashcode, col)
            self.table[hashcode] = start
        pickle.dump(self.table, open(pickle_file, "wb"))
        
        elapsed = time.time() - startTime
        print("Done in {0} mins, {1} secs.".format(int(elapsed / 60), elapsed % 60))
  
    def load_table(self, pickle_file="table.pickle"):
        startTime = time.time()
        self.table = {}
        
        if pickle_file.endswith('.csv'):
            print("Loading rainbow table from CSV...")
            with open(pickle_file, 'r') as table:
                reader = csv.DictReader(table)
                for row in reader:
                    self.table[row[CSV_FIELDNAMES[1]]] = row[CSV_FIELDNAMES[0]]
        else:
            print("Loading rainbow table from pickle...")
            self.table = pickle.load(open(pickle_file, "rb"))
            
        print("Done loading in {0} secs.".format(time.time() - startTime))
  
    def export_csv(self, filename="RainbowTable.csv"):
        with open(filename, 'w') as table:
            writer = csv.DictWriter(table, fieldnames=CSV_FIELDNAMES) 
            writer.writeheader()
            for k, v in self.table.items():
                writer.writerow({CSV_FIELDNAMES[0]: v, CSV_FIELDNAMES[1]: k})

    def crack(self, hashedPassword):
        for startCol in range(self.chain_length-1, -1, -1):
            candidate = hashedPassword
            for col in range(startCol, self.chain_length):
                candidate = self.hash_func(self.reduction_func(candidate, col-1).encode('utf-8')).hexdigest()
            if candidate in self.table:
                traversalResult = self.traverse_chain(hashedPassword, self.table[candidate])
                if traversalResult:
                    return traversalResult
 
    def traverse_chain(self, hashedPassword, start):
        for col in range(self.chain_length):
            hash = self.H(start)
            if hash == hashedPassword:
                return start
            start = self.reduction_func(hash, col)
            
        return None