const { Comment } = require('../models');

exports.getComments = async (req, res) => {
  try {
    const comments = await Comment.find().populate('user', 'username');
    res.status(200).json(comments);
  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
};

exports.createComment = async (req, res) => {
  try {
    const { text, userId } = req.body;
    const newComment = new Comment({ text, user: userId });
    await newComment.save();

    res.status(201).json({ message: 'Comment created successfully' });
  } catch (error) {
    res.status(500).json({ error: 'An error occurred' });
  }
};
