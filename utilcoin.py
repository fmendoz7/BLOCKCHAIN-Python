# NECESSARY DEPENDENCIES
    # Flask v0.12.2 
    # Postman
    # requests v2.18.4

import datetime 
import hashlib 
import json
from flask import Flask, jsonify, request
import requests #used to check on Blockchain Nodes

from uuid import uuid4
from urllib.parse import urlparse

import requests

#(!)WARNING: SHA256 library only accepts encoded strings 

class Blockchain:
    #Need genesis block

    #Blockchain Constructor
    def __init__(self):
        self.chain = []
        self.transactions = [] #For cryptocurrency
        self.create_block(proof = 1, previous_hash = '0')

    #METHOD: Creates block
    def create_block(self, proof, previous_hash):
        #Block is dictionary type 
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions':self.transactions #ever-increasing list of transactions
                 }
        self.transactions = []
        self.chain.append(block)
        return block

    #METHOD: Getter method for previous
    def get_previous_block(self):
        return self.chain[-1] #gets last

    #METHOD: Helper method to give complex input for sha256 algorithm
    def proof_complexity(new_proof, previous_proof):
        tempProof = str(new_proof**2 - previous_proof**2).encode()
        return tempProof

    #METHOD: Proof Of Work Mechanism
    def proof_of_work(self, previous_proof):
        new_proof = 1 #initial value 
        check_proof = False

        while(check_proof is False):
            #Create helper method later that will increase complexity of input for sha256 library
            hash_operation = hashlib.sha256(proof_complexity(new_proof, previous_proof)).hexdigest()
            
            #(!) REMEMBER: Number of zeros correspond to mining difficulty. Itc, 4
            if(hash_operation[:4] == '0000'):
                check_proof = True
            #Else, keep incrementng new_proof by one
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        #Encode into the right format to be accepted by SHA256 library
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        
        while(block_index < len(chain)):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(proof_complexity(proof, previous_proof)).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})

        previous_block = self.get_previous_block()
        #Return new block
        return previous_block['index'] + 1 

#=========================================================================================
# FLASK WEBAPP
app = Flask(__name__)

# Blockchain Instance
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])

# METHOD: Check if Blockchain Is Valid
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'SUCCESS: Blockchain Is Valid'}
    else:
        response = {'message': 'WARNING: Blockchain Is NOT Valid'}
    return jsonify(response), 200

#METHOD: Mine block
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Block Successfully Mined!',
                'index': block[index],
                'timestamp': block['timestamp'],
                'proof': block['proof'], 
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200 #status code 200 = request has succeeded

# REQUEST: Get Full Blockchain
@app.route('/get_chain', methods = ['GET'])

def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Run the App
app.run(host = '0.0.0.0', port = 5000)

#=========================================================================================
# Incorporate Cryptocurrency (new code)

class UtilCoin(Blockchain):
    def __init__(self):
        self.node_address = stry(uuid64()).replace('-', '')
        self.transactions = [] #transaction is a list (of dictionaries)
        self.nodes = set()
        super().__init__() #inherit from superclass Blockchain

    # Method to create block 
    def create_block(self, proof, previous_hash):
        "Create a block with new transactions."

        # Block takes DICTIONARY form with index, timestamp, proof, previous hash, transaction
        block = {
            'index': len(self.chain),
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.transactions
        }

        self.transactions = []
        self.chain.append(block)

        return block

    #Append individual transaction (dictionary) to list of transactions
    def add_transaction(self, sender, receiver, amount):
        "Add a transaction to list of transactions."

        #Append new transaction from parameters
        self.transactions.append(
            {
                'sender': sender,
                'receiver': receiver,
                'amount': amount
            })
        
        #Return new block (remember: multiple transactions are packaged in a block)
        return self.get_previous_block()['index'] + 1

    #METHOD: Add node to UtilCoin network given address
    def add_node(self, address):
        "Add a node to UtilCoin network."

        parsed_url = urlparse(aaddress)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        "Scan the network for longest chain and replace current chain accordingly."
            #Handled using Redis in alternative JS implementation

        longest_chain = None
        longest_chain_length = len(self.chain)

        for node in self.nodes: 
            response = requests.get(f'http://{node}blocks')

            #Will continue to retry the node until it connects
            if not response.status_code == 200:
                printf(f'Bad response from {node}: {response.status_code}')
                continue #rejects all remaining statements, moves control to the top of the loop

            node_chain = response.json()['chain']
            node_chain_length = response.json()['length']

            if node_chain_length > longest_chain_length and self.is_chain_valid(node_chain):
                longest_chain_length = node_chain_length
                longest_chain = node_chain

        if longest_chain is not None:
            self.chain = longest_chain
            return True

        return False