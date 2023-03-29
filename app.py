from flask import Flask, jsonify,request
import psycopg2
import json

app = Flask(__name__)
# Define database connection parameters
DB_HOST = 'db'
DB_NAME = 'movies'
DB_USER = 'postgres'
DB_PASSWORD = 'opke1987'

# Connect to database
conn = psycopg2.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
# Create a cursor object
cur = conn.cursor()
# Execute a SELECT query to fetch all movies from the database
cur.execute('SELECT id, title, director, year FROM movies')
rows = cur.fetchall()
# Convert the list of tuples to a list of dictionaries
movies = []
for row in rows:
    movies.append({'id': row[0], 'title': row[1], 'director': row[2], 'year': row[3]})
# Serialize the list of dictionaries to a JSON string
json_movies = json.dumps(movies)
# Close the cursor and connection
cur.close()
conn.close()

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    cur = conn.cursor()
    cur.execute('SELECT title, director, year FROM movies WHERE id = %s', (id,))
    row = cur.fetchone()
    cur.close()

    if row is None:
        # If no movie with the given ID is found, return a 404 error.
        return jsonify({'error': 'Movie not found'}), 404
    else:
        # If a movie with the given ID is found, return its details.
        movie = {'title': row[0], 'director': row[1], 'year': row[2]}
        return jsonify({'movie': movie})


@app.route('/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    # Get the JSON data from the request body
    data = request.get_json()

    # Update the corresponding movie record in the database
    cur = conn.cursor()
    cur.execute('UPDATE movies SET title=%s, director=%s, year=%s WHERE id=%s',
                (data['title'], data['director'], data['year'], id))
    conn.commit()
    cur.close()

    # Get the updated movie details from the database
    cur = conn.cursor()
    cur.execute('SELECT id, title, director, year FROM movies WHERE id=%s', (id,))
    row = cur.fetchone()
    cur.close()

    # If the movie was successfully updated, return its details
    if row is not None:
        movie = {'id': row[0], 'title': row[1], 'director': row[2], 'year': row[3]}
        return jsonify({'movie': movie}), 200
    else:
        return jsonify({'error': 'Failed to update movie'}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0')
