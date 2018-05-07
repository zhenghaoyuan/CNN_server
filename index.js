var http = require("http");
var formidable = require("formidable");
var fs = require("fs");

const host = "localhost";
const port = 3000;
const server = http.createServer(function(req, res) {
	res.statusCode = 200;
	res.setHeader("content-Type", "text/plain");
	res.end("OK\n");
	var filename = req.headers["x-filename"];

	var file = fs.createWriteStream(`${filename}`);
});

server.listen(port, host, () => {
	console.log("we are listening to the port");
});
