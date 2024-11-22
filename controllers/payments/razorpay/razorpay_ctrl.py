from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from models.common_model import getAllRecords
from bson.objectid import ObjectId

razorPayment = Blueprint('/razorpay',__name__)


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