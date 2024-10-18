# Problem 2

Recall that the socket is a stream socket.
Thus, there is no natural "message" boundary at the transport layer.
The OS or any intermediary is free to split or merge messages based on many different factors.

That is, if we send 3 messages: `message1\n`, `message2\n`, `message3\n`, it is possible that the application can
receive: `mess`, `age1\nme`, `ssage2\nmessage3\n` as 3 separate packets.
This is why the protocol used `\n` as a message terminator.

This problem requires you to also handle cases where messages can be arbitrarily split or merged.
The server must still reply to a message as soon as a terminator is received.
For example, as soon as it receives: `message1\nme`, it must immediately process `message1`.

The test suite will still only contain the `echo` request type.

If the answer is correct, you will receive a link to the next question.