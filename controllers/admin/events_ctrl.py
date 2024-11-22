from flask import Blueprint,request,jsonify
from flask_cors import cross_origin
from database import mongo, bcrypt
from models.common_model import deleteRecordWithOutResponce, getAllRecords, getSingleRecord, insertRecordReturnId, updateRecordWithOutResponce
from utils.jithu_helper import getTimeStamp, getTimestampToOnlyDate
from bson.objectid import ObjectId

adminEventsCtrl = Blueprint('/events',__name__)
table = "events"
@adminEventsCtrl.route('all',methods=[ "GET"])
@cross_origin() 
def event_list():
    result = getAllRecords(table,{'status':"Active"},True,"event_date",-1,{})
    
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

@adminEventsCtrl.route('add',methods=[ "POST"])
@cross_origin() 
def event_add():
    if request.method == "POST":
        event_title = request.json['event_title']
        event_image = request.json['event_image']
        event_date = request.json['event_date']
        event_city = request.json['event_city']
        about_event = request.json['about_event']
        
        map_location = request.json['map_location']
        lat = request.json['lat']
        long = request.json['long']
        
        organizer_name = request.json['organizer_name']
        organizer_profile_image = request.json['organizer_profile_image']
        event_website_url = request.json['event_website_url']
        event_state = request.json['event_state']
        
        if event_title is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = insertRecordReturnId(table,{
                'event_image':event_image, 
                'event_title':event_title,
                'about_event':about_event, 
                'event_date':event_date, 
                
                'map_location':map_location, 
                'lat':lat, 
                'long':long,  
                
                'organizer_name':organizer_name, 
                'organizer_profile_image':organizer_profile_image, 
                
                'event_website_url':event_website_url, 
                
                'event_state':event_state, 
                'event_city':event_city, 
                
                'event_added_by':"Admin", 
            
                'status':"Active",
                'created_at':getTimeStamp()
                })
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data added successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})      

# update  function
@adminEventsCtrl.route('update/<id>', methods=["POST"])
@cross_origin() 
def event_update(id):
    if request.method == "POST":
        event_title = request.json['event_title']
        event_image = request.json['event_image']
        event_date = request.json['event_date']
        event_city = request.json['event_city']
        about_event = request.json['about_event']
        
        map_location = request.json['map_location']
        lat = request.json['lat']
        long = request.json['long']
        
        organizer_name = request.json['organizer_name']
        organizer_profile_image = request.json['organizer_profile_image']
        event_website_url = request.json['event_website_url']
        event_state = request.json['event_state']
        status = request.json['status']
        
        
        
        if event_title is None:
            return jsonify({'status':'invalid','message':"Name is required."}),400
        else:
            result = updateRecordWithOutResponce(table,{'_id':ObjectId(id)},{
                'event_image':event_image, 
                'event_title':event_title,
                'about_event':about_event, 
                'event_date':event_date, 
                
                'map_location':map_location, 
                'lat':lat, 
                'long':long, 
                
                'organizer_name':organizer_name, 
                'organizer_profile_image':organizer_profile_image, 
                
                'event_website_url':event_website_url, 
                
                'event_state':event_state, 
                'event_city':event_city, 
                
                'status':status,
                'view_count':0,
                'updated_at':getTimeStamp()
                })
            if result is None:
                return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
            else:
                return jsonify({'status':'valid','message':"Data updated successfully"}),200
            
    return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})


# delete  function
@adminEventsCtrl.route('delete/<id>', methods=[ "POST"])
@cross_origin() 
def event_delete(id):
    result = deleteRecordWithOutResponce(table,id)
    if result == False:
        return jsonify({'status':'invalid','message':"Something went wrong.try again..!"})
    else:
        return jsonify({'status':'valid','message':"Data deleted successfully"}),200



@adminEventsCtrl.route('/view_count_update/<id>', methods=['POST'])
@cross_origin()
def update_views_count(id):
    if id is None:
        return jsonify({"status": "invalid", "message": "Invalid Job ID", "error": "invalid_job_id"}), 200
    # get the data 
    pre_data = getSingleRecord(table,id)
    try:
        data = {"views_count": pre_data['views_count'] + 1}
        update = updateRecordWithOutResponce(table, {"_id": ObjectId(id)}, data)
        if update:
            return jsonify({'status': 'valid','message': 'Event View Count Updated Successfully.'})
        else:
            return jsonify({'status': 'invalid','message': 'Failed to update event'})
    except Exception as e:
        return jsonify({'status': 'invalid','message': str(e)})
   








