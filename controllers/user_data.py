from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, insertRecordReturnId, updateRecordWithOutResponce
from models.users_model import updateUserData
from utils.jithu_helper import date_to_timestamp, generate_otp,get_random_strings,getTimeStamp, getTimestampToOnlyDate
from utils.send_email import send_mail
from bson.objectid import ObjectId

userDataCtrl = Blueprint('/user_data',__name__)

@userDataCtrl.route('all',methods=[ "GET"])
@cross_origin() 
def categories_list():
    result = getAllRecords('categories',{'status':"Active"},True,"name",1,{"_id":1,"name":1})
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200

@userDataCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def categories_add():
    if request.method == "POST":
        name = request.json['name']
        display_order = request.json['display_order']
        if name is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = insertRecordReturnId('categories',{'name':name,'display_order':display_order, 'status':"Active",'created_at':getTimeStamp()})
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data added successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})      

# update category function
@userDataCtrl.route('update/<id>', methods=[ "POST"])
@cross_origin() 
def categories_update(id):
    if request.method == "POST":
        name = request.json['name']
        display_order = request.json['display_order']
        status = request.json['status']
        if name is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = updateRecordWithOutResponce('categories',{'_id':ObjectId(id)},{'$set':{'name':name,'status':status,'display_order':display_order}})
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete category function
@userDataCtrl.route('delete/<id>', methods=[ "DELETE"])
@cross_origin() 
def categories_delete(id):
    result = deleteRecordWithOutResponce('categories',id)
    if result == False:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Data deleted successfully"}),200



@userDataCtrl.route('events',methods=[ "GET"])
@cross_origin() 
def event_list():
    where = {'status':"Active"}
    if request.method == "POST":
        from_date = date_to_timestamp(request.json['from_date'])
        to_date = date_to_timestamp(request.json['to_date'])
        where.update({ 'event_date': {
        '$gte': from_date,  # Greater than or equal to from_date
        '$lte': to_date     # Less than or equal to to_date
        }})   
    # add where conditions from and to date from inputs in database date format is timestamp format
    
    result = getAllRecords('events',{'status':"Active"},True,"event_date",-1,{})
    
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        #  crated_at timestamp to date convert 
        # result = [ {**r, 'event_date': getTimestampToOnlyDate(int(r['event_date']))} for r in result]
        result = [
        {
            **r, 
            'created_at': getTimestampToOnlyDate(int(r['created_at'])),
            'event_date': getTimestampToOnlyDate(int(r['event_date']))
        }
        for r in result
        ]
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200








