var express = require("express");
var router = express.Router();
router.get("/", function (req, res) {
    res.render("index", {
        title: "Hey",
        message: "Hello there!"
    });
});
router.get("/te", function (req, res) {
    res.render("index", {
        title: "test",
        message: "Hello there!"
    });
});
module.exports = router;