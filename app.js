var express = require('express'),	
http = require('http'),
app = express(),
server = http.createServer(app),
io = require('socket.io').listen(server);

// routing
app.get("/", function(req, res) {
	res.sendfile(__dirname + '/index.html');
});

server.listen(8080);

var usernames = {};
var messages = [];

io.sockets.on('connection', function(socket) {
	// when the client emits sendchat, this listens and executes
	socket.on('sendchat', function(data) {
		// tell the client to execute updatechat with 2 paramaters
		io.sockets.emit('updatechat', socket.username, data);

		// store the last ten messages
		if (messages.length == 10)
		{
			messages.shift();
		}
		messages.push([socket.username, data]);
	});

	// when the client emits adduser this listen and executes
	socket.on('adduser', function(username) {
		if (usernames[username] != undefined)
		{
			socket.emit('askagain');
		}
		else
		{
		// we store the username in the socket session for this client
		socket.username = username;
		// add username to global list
		usernames[username] = username;
		// echo to client that they've connected
		socket.emit('updatechat', 'SERVER', 'you have connected');

		// send new user the last 10 messages
		messages.forEach(function(msg)
		{
			socket.emit('updatechat', msg[0], msg[1], msg[2]);
		});

		// echo globally that a person has connected
		socket.broadcast.emit('updatechat', 'SERVER', username + ' connected');
		// update the list of users in chat,client side
		io.sockets.emit('updateusers', usernames);
		}
	});

	// when the user disconnects
	socket.on('disconnect', function() {
		// remove username from global list
		delete usernames[socket.username];
		// update list of users in chat client side
		io.sockets.emit('updateusers', usernames);
		// echo globally that the user has left
		socket.broadcast.emit('updatechat', 'SERVER', socket.username + ' left');
	});

	// when user sends a MIDI event
	socket.on('sendNote', function(data) {
		// broadcast MIDI event to all users
		io.sockets.emit('playnote', socket.username, data);
	});
});
