var express = require("express");
var multer = require("multer");
var router = express();
router.post(
	"/upload",
	multer({
		dest: "./uploads",
		onFileUploadStart: function(file, req, res) {
			console.log(file.originalname + " is starting ...");
			return true;
		},
		onFileUploadComplete: function(file) {
			console.log(file.fieldname + " uploaded to  " + file.path);
		},
		onParseStart: function() {
			console.log("Form parsing started at: ", new Date());
		},
		onParseEnd: function(req, next) {
			console.log("Form parsing completed at: ", new Date());
			// call the next middleware
			next();
		}
	}),
	function(req, res, next) {
		console.log("upload image api");
	}
);

router.listen(3001, function() {
	console.log("Nodejs is listening on the port");
});
