from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import updateUserData
from utils.jithu_helper import generate_otp,get_random_strings,getTimeStamp
from utils.send_email import send_mail
from bson.objectid import ObjectId

userEducationCtrl = Blueprint('/user_education',__name__)
table = 'user_education'
@userEducationCtrl.route('all',methods=[ "POST"])
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

@userEducationCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def add():
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        name_of_institution = request.json['name_of_institution']
        specialization = request.json['specialization']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        course_type = request.json['course_type']
        grade_point_average = request.json['grade_point_average']
        course = request.json['course'] 
        if name_of_institution is None:
            return jsonify({'status':'invalid','message':"Name of institution is required."}),200
        if course is None:
            return jsonify({'status':'invalid','message':"Course is required."}),200
        else:
            ins_data = {
                'user_id':user["_id"],
                'name_of_institution':name_of_institution,
                'course':course,
                'specialization':specialization,
                'start_date':start_date,
                'grade_point_average':grade_point_average,
                'end_date':end_date,
                'course_type':course_type,
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
@userEducationCtrl.route('update', methods=[ "POST"])
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
        name_of_institution = request.json['name_of_institution']
        specialization = request.json['specialization']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        course_type = request.json['course_type']
        course = request.json['course']
        grade_point_average = request.json['grade_point_average']
        
        if name_of_institution is None:
            return jsonify({'status':'invalid','message':"Name of institution is required."}),200
        if course is None:
            return jsonify({'status':'invalid','message':"Course is required."}),200
        if id is None:
            return jsonify({'status':'invalid','message':"Id is required."}),200
        else:
            set_data.update({
                 'name_of_institution':name_of_institution,
                'course':course,
                'specialization':specialization,
                'start_date':start_date,
                'grade_point_average':grade_point_average,
                'end_date':end_date,
                'course_type':course_type, 
                "updated_at":getTimeStamp()
                })
            result = updateRecordWithOutResponce(table,{'_id':ObjectId(id)},set_data)
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete category function
@userEducationCtrl.route('delete/<id>', methods=[ "POST"])
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












