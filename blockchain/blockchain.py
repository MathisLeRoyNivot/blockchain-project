# Blockchain algorithm
import json
from hashlib import sha256
from time import time
from uuid import uuid4

from PyPDF2 import PdfFileReader
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests

FILE_PATH = "assets/Maupassant_Bel_Ami.pdf"
PAGE_ITERATION = 5

pages_list_selected = list()
pages_list_selected_content = list()
pages_list_selected_hashed = list()


# Hash any content
def hash_content(content):
    return sha256(bytes(content, "utf8")).hexdigest()


# PDF Get number of pages
def get_pdf_num_pages(file):
    pdf_reader = PdfFileReader(file)
    num_pages = pdf_reader.getNumPages()
    return num_pages


# PDF Get content of specified page
def get_page_content(file, page_num):
    pdf_reader = PdfFileReader(file)
    page_content = pdf_reader.getPage(page_num).extractText()
    return page_content


# PDF Hash page content
def hash_page_content(file, page_num):
    page_content = get_page_content(file, page_num)
    hashed_content = hash_content(page_content)
    pages_list_selected_hashed.append(hashed_content)
    return hashed_content


# Page treatment
def pages_treatment(file, page):
    if page % PAGE_ITERATION == 0:
        num_pages = get_pdf_num_pages(file)

        for i in range(page, page + PAGE_ITERATION):
            if i <= num_pages:
                pages_list_selected.append(i)
                pages_list_selected_content.append(get_page_content(file, i))
                hash_page_content(file, i)
        # 5 pages full content concat to give one and only one sting
        pages_list_selected_content_concat = " ".join(pages_list_selected_content)
        return pages_list_selected_content_concat
    else:
        return "Error ! 'pages' property needs to be mod(5)", 400


# BLOCKCHAIN Class
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, pages):

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'pages': hash_content(pages_treatment(FILE_PATH, pages))
        })

        return self.last_block['index'] + 1

    def new_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            # Check that the hash of the block is correct
            if block['previous_hash'] != self.hash(last_block):
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):

        neighbours = self.nodes
        new_chain = None

        # Get longer chain compared to current
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace the chain if new one is longer
        if new_chain:
            self.chain = new_chain
            return True

        return False

    @staticmethod
    def hash(block):
        block_string_format = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string_format).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        hashed_guess = sha256(guess).hexdigest()
        return hashed_guess[:4] == "0000"


# Initialize the Node
app = Flask(__name__)

# Generate unique id for the node
node_unique_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # POW to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Mine new block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    block_hash = blockchain.hash(block)

    response = {
        'message': "New block created",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'hash': block_hash,
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200


@app.route('/transactions', methods=['POST'])
def new_transaction():
    data = request.get_json()

    # Check required fields
    required = ['sender', 'recipient', 'pages']
    if not all(k in data for k in required):
        return 'Missing parameters', 400

    # Create a new Transaction
    index = blockchain.new_transaction(data['sender'], data['recipient'], data['pages'])

    response = {'message': f'Transaction will be added to Block #{index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def get_full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    data = request.get_json()

    nodes = data.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.new_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'The chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'The chain is reliable',
            'chain': blockchain.chain
        }

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
