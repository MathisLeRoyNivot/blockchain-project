var express = require("express");
var router = express.Router();
const fs = require("fs");



router.get("/", function (req, res) {
    res.render("index");
});
router.post("/accueil", function (req, res) {
    res.render("accueil", {
        title: "post",
    }); 
});
router.get("/accueil", function (req, res) {
    const fichier_livres = JSON.parse(fs.readFileSync("./server/routes/livres.json", "utf8"));
    res.render("accueil", {
        livre: fichier_livres.livres[0]
    });
});
router.post("/lecture", function (req, res) {
    res.render("lecture", {
        title: "post",
    });
});
router.post("/index", function (req, res) {
    res.render("index", {
        title: "post",
    });
});
module.exports = router;