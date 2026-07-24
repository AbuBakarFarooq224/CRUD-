const express = require('express');
const app = express();
const port = 3000;
app.use(express.json());

const swaggerUi = require('swagger-ui-express');
const swaggerDocument = require('./swagger.json');

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));


let tasks = [
  { id: 1, title: 'Learn Node.js basics', done: true },
  { id: 2, title: 'Understand Express routing', done: false },
  { id: 3, title: 'Build a CRUD API', done: false }
];


//READ
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
    return res.status(404).json({ "error": `Task ${req.params.id} not found` });
  }
  res.json(task);
});


//CREATE
app.post('/tasks', (req, res) => {
    if (!req.body || !req.body.title) {
    return res.status(400).json({ "error": "Title is required" });
  }
  const newTask = {
    id: tasks.length + 1,
    title: req.body.title,
    done: false
  };
  tasks.push(newTask);
  res.status(201).json({ "message": `Done, here's your receipt Created: ${newTask.title}` });
});


//UPDATE
app.put('/tasks/:id', (req, res) => {
    const task = tasks.find(t => t.id === parseInt(req.params.id));
    if (!task) {
      return res.status(404).json({ "error": `Unknown ID: ${req.params.id}` });
    }
    if (req.body.title === undefined && req.body.done === undefined) {
    return res.status(400).json({ "error": "Empty/Invalid body" });
  }
    if (req.body.title !== undefined) {
      task.title = req.body.title;
    }
     if (req.body.done !== undefined) {
      task.done = req.body.done;
    }
    return res.json(task);
  });


//DELETE
app.delete('/tasks/:id', (req, res) => {
    const taskIndex = tasks.findIndex(t => t.id === parseInt(req.params.id));
    if (taskIndex === -1) {
      return res.status(404).json({ "error": `Unknown ID: ${req.params.id}` });
    }                                                                                                   
    tasks.splice(taskIndex, 1);
    return res.status(204).send();
  });


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});