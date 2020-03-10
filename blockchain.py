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