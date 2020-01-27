const express = require("express");
const app = express();
const bodyParser = require("body-parser");
const path = require("path");
const fs = require('fs');



app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "/public")));
app.use(
    bodyParser.urlencoded({
        extended: true
    })
);

app.get("/", function (req, res) {
    res.sendFile(path.join(__dirname + "/index.html"));
});

//APP.POST POUR RECUP LE CHANGEMENT DE CARTE
app.listen(8080, function () {
    console.log("Example app listening on port 8080!"
        s);

});