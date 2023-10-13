from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'iifoagohabfoijsmhdoaijd'
app.config['JWT_SECRET_KEY'] = 'aldgnajkgjndfpnpqejnf'

# Create the JWT manager
jwt = JWTManager(app)

# Connect to the Flectra database
connection = psycopg2.connect(
    host='localhost',
    port=5432,
    database='flectra', 
    user='flectra',       
    password='flectra'    
)


# Define the routes
@app.route('/web/login', methods=['GET','POST'])
def login():

    # email = request.json['email']
    data = request.get_json()
    email = data.get('email')
    # Query the database to verify the email
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT * FROM res_users WHERE login = %s',
            (email,)
        )
        user = cursor.fetchone()

    if user is not None:
        access_token = create_access_token(identity=user['id'])
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'error': 'Invalid email'})

if __name__ == '__main__':
    app.run(debug=True)
