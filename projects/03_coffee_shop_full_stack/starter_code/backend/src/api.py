import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks')
def get_drinks():
    data = Drink.query.all()
    return jsonify(
        {
            "success":True,
            "drinks": [d.short() for d in data]
        }
     ), 200 


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
def drinks_details():
    data = Drink.query.all()
    return jsonify(
        {
            "success":True,
            "drinks": [d.long() for d in data]
        }
     ), 200 


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):
    new_drink_data = request.get_json()
    if new_drink_data is None:
        abort(401)
    
    try:
        data = Drink()
        data.title = new_drink_data.get('title')
        data.recipe = json.dumps(new_drink_data.get('recipe'))
        data.insert()
    
    except:
        print(sys.exc_info())
        abort(422)
    
    return jsonify(
        {
            'success':True,
            'drinks': data.long()
        }
    )

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(id):
    new_drink_data = request.get_json()
    error = False
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()#.query.get(id)
        drink.title = new_drink_data.get('title')
        drink.recipe = json.dumps(new_drink_data.get('recipe'))
        drink.update()
    except:
        db.session.rollback()
        error = true
        print(sys.exc_info())
    finally:
        db.session.close()
    
    if error:
        abort(404)
    else:
        return jsonify(
            {
                "success": True, 
                "drinks": drink.long()
            }
        ), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(id):
    error = False
    try:
        #Todo.query.filter_by(id=todo_id).delete()
        drink = Drink.query.get(id)
        db.session.delete(drink)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(401)
    else:
        return jsonify(
            {
                "success": True,
                "delete": id
            }
        )

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return (
      jsonify(
        {
            "success": False, 
            "error": 404, 
            "message": "resource not found"
        }
        ),
      404,
    )

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(401)
def unauthorized(error):
    return (
      jsonify(
        {
            "success": False, 
            "error": 401, 
            "message": "the user is not authorized to perform the task"
        }
        ),
      404,
    )

if __name__ == "__main__":
    app.debug = True
    app.run()
