from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import updateUserData
from utils.jithu_helper import generate_otp,get_random_strings,getTimeStamp
from utils.send_email import send_mail
from bson.objectid import ObjectId

userEmploymentsCtrl = Blueprint('/user_employment',__name__)
table = 'user_employments'
@userEmploymentsCtrl.route('all',methods=[ "POST"])
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

@userEmploymentsCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def add():
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        is_currently_working = request.json['is_currently_working']
        job_title = request.json['job_title']
        employment_type = request.json['employment_type']
        company_name = request.json['company_name']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        current_ctc = request.json['current_ctc']
        total_years = request.json['total_years']
        skills_used = request.json['skills_used']
        status = request.json['status']
        job_description = request.json['job_description']
        notice_period_in_months = request.json['notice_period_in_months']
        if job_title is None:
            return jsonify({'status':'invalid','message':"Title is required."}),200
        
        if  is_currently_working == 'yes':
            if current_ctc is None:
                return jsonify({'status':'invalid','message':"current ctc is required."}),200
            if notice_period_in_months is None:
                return jsonify({'status':'invalid','message':"notice_period_in_months is required."}),200
            if skills_used is None:
                return jsonify({'status':'invalid','message':"skills_used is required."}),200
            if job_description is None:
                return jsonify({'status':'invalid','message':"job description is required."}),200
        ins_data = {
            'user_id':user["_id"],
            'job_title':job_title,
            'employment_type':employment_type,
            'company_name':company_name,
            'is_currently_working':is_currently_working,
            'status':status,
            'start_date':start_date,
            'end_date':end_date,
            'total_years':total_years,
            'created_at':getTimeStamp()
            }
        if is_currently_working == 'yes':
            ins_data.update({
                'current_ctc':current_ctc,
                'skills_used':skills_used,
                'job_description':job_description,
                'notice_period_in_months':notice_period_in_months,
            })
        
        result = insertRecordReturnId(table,ins_data)
        if result is None:
            return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
        else:
            return jsonify({'status':'valid','message':"Data added successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})      

# update category function
@userEmploymentsCtrl.route('update', methods=[ "POST"])
@cross_origin() 
def update():
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        try:
            id = request.json['id']
        except Exception as e:
            return jsonify({'status':'invalid','message':"Id should be in valid format."}),200
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        is_currently_working = request.json['is_currently_working']
        job_title = request.json['job_title']
        employment_type = request.json['employment_type']
        company_name = request.json['company_name']
        start_date = request.json['start_date']
        end_date = request.json['end_date']
        current_ctc = request.json['current_ctc']
        total_years = request.json['total_years']
        skills_used = request.json['skills_used']
        status = request.json['status']
        job_description = request.json['job_description']
        notice_period_in_months = request.json['notice_period_in_months']
        if job_title is None:
            return jsonify({'status':'invalid','message':"Title is required."}),200
        
        if  is_currently_working == 'yes':
            if current_ctc is None:
                return jsonify({'status':'invalid','message':"current ctc is required."}),200
            if notice_period_in_months is None:
                return jsonify({'status':'invalid','message':"notice_period_in_months is required."}),200
            if skills_used is None:
                return jsonify({'status':'invalid','message':"skills_used is required."}),200
            if job_description is None:
                return jsonify({'status':'invalid','message':"job description is required."}),200
        id = request.json['id']
        
        ins_data = {
            'job_title':job_title,
            'employment_type':employment_type,
            'company_name':company_name,
            'is_currently_working':is_currently_working,
            'user_id':user["_id"],
            'status':status,
            'start_date':start_date,
            'end_date':end_date,
            'total_years':total_years,
            'updated_at':getTimeStamp()
            }
        if is_currently_working == 'yes':
            ins_data.update({
                'current_ctc':current_ctc,
                'skills_used':skills_used,
                'job_description':job_description,
                'notice_period_in_months':notice_period_in_months,
            })
        
        result = updateRecordWithOutResponce(table,{'_id':ObjectId(id)},ins_data)
        if result is None:
            return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
        else:
            return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete category function
@userEmploymentsCtrl.route('delete/<id>', methods=[ "POST"])
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












