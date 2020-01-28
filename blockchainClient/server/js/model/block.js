const crypto = require('crypto');

const Pages = require('./pages');

class Block {
    constructor(index, previousBlockHash, previousProof, pages) {
        this.index = index;
        this.proof = previousProof;
        this.previousBlockHash = previousBlockHash;
        this.pages = pages;
        this.timestamp = Date.now();
    }
    getDetails() {
        const {
            index,
            proof,
            previousBlockHash,
            pages,
            timestamp
        } = this;
        return {
            index,
            proof,
            timestamp,
            previousBlockHash,
            pages: pages.map(page => page.getDetails()),
        };
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
    parseBlock(block) {
        this.index = block.index;
        this.proof = block.proof;
        this.previousBlockHash = block.previousBlockHash;
        this.timestamp = block.timestamp;
        this.pages = block.pages.map(pages => {
            const parsedPages = new Pages();
            parsedPages.parsePages(pages);
            return parsedPages;
        });
    }


    printpages() {
        this.pages.forEach(pages => console.log(pages));
    }
    /* Stringify and Parsing functions */
}

module.exports = Block;