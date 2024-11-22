from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import updateUserData
from utils.jithu_helper import generate_otp,get_random_strings,getTimeStamp
from utils.send_email import send_mail
from bson.objectid import ObjectId

userLocationCtrl = Blueprint('/post_job',__name__)
table = 'jobs'
@userLocationCtrl.route('all',methods=[ "POST"])
@cross_origin() 
def list():
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

@userLocationCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def add():
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        
        
        location_description = request.json['location_description']
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        location_title = request.json['location_title']
        land_mark = request.json['land_mark']
        address_line = request.json['address_line']
        address_line2 = request.json['address_line2']
        if location_description is None:
            return jsonify({'status':'invalid','message':"Name of institution is required."}),200
        elif location_title is None:
            return jsonify({'status':'invalid','message':"location title is required."}),200
        else:
            ins_data = {
                'user_id':user["_id"],
                'location_description':location_description,
                'address_line':address_line,
                'address_line2':address_line2,
                'latitude':latitude,
                'longitude':longitude,
                'location_title':location_title,
                'land_mark':land_mark,
                'status':"Active",
                'created_at':getTimeStamp()
                }
            result = insertRecordReturnId(table,ins_data)
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data added successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})      

# update category function
@userLocationCtrl.route('update', methods=[ "POST"])
@cross_origin() 
def update():
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        if request.json['id'] is None:
            return jsonify({'status':'invalid','message':"Id is required."}),200
        set_data = {}
        try:
            id = request.json['id']
        except Exception as e:
            return jsonify({'status':'invalid','message':"Id should be in valid format."}),200
        location_description = request.json['location_description']
        latitude = request.json['latitude']
        longitude = request.json['longitude']
        location_title = request.json['location_title']
        land_mark = request.json['land_mark']
        address_line = request.json['address_line']
        address_line2 = request.json['address_line2']
        if location_description is None:
            return jsonify({'status':'invalid','message':"Name of institution is required."}),200
        if address_line is None:
            return jsonify({'status':'invalid','message':"Address_line is required."}),200
        if id is None:
            return jsonify({'status':'invalid','message':"Id is required."}),200
        else:
            set_data.update({
                 'location_description':location_description,
                'address_line':address_line,
                'address_line2':address_line2,
                'latitude':latitude,
                'longitude':longitude,
                'location_title':location_title,
                'land_mark':land_mark,
                "updated_at":getTimeStamp()
                })
            result = updateRecordWithOutResponce(table,{'_id':ObjectId(id)},set_data)
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete category function
@userLocationCtrl.route('delete/<id>', methods=[ "POST"])
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















