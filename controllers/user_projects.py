from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import updateUserData
from utils.jithu_helper import generate_otp,get_random_strings,getTimeStamp
from utils.send_email import send_mail
from bson.objectid import ObjectId

userProjectsCtrl = Blueprint('/user_projects',__name__)
table = 'user_projects'
@userProjectsCtrl.route('all',methods=[ "POST"])
@cross_origin() 
def list():
    return "test" 
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        result = getAllRecords(table,{'user_id':user['_id']},True,"_id",-1,{})
        if result is None:
            return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
        else:
            return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200
    return jsonify({"status": "invalid", "message": "details not found", "error": "invalid_data"}), 200

@userProjectsCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def add():
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        title = request.json['title']
        client_name = request.json['client_name']
        project_url = request.json['project_url']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        description = request.json['description']
        status = request.json['status'] # "Completed"/"InProgress"
        if title is None:
            return jsonify({'status':'invalid','message':"Title is required."}),200
        else:
            ins_data = {
                'user_id':user["_id"],
                'title':title,
                'client_name':client_name,
                'project_url':project_url,
                'start_date':start_date,
                'end_date':end_date,
                'description':description,
                'status':status,
                'created_at':getTimeStamp()
                }
            result = insertRecordReturnId(table,ins_data)
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data added successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})      

# update category function
@userProjectsCtrl.route('update', methods=[ "POST"])
@cross_origin() 
def update():
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        set_data = {}
        id = request.json['id']
        title = request.json['title']
        client_name = request.json['client_name']
        project_url = request.json['project_url']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        description = request.json['description']
        status = request.json['status'] # "Completed"/"InProgress"
        if title is None:
            return jsonify({'status':'invalid','message':"Title is required."}),200
        if id is None:
            return jsonify({'status':'invalid','message':"Id is required."}),200
        else:
            set_data.update({
                'title':title,
                'client_name':client_name,
                'project_url':project_url,
                'start_date':start_date,
                'end_date':end_date,
                'description':description,
                'status':status,
                "updated_at":getTimeStamp()
                })
            result = updateRecordWithOutResponce(table,{'_id':ObjectId(id)},set_data)
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete category function
@userProjectsCtrl.route('delete/<id>', methods=[ "POST"])
@cross_origin() 
def delete(id):
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        result = deleteRecordWithOutResponce(table,id)
        if result == False:
            return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
        else:
            return jsonify({'status':'valid','message':"Data deleted successfully"}),200












