from flask import Flask, request, redirect, render_template, session, flash
import datetime
from mysqlconnection import MySQLConnector
app = Flask(__name__)
app.secret_key = 'rangersleadtheway'
mysql = MySQLConnector(app,'friendsdb')

@app.route('/')
def index():
    query = "SELECT * FROM friends"                           # define your query
    friends = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_friends=friends) # pass data to our template

@app.route('/users/<id>', methods=['GET'])
def show(id):
    # check if you are coming from and HTML page or from another route
    if id != "<id>":
        session['id'] = id
    # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': session['id']}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('users/show.html', friend=friends)

@app.route('/users/new')
def new():
    return render_template('users/new.html')

@app.route('/users/<id>/edit', methods=['GET'])
def edit(id):
     # Write query to select specific user by id. At every point where
    # we want to insert data, we write ":" and variable name.
    query = "SELECT * FROM friends WHERE id = :specific_id"
    # Then define a dictionary with key that matches :variable_name in query.
    data = {'specific_id': id}
    # Run query with inserted data.
    friends = mysql.query_db(query, data)
    # Friends should be a list with a single object,
    # so we pass the value at [0] to our template under alias one_friend.
    return render_template('users/edit.html', friend=friends)

@app.route('/create', methods=['POST'])
def create():
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "INSERT INTO friends (first_name, last_name, email, created_at, updated_at) VALUES (:first_name, :last_name, :email, NOW(), NOW())"
    query2 = "SELECT id FROM friends WHERE email = :email;"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'email': request.form['email']
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    new_id = mysql.query_db(query2, data)
    session['id'] = new_id[0]['id']
    return redirect('/users/<id>')

@app.route('/update', methods=['POST'])
def update():
   # Query to update our Db record.
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name, email = :email, updated_at = NOW() WHERE id = :id;"
    # We'll then create a dictionary of data from the POST data received.
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'email': request.form['email'],
             'id': request.form['id']
           }
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    session['id'] = request.form['id']
    return redirect('/users/<id>')

@app.route('/users/<id>/destroy', methods=['GET'])
def destroy(id):
    # Write query as a string. Notice how we have multiple values
    # we want to insert into our query.
    query = "DELETE FROM friends WHERE id= :specific_id;"
    # We'll then create a dictionary of data from the POST data received.
    data = {'specific_id': id}
    # Run query, with dictionary values injected into the query.
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)
