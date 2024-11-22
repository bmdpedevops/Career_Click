from flask import Blueprint,jsonify,request
from bson.json_util import dumps
from flask_cors import cross_origin
from database import mongo, bcrypt
import json
from bson import ObjectId, json_util
from models.common_model import deleteRecord, deleteRecordWithOutResponce, getAllRecords, getAllRecordsWithJoins, updateRecordWithOutResponce
from models.users_model import getMembersList, updateUserData
from utils.jithu_helper import base_url, convertTimeStampToDate, get_random_strings, getTimeStamp
from utils.send_email import send_mail

userCtrl = Blueprint('/user',__name__)



@userCtrl.route("/delete_account", methods=["POST"])
@cross_origin()   
def delete_account(): 
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        # delete the user
        deleteUser =deleteRecordWithOutResponce('users',{"_id": user["_id"]})
        if deleteUser == False:
            return jsonify({"status": "invalid", "message": "User deletion failed", "error": "user_deletion_failed"}), 200
        else:
            return jsonify({"status": "valid", "message": "User deleted successfully"}), 200
    return jsonify({"status": "valid", "message": "Invalid data privded"})


@userCtrl.route("/details", methods=["POST"])
@cross_origin()     
def index():
    # user profile details getting
    access_token = request.json['access_token']
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    projection = {
                '_id': False,
                "access_token": True,
                "name": True,
                "ref_id":True,
                "designation": True,
                "email": True,
                "profile_image": True,
                "mobile": True,
                "created_at":True,
                "active_status":True,
                "first_name":True, 
                "last_name":True,
                "profile_title":True,
                "work_status":True,
                "total_years_of_experance":True,
                "package_per_anum":True,
                "notice_period_in_months":True, 
                "lat":True,
                "long":True,
                "location":True,
                "resume":True,
                "last_login_time":True
                }
    user = mongo.db.users.find_one({"access_token": access_token}, projection)
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    else:
        # user["_id"] = str(user["_id"])
        # user["profile_image"] = ""
        if user["profile_image"] is not None:
            # add full url to user profile image
            user["profile_image"] =  base_url( user["profile_image"])  #("https://43.204.97.119/" + user["profile_image"])

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
        return jsonify({"status": "valid","message": "Success", "data": json.loads(json_util.dumps(user))})
    
    
@userCtrl.route("/profile_update", methods=["POST"])
@cross_origin()
def update():
    access_token = request.json['access_token']
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    # return jsonify({"status":"valid","message":"Success","data":request.json})
    if access_token is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    
    if first_name is None:
        return jsonify({"status": "invalid", "message": "Name is required", "error": "invalid_name"}), 200
    
    user = mongo.db.users.find_one({"access_token": access_token})
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    try:
        request.json['lat'] = request.json['lat']
    except KeyError:
        request.json['lat'] = ""
    try:
        request.json['long'] = request.json['long']
    except KeyError:
        request.json['long'] = ""
        
    try:
        request.json['profile_image'] = request.json['profile_image']
    except KeyError:
        request.json['profile_image'] = ""
    
    
    try:
        request.json['referral_code'] = request.json['referral_code']
    except KeyError:
        request.json['referral_code'] = ""
    try:
        request.json['profile_title'] = request.json['profile_title']
    except KeyError:
        request.json['profile_title'] = ""
    try:
        request.json['work_status'] = request.json['work_status']
    except KeyError:
        request.json['work_status'] = ""
    try:
        request.json['total_years_of_experance'] = request.json['total_years_of_experance']
    except KeyError:
        request.json['total_years_of_experance'] = ""
    try:
        request.json['package_per_anum'] = request.json['package_per_anum']
    except KeyError:
        request.json['package_per_anum'] = ""
    try:
        request.json['notice_period_in_months'] = request.json['notice_period_in_months']
    except KeyError:
        request.json['notice_period_in_months'] = ""
    try:
        request.json['location'] = request.json['location']
    except KeyError:
        request.json['location'] = ""
    try:
        request.json['resume'] = request.json['resume']
    except KeyError:
        request.json['resume'] = ""

    try:
        request.json['first_name'] = request.json['first_name']
    except KeyError:
        request.json['first_name'] = ""

    try:
        request.json['last_name'] = request.json['last_name']
    except KeyError:
        request.json['last_name'] = ""

    profileData = {}
    if request.json['first_name']:
        profileData.update({
            "first_name": request.json['first_name'],
    })
    if request.json['last_name']:
        profileData.update({
            "last_name": request.json['last_name'],
    })
    if request.json['email']:
        profileData.update({
            "email": request.json['email'],
    })

    if request.json['lat']:
        profileData.update({
            "lat": request.json['lat'],
    })
    if request.json['long']:
        profileData.update({
            "long": request.json['long'],
    })

    if request.json['referral_code']:
        # get the by ref_id 
        referred_by = mongo.db.users.find_one({"ref_id": request.json['referral_code']})
        if referred_by:
            profileData.update({
                "referred_by_user_id": referred_by["_id"]
            })
        

    if request.json['profile_image']:
        profileData.update({
            "profile_image":request.json['profile_image']
        })
    if request.json['profile_title']:
        profileData.update({
            "profile_title":request.json['profile_title']
        })
    if request.json['work_status']:
        profileData.update({
            "work_status":request.json['work_status']
        })
    if request.json['total_years_of_experance']:
        profileData.update({
            "total_years_of_experance":request.json['total_years_of_experance']
        })
    if request.json['package_per_anum']:
        profileData.update({
            "package_per_anum":request.json['package_per_anum']
        })
    if request.json['notice_period_in_months']:
        profileData.update({
            "notice_period_in_months":request.json['notice_period_in_months']
        })
    if request.json['location']:
        profileData.update({
            "location":request.json['location']
        })
    if request.json['resume']:
        profileData.update({
            "resume":request.json['resume']
        })
    
    updateddate = updateUserData({"access_token": access_token}, profileData)
    if updateddate:
        return jsonify({"status": "valid", "message": "Profile updated successfully"}), 200
    else:
        return jsonify({"status": "invalid", "message": "Modification not made"}), 200


