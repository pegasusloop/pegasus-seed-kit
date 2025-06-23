const express = require('express');
const router = express.Router();
const tags = require('../data/tags.json');

router.get('/', (req, res) => {
  res.json(tags);
});

module.exports = router;
