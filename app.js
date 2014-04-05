var http		= require('http');
var express		= require('express');

var app		= express();

app.get('/', function(req, res){
			res.send("Hello world...");
		});
