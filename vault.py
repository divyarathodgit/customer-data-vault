import os
import random
import string
import time
import json

class CustomerDataVault:
    def __init__(self, db_file="vault_data.log"):
        self.db_file = db_file
        self.index = {}  # The In-Memory Hash Map (Key: Transaction ID, Value: Byte Offset)
        
        # Make sure the file exists
        if not os.path.exists(self.db_file):
            open(self.db_file, 'w').close()
            
        # If the database already has data, we need to rebuild the index on startup
        self._build_index()

    def _build_index(self):
        """Reads the existing log file and maps IDs to their byte locations."""
        print("Building in-memory index from disk...")
        with open(self.db_file, 'r') as f:
            while True:
                offset = f.tell() # Get the exact byte location before reading the line
                line = f.readline()
                if not line:
                    break
                
                # Parse the JSON record and save the offset
                record = json.loads(line)
                self.index[record['transaction_id']] = offset

    def insert_record(self, transaction_id, sale_amount, customer_name, category):
        """Appends a new record to the end of the file and updates the index."""
        record = {
            "transaction_id": transaction_id,
            "sale_amount": sale_amount,
            "customer_name": customer_name,
            "category": category
        }
        
        with open(self.db_file, 'a') as f:
            offset = f.tell() # Get the byte location where we are about to write
            # We use json.dumps to make the data clean and structured
            f.write(json.dumps(record) + '\n') 
            
        # Update our RAM index so we can find it instantly later
        self.index[transaction_id] = offset

    def get_record_fast(self, transaction_id):
        """O(1) Real-World Retrieval: Jumps instantly to the byte location."""
        if transaction_id not in self.index:
            return None
            
        offset = self.index[transaction_id]
        
        with open(self.db_file, 'r') as f:
            f.seek(offset) # BLINDINGLY FAST: Jump directly to the byte offset on disk
            line = f.readline()
            return json.loads(line)

    def get_record_slow(self, transaction_id):
        """O(N) Academic Retrieval: Scans the file line by line (The old way)."""
        with open(self.db_file, 'r') as f:
            for line in f:
                record = json.loads(line)
                if record['transaction_id'] == transaction_id:
                    return record
        return None

# def generate_and_test():
#     vault = CustomerDataVault("production_vault.log")
#     num_records = 100000 # 100k records for a real stress test
    
#     # 1. GENERATE DATA
#     print(f"\n--- 1. Generating {num_records} Records ---")
#     for i in range(1, num_records + 1):
#         sale = random.randint(1, 80000)
#         name = ''.join(random.choices(string.ascii_uppercase, k=3))
#         cat = random.randint(1, 1500)
#         vault.insert_record(i, sale, name, cat)
#     print("Data successfully written to production_vault.log")

#     # 2. THE STRESS TEST
#     target_id = 99999 # Searching for a record near the very end of the database
#     print(f"\n--- 2. Performance Stress Test (Searching for ID: {target_id}) ---")
    
#     # Test A: The Slow Way (Sequential Scan)
#     start_time = time.perf_counter()
#     vault.get_record_slow(target_id)
#     slow_time = time.perf_counter() - start_time
#     print(f"Standard Sequential Scan: {slow_time:.6f} seconds")

#     # Test B: Your Custom Engine (Byte-Offset Seek)
#     start_time = time.perf_counter()
#     vault.get_record_fast(target_id)
#     fast_time = time.perf_counter() - start_time
#     print(f"Custom Hash-Indexed Seek: {fast_time:.6f} seconds")

#     # 3. THE RESUME METRIC
#     speedup = ((slow_time - fast_time) / slow_time) * 100
#     print(f"\n>>> RESULT: Your engine is {speedup:.2f}% faster than a standard scan. <<<")

# if __name__ == "__main__":
#     generate_and_test()
def interactive_cli():
    print("\n=========================================")
    print("   CUSTOMER DATA VAULT - SERVER ACTIVE   ")
    print("=========================================")
    
    # Initialize the vault (it will load the 100k records we just built)
    vault = CustomerDataVault("production_vault.log")
    print(f"Index loaded. Currently tracking {len(vault.index)} records.")
    
    while True:
        print("\nCommands: [1] Search ID  [2] Insert New  [3] Exit")
        choice = input("vault> ").strip()
        
        if choice == '1':
            target = input("Enter Transaction ID to search: ").strip()
            if not target.isdigit():
                print("Error: ID must be a number.")
                continue
                
            # Start the timer for the fast seek
            start = time.perf_counter()
            record = vault.get_record_fast(int(target))
            latency = time.perf_counter() - start
            
            if record:
                print(f"Found in {latency:.6f}s: {record}")
            else:
                print("Record not found.")
                
        elif choice == '2':
            try:
                t_id = int(input("New Transaction ID: "))
                if t_id in vault.index:
                    print("Error: ID already exists.")
                    continue
                    
                sale = int(input("Sale Amount (1-80000): "))
                name = input("Customer Name (3 letters): ").upper()[:3]
                cat = int(input("Item Category (1-1500): "))
                
                vault.insert_record(t_id, sale, name, cat)
                print(f"Success! Record {t_id} appended to disk and indexed in RAM.")
            except ValueError:
                print("Invalid input. Please enter correct data types.")
                
        elif choice == '3':
            print("Shutting down vault server. Goodbye!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    # If you ever need to regenerate the 100k records, uncomment the line below:
    # generate_and_test() 
    
    interactive_cli()