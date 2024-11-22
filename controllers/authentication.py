from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import generate_ref_id, updateUserData, updated_ref_id
from utils.jithu_helper import generate_otp,get_random_strings,getTimeStamp
from utils.send_email import send_mail
from bson.objectid import ObjectId

authCtrl = Blueprint('/auth',__name__)

@authCtrl.route('resend_otp',methods=[ "POST"])
@cross_origin()
def resend_otp():
    mobile = request.json['mobile']
    if mobile is None:
            return jsonify(
                {"status": "invalid", 'message': "Mobile is required.", "error_code": "mobile_required" }), 200
            
    # Check if mobile exists before inserting OTP
    mobile_exists = mongo.db.users.find_one({"mobile": request.json['mobile']}) is not None
    
    # Generate OTP
    otp = generate_otp()  # Assuming this function generates the OTP
    if not mobile_exists:
        # If mobile doesn't exist, return error response
        return jsonify({'message': "Mobile not registered.", "status": "invalid", "error": "mobile_not_exists" }), 200
    else:
        # Update OTP for the user
        myquery = {"mobile": request.json['mobile']}
        newvalues = {"$set": {"otp": otp}}
        is_updated = mongo.db.users.update_one(myquery, newvalues)
        # Return success response
        return jsonify({'status': "valid", 'message': "OTP Sent Successfully."})

@authCtrl.route('login',methods=["GET","POST"])
@cross_origin() 
def login_user():
    # return {"H":"fjdkafjdsk"}
    mobile = request.json["mobile"]
    user = mongo.db.users.find_one({"mobile": mobile})
    otp = generate_otp()
    # otp = 1234
    # print(user)
    if user is None: 
        #New mobile number
        where = {}
        #  Next Number Generation 
        refdata = generate_ref_id()
        nxtNum = refdata["next_number"]
        insdata = {
            "mobile": request.json['mobile'],
            "ref_id":refdata['ref_id'],
            "referred_by_user_id":"",
            "otp": otp,
            "created_at":getTimeStamp(),
            "updated_at":getTimeStamp(),
            "active_status":"Inactive",
            "first_name":"", 
            "last_name":"",
            "profile_title":"",
            "work_status":"",
            "total_years_of_experance":"",
            "package_per_anum":"",
            "notice_period_in_days":"", 
            "email":"",
            "lat":"",
            "long":"",
            "location":"",
            "resume":"",
            "last_login_time":""
            }
        insertData = insertRecordReturnId("users",insdata) 
        if insertData:
            # send otp here
            updated_ref_id(nxtNum)
            return jsonify({'status':"valid","message":"Otp Sent to your mobile check once.","otp":otp})
    else:
        #exist mobile number
        where = {"mobile": mobile}
        set_data = {"otp": otp,"mobile_verified":0}
        update = updateRecordWithOutResponce("users",where,set_data) 
        if update:
            # send otp here
            return jsonify({'status':"valid","message":"Otp Sent to your mobile check once.","otp":otp})
    return jsonify({'status':"invalid","message":"Otp Sent failed.try again."})  
    
    
@authCtrl.route("/verify_otp", methods=["POST"])
@cross_origin()
def verify_otp():
    # Email exists  checking
    otp = request.json['otp']
    mobile = request.json['mobile']
    user = mongo.db.users.find_one({"mobile": mobile})
    if user is None:
        # If user data is not found, return error response
        return jsonify({'message': "Mobile not registered.", "status": "invalid", "error": "mobile_not_exists", }), 200
    
    if otp == "":
        return jsonify({'message': "Please provide OTP.", "status": "invalid", "error": "otp_required"}), 200
    if user is None:
        return jsonify({"status": "invalid", "message": "Mobile not existed", "error": "mobile_not_found"}), 200

    if str(user["otp"]) != str(otp):
        return jsonify({'message': "Entered OTP is Invalid.Try again..!", "status": "invalid", "error": "otp_invalid"}), 200
    else:
        accesstoken = get_random_strings(45)
        update = updateUserData({"_id": user["_id"]}, {"access_token":accesstoken,"mobile_verified": 1,"otp":"","active_status":"Active", "last_login_time":getTimeStamp() ,"mobile_verified_at": getTimeStamp()})
        if update:
            return jsonify( 
                {'status': "valid", 'message': "Mobile Verified Successfully.","data":{
                    "access_token":accesstoken,
                }})
    return jsonify({'message': "Invalid OTP.Try Again", "status": "invalid", "error": "otp_invalid"}), 200

#Forgot password flow

@authCtrl.route('logout',methods=[ "POST"])
@cross_origin()
def userLogout():
    user = request.json['access_token']
    if user is None:
            return jsonify(
                {"status": "invalid", 'message': "User is required.", "error_code": "user_required" }), 200
            
    # Check if User exists
    user_exists = mongo.db.users.find_one({"access_token": request.json['access_token']}) is not None
    
    
    if not user_exists:
        # If user doesn't exist, return error response
        return jsonify({'message': "user not found.Try again..!", "status": "invalid", "error": "user_not_exists" }), 200
    else:
        # Update OTP for the user
        myquery = {"access_token":user}
        newvalues = {"$set": {"access_token": ""}}
        mongo.db.users.update_one(myquery, newvalues)
        
        
        # Return success response
        return jsonify({'status': "valid", 'message': "Logout Successfully."})
