from fla import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.String(50), primary_key=True) 
    name = db.Column(db.String(100), nullable=False)


@app.route('/users/<string:user_id>', methods=['PUT'])
def update_user_name(user_id):
    data = request.get_json()
    new_name = data.get('name')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.name = new_name
    db.session.commit()

    return jsonify({'message': f'User with id {user_id} updated'}), 200

if __name__ == '__main__':
    app.run(debug=True)
