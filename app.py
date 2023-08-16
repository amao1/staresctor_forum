from flask import Flask, render_template, redirect, url_for, jsonify, request, session, Markup
import sqlite3
import hashlib
import datetime

app = Flask(__name__)

conn = sqlite3.connect('database/data.db', check_same_thread=False)
cur = conn.cursor()

app.secret_key = 'securekey'

@app.route('/')
def home():
    if 'userName' in session:
        data = cur.execute('SELECT * FROM users WHERE userName = ?', (session['username',]))
        data = data.fetchone()
        if data[1] is not None:
            data = "Welcome, " + data[1]
        else :
            data = "Welcome, " 
        return render_template('index.html', loginName = data)
    else: 
        data = "Login"
        return render_template('index.html', loginName = data)
    #return render_template('index.html')
    
@app.route('/post', methods=['POST', 'GET'])
def post():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('login'))
        #get info
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        dateCreated = datetime.datetime.now()
        fortune = 1

        #check for missing info
        if not title or not content or not category:
            error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Please fill out all fields </div>')
            return render_template('post.html', error=error_message)
        #insert post into data.db
        try:
            cur.execute('INSERT INTO posts (category, title, body, datePosted, userID, fortune) VALUES (?, ?, ?, ?, ?, ?)', (category, title, content, dateCreated, session['ID'], fortune))
            conn.commit()
            success_message = Markup('<div id="alert" class="alert alert-success" role="alert"> Post successfully created </div>')
            return render_template('post.html', error=success_message)
        except:
            error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> An error occured </div>')
            return render_template('post.html', error=error_message)
    return render_template('post.html') 

@app.route('/login', methods=['POST','GET'])
def login():
    #if user is already logged in
    if 'username' in session:
        return redirect(url_for('home'))
    if request.method == 'POST':
        #user login 
        if request.form['submitButton'] == 'login':
            #get email and password
            emailUsername = request.form['emailUsername']
            password = request.form['loginPassword']
            if not emailUsername or not password:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Invalid email/username or password </div>')
                return render_template("login.html", error=error_message)
            #hash password
            passwordHash = hashlib.md5(password.encode()).hexdigest()
            #check for user
            data = cur.execute('SELECT * FROM users WHERE (emailAddress = ?) AND hashedPassword = ?', (emailUsername, passwordHash))
            data = data.fetchone()
            if data is None:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Invalid email/username or password </div>')
                return render_template('login.html', error=error_message)
            else:
                session['username'] = data[3]
                session['email'] = data[4]
                session['firstName'] = data[1]
                session['lastName'] = data[2]
                session['phoneNumber'] = data[6]
                session['ID'] = data[0]
            return redirect(url_for('home'))
        #user registration
        elif request.form['submitButton'] == 'register' :
            username = request.form['username']
            email =  request.form['registerEmail']
            firstName = request.form['firstName']
            lastName = request.form["lastName"]
            phoneNumber = request.form['phone']
            password = request.form['registerPassword']
            passwordRepeat = request.form['registerRepeatPassword']

            print("username: ", username)
            print("email: ", email)
            print("first name: ", firstName)
            print("last name: ", lastName)
            print("phone: ", phoneNumber)
            print("password: ", password)
            print("password repeat: ", passwordRepeat)

            #check if all fields entered
            if not username or not email or not firstName or not lastName or not phoneNumber or not password or not passwordRepeat:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Please fill out all fields </div> ')
                return render_template('login.html', error=error_message)

            #check if email unique
            data = cur.execute('SELECT * FROM users WHERE emailAddress = ?', (email,))
            data = data.fetchone()
            if data is not None:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Email already exists </div> ')
                return render_template('login.html', error=error_message)

            #check if username unique
            data = cur.execute('SELECT * FROM users WHERE userName = ?', (username,))
            data = data.fetchone()
            if data is not None:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Username already exists </div> ')
                return render_template('login.html', error=error_message)

            #check for password match
            if password != passwordRepeat:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Passwords do not match </div> ')
                return render_template('login.html', error=error_message)

            #hash password
            passwordHash = hashlib.md5(password.encode()).hexdigest()

            #insert into database
            try:
                cur.execute('INSERT INTO users (firstName, lastName, userName, emailAddress, hashedPassword, phoneNumber) VALUES (?, ?, ?, ?, ?, ?)', 
                            (firstName, lastName, username, email, passwordHash, phoneNumber))
                conn.commit()
            except Exception as e:
                print(e, e.args)
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> There was an issue creating your account </div> ')
                return render_template('login.html', error=error_message)

            success_message = Markup('<div id="alert" class="alert alert-success" role="alert"> Account creation successful. Please sign in </div> ')
            return render_template('login.html', error=success_message)

    return render_template('login.html')

@app.route('/account', methods=['POST', 'GET'])
def account():
    if request.method == 'POST':
        #getting user changed data
        username = request.form['username']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        phone = request.form['phone']
        email = request.form['registerEmail']
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        repeatNewPassword = request.form['repeatNewPassword']

        #enter info in database
        if firstName:
            cur.execute('UPDATE users SET firstName = ? WHERE ID = ?', (firstName, session['ID']))
            conn.commit()
            session['firstName'] = firstName
        if lastName:
            cur.execute('UPDATE users SET lastName = ? WHERE ID = ?', (lastName, session['ID']))
            conn.commit()
            session['lastName'] = lastName
        if username:
            verify = cur.execute('SELECT * FROM users WHERE userName = ?', (username,))
            verify = verify.fetchone()
            if verify is not None:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert">Username already exists</div>')
                return render_template('account.html', errorTop=error_message)
            cur.execute('UPDATE users SET userName = ? WHERE ID = ?', (username, session['ID']))
            conn.commit()
            session['username'] = username
        if phone:
            verify = cur.execute('SELECT * FROM users WHERE phoneNumber = ?', (phone,))
            verify = verify.fetchone()
            if verify is not None:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert">Phone number already exists</div>')
                return render_template('account.html', errorTop=error_message)
            cur.execute('UPDATE users SET phoneNumber = ? WHERE ID = ?', (phone, session['ID']))
            conn.commit()
            session['phoneNumber'] = phone
        if email:
            verify = cur.execute('SELECT * FROM users WHERE emailAddress = ?', (email,))
            verify = verify.fetchone()
            if verify is not None:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert">Email already exists</div>')
                return render_template('account.html', errorTop=error_message)
            cur.execute('UPDATE users SET emailAddress = ? WHERE ID = ?', (email, session['ID']))
            conn.commit()
            session['email'] = email
        if oldPassword and newPassword and repeatNewPassword:
            oldPasswordHash = hashlib.md5(oldPassword.encode()).hexdigest()
            newPasswordHash = hashlib.md5(newPassword.encode()).hexdigest()
            #verify old password
            verify = cur.execute('SELECT * FROM users WHERE hashedPassword = ? AND ID= ?', (oldPasswordHash, session['ID']))
            verify = verify.fetchone()
            if verify is None:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Incorrect password </div>')
                return render_template('account.html', error=error_message)
            else:
                #verify password match
                if newPassword != repeatNewPassword:
                    error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Passwords do not match </div>')
                    return render_template('account.html', error=error_message)
                #update new password
                else:
                    cur.execute("UPDATE users SET hashedPassword = ? WHERE ID = ?", (newPasswordHash, session['ID']))
                    conn.commit()
                    success_message = Markup('<div id="alert" class="alert alert-success" role="alert"> Password successfully changed </div>')
                    return render_template('account.html',error=success_message)
                
    if 'username' in session:
        return render_template('account.html')
    else:
        return render_template('login.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('home'))
    
@app.route('/vote', methods=['POST', 'GET'])
def vote():
    if 'username' not in session:
        print('user is not logged in')
        error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Please login or create an account to vote </div>')
        return redirect(url_for('login', error=error_message))
    if request.method == 'POST':
        #get data from fetch api
        data = request.get_json()
        targetID = data.get('targetID')
        userID = data.get('userID')
        voteType = data.get('voteType')
        targetType = data.get('targetType')

        print("targetID: ", targetID)
        print("userID: ", userID )
        print("voteType: ", voteType )
        print("targetType: ", targetType)

        if not targetID or not userID or not voteType or not targetType:
            return jsonify(message="an error occured")

        #insert to post
        if targetType == 'post':
            try:
                cur.execute('INSERT INTO postVote (userID, postID, postScore) VALUES (?, ?, ?)', (userID, targetID, voteType, ))
                conn.commit()
                return jsonify(message="Vote processed successfully")
        
            except Exception as e:
                print("there was an error upvoting/downvoting:", e)

        #insert to comments
        else:
            try:
                cur.execute('INSERT INTO commentVote (userID, commentID, commentScore) VALUES (?, ?, ?)', (userID, targetID, voteType, ))
                conn.commit()
                return jsonify(message="Vote processed successfully")
        
            except Exception as e:
                print("there was an error upvoting/downvoting:", e)

        return jsonify(message="done")

@app.route('/news', methods=['POST', 'GET'])
def news():
    #get all fortune values
    cur.execute('UPDATE posts SET fortune = (SELECT SUM(postScore) FROM postVote WHERE postVote.postID = posts.id) WHERE (SELECT SUM(postScore) FROM postVote WHERE postVote.postID = posts.id) IS NOT NULL')
    conn.commit()
    cur.execute('UPDATE comments SET fortune = (SELECT SUM(commentScore) FROM commentVote WHERE commentVote.commentID = comments.id) WHERE (SELECT SUM(commentScore) FROM commentVote WHERE commentVote.commentID = comments.id) IS NOT NULL')
    conn.commit()

    #get all news posts
    data = cur.execute('SELECT * FROM posts WHERE category = "News"')
    data = data.fetchall()

    #show posts
    if request.method == 'GET':
        authorName=dict()
        allComments=dict()
        for post in data:
            author = cur.execute('SELECT userName FROM users WHERE id = ?', (post[5],))
            author = author.fetchone()
            authorName[post[5]] = author[0]
        for post in data: 
            comments = cur.execute('SELECT * FROM comments WHERE postID = ?', (post[0],))
            comments = comments.fetchall()
            for comment in comments:
                author = cur.execute('SELECT userName FROM users WHERE id = ?', (comment[3], ))
                author = author.fetchone()
                commentID = comment[0]
                commentContent = comment[1]
                commentScore = comment[5]
                if post[0] is not None:
                    content = [author[0], commentContent, commentID, commentScore]
                    if post[0] not in allComments:
                        allComments[post[0]] = list()
                    allComments[post[0]].append(content)

        if 'error' in request.args:
            error_message = Markup(request.args['error'])
            return render_template('news.html', posts=data, authorName=authorName, allComments=allComments, error=error_message)
        return render_template('news.html', posts=data, authorName=authorName, allComments=allComments)

@app.route('/general', methods=['POST', 'GET'])
def general():
    #get all fortune values
    cur.execute('UPDATE posts SET fortune = (SELECT SUM(postScore) FROM postVote WHERE postVote.postID = posts.id) WHERE (SELECT SUM(postScore) FROM postVote WHERE postVote.postID = posts.id) IS NOT NULL')
    conn.commit()
    cur.execute('UPDATE comments SET fortune = (SELECT SUM(commentScore) FROM commentVote WHERE commentVote.commentID = comments.id) WHERE (SELECT SUM(commentScore) FROM commentVote WHERE commentVote.commentID = comments.id) IS NOT NULL')
    conn.commit()

    #get all general posts
    data = cur.execute('SELECT * FROM posts WHERE category = "General"')
    data = data.fetchall()

    #show posts
    if request.method == 'GET':
        authorName=dict()
        allComments=dict()
        for post in data:
            author = cur.execute('SELECT userName FROM users WHERE id = ?', (post[5],))
            author = author.fetchone()
            authorName[post[5]] = author[0]
        for post in data: 
            comments = cur.execute('SELECT * FROM comments WHERE postID = ?', (post[0],))
            comments = comments.fetchall()
            for comment in comments:
                author = cur.execute('SELECT userName FROM users WHERE id = ?', (comment[3], ))
                author = author.fetchone()
                commentID = comment[0]
                commentContent = comment[1]
                commentScore = comment[5]
                if post[0] is not None:
                    content = [author[0], commentContent, commentID, commentScore]
                    if post[0] not in allComments:
                        allComments[post[0]] = list()
                    allComments[post[0]].append(content)

        if 'error' in request.args:
            error_message = Markup(request.args['error'])
            return render_template('general.html', posts=data, authorName=authorName, allComments=allComments, error=error_message)
        return render_template('general.html', posts=data, authorName=authorName, allComments=allComments)

@app.route('/modded', methods=['POST', 'GET'])
def modded():
    #get all fortune values
    cur.execute('UPDATE posts SET fortune = (SELECT SUM(postScore) FROM postVote WHERE postVote.postID = posts.id) WHERE (SELECT SUM(postScore) FROM postVote WHERE postVote.postID = posts.id) IS NOT NULL')
    conn.commit()
    cur.execute('UPDATE comments SET fortune = (SELECT SUM(commentScore) FROM commentVote WHERE commentVote.commentID = comments.id) WHERE (SELECT SUM(commentScore) FROM commentVote WHERE commentVote.commentID = comments.id) IS NOT NULL')
    conn.commit()

    #get all modded posts
    data = cur.execute('SELECT * FROM posts WHERE category = "Modded"')
    data = data.fetchall()

    #show posts
    if request.method == 'GET':
        authorName=dict()
        allComments=dict()
        for post in data:
            author = cur.execute('SELECT userName FROM users WHERE id = ?', (post[5],))
            author = author.fetchone()
            authorName[post[5]] = author[0]
        for post in data: 
            comments = cur.execute('SELECT * FROM comments WHERE postID = ?', (post[0],))
            comments = comments.fetchall()
            for comment in comments:
                author = cur.execute('SELECT userName FROM users WHERE id = ?', (comment[3], ))
                author = author.fetchone()
                commentID = comment[0]
                commentContent = comment[1]
                commentScore = comment[5]
                if post[0] is not None:
                    content = [author[0], commentContent, commentID, commentScore]
                    if post[0] not in allComments:
                        allComments[post[0]] = list()
                    allComments[post[0]].append(content)

        if 'error' in request.args:
            error_message = Markup(request.args['error'])
            return render_template('modded.html', posts=data, authorName=authorName, allComments=allComments, error=error_message)
        return render_template('modded.html', posts=data, authorName=authorName, allComments=allComments)

@app.route('/comment', methods=['POST','GET'])
def comment():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        comment = request.form['comment']
        postID = request.form['submit']
        fortune = 1
        dateCreated = datetime.datetime.now()
        category = cur.execute('SELECT category FROM posts WHERE id = ?', (postID,))
        category = category.fetchone()
        #check if comment is empty
        if not comment:
            error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> Please fill out all fields </div>')
            if category[0] == 'News':
                return redirect(url_for('news', error=error_message))
            elif category[0] == 'General':
                return redirect(url_for('general', error=error_message))
            elif category[0] == 'Modded':
                return redirect(url_for('modded', error=error_message))
        else:
            #insert comment into db
            try:
                cur.execute('INSERT into COMMENTS (body, datePosted, userID, postID, fortune) VALUES (?, ?, ?, ?, ?)', (comment, dateCreated, session['ID'], postID, fortune))
                conn.commit()
                success_message = Markup('<div id="alert" class="alert alert-success" role="alert"> Comment successfully created </div>')
                if category[0] == 'News':
                    return redirect(url_for('news', error=success_message))
                elif category[0] == 'General':
                    return redirect(url_for('general', error=success_message))
                elif category[0] == 'Modded':
                    return redirect(url_for('modded', error=success_message)) 
                else :
                    return redirect(url_for('general', error=success_message))
            except Exception as e:
                error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> An error occured while creating your comment</div>')
                if category == 'News':
                    return redirect(url_for('news', error=error_message))
                elif category == 'General':
                    return redirect(url_for('general', error=error_message))
                elif category == 'Modded':
                    return redirect(url_for('modded', error=error_message))
                else :
                    return redirect(url_for('general', error=e))

@app.route('/postHistory', methods=['POST', 'GET'])
def postHistory():
    if 'username' not in session:
        return redirect(url_for('login'))
    #get all posts by user
    data = cur.execute('SELECT * FROM posts WHERE userID = ?', (session['ID'],))
    data = data.fetchall()
    #show posts
    if request.method == 'GET':
        if 'error' in request.args:
            error_message = Markup(request.args['error']) 
        else :
            error_message = None
        return render_template('postHistory.html', posts=data, authorName=session['username'], error = error_message)

@app.route('/commentHistory', methods=['POST', 'GET'])
def commentHistory():
    if 'username' not in session:
        return redirect(url_for('login'))
    #get all comments by user
    comments = cur.execute('SELECT * FROM comments WHERE userID = ?', (session['ID'],))
    comments = comments.fetchall()
    #get names of posts commented on
    posts = dict()
    for comment in comments:
        post = cur.execute('SELECT category, title from posts where ID = ?', (comment[4],))
        post = post.fetchone()
        posts[comment[4]] = [post[0], post[1]]
    if 'error' in request.args:
        error = Markup(request.args['error'])
        return render_template('commentHistory.html', comments=comments, posts=posts, authorName=session['username'], error=error)
    return render_template('commentHistory.html', comments=comments, posts=posts, authorName=session['username'])

@app.route('/deletePost', methods=['POST', 'GET'])
def deletePost():
    if request.method == 'POST' : 
        #get postID
        postID = request.form.get('postID')
        #delete post
        try:
            cur.execute('DELETE FROM posts WHERE ID = ?', (postID,))
            conn.commit()
            #delete comments
            cur.execute('DELETE FROM comments WHERE postId = ?', (postID,))
            conn.commit()
            success_message = Markup('<div id="alert" class="alert alert-success" role="alert"> Post successfully deleted </div>')
            return redirect(url_for('postHistory', error=success_message))
        except:
            error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> An error occured </div>')
            return redirect(url_for('postHistory', error=error_message))
        
@app.route('/deleteComment', methods=['POST', 'GET'])
def deleteComment():
    if request.method == 'POST':
        commentID = request.form.get('comment-id')
        print("comment-id: ", commentID)
        try:
            cur.execute('DELETE FROM comments WHERE id = ?', (commentID,))
            conn.commit()
            success_message = Markup('<div id="alert" class="alert alert-success" role="alert"> Comment successfully deleted </div>')
            print("success")
            return redirect(url_for('commentHistory', error=success_message))
        except Exception as e:
            print("fail")
            error_message = Markup('<div id="alert" class="alert alert-danger" role="alert"> An error occured </div>')
            return redirect(url_for('commentHistory', error=error_message))
if __name__ == '__main__':
    app.run(debug=True, port=8000)
