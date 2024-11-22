from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from models.common_model import getAllRecords
from bson.objectid import ObjectId

categoriesCtrl = Blueprint('/categories',__name__)

@categoriesCtrl.route('all',methods=[ "GET"])
@cross_origin() 
def cateList():
    result = getAllRecords('categories',{'status':"Active"},True,"name",1,{"_id":1,"name":1})
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200
    
@categoriesCtrl.route('sub_categories',methods=[ "GET"])
@cross_origin() 
def subs():
    if request.method == "POST":
        category = request.json["category_id"]
        result = getAllRecords('sub_categories',{'status':"Active",'category_id':ObjectId(category)},True,"name",1,{"_id":1,"category":1,"name":1})
        if result is None:
            return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
        else:
            return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


@categoriesCtrl.route('packages',methods=[ "GET"])
@cross_origin() 
def packages():
    result = []
    # create a loop for experance in years and add into result array
    for i in range(1,51):
        result.append({"id":i,"years":"{} Lakhs".format(i)})

    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid)','message':"Getting data successfully","data":result}),200

@categoriesCtrl.route('experience',methods=[ "GET"])
@cross_origin() 
def experience():
    result = []
    # create a loop for experance in years and add into result array
    for i in range(1,50):
        result.append({"id":i,"years":"{}+ Years".format(i)})

    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid)','message':"Getting data successfully","data":result}),200
    


@categoriesCtrl.route('languages',methods=[ "GET"])
@cross_origin() 
def languages():
    result = [
        {"name":"Telugu"},
        {"name":"English"},
        {"name":"Hindi"},
        {"name":"Tamil"},
        {"name":"Kannada"},
        {"name":"Odiya"}
    ]
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200
    
    

@categoriesCtrl.route('work_status',methods=[ "GET"])
@cross_origin() 
def work_status():
    
    result = [
        {"name":"Fresher"},
        {"name":"Expereieced"}
    ]
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200
    

@categoriesCtrl.route('notice_periods',methods=[ "GET"])
@cross_origin() 
def noticeperios():
    result = [
        { "id":"1", "name":"> 1 Month"},
        { "id":"2", "name":"2 Months"},
        { "id":"3", "name":"3 Months"},
        { "id":"4", "name":"4 Months"},
        { "id":"5", "name":"5 Months"},
        { "id":"6", "name":"6 Months"},
        { "id":"7", "name":"7 Months"},
        { "id":"8", "name":"8 Months"},
        { "id":"9", "name":"9 Months"},
        { "id":"10", "name":"10 Months"},
        { "id":"11", "name":"11 Months"},
        { "id":"12", "name":" 12 Months"}
    ]
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200