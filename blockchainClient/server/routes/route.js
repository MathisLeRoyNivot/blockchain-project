var express = require("express");
var router = express.Router();
router.get("/", function (req, res) {
    res.render("index", {
        title: "Hey",
        message: "Hello there!"
    });
});
router.post("/accueil", function (req, res) {
    res.render("accueil", {
        title: "post",
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