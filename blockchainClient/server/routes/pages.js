var express = require("express");
var router = express.Router();

const Blockchain = require('../js/model/chain_model')
const Pages = require('../js/model/pages')

router.post('/pages', (req, res) => {
    const {
        sender,
        receiver,
        data
    } = req.body;
    io.emit(SocketActions.ADD_TRANSACTION, sender, receiver, data);
    res.json({
        message: 'transaction success'
    }).end();
});

module.exports = router;