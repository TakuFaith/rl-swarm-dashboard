const express = require('express');
const fs = require('fs');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());

const DATA_FILE = './data.json';

app.get('/api/data', (req, res) => {
  fs.readFile(DATA_FILE, 'utf8', (err, data) => {
    if (err) return res.status(500).json({ error: 'Could not read data' });
    res.json(JSON.parse(data));
  });
});

app.post('/api/data', (req, res) => {
  fs.writeFile(DATA_FILE, JSON.stringify(req.body, null, 2), (err) => {
    if (err) return res.status(500).json({ error: 'Could not write data' });
    res.status(200).json({ message: 'Data saved' });
  });
});

app.listen(PORT, () => console.log(`Server is running on http://localhost:${PORT}`));
