# Real-Time Javascript

## HTTP/2 Push

### Server

```js
import http2 from "http2";
import fs from "fs";
import path from "path";

/*
HTTP/2 only works over HTTPS

openssl req -new -newkey rsa:4096 -new -nodes -keyout key.pem -out csr.pem

openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out server.crt
*/
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const server = http2.createSecureServer({
  cert: fs.readFileSync(path.join(__dirname, "/../server.crt")),
  key: fs.readFileSync(path.join(__dirname, "/../key.pem")),
});

const messages = [];
const getMessages = () => messages.reverse().slice(0, 50);

let connections = [];

server.on("stream", (stream, headers) => {
  const method = headers[":method"];
  const path = headers[":path"];

  if (path === "/messages" && method === "GET") {
    // Immediately respond with 200 OK and encoding
    stream.respond({
      ":status": 200,
      "content-type": "text/plain; charset=utf-8",
    });

    // Write the first response
    stream.write(JSON.stringify({ messages: getMessages() }));

    // Keep track of the connection
    connections.push(stream);

    // When the connection closes, stop keeping track of it
    stream.on("close", () => {
      connections = connections.filter((s) => s !== stream);
    });
  }
});

server.on("request", async (req, res) => {
  const path = req.headers[":path"];
  const method = req.headers[":method"];

  if (path === "/messages" && method === "POST") {
    // Get data out of POST
    const buffers = [];
    for await (const chunk of req) {
      buffers.push(chunk);
    }
    const data = Buffer.concat(buffers).toString();
    const { user, text } = JSON.parse(data);
    messages.push({
      user,
      text,
      time: Date.now(),
    });

    // Finished with the request
    res.end();

    // Notify all connected users
    connections.forEach((stream) => {
      stream.write(JSON.stringify({ messages: getMessages() }));
    });
  }
});
```

### Client

```js
async function getNewMessages() {
  let reader;
  const utf8Decoder = new TextDecoder("utf-8");

  try {
    const res = await fetch("/messages");
    reader = res.body.getReader();
  } catch (e) {
    console.log("Connection error", e);
  }

  // We are connected
  let done;
  do {
    let readerResponse;
    try {
      readerResponse = await reader.read();
    } catch (e) {
      // Connection closed
      console.error("Reader failed", e);
      return;
    }

    done = readerResponse.done;
    const chunk = utf8Decoder.decode(readerResponse.value, { stream: true });
    if (chunk) {
      try {
        const json = JSON.parse(chunk);
        allChat = json.messages;

        // Do something with the data
        render();
      } catch (e) {
        console.error("Parse error", e);
      }
    }

    console.log("Done", done);
  } while (!done);

  // If the HTTP/2 connection closed, `done` comes back as true and we're no longer be connected.
  // Connection closed
}
```
