const express = require("express");
const app = express();
const httpServer = require("http").Server(app);
const bodyParser = require("body-parser");
const path = require("path");
const fs = require("fs");
const argv = require("yargs").argv;

//axios
const axios = require("axios");

const Blockchain = require("./server/js/model/chain_model");
const socketListeners = require("./server/js/socket/socket");
const SocketActions = require("./server/js/socket/constant");

//socket.io
const client = require("socket.io-client");
const io = require("socket.io")(httpServer);

//routes
const index = require("./server/routes/route");
const user = require("./server/routes/user");

//db postgresql
var pg = require("pg");
var connectionString = "pg://postgres:persival99@localhost:5432/blockchain";
var clientpg = new pg.Client(connectionString);
clientpg.connect();

//PORT
const PORT = argv.port;

//setup block chain
const blockChain = new Blockchain(null, io);

/* require("./server/routes/block"). */

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "/public")));
app.use(
  bodyParser.urlencoded({
    extended: true
  })
);

//set the view engine
app.set("view engine", "ejs");

//use router
app.use("/", index);

//block
app.post("/nodes", (req, res) => {
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
  if (callback === "true") {
    console.info(`Added node ${node} back`);
    res
      .json({
        status: "Added node Back"
      })
      .end();
  } else {
    axios.post(`${node}/nodes?callback=true`, {
      host: req.hostname,
      port: PORT
    });
    console.info(`Added node ${node}`);
    res
      .json({
        status: "Added node"
      })
      .end();
  }
});

app.get("/chain", (req, res) => {
  res.json(blockChain.blocks).end();
});

//pages
app.post("/pages", (req, res) => {
  const {
    sender,
    receiver,
    data
  } = req.body;
  io.emit(SocketActions.ADD_PAGES, sender, receiver, data);
  res.json({
      message: "transaction success"
    })
    .end();
});

io.on("connection", socket => {
  console.info(`Socket connected, ID: ${socket.id}`);
  socket.on("disconnect", () => {
    console.log(`Socket disconnected, ID: ${socket.id}`);
  });
});
/* 
app.use('/', user);
app.use('/', block);

*/

blockChain.addNode(
  socketListeners(client(`http://localhost:${PORT}`), blockChain)
);
//APP.POST POUR RECUP LE CHANGEMENT DE CARTE
httpServer.listen(PORT, () =>
  console.info(`Express server running on ${PORT}...`)
);