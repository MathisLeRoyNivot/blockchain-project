# Block object
from hashlib import sha256
import datetime


class Block:
    block_num = 0
    data = None
    next = 0
    block_hash = None
    nonce = 0
    previous_hash = 0x0
    timestamp = datetime.datetime.now()

    def __init__(self, data):
        self.data = data

    def hash(self):
        return sha256(
            bytes(str(self.nonce), "utf8") +
            bytes(str(self.data), "utf8") +
            bytes(str(self.previous_hash), "utf8") +
            bytes(str(self.timestamp), "utf8") +
            bytes(str(self.block_num), "utf8")
        ).hexdigest()

    def __str__(self):
        return "Block Hash: " + \
               str(self.hash()) + "\nBlockNo: " + \
               str(self.block_num) + "\nBlock Data: " + \
               str(self.data) + "\nHashes: " + str(self.nonce) + "\n--------------"
