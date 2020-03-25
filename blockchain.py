import datetime 
import hashlib 
import json
from flask import Flask, jsonify

#(!)WARNING: SHA256 library only accepts encoded strings 

class Blockchain:
    #Need genesis block

    #Blockchain Constructor
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    #METHOD: Creates block
    def create_block(self, proof, previous_hash):
        #Block is dictionary type 
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
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

#=========================================================================================
# FLASK WEBAPP
app = Flask(__name__)

# Blockchain Instance
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods = ['GET'])

# METHOD: Check if Blockchain Is Valid
def is_valid():
    is_valid = blockchain.is_chain_valid()

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