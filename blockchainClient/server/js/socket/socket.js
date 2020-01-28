const SocketActions = require('./constant');

const Pages = require('../model/pages');
const Blockchain = require('../model/chain_model');

const socketListeners = (socket, chain) => {
    socket.on(SocketActions.ADD_Pages, (sender, receiver, data) => {
        const pages = new Pages(sender, receiver, data);
        chain.newPages(pages);
        console.info(`Added transaction: ${JSON.stringify(pages.getDetails(), null, '\t')}`);
    });

    socket.on(SocketActions.END_MINING, (newChain) => {
        console.log('End Mining encountered');
        process.env.BREAK = true;
        const blockChain = new Blockchain();
        blockChain.parseChain(newChain);
        if (blockChain.checkValidity() && blockChain.getLength() >= chain.getLength()) {
            chain.blocks = blockChain.blocks;
        }
    });

    return socket;
};

module.exports = socketListeners;