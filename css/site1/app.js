const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

const mongoose = require('mongoose');
const DB_URI = 'mongodb://localhost:27017/commentApp';

mongoose.connect(DB_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
});

const db = mongoose.connection;
db.on('error', console.error.bind(console, 'MongoDB connection error:'));
db.once('open', () => {
    console.log('Connected to MongoDB');
});

const routes = require('./routes');
app.use('/api', routes);

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
