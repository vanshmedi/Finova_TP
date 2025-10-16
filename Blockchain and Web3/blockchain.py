import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        """Create a new block and add it to the chain"""
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.pending_transactions = []
        self.chain.append(block)
        return block
    @staticmethod
    def hash(block):
        """Hashes a block"""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def new_transaction(self, sender, recipient, amount):
        self.pending_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1 if self.chain else 1

    @property
    def last_block(self):
        return self.chain[-1]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            block = self.chain[i]
            last_block = self.chain[i-1]
            if block['previous_hash'] != self.hash(last_block):
                return False
        return True

def main():
    blockchain = Blockchain()
    blockchain.new_transaction('Persons A', 'Person B', 2344)
    blockchain.new_block(proof=12345)

    blockchain.new_transaction('Person C', 'Person D', 50)
    blockchain.new_transaction('Person C', 'Person D', 1150)
    blockchain.new_block(proof=1234567890)

    blockchain.new_transaction('Person C', 'Person D', 50)
    blockchain.new_transaction('Person C', 'Person D', 1150)
    blockchain.new_block(proof=1234567890)

    print("Blockchain created:")
    print(json.dumps(blockchain.chain, indent=2))
    print(f"\nIs the initial chain valid? {blockchain.is_chain_valid()}")

    # Tampering 
    print("\n--- TAMPERING WITH THE CHAIN ---")
    blockchain.chain[2]['transactions'][0]['amount'] = 9999
    print("Changed transaction 1 in Block 2 and setting it to 9999.")

    print(f"Is the tampered chain valid? {blockchain.is_chain_valid()}")
    print("\nValidation fails because the hash of the tampered block no longer matches the 'previous_hash' stored in the next block.")

main()