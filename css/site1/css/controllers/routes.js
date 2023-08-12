const express = require('express');
const router = express.Router();
const authController = require('../controllers/authController');
const commentController = require('../controllers/commentController');

router.post('/register', authController.register);
router.get('/comments', commentController.getComments);
router.post('/comments', commentController.createComment);

module.exports = router;
