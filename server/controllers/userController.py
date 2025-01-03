from flask import Blueprint, jsonify, request
from services.userService import createUser, getAllUsers, getUserById, deleteUserById, updateUserById

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
def register():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  result, statusCode = createUser(username, password)

  if result.get('error'):
    return jsonify(result), statusCode
  
  return jsonify(result), statusCode

# @user_bp.route('/login', methods=['POST'])
# def login():
#   pass

@user_bp.route('', methods=['GET'])
def readAll():
  result, statusCode = getAllUsers()
  return jsonify(result), statusCode

@user_bp.route('/<userId>', methods=['GET'])
def readById(userId):
  result, statusCode = getUserById(userId)

  if result.get('error'):
    return jsonify(result), statusCode

  return jsonify(result), statusCode

@user_bp.route('/<userId>', methods=['PATCH'])
def update(userId):
  data = request.json
  username = data.get('username')

  if username:
    if len(username) > 16 or len(username) < 3:
      return jsonify(), 400

  result, statusCode = updateUserById(userId, username)

  return jsonify(result), statusCode

@user_bp.route('/<userId>', methods=['DELETE'])
def delete(userId):
  result, statusCode = deleteUserById(userId)

  if result.get("error"):
    return jsonify(result), statusCode
  
  return jsonify(), statusCode