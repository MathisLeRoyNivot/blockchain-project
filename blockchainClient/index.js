const express = require("express");
const app = express();
const httpServer = require("http").Server(app);
const bodyParser = require("body-parser");
const path = require("path");
const fs = require("fs");
const argv = require("yargs").argv;

const Blockchain = require("./server/js/model/chain_model");
const socketListeners = require("./server/js/socket/socket");
//routes
const pages = require("./server/routes/pages");
const index = require("./server/routes/route");
const user = require("./server/routes/user");
const block = require("./server/routes/block");

//db postgresql
var pg = require("pg");
var connectionString = "pg://postgres:persival99@localhost:5432/blockchain";
var clientpg = new pg.Client(connectionString);
clientpg.connect();

//PORT
const PORT = argv.port;

//socket.io
const client = require("socket.io-client");
const io = require("socket.io")(httpServer);

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

//use router
app.use("/", index);
app.use("/", block);
app.use("/", pages);

//set the view engine
app.set("view engine", "ejs");

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