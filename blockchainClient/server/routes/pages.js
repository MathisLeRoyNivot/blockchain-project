var express = require("express");
var router = express.Router();
const io = require("socket.io")
const Blockchain = require('../js/model/chain_model')
const Pages = require('../js/model/pages')
const socketListeners = require("../js/socket/socket");


router.post('/pages', (req, res) => {
    const {
        sender,
        receiver,
        data
    } = req.body;
    io.emit(SocketActions.ADD_PAGES, sender, receiver, data);
    res.json({
        message: 'transaction success'
    }).end();
});

module.exports = router;