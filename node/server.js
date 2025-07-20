const express = require("express");
const { spawn } = require("child_process");
const fs = require("fs");
const path = require("path");
const { v4: uuidv4 } = require("uuid");
const cors = require("cors");
const http = require("http");
const { Server } = require("socket.io");

const app = express();
app.use(cors());
app.use(express.json());

const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
  },
});

const DOWNLOAD_DIR = path.join(__dirname, "downloads");
if (!fs.existsSync(DOWNLOAD_DIR)) fs.mkdirSync(DOWNLOAD_DIR);

io.on("connection", (socket) => {
  console.log("🟢 New client connected");

  socket.on("disconnect", () => {
    console.log("🔌 Client disconnected");
  });
});

app.post("/api/download", (req, res) => {
  const { url, platform, downloadId } = req.body;
  if (!url || !downloadId) return res.status(400).json({ error: "Missing URL or downloadId" });

  const filename = `${uuidv4()}.mp4`;
  const filepath = path.join(DOWNLOAD_DIR, filename);
  const pythonScriptPath = path.join(__dirname, "../download.py");

  const py = spawn("python", [pythonScriptPath, url, filepath, downloadId]);

  py.stdout.on("data", (data) => {
    const message = data.toString().trim();
    console.log(`[PYTHON LOG] ${message}`);

    const match = message.match(/^\[(.+?)\]\s+(.*)$/);
    if (match) {
      const id = match[1];
      const log = match[2];
      io.emit(`progress-${id}`, log); // broadcast to Flutter
    }
  });

  py.stderr.on("data", (data) => {
    console.error(`[PYTHON ERROR] ${data.toString()}`);
  });

  py.on("close", (code) => {
    if (fs.existsSync(filepath)) {
      const stream = fs.createReadStream(filepath);
      stream.on("open", () => {
        res.setHeader("Content-Disposition", `attachment; filename="${filename}"`);
        res.setHeader("Content-Type", "video/mp4");
        stream.pipe(res);

        stream.on("end", () => fs.unlinkSync(filepath));
      });

      stream.on("error", (err) => {
        console.error("Stream error:", err);
        res.status(500).json({ error: "Stream failed" });
      });
    } else {
      res.status(500).json({ error: "File not found" });
    }
  });
});

server.listen(3000, () => {
  console.log("🚀 Server running on http://localhost:3000");
});
