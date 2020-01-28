const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const path = require("path");
const fs = require("fs");
const index = require("./server/routes/route");
const user = require("./server/routes/user");
const block = require("./server/routes/block");
var pg = require("pg");
const io = require("socket.io");
var connectionString = "pg://postgres:persival99@localhost:5432/blockchain";
var client = new pg.Client(connectionString);
client.connect();
var cors = require("cors");

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "/public")));
app.use(
  bodyParser.urlencoded({
    extended: true
  })
);

//set the view engine
app.set("view engine", "ejs");

app.use("/", index);
app.use(cors());
app.use(express.json());

/* 
app.use('/', user);
app.use('/', block);
*/

//APP.POST POUR RECUP LE CHANGEMENT DE CARTE
app.listen(8080, function() {
  console.log("Example app listening on port 8080!");
});
