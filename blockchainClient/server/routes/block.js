var express = require("express");
var router = express.Router();
const axios = require('axios');
const Blockchain = require('../js/model/chain_model')
const socketListeners = require("../js/socket/socket");
//setup block chain
const blockChain = new Blockchain(null, io);

router.post('/nodes', (req, res) => {
    const {
        host,
        port
    } = req.body;
    const {
        callback
    } = req.query;
    const node = `http://${host}:${port}`;
    const socketNode = socketListeners(client(node), blockChain);
    blockChain.addNode(socketNode, blockChain);
    if (callback === 'true') {
        console.info(`Added node ${node} back`);
        res.json({
            status: 'Added node Back'
        }).end();
    } else {
        axios.post(`${node}/nodes?callback=true`, {
            host: req.hostname,
            port: PORT,
        });
        console.info(`Added node ${node}`);
        res.json({
            status: 'Added node'
        }).end();
    }
});

router.get('/chain', (req, res) => {
    res.json(blockChain.toArray()).end();
});

module.exports = {
    router,
    blockChain
};