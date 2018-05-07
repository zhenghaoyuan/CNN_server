var express = require("express");
var multer = require("multer");
var PythonShell = require("python-shell");

var app = express();

var storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, "./my-uploads");
	},
	filename: function(req, file, cb) {
		cb(null, file.fieldname + "-" + Date.now() + ".jpg");
	}
});
var upload = multer({ storage: storage }).single("image");
app.post("/upload", function(req, res) {
	upload(req, res, function(err) {
		if (err) {
			// An error occurred when uploading
			return;
		}
		const { spawn } = require("child_process");
		var args1 = "./my-uploads/" + req.file.filename;
		const pyprog = spawn("python", ["./label_image.py", args1]);
		pyprog.stdout.on("data", function(data) {
			var str = data.toString("utf8");
			console.log(str);
			var arr = str.split("(");
			res.end(arr[0]);
		});
		//console.log(req.file.filename);
		//console.log("Haha I am here");

		// Everything went fine
	});
});

app.get("/update", function(req, res) {
	res.end("I got it");
	var args1 = req.query.label;
	var PythonShell = require("python-shell");
	var options = {
		args: [args1]
	};
	PythonShell.run("spider.py", options, function(err, results) {
		if (err) throw err;
		console.log("finish collecting data");
		console.log("start retraining");
		const { spawn } = require("child_process");
		const pyprog = spawn("python", [
			"retrain.py",
			"--bottleneck_dir=bottlenecks",
			"--how_many_training_steps=100",
			"--model_dir=inception",
			"--summaries_dir=training_summaries/basic",
			"--output_graph=retrained_graph_copy.pb",
			"--output_labels=retrained_labels.txt",
			"--image_dir=image"
		]);
		pyprog.stderr.on("data", data => {
			console.log(`stderr: ${data}`);
		});
		pyprog.on("close", code => {
			console.log(`child process exited with code ${code}`);
			console.log("start ");
		});
		// var PythonShell2 = require("python-shell");
		// var options2 = {
		// 	args: [
		// 		"--bottleneck_dir=bottlenecks",
		// 		"--how_many_training_steps=100",
		// 		"--model_dir=inception",
		// 		"--summaries_dir=training_summaries/basic",
		// 		"--output_graph=retrained_graph.pb",
		// 		"--output_labels=retrained_labels.txt",
		// 		"--image_dir=image"
		// 	]
		// };
		//
		// PythonShell2.run("retrain.py", options2, function(err, results) {
		// 	if (err) throw err;
		// 	console.log("finish retraining");
		// });
	});
});
// let runPy = new Promise(function(sucess, nosuccess) {
// 	const { spawn } = require("child_process");
// 	const pyprog = spawn("python", ["./ML_model/classify_image.py"]);
//
// 	pyprog.stdout.on("data", function(data) {
// 		console.log("I success");
// 		sucess(data);
// 	});
// 	pyprog.stderr.on("data", data => {
// 		console.log("I fail");
// 		nosuccess(data);
// 	});
// });

var server = app.listen(3001, function() {
	console.log("Nodejs is listening on the port");
});
