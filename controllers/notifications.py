from flask import Blueprint, json,request,jsonify
from flask_cors import cross_origin
from models.common_model import getAllRecords
from bson.objectid import ObjectId
from database import mongo, bcrypt

notificationCtrl = Blueprint('/notifications',__name__)

API_ACCESS_KEY = 'YOUR_API_ACCESS_KEY' 
table = "notifications"


@notificationCtrl.route('/all', methods=['POST'])
def getall():
    access_token = request.json['access_token']
    if  access_token == '':
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
   
    user = mongo.db.users.find_one({"access_token": access_token}, {"_id":1})
    if user is None:
        return jsonify({"status": "invalid", "message": "User details not found", "error": "invalid_userdata"}), 200
    
    result = getAllRecords('notifications',{'user_id':user['_id']},True,"_id",-1,{})
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200
    
    
# {
#    "to": "DEVICE_TOKEN",
#    "title": "Notification Title",
#    "message": "Notification Body",
#    "img": "https://example.com/image.png",
#    "id": "1234",
#    "data_title": "Custom Data Title",
#    "data_body": "Custom Data Body"
# }



@notificationCtrl.route('/send-notification', methods=['POST'])
def send_notification():
    data = request.json
    to = data.get('to')
    title = data.get('title')
    message = data.get('message')
    img = data.get('img', '')
    id = data.get('id', '')
    data_title = data.get('data_title', '')
    data_body = data.get('data_body', '')

    result = send_push_notification(to, title, message, img, id, data_title, data_body)
    if result is None:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Getting data successfully","data":result}),200
    
    

def send_push_notification(to, title, message, img='', id='', data_title='', data_body=''):
    url = "https://fcm.googleapis.com/fcm/send"

    notification = {
        'title': title,
        'body': message,
        'image': img,
        'sound': 'default',
        'badge': '1'
    }

    data = {
        'title': data_title,
        'body': data_body,
        'route': 'red',
        'id': id,
        'click_action': 'FLUTTER_NOTIFICATION_CLICK'
    }

    array_to_send = {
        'to': to,
        'notification': notification,
        'data': data,
        'priority': 'high'
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + API_ACCESS_KEY
    }

    response = request.post(url, data=json.dumps(array_to_send), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': 'FCM Send Error: ' + response.text}
