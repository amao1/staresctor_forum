--ALTER TABLE postVote
--DROP CONSTRAINT unique_user_post_vote;
--ADD CONSTRAINT unique_user_post_vote UNIQUE (userID, postID);

--ALTER TABLE commentVote 
--DROP CONSTRAINT unique_user_comment_vote;
--ADD CONSTRAINT unique_user_comment_vote UNIQUE (userID, commentID);

CREATE TABLE IF NOT EXISTS categorys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoryName TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    datePosted NULL,
    userID INTEGER NOT NULL,
    fortune INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL,
    userName TEXT NOT NULL UNIQUE,
    emailAddress TEXT NOT NULL UNIQUE,
    hashedPassword TEXT NOT NULL,
    phoneNumber TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    body TEXT NOT NULL,
    datePosted TEXT NOT NULL,
    userID INTEGER NOT NULL,
    postID INTEGER NOT NULL,
    fortune INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS postVote (
    pVoteID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    postID INTEGER NOT NULL,
    postScore INTEGER NOT NULL,
    UNIQUE(userID, postID)
);

CREATE TABLE IF NOT EXISTS commentVote (
    cVoteID INTEGER PRIMARY KEY AUTOINCREMENT,
    userID INTEGER NOT NULL,
    commentID INTEGER NOT NULL,
    commentScore INTEGER NOT NULL,
    UNIQUE(userID, commentID)
);
