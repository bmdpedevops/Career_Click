from utils.jithu_helper import date_to_timestamp, getTimeStamp
from . import recruiter_bp
from database import mongo
from flask import request,jsonify
from flask_cors import cross_origin
from models.common_model import deleteRecordWithOutResponce, getAllRecordsWithJoinsPagination, getSingleRecordJson, getSingleRecordWithWhere, insertRecordReturnId, updateRecordWithOutResponce
from bson.objectid import ObjectId

table = "jobs"
recruiter_table = "recruiters"
@recruiter_bp.route('/jobs/all', methods=['POST'])
@cross_origin()
def jobs_all():
    access_token = request.json['access_token']
    active_status = request.json['active_status']
    #extra parameters for filters 
    try:
        is_featured = request.json['is_featured']
    except KeyError:
        is_featured = False
    
    try:
        job_id = request.json['job_id']
    except KeyError:
        job_id = False
    
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    user = getSingleRecordWithWhere(recruiter_table,{"access_token": access_token})
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    where = {}
    page =1,
    per_page = 10
    if request.method == "POST":
        #active_status
        if "job_id" in request.json and request.json["job_id"]:
            where.update({"_id": ObjectId(request.json["job_id"])}) 
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


@recruiter_bp.route('/jobs/details/<id>', methods=[ "POST"])
@cross_origin() 
def details_job_now(id):
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = getSingleRecordWithWhere(recruiter_table,{"access_token": access_token})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        # return str(user)
        result = getSingleRecordJson(table,id)
        # return str(result)
        if result == False:
            return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
        else:
            return jsonify({'status':'valid','message':"Getting Data successfully","data":result}),200
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})

@recruiter_bp.route('/jobs/delete_job/<id>', methods=[ "POST"])
@cross_origin() 
def delete_job_now(id):
    if request.method == "POST":
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = getSingleRecordWithWhere(recruiter_table,{"access_token": access_token}) 
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        result = deleteRecordWithOutResponce(table,id)
        if result == False:
            return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
        else:
            return jsonify({'status':'valid','message':"Job deleted successfully"}),200
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})

@recruiter_bp.route('/jobs/add', methods=[ 'POST'])
@cross_origin()
def jobs_add():
    if request.method == 'POST':
        # register with title, years_of_experience_required, salary_offer, salary_not_disclosure, industry_type,employment_type,job_description,skills_required,work_mode,location

        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = getSingleRecordWithWhere(recruiter_table,{"access_token": access_token})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        job_title = request.json['job_title']
        years_of_experience_required = request.json['years_of_experience_required']
        salary_from = request.json['salary_from'] 
        salary_to = request.json['salary_to'] 
        salary_not_disclosed = request.json['salary_not_disclosed'] 
        category_id = request.json['category_id']
        sub_category_id = request.json['sub_category_id']
        job_types_id = request.json['job_types_id']
        job_description = request.json['job_description']
        work_mode = request.json['work_mode'] # Remote, On-Site or Hybrid
        skills_list = request.json['skills_list'] # category and sub category based 
        state = request.json['state']
        city = request.json['city']
        if salary_not_disclosed == "Yes":
            if salary_to == "" or salary_from == "" :
                return jsonify({'status':'invalid','message':"salary_to and salary_from are required."}),200
            
        
        # prepare json object for insert operation
        data = {
            "recruiter_id": user['_id'],
            "is_featured": "No",
            "job_title": job_title,
            "years_of_experience_required": years_of_experience_required,
            "salary_not_disclosed": salary_not_disclosed, # Yes / No  
            "salary_to": salary_to, 
            "salary_from": salary_from, 
            "category_id": ObjectId(category_id),
            "sub_category_id": ObjectId(sub_category_id),
            "skills_list": skills_list,
            "work_mode": work_mode,
            "job_description": job_description,
            "job_types_id": ObjectId(job_types_id),
            "state": state,
            "city": city,
            "created_at": getTimeStamp(),
            "updated_at": getTimeStamp(),
            "active_status": "Active",
            "views_count": 0,
            "total_applicants_count": 0,
        }
        # insert data to database
        is_inserted = insertRecordReturnId(table,data)
        if is_inserted:
            
            return jsonify({'status': 'valid','message': 'Job Posted Successfully.'})
        else:
            return jsonify({'status': 'invalid','message': 'Failed to register'})




@recruiter_bp.route('/jobs/update/<id>', methods=['POST'])
@cross_origin()
def jobs_update(id):
    if id is None:
            return jsonify({"status": "invalid", "message": "Invalid Job ID", "error": "invalid_job_id"}), 200
    if request.method == 'POST':
        # register with title, years_of_experience_required, salary_offer, salary_not_disclosure, industry_type,employment_type,job_description,skills_required,work_mode,location
        if id is None:
            return jsonify({"status": "invalid", "message": "Invalid Job ID", "error": "invalid_job_id"}), 200
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = getSingleRecordWithWhere(recruiter_table,{"access_token": access_token})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
     
        job_title = request.json['job_title']
        years_of_experience_required = request.json['years_of_experience_required']
        salary_from = request.json['salary_from'] 
        salary_to = request.json['salary_to'] 
        salary_not_disclosed = request.json['salary_not_disclosed'] 
        category_id = request.json['category_id']
        sub_category_id = request.json['sub_category_id']
        job_types_id = request.json['job_types_id']
        job_description = request.json['job_description']
        work_mode = request.json['work_mode'] # Remote, On-Site or Hybrid
        skills_list = request.json['skills_list'] # category and sub category based 
        state = request.json['state']
        city = request.json['city']
        if salary_not_disclosed == "Yes":
            if salary_to == "" or salary_to == "" :
                return jsonify({'status':'invalid','message':"salary_to and salary_from are required."}),200
            
        try:
            request.json['is_featured'] = request.json['is_featured']
        except KeyError:
            request.json['is_featured'] = ""
        # prepare json object for insert operation
        data = {
            "recruiter_id": user['_id'],
            "job_title": job_title,
            "years_of_experience_required": years_of_experience_required,
            "salary_not_disclosed": salary_not_disclosed, # Yes / No  
            "salary_to": salary_to, 
            "salary_from": salary_from, 
            "category_id": ObjectId(category_id),
            "sub_category_id": ObjectId(sub_category_id),
            "skills_list": skills_list,
            "work_mode": work_mode,
            "job_description": job_description,
            "job_types_id": ObjectId(job_types_id),
            "state": state,
            "city": city,
            "created_at": getTimeStamp(),
            "updated_at": getTimeStamp(),
            "active_status": "Active",
            "views_count": 0,
            "total_applicants_count": 0,
        }

        if request.json['is_featured']:
            data.update({
                "is_featured": request.json['is_featured'],
            })
        else:
            data.update({
                "is_featured": "No",
            })
        # insert data to database
        is_inserted = updateRecordWithOutResponce(table,{"_id":ObjectId(id)},data)
        if is_inserted:
            return jsonify({'status': 'valid','message': 'Job Post Updated Successfully.'})
        else:
            return jsonify({'status': 'invalid','message': 'Failed to update job post'})

@recruiter_bp.route('/jobs/status_update/<id>', methods=['POST'])
@cross_origin()
def jobs_status_update(id):
    # id = job_applications_id is required
    if id is None:
            return jsonify({"status": "invalid", "message": "Invalid Job ID", "error": "invalid_job_id"}), 200
    if request.method == 'POST':
        # register with title, years_of_experience_required, salary_offer, salary_not_disclosure, industry_type,employment_type,job_description,skills_required,work_mode,location
        if id is None:
            return jsonify({"status": "invalid", "message": "Invalid Job ID", "error": "invalid_job_id"}), 200
        access_token = request.json['access_token']
        if  access_token == '':
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        user = getSingleRecordWithWhere(recruiter_table,{"access_token": access_token})
        if user is None:
            return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
        
        job_status = request.json['job_status']
        if job_status is None:
            return jsonify({"status": "invalid", "message": "Invalid Job job_status", "error": "invalid_job_status"}), 200
        # prepare json object for insert operation
        data = {
            "job_status": job_status,
            "updated_at": getTimeStamp()
        }
        # insert data to database
        is_inserted = updateRecordWithOutResponce("job_applications",{"_id":ObjectId(id)},data)
        if is_inserted:
            return jsonify({'status': 'valid','message': 'Updated Successfully.'})
        else:
            return jsonify({'status': 'invalid','message': 'Failed to update data'})



@recruiter_bp.route('/jobs/applied_candidates_list/<id>', methods=['POST'])
@cross_origin()
def applied_candidates_list(id):
    access_token = request.json['access_token']
    #extra parameters for filters 
    try:
        is_featured = request.json['is_featured']
    except KeyError:
        is_featured = False
    
    
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    user = getSingleRecordWithWhere(recruiter_table,{"access_token": access_token})
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    where = {}
    page =1,
    per_page = 10
    if request.method == "POST":
        #active_status
        if 'job_status' in request.json and request.json['job_status']:
            where.update({"job_status": request.json['job_status']})
        else:
            where.update({"job_status": "Applied"})
        
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
        {"from":"jobs","localField":"job_id","type":"single_record","as":"job_details","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"job_title":1,"job_description":1,"city":1,"state":1,"active_status":1}},
        {"from":"users","localField":"user_id","type":"single_record","as":"users_details","sort_enable":False,"sort_column":"_id","selected_fields":{"_id":0,"name":1,"mobile":1,"email":1}},
    ]
    services =  getAllRecordsWithJoinsPagination("job_applications",joinTable,where,selectedFields,False,{},"_id",page=page,per_page=per_page)
    return jsonify({'status': "valid", 'message': "Getting data successfully", "data": services})