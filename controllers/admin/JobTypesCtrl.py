from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import updateUserData
from utils.jithu_helper import generate_otp,get_random_strings,getTimeStamp
from utils.send_email import send_mail
from bson.objectid import ObjectId

adminJobTypesCtrl = Blueprint('/job_types',__name__)
table = "job_types"
@adminJobTypesCtrl.route('all',methods=[ "GET"])
@cross_origin() 
def categories_list():
    result = getAllRecords(table,{'status':"Active"},True,"name",1,{"_id":1,"name":1})
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200

@adminJobTypesCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def categories_add():
    if request.method == "POST":
        name = request.json['name']
        display_order = request.json['display_order']
        if name is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = insertRecordReturnId(table,{'name':name,'display_order':display_order, 'status':"Active",'created_at':getTimeStamp()})
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data added successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})      

# update category function
@adminJobTypesCtrl.route('update/<id>', methods=[ "POST"])
@cross_origin() 
def categories_update(id):
    if request.method == "POST":
        name = request.json['name']
        display_order = request.json['display_order']
        status = request.json['status']
        if name is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = updateRecordWithOutResponce(table,{'_id':ObjectId(id)},{'$set':{'name':name,'status':status,'display_order':display_order}})
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete category function
@adminJobTypesCtrl.route('delete/<id>', methods=[ "DELETE"])
@cross_origin() 
def categories_delete(id):
    result = deleteRecordWithOutResponce(table,id)
    if result == False:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Data deleted successfully"}),200












