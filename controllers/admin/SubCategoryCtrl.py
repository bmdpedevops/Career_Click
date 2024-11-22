from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import updateUserData
from utils.jithu_helper import generate_otp,get_random_strings,getTimeStamp
from utils.send_email import send_mail
from bson.objectid import ObjectId

adminSubCategoriesCtrl = Blueprint('/sub_categories',__name__)
table = "sub_categories"
@adminSubCategoriesCtrl.route('all',methods=[ "GET"])
@cross_origin() 
def list():
    result = getAllRecords(table,{'status':"Active"},True,"name",1,{"_id":1,"name":1})
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200

@adminSubCategoriesCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def add():
    if request.method == "POST":
        category_id = request.json['category_id']
        name = request.json['name']
        display_order = request.json['display_order']
        if category_id is None:
            return jsonify({'status':'invalid','message':"Category is required."}),400
        
        if name is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = insertRecordReturnId(table,{'name':name,'category_id':ObjectId(category_id),'display_order':display_order, 'status':"Active",'created_at':getTimeStamp()})
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data added successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})      

# update category function
@adminSubCategoriesCtrl.route('update/<id>', methods=[ "POST"])
@cross_origin() 
def update(id):
    if request.method == "POST":
        category_id = request.json['category_id']
        name = request.json['name']
        display_order = request.json['display_order']
        status = request.json['status']
        if name is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = updateRecordWithOutResponce(table,{'_id':ObjectId(id)},{'$set':{'name':name,'category_id':ObjectId(category_id),'status':status,'display_order':display_order}})
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete category function
@adminSubCategoriesCtrl.route('delete/<id>', methods=[ "DELETE"])
@cross_origin() 
def delete(id):
    result = deleteRecordWithOutResponce(table,id)
    if result == False:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Data deleted successfully"}),200












