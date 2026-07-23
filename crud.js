const express = require('express');
const app = express();
const port = 3000;

let tasks = [
  { id: 1, title: 'Learn Node.js basics', done: true },
  { id: 2, title: 'Understand Express routing', done: false },
  { id: 3, title: 'Build a CRUD API', done: false }
];

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.get('/api', (req, res) => {
  res.json({ name: 'Task API', version: '1.0', endpoints: ['/tasks'] });
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

app.get('/tasks', (req, res) => {
  res.json(tasks);
});

app.get('/tasks/:id', (req, res) => {
  const task = tasks.find(t => t.id === parseInt(req.params.id));
  if (!task) {
    return res.status(404).json({ error: 'Task not found' });
  }
  res.json(task);
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});