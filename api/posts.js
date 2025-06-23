const express = require('express');
const router = express.Router();
const posts = require('../data/index.json');

router.get('/', (req, res) => {
  res.json(posts);
});

router.get('/:id', (req, res) => {
  const post = posts.find(p => p.id === req.params.id);
  if (!post) return res.status(404).json({ error: 'Post not found' });
  res.json(post);
});

module.exports = router;
