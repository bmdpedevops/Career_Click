from models.common_model import getSingleRecordWithWhere, insertRecordReturnId, updateRecordWithOutResponce
from models.countries import getCities, getCountries, getStates
from models.recruiter import generate_ref_id, updated_ref_id
from utils.jithu_helper import generate_otp, get_random_strings, getTimeStamp
from . import recruiter_bp
from flask import Blueprint,request,jsonify
from flask_cors import cross_origin

table = "recruiters"
@recruiter_bp.route('/login', methods=['GET', 'POST'])
@cross_origin()
def recruiter_login():
    # return getStates()
    # return getCities("Andhra Pradesh")
    if request.method == 'POST':
        # login with email and password
        if request.json['mobile']:
            # check if mobile exists in database
            user = getSingleRecordWithWhere(table,{"mobile":request.json['mobile']})
            if user is None:
                return jsonify({'status': 'invalid','message': 'Mobile does not exist'})
            else:
                # Generate OTP
                otp = generate_otp()  # Assuming this function generates the OTP
                    # Update OTP for the user
                where = {"mobile": request.json['mobile']}
                set_data = {"otp": otp,"updated_at":getTimeStamp()}
                is_updated = updateRecordWithOutResponce(table,where,set_data) 
                if is_updated:
                    # send otp here
                    return jsonify({'status': 'valid','message': "OTP Sent Successfully."})
                else:
                    return jsonify({'status': 'invalid','message': 'Failed to send OTP'})
        else:
            return jsonify({'status': 'invalid','message': 'Mobile is required'})



@recruiter_bp.route("/verify_otp", methods=["POST"])
@cross_origin()
def verify_otp():
    # Email exists  checking
    otp = request.json['otp']
    mobile = request.json['mobile']
    user = getSingleRecordWithWhere(table,{"mobile":mobile})
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
        update = updateRecordWithOutResponce(table,{"_id": user["_id"]}, {"access_token":accesstoken,"mobile_verified": 1,"otp":"","active_status":"Active", "last_login_time":getTimeStamp() ,"mobile_verified_at": getTimeStamp()})
        if update:
            return jsonify({'status': "valid", 'message': "Mobile Verified Successfully.","data":{
                    "access_token":accesstoken,
                }})
    return jsonify({'message': "Invalid OTP.Try Again", "status": "invalid", "error": "otp_invalid"}), 200



@recruiter_bp.route('logout',methods=[ "POST"])
@cross_origin()
def userLogout():
    user = request.json['access_token']
    if user is None:
            return jsonify(
                {"status": "invalid", 'message': "User is required.", "error_code": "user_required" }), 200
            
    # Check if User exists
    user_exists = updateRecordWithOutResponce(table,{"access_token": request.json['access_token']},{"access_token": ""}) 
    if user_exists:
        return jsonify({"status": "valid", "message": "Logged Out Successfully."}), 200
    else:
        return jsonify({"status": "invalid", "message": "User is not logged in.", "error": "user_not_logged_in"}), 200

# register user with database columns like name,company_name,company_address,mobile,email,no_of_employees
@recruiter_bp.route('/register', methods=['POST'])
@cross_origin()
def register_user():
    if request.method == 'POST':
        # register with name, company_name, company_address, mobile, email, no_of_employees
        try:
            name = request.json['name']
        except Exception as e:
            return jsonify({'status':"invalid","message":"name is required"})
        try:
            company_name = request.json['company_name']
        except Exception as e:
            return jsonify({'status':"invalid","message":"company name is required"})
        try:
            mobile = request.json['mobile']
        except Exception as e:
            return jsonify({'status':"invalid","message":"mobile is required"})
        try:
            email = request.json['email']
        except Exception as e:
            return jsonify({'status':"invalid","message":"email is required"})
        
        try:
            state = request.json['state']
        except Exception as e:
            return jsonify({'status':"invalid","message":"state is required"})
        try:
            city = request.json['city']
        except Exception as e:
            return jsonify({'status':"invalid","message":"city is required"})
        
        name = request.json['name']
        company_name = request.json['company_name']
        mobile = request.json['mobile']
        email = request.json['email']
        company_address = request.json['company_address']
        
        try:
            no_of_employees = request.json['no_of_employees']
        except Exception as e:
            no_of_employees =  ""
            
        try:
            no_of_employees = request.json['no_of_employees']
        except Exception as e:
            no_of_employees =  ""
                
        state = request.json['state']
        city = request.json['city']
        
        access_token = get_random_strings(45)
        
        if name is None or company_name is None or company_address is None or mobile is None or email is None or state is None:
            return jsonify({'status':'invalid','message':"All fields are required."}),200
        
        otp = generate_otp()  # Assuming this function generates the OTP
        # prepare json object for insert operation
        refdata = generate_ref_id()
        nxtNum = refdata["next_number"]
        data = {
            "name": name,
            "ref_id":refdata['ref_id'],
            "company_name": company_name,
            "mobile": mobile,
            "email": email,
            "state": state,
            "city": city,
            "company_address": company_address,
            "no_of_employees": no_of_employees,
            "access_token": access_token,
            "created_at": getTimeStamp(),
            "updated_at": getTimeStamp(),
            "active_status": "Inactive",
            "mobile_verified": 0,
            "otp": otp,
            "profile_image": "",
            "company_logo": "",
            "last_login_time": "",
            "mobile_verified_at": ""
        }
        # insert data to database
        is_inserted = insertRecordReturnId(table,data)
        if is_inserted:
            # sent otp here
            updated_ref_id(nxtNum)
            return jsonify({'status': 'valid','message': 'User Registered Successfully.OTP sent to your mobile.','data':{
                    "access_token": access_token,
                }})
        else:
            return jsonify({'status': 'invalid','message': 'Failed to register'})