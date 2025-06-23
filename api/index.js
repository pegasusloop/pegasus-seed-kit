const express = require('express');
const cors = require('cors');
const postsRoute = require('./posts');
const tagsRoute = require('./tags');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors()); // Allow cross-origin requests
app.use(express.json()); // Handle JSON request bodies

// API routes
app.use('/api/posts', postsRoute);
app.use('/api/tags', tagsRoute);

// Health check route
app.get('/', (req, res) => {
  res.send('Pegasus Seed Kit API is live 🚀');
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
