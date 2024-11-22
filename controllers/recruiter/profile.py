from datetime import datetime, timedelta
from flask import request,jsonify
from models.common_model import deleteRecordWithOutResponce, getCountWithWhere, getSingleRecordWithWhere, updateOtp
from utils.jithu_helper import convertTimeStampToDate
from bson.objectid import ObjectId
from database import mongo
from . import recruiter_bp
from flask_cors import cross_origin

table = "recruiters"

@recruiter_bp.route('/profile/details', methods=['POST'])
@cross_origin()     
def recruiter_profile_details():
    # user profile details getting
    access_token = request.json['access_token']
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    projection = {
                '_id': False,
                "access_token": True,
                "name": True,
                "email": True,
                "profile_image": True,
                "mobile": True,
                "last_login_time": True,
                "created_at":True
                }
    # return {"access_token": access_token}
    user = getSingleRecordWithWhere(table,{"access_token": access_token},True)  #mongo.db[table].find_one({"access_token": access_token}, projection)
    # return str(user)
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    else:
        # user["_id"] = str(user["_id"])
        # user["profile_image"] = ""
        if user["created_at"] is not None:
            user["created_at"] = convertTimeStampToDate(user["created_at"])
        # # user["updated_at"] = convertTimeStampToDate(user["updated_at"])
        if user["last_login_time"] != "":
            try:
                timestamp = int(user["last_login_time"])
                user["last_login_time"] = convertTimeStampToDate(timestamp)
            except ValueError:
                # Handle the case where the string cannot be converted to an integer
                pass
            # user["last_login_time"] = convertTimeStampToDate(user["last_login_time"])
        return jsonify({"status": "valid","message": "Success", "data": user })
    
@recruiter_bp.route('/profile/statistics', methods=['POST'])
@cross_origin()     
def recruiter_statistics():
    # user profile details getting
    result = {
        "total_jobs_posted":0,
        "total_active_jobs":0,
        "total_inactive_jobs":0,
        "total_applied_candidate":0,
    }
    access_token = request.json['access_token']
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    projection = {
                '_id': False,
                "access_token": True,
                "name": True,
                "email": True,
                "profile_image": True,
                "mobile": True,
                "last_login_time": True,
                "created_at":True
                }
    # return {"access_token": access_token}
    user = getSingleRecordWithWhere(table,{"access_token": access_token})  #mongo.db[table].find_one({"access_token": access_token}, projection)
    # return str(user)
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    else:
        # user["_id"] = str(user["_id"])
        # user["profile_image"] = ""
        all_jobs = getCountWithWhere("jobs",{'recruiter_id': (user["_id"])})
        total_active_jobs = getCountWithWhere("jobs",{'recruiter_id': (user["_id"]),"active_status":"Active"})
        total_inactive_jobs = getCountWithWhere("jobs",{'recruiter_id': (user["_id"]),"active_status":"Inactive"})
        
        total_applied_candidate_data = mongo.db.jobs.aggregate([{
                                "$match": {
                                "recruiter_id": user["_id"]
                                }
                            },
                            { "$lookup": {
                                "from": "job_applications",
                                "localField": "_id",
                                "foreignField": "job_id",
                                "as": "applications"
                                }
                            },
                            {
                                "$addFields": {
                                "total_applied_candidates": { "$size": "$applications" }
                                }
                            },
                            {
                                "$project": {
                                    "_id": 1,
                                    "job_title": 1,
                                    "total_applied_candidates": 1
                                    }
                            }
                            ])
                                    
        result.update({'total_jobs_posted':all_jobs,
                        "total_inactive_jobs":total_inactive_jobs,
                        "total_active_jobs":total_active_jobs,
                        "total_applied_candidate":list(total_applied_candidate_data)[0]["total_applied_candidates"] 
                        })
        return jsonify({"status": "valid","message": "Success", "data": result })
    


@recruiter_bp.route('/profile/job_posting_counts', methods=['GET'])
def get_job_posting_counts():
    # Get the current time
    now = datetime.utcnow()
    
    # Define the start of the day, week, month, and year
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_day - timedelta(days=start_of_day.weekday())
    start_of_month = start_of_day.replace(day=1)
    start_of_year = start_of_day.replace(month=1, day=1)
    
    # Define the end of the day, week, month, and year
    end_of_day = start_of_day + timedelta(days=1)
    end_of_week = start_of_week + timedelta(weeks=1)
    end_of_month = (start_of_month + timedelta(days=31)).replace(day=1)
    end_of_year = start_of_year.replace(year=start_of_year.year + 1)
    
    # Convert datetime to Unix timestamp
    start_of_day_ts = int(start_of_day.timestamp())
    end_of_day_ts = int(end_of_day.timestamp())
    start_of_week_ts = int(start_of_week.timestamp())
    end_of_week_ts = int(end_of_week.timestamp())
    start_of_month_ts = int(start_of_month.timestamp())
    end_of_month_ts = int(end_of_month.timestamp())
    start_of_year_ts = int(start_of_year.timestamp())
    end_of_year_ts = int(end_of_year.timestamp())
    
    # Aggregate the job counts
    pipeline = [
        {
            '$facet': {
                'daily': [
                    {'$match': {'created_at': {'$gte': start_of_day_ts, '$lt': end_of_day_ts}}},
                    {'$count': 'count'}
                ],
                'weekly': [
                    {'$match': {'created_at': {'$gte': start_of_week_ts, '$lt': end_of_week_ts}}},
                    {'$count': 'count'}
                ],
                'monthly': [
                    {'$match': {'created_at': {'$gte': start_of_month_ts, '$lt': end_of_month_ts}}},
                    {'$count': 'count'}
                ],
                'yearly': [
                    {'$match': {'created_at': {'$gte': start_of_year_ts, '$lt': end_of_year_ts}}},
                    {'$count': 'count'}
                ]
            }
        }
    ]
    
    result = list(mongo.db.jobs.aggregate(pipeline))
    
    counts = result[0] if result else {}
    # return counts
    return jsonify({"status": "valid","message": "Success", "data": counts })
    
    
    
#updateOtp
@recruiter_bp.route("/profile/generate_otp", methods=["POST"])
@cross_origin()   
def generate_otp(): 
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        user =  getSingleRecordWithWhere(table,{"access_token": access_token}) #mongo.db[table].find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        #updateOtp
        update = updateOtp(table,{"_id":user['_id']}) 
        if update == False:
            return jsonify({"status": "invalid", "message": "OTP verification failed", "error": "invalid_otp"}), 200
        else:
            return jsonify({"status": "valid", "message": "OTP sent successfully"}), 200
        
@recruiter_bp.route("/profile/delete_account", methods=["POST"]) 
@cross_origin()   
def recruiter_delete_account(): 
    if request.method == "POST":
        access_token = request.json['access_token']
        otp = request.json['otp']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        user =  getSingleRecordWithWhere(table,{"access_token": access_token,"otp": int(otp)}) #mongo.db[table].find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        # delete the user
        deleteUser =deleteRecordWithOutResponce(table,{"_id": user["_id"]})
        if deleteUser == False:
            return jsonify({"status": "invalid", "message": "User deletion failed", "error": "user_deletion_failed"}), 200
        else:
            return jsonify({"status": "valid", "message": "User deleted successfully"}), 200
    return jsonify({"status": "valid", "message": "Invalid data provided"})


# # register user with database columns like name,company_name,company_address,mobile,email,no_of_employees
# @recruiter_bp.route('/profile/update', methods=['POST'])
# @cross_origin()
# def recruiter_update_user():
#     if request.method == 'POST':
#         # register with name, company_name, company_address, mobile, email, no_of_employees
#         try:
#             name = request.json['name']
#         except Exception as e:
#             return jsonify({'status':"invalid","message":"name is required"})
#         try:
#             company_name = request.json['company_name']
#         except Exception as e:
#             return jsonify({'status':"invalid","message":"company name is required"})
#         try:
#             mobile = request.json['mobile']
#         except Exception as e:
#             return jsonify({'status':"invalid","message":"mobile is required"})
#         try:
#             email = request.json['email']
#         except Exception as e:
#             return jsonify({'status':"invalid","message":"email is required"})
        
#         try:
#             state = request.json['state']
#         except Exception as e:
#             return jsonify({'status':"invalid","message":"state is required"})
#         try:
#             city = request.json['city']
#         except Exception as e:
#             return jsonify({'status':"invalid","message":"city is required"})
        
#         name = request.json['name']
#         company_name = request.json['company_name']
#         mobile = request.json['mobile']
#         email = request.json['email']
#         company_address = request.json['company_address']
        
#         try:
#             no_of_employees = request.json['no_of_employees']
#         except Exception as e:
#             no_of_employees =  ""
            
#         try:
#             no_of_employees = request.json['no_of_employees']
#         except Exception as e:
#             no_of_employees =  ""
                
#         state = request.json['state']
#         city = request.json['city']
        
#         access_token = get_random_strings(45)
        
#         if name is None or company_name is None or company_address is None or mobile is None or email is None or state is None:
#             return jsonify({'status':'invalid','message':"All fields are required."}),200
        
#         otp = generate_otp()  # Assuming this function generates the OTP
#         # prepare json object for insert operation
#         refdata = generate_ref_id()
#         nxtNum = refdata["next_number"]
#         data = {
#             "name": name,
#             "ref_id":refdata['ref_id'],
#             "company_name": company_name,
#             "mobile": mobile,
#             "email": email,
#             "state": state,
#             "city": city,
#             "company_address": company_address,
#             "no_of_employees": no_of_employees,
#             "access_token": access_token,
#             "created_at": getTimeStamp(),
#             "updated_at": getTimeStamp(),
#             "active_status": "Inactive",
#             "mobile_verified": 0,
#             "otp": otp,
#             "profile_image": "",
#             "company_logo": "",
#             "last_login_time": "",
#             "mobile_verified_at": ""
#         }
#         # insert data to database
#         is_inserted = insertRecordReturnId(table,data)
#         if is_inserted:
#             # sent otp here
#             updated_ref_id(nxtNum)
#             return jsonify({'status': 'valid','message': 'User Registered Successfully.OTP sent to your mobile.','data':{
#                     "access_token": access_token,
#                 }})
#         else:
#             return jsonify({'status': 'invalid','message': 'Failed to register'})