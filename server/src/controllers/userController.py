from flask import Blueprint, jsonify, request
from src.services.userService import createUser, deleteUserById, updateUserById, updateUserPasswordById, loginUser
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.repositories import userRepository

user_bp = Blueprint('user', __name__, url_prefix='/users')

@user_bp.route('/register', methods=['POST'])
def register():
  data = request.json
  username = data.get('username')
  email = data.get('email')
  password = data.get('password')
  confirmPassword = data.get('confirmPassword')

  result, statusCode = createUser(username, email, password, confirmPassword)
  return jsonify(result), statusCode

@user_bp.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  result, statusCode = loginUser(username, password)
  return jsonify(result), statusCode

@user_bp.route('', methods=['GET'])
def readAll():
  result, statusCode = userRepository.findAll()
  return jsonify(result), statusCode

@user_bp.route('/<userId>', methods=['GET'])
# @jwt_required()
def readById(userId):
  result, statusCode = userRepository.findById(userId)
  # jwt_identity = get_jwt_identity()

  # if statusCode == 200 and result['id'] != jwt_identity:
  #   return {"error": "Access Denied, UserId and JWT Identity Doesn't Match!"}, 403

  return jsonify(result), statusCode

@user_bp.route('/<userId>', methods=['PATCH'])
# @jwt_required()
def update(userId):
  data = request.json
  username = data.get('username')
  email = data.get('email')

  if username:
    if len(username) > 16 or len(username) < 3:
      return jsonify(), 400

  result, statusCode = updateUserById(userId, username, email)
  return jsonify(result), statusCode

@user_bp.route('/password/<userId>', methods=['PATCH'])
# @jwt_required()
def updatePassword(userId):
  data = request.json
  password = data.get('password')
  confirmPassword = data.get('confirmPassword')

  result, statusCode = updateUserPasswordById(userId, password, confirmPassword)
  return jsonify(result), statusCode

@user_bp.route('/<userId>', methods=['DELETE'])
# @jwt_required()
def delete(userId):
  result, statusCode = deleteUserById(userId)
  return jsonify(result), statusCode