
from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo
from models.common_model import  getAllRecordsWithJoinsPagination, getSingleRecord, getSingleRecordWithWhere, insertRecordReturnId, updateRecordWithOutResponce
from bson.objectid import ObjectId
from utils.jithu_helper import date_to_timestamp, getTimeStamp

userJobsCtrl = Blueprint('/user_jobs',__name__)
table = 'jobs'

@userJobsCtrl.route('/single/<id>', methods=['POST'])
@cross_origin()
def get_single_jobs(id):
    access_token = request.json['access_token']
    #extra parameters for filters 
    try:
        is_featured = request.json['is_featured']
    except KeyError:
        is_featured = False
    
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    where = {}
    page =1,
    per_page = 10
    if request.method == "POST":
        where.update({"_id": ObjectId(id)})
        #active_status
        if 'active_status' in request.json and request.json['active_status']:
            where.update({"active_status": request.json['active_status']})
        if 'from_date' in request.json and request.json['from_date']:
            try:
                from_date =  date_to_timestamp(request.json['from_date'])   
                where.update({"created_at": {"$gte": from_date}})
            except ValueError:
                # Handle invalid date format
                pass

        if 'to_date' in request.json and request.json['to_date']:
            try:
                to_date = date_to_timestamp(request.json['to_date'])  
                # Combine with existing 'created_at' condition using $lte
                if 'created_at' in where:
                    where['created_at'].update({"$lte": to_date})
                else:
                    where.update({"created_at": {"$lte": to_date}})
            except ValueError:
                # Handle invalid date format
                pass
        # Pagination parameters
        if 'page' in request.json and request.json['page'] is not None:
            try:
                page = request.json['page']
                # Combine with existing 'created_at' condition using $lte
            except  KeyError:
                # Handle invalid date format
                pass
        if 'per_page' in request.json and request.json['per_page'] is not None:
            try:
                per_page = request.json['per_page']
                # Combine with existing 'created_at' condition using $lte
            except (ValueError,KeyError):
                # Handle invalid date format
                pass   
    selectedFields = {}     
    joinTable = [
        {"from":"categories","localField":"category_id","type":"single_record","as":"category","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"name":1}},
        {"from":"sub_categories","localField":"sub_category_id","type":"single_record","as":"sub_category","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"name":1}},
        {"from":"recruiters","localField":"recruiter_id","type":"single_record","as":"recruiter_details","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"company_name":1,"name":1,"mobile":1,"email":1}},
    ]
    services =  getAllRecordsWithJoinsPagination(table,joinTable,where,selectedFields,False,{},"_id",page=page,per_page=per_page)
    return jsonify({'status': "valid", 'message': "Getting data successfully", "data": services}) 

@userJobsCtrl.route('/all', methods=['POST'])
@cross_origin()
def get_all_jobs():
    access_token = request.json['access_token']
    #extra parameters for filters 
    try:
        is_featured = request.json['is_featured']
    except KeyError:
        is_featured = False
    
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    
    
    
    user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    where = {}
    page =1,
    per_page = 10
    if request.method == "POST":
        #active_status
        if 'active_status' in request.json and request.json['active_status']:
            where.update({"active_status": request.json['active_status']})

        # is_featured Yes/ No
        if 'is_featured' in request.json and request.json['is_featured']:
            where.update({"is_featured": request.json['is_featured']})

        if 'from_date' in request.json and request.json['from_date']:
            try:
                from_date =  date_to_timestamp(request.json['from_date'])   
                where.update({"created_at": {"$gte": from_date}})
            except ValueError:
                # Handle invalid date format
                pass

        if 'to_date' in request.json and request.json['to_date']:
            try:
                to_date = date_to_timestamp(request.json['to_date'])  
                # Combine with existing 'created_at' condition using $lte
                if 'created_at' in where:
                    where['created_at'].update({"$lte": to_date})
                else:
                    where.update({"created_at": {"$lte": to_date}})
            except ValueError:
                # Handle invalid date format
                pass
        # Pagination parameters
        if 'page' in request.json and request.json['page'] is not None:
            try:
                page = request.json['page']
                # Combine with existing 'created_at' condition using $lte
            except  KeyError:
                # Handle invalid date format
                pass
        if 'per_page' in request.json and request.json['per_page'] is not None:
            try:
                per_page = request.json['per_page']
                # Combine with existing 'created_at' condition using $lte
            except (ValueError,KeyError):
                # Handle invalid date format
                pass   
    selectedFields = {}     
    joinTable = [
        {"from":"categories","localField":"category_id","type":"single_record","as":"category","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"name":1}},
        {"from":"sub_categories","localField":"sub_category_id","type":"single_record","as":"sub_category","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"name":1}},
        {"from":"recruiters","localField":"recruiter_id","type":"single_record","as":"recruiter_details","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"company_name":1,"name":1,"mobile":1,"email":1}},
    ]
    services =  getAllRecordsWithJoinsPagination(table,joinTable,where,selectedFields,False,{},"_id",page=page,per_page=per_page)
    return jsonify({'status': "valid", 'message': "Getting data successfully", "data": services}) 

@userJobsCtrl.route('/view_count_update/<id>', methods=['POST'])
@cross_origin()
def update_views_count(id):
    if id is None:
        return jsonify({"status": "invalid", "message": "Invalid Job ID", "error": "invalid_job_id"}), 200
    table = "jobs"
    # get the data 
    pre_data = getSingleRecord(table,id)
    data = {"views_count": pre_data['views_count'] + 1}
    update = updateRecordWithOutResponce(table, {"_id": ObjectId(id)}, data)
    if update:
        return jsonify({'status': 'valid','message': 'Job Post View Count Updated Successfully.'})
    else:
        return jsonify({'status': 'invalid','message': 'Failed to update job post'})
    
@userJobsCtrl.route('/apply_job/<id>', methods=['POST'])
@cross_origin()
def apply_job_post(id):
    access_token = request.json['access_token']
    try:
        resume = request.json['resume']
    except KeyError:
        resume = ""
    job_id = id
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    
    table = 'job_applications'
    where = {"user_id": user["_id"], "job_id": ObjectId(id)}
    #check before insert already applied
    pre_application = getSingleRecordWithWhere(table, where)
    if pre_application:
        return jsonify({"status": "invalid", "message": "You have already applied for this job", "error": "already_applied"}), 200
    #insert job application data

    data = {"user_id": user["_id"],"resume":resume, "job_id": ObjectId(id),"job_status":"Applied", "created_at": getTimeStamp()}
    
    apply_job = insertRecordReturnId(table, data)
    if apply_job: 
        return jsonify({'status': 'valid','message': 'Job Application Submitted Successfully.'})
    else:
        return jsonify({'status': 'invalid','message': 'Failed to submit job application'})
    