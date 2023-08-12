const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username: String,
    password: String
});

const commentSchema = new mongoose.Schema({
    text: String,
    user: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User'
    }
});

const User = mongoose.model('User', userSchema);
const Comment = mongoose.model('Comment', commentSchema);

module.exports = { User, Comment };
