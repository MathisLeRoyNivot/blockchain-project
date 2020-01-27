const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const path = require("path");
const fs = require("fs");

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "/public")));
app.use(
  bodyParser.urlencoded({
    extended: true
  })
);

//set the view engine
app.set("view engine", "ejs");

app.get("/", function(req, res) {
  res.render("index", { title: "Hey", message: "Hello there!" });
});

//APP.POST POUR RECUP LE CHANGEMENT DE CARTE
app.listen(8080, function() {
  console.log("Example app listening on port 8080!");
});
