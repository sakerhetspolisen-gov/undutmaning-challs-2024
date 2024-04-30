const express = require('express');
const { Server } = require('ws');
const pty = require('node-pty');
const path = require('path');

const app = express();
const port = 3000;

// Serve static files from the public directory
app.use(express.static('/var/www/public'));

const server = app.listen(port, () => {
  console.log(`Web terminal server running on port ${port}`);
});

const wss = new Server({ server });

wss.on('connection', (ws) => {
  const ptyProcess = pty.spawn('tmux', ['attach'], {
    name: 'xterm-color',
    cols: 80,
    rows: 30,
    cwd: process.env.PWD,
    env: process.env
  });

  ws.onmessage = (event) => {
    try {
      const msg = JSON.parse(event.data);
      if (msg.action === 'resize') {
        ptyProcess.resize(msg.cols, msg.rows);
      } else if (msg.action === 'input') {
        ptyProcess.write(msg.data);
      }
      // No need to send back any response to the resize or input commands
    } catch (e) {
      // If it's not JSON, it's regular terminal data, write it to the pty
      ptyProcess.write(event.data);
    }
  };

  ptyProcess.onData(data => {
    // Only send back the terminal output, not the resize commands
    ws.send(JSON.stringify({ action: 'output', data: data }));
  });

  ws.on('close', () => {
    ptyProcess.kill();
  });
});

