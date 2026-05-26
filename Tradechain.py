"""
TRADECHAIN - Interactive Blockchain-Based Trading System

REAL-LIFE USE:
Blockchain is used in Bitcoin, Ethereum, and banking systems
to securely store transactions in an immutable ledger.

This project simulates a trading system where users can
send/receive coins and every transaction is stored in a blockchain.
"""

import hashlib
import time



# BLOCK CLASS

class Block:
    def __init__(self, index, data, previous_hash, difficulty=2):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.proof_of_work(difficulty)

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, difficulty):
        prefix = "0" * difficulty

        while True:
            hash_value = self.compute_hash()
            if hash_value.startswith(prefix):
                return hash_value
            self.nonce += 1



# BLOCKCHAIN CLASS

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis Block", "0")

    def add_block(self, data, difficulty=2):
        last_block = self.chain[-1]
        new_block = Block(len(self.chain), data, last_block.hash, difficulty)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.compute_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True

    def display(self):
        for block in self.chain:
            print("\n-------------------")
            print(f"Index: {block.index}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print(f"Prev Hash: {block.previous_hash}")



# TRADE SYSTEM

class TradeSystem:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.wallets = {}

    # Add user
    def add_user(self):
        name = input("Enter user name: ")
        balance = int(input("Enter initial balance: "))
        self.wallets[name] = balance
        print(f"User {name} added successfully!")

    # Show wallets
    def show_wallets(self):
        print("\n--- Wallets ---")
        for user, bal in self.wallets.items():
            print(f"{user}: {bal}")

    # Create transaction
    def create_transaction(self):
        sender = input("Sender: ")
        receiver = input("Receiver: ")
        amount = int(input("Amount: "))

        if sender not in self.wallets or receiver not in self.wallets:
            print("User not found!")
            return

        if self.wallets[sender] < amount:
            print("Insufficient balance!")
            return

        # update balances
        self.wallets[sender] -= amount
        self.wallets[receiver] += amount

        transaction = {
            "from": sender,
            "to": receiver,
            "amount": amount
        }

        self.blockchain.add_block(transaction)
        print("Transaction added to blockchain!")

    # validate chain
    def validate_chain(self):
        if self.blockchain.is_valid():
            print("Blockchain is valid")
        else:
            print("Blockchain is corrupted")



# MENU SYSTEM

def menu():
    chain = Blockchain()
    system = TradeSystem(chain)

    while True:
        print("\n========= TRADECHAIN MENU =========")
        print("1. Add User")
        print("2. Show Wallets")
        print("3. Create Transaction")
        print("4. View Blockchain")
        print("5. Validate Blockchain")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            system.add_user()

        elif choice == "2":
            system.show_wallets()

        elif choice == "3":
            system.create_transaction()

        elif choice == "4":
            chain.display()

        elif choice == "5":
            system.validate_chain()

        elif choice == "6":
            print("Exiting TradeChain...")
            break

        else:
            print("Invalid choice!")



# RUN PROGRAM

if __name__ == "__main__":
    menu()