const crypto = require('crypto');

const pages = require('./pages');

class Block {
    constructor(index, previousBlockHash, previousProof, pages) {
        this.index = index;
        this.proof = previousProof;
        this.previousBlockHash = previousBlockHash;
        this.pages = pages;
        this.timestamp = Date.now();
    }

    hashValue() {
        const {
            index,
            proof,
            pages,
            timestamp
        } = this;
        const blockString = `${index}-${proof}-${JSON.stringify(pages)}-${timestamp}`;
        const hashFunction = crypto.createHash('sha256');
        hashFunction.update(blockString);
        return hashFunction.digest('hex');
    }

    setProof(proof) {
        this.proof = proof;
    }

    getProof() {
        return this.proof;
    }

    getIndex() {
        return this.index;
    }

    getPreviousBlockHash() {
        return this.previousBlockHash;
    }

    /* Stringify and Parsing functions */
}

module.exports = Block;