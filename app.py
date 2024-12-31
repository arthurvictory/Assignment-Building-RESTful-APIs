from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

# Define the Customer Schema
class MembersSchema(ma.Schema):
    id = fields.String(required = True)
    name = fields.String(required = True)
    age = fields.String(required = True)
    
    class Meta:
        fields = ("id", "name", "age")

member_schema = MembersSchema()
members_schema = MembersSchema(many = True)

# Define Workout Schema
class SessionSchema(ma.Schema):
    session_id = fields.Integer(required = True)
    member_id = fields.String(required = True)
    session_date = fields.String(required = True)
    duration_minutes = fields.String(required = True)
    calories_burned = fields.String(required = True)

    class Meta:
        fields = ('session_id', 'member_id', 'session_date', 'duration_minutes', 'calories_burned',)

session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)

def get_db_connection():
    db_name = "fitness_center_db"
    user = "root"
    password = "Mp261Vk823!"
    host = "localhost"

    try:
        conn = mysql.connector.connect(
            database = db_name,
            user = user,
            password = password,
            host = host
        )

        print("Connected to MySQL database successfully!")
        return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return 'Welcome to the Fitness Center Database!'

#Task 2 Implementing CRUD Operations for Members
@app.route("/members", methods=["POST"])
def add_members():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['id'], member_data['name'], member_data['age'])

        query = "INSERT INTO members (id, name, age) VALUES (%s, %s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "New member added successfully"}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members", methods = ["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True)

        query = "SELECT * FROM Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["PUT"])
def update_members(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['id'], member_data['name'], member_data['age'], id)

        query = "UPDATE Members SET id = %s, name = %s, age = %s WHERE id = %s"

        cursor.execute(query, updated_member)
        conn.commit()

        return jsonify({"message": "Current member updated successfully"}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/members/<int:id>", methods=["DELETE"])
def delete_members(id):    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        deleted_member = (id, )

        cursor.execute("SELECT * FROM Members WHERE id = %s", deleted_member)
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Member not found"})

        query = "DELETE FROM Members WHERE id = %s"
        cursor.execute(query, deleted_member)
        conn.commit()

        return jsonify({"message": "Member has been removed from the system"}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# Task 3 Managing workout sessions
@app.route("/workoutsessions", methods = ["GET"])
def get_workouts():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True)

        query = "SELECT * FROM workoutsessions"

        cursor.execute(query)

        sessions = cursor.fetchall()

        return sessions_schema.jsonify(sessions)
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions", methods=["POST"])
def add_workout():
    try:
        workout_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_workout = (workout_data['session_id'], workout_data['member_id'], workout_data['session_date'], workout_data['duration_minutes'], workout_data['calories_burned'])

        query = "INSERT INTO workoutsessions (session_id, member_id, session_date, duration_minutes, calories_burned) VALUES (%s, %s, %s, %s, %s)"

        cursor.execute(query, new_workout)
        conn.commit()

        return jsonify({"message": "New workout session added successfully"}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions/<int:session_id>", methods=["PUT"])
def update_workout(session_id):
    try:
        workout_data = session_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_workout = (workout_data['session_id'], workout_data['member_id'], workout_data['session_date'], workout_data['duration_minutes'], workout_data['calories_burned'], session_id)

        query = "UPDATE Workoutsessions SET session_id = %s, member_id = %s, session_date = %s, duration_minutes = %s, calories_burned = %s WHERE session_id = %s"

        cursor.execute(query, updated_workout)
        conn.commit()

        return jsonify({"message": "Current workout updated successfully"}), 201
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route("/workoutsessions/<int:session_id>", methods=["GET"])
def display_workout(session_id):    
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary = True)

        display_workouts = (session_id, )

        cursor.execute("SELECT * FROM Workoutsessions WHERE session_id = %s", display_workouts)
        workout = cursor.fetchone()

        if not workout:
            return jsonify({"error": "Session ID not found"})

        query = "SELECT * FROM Workoutsessions WHERE session_id = %s"
        cursor.execute(query, display_workouts)
        sessions = cursor.fetchall()
        return sessions_schema.jsonify(sessions)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    app.run(debug = True)