# Blockchain algorithm
import json
import datetime
from hashlib import sha256
from PyPDF2 import PdfFileReader
from flask import Flask, request
import requests

PAGE_ITERATION = 5

pdf_file_path = input("Which file you want to proceed into the blockchain ? (copy/paste file path)\n")
pdf_file_page_number = int(input("Page no. ?\n"))

pdf_file = open(pdf_file_path, 'rb')
pages_list_selected = list()
pages_list_selected_content = list()
pages_list_selected_hashed = list()


def hash_content(content):
    return sha256(bytes(content, "utf8")).hexdigest()


def get_pdf_num_pages(file):
    pdf_reader = PdfFileReader(file)
    num_pages = pdf_reader.getNumPages()
    return num_pages


def get_page_content(file, page_num):
    pdf_reader = PdfFileReader(file)
    page_content = pdf_reader.getPage(page_num).extractText()
    return page_content


def hash_page_content(file, page_num):
    page_content = get_page_content(file, page_num)
    hashed_content = hash_content(page_content)
    pages_list_selected_hashed.append(hashed_content)


def pages_treatment(file, page):
    if page % PAGE_ITERATION == 0:
        num_pages = get_pdf_num_pages(file)

        for i in range(page, page + PAGE_ITERATION):
            if i <= num_pages:
                pages_list_selected.append(i)
                pages_list_selected_content.append(get_page_content(file, i))
                hash_page_content(file, i)
    else:
        print("Error !")


class Block:
    block_num = 0
    transactions = []
    previous_hash = "0"
    block_hash = None
    nonce = 0
    timestamp = datetime.datetime.now()
    
    def __init__(self, block_num, transactions):
        self.block_num = block_num
        self.transactions = transactions

    def hash_object(self):
        json_data = json.dumps(self.__dict__, sort_keys=True)
        self.block_hash = hash_content(json_data)
        return self.block_hash

    def __str__(self):
        return "Block # : " + str(self.block_num) + \
               "\nBlock hash : " + self.block_hash + \
               "\nBlock previous hash : " + self.previous_hash + \
               "\nBlock nonce : " + str(self.nonce) + \
               "\nBlock transaction hash : " + " ".join(self.transactions) + \
               "\nBlock timestamp : " + self.timestamp.strftime("%m/%d/%Y %H:%M:%S")


class Blockchain:
    # Proof of work difficulty
    difficulty = 2

    def __init__(self):
        self.transactions_awaiting_confirmation = []
        self.chain = []

    # Create the first blockchain block
    def create_genesis_block(self):
        genesis_block = Block(0, [])
        genesis_block.hash = genesis_block.hash_object()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_new_block(self, block, proof):
        previous_hash = self.last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    @staticmethod
    def proof_of_work(block):
        block.nonce = 0

        computed_hash = block.hash_object()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.hash_object()

        return computed_hash

    def add_new_transaction(self, transaction):
        self.transactions_awaiting_confirmation.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.hash_object())

    @classmethod
    def check_chain_validity(cls, chain):
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash
            # remove the hash field to recompute the hash again
            # using `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block.hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.transactions_awaiting_confirmation:
            return False

        last_block = self.last_block

        new_block = Block(block_num=last_block.index + 1,
                          transactions=self.transactions_awaiting_confirmation)

        new_block.previous_hash = last_block.hash

        proof = self.proof_of_work(new_block)
        self.add_new_block(new_block, proof)

        self.transactions_awaiting_confirmation = []

        return True


app = Flask(__name__)

#blockchain = Blockchain()
#blockchain.create_genesis_block()

# the address to other participating members of the network
peers = set()


# endpoint to submit a new transaction. This will be used by
# our application to add new data (posts) to the blockchain
@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    tx_data = request.get_json()
    required_fields = ["author", "content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = datetime.datetime.now()

    blockchain.add_new_transaction(tx_data)

    return "Success", 201


# endpoint to return the node's copy of the chain.
# Our application will be using this endpoint to query
# all the posts to display.
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({
        "length": len(chain_data),
        "chain": chain_data,
        "peers": list(peers)
    })


# endpoint to request the node to mine the unconfirmed
# transactions (if any). We'll be using it to initiate
# a command to mine from our application itself.
@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    result = blockchain.mine()
    if not result:
        return "No transactions to mine"
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        consensus()
        if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
            announce_new_block_added(blockchain.last_block)
        return "Block #{} is mined.".format(blockchain.last_block.index)


# endpoint to add new peers to the network.
@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.add(node_address)

    # Return the consensus blockchain to the newly registered node
    # so that he can sync
    return get_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the node specified in the
    request, and sync the blockchain as well as peer data.
    """
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        return response.content, response.status_code


def create_chain_from_dump(chain_dump):
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()
    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # skip genesis block
        block = Block(block_data["block_num"],
                      block_data["transactions"])

        block.previous_hash = block_data["previous_hash"]
        block.nonce = block_data["nonce"]
        proof = block_data['hash']
        added = generated_blockchain.add_new_block(block, proof)
        if not added:
            raise Exception("The chain dump is tampered!!")
    return generated_blockchain


# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["block_num"],
                  block_data["data"],
                  block_data["transactions"],
                  block_data["previous_hash"],
                  block_data["nonce"])

    proof = block_data['hash']
    added = blockchain.add_new_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


# endpoint to query unconfirmed transactions
@app.route('/pending_transactions')
def get_pending_transactions():
    return json.dumps(blockchain.transactions_awaiting_confirmation)


def consensus():
    """
    Our naive consnsus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']

        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block_added(block):
    """
    A function to announce to the network once a block has been mined.
    Other blocks can simply verify the proof of work and add it to their
    respective chains.
    """
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        requests.post(
            url,
            data=json.dumps(block.__dict__, sort_keys=True),
            headers=headers)


# Uncomment this line if you want to specify the port number in the code
# app.run(debug=True, port=8000)

def main():
    # Select only requested pages
    pages_treatment(pdf_file_path, pdf_file_page_number)

    # 5 pages selected list content concat hashed
    pages_list_selected_content_concat = " ".join(pages_list_selected_content)
    hash_content(pages_list_selected_content_concat)

    block = Block(block_num=0, transactions=pages_list_selected_content_concat)
    blockchain = Blockchain()
    # blockchain.create_genesis_block()
    # print(blockchain.__dict__)

    #for attr in blockchain.__dict__:
    #    if attr == "chain":
    #        for i in getattr(blockchain, attr):
    #            print(i)
            # print(json.dumps(getattr(blockchain, attr)))
    # Block(0, hash_content(pages_list_selected_content_concat))


main()
