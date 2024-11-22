import json
from database import mongo
from bson.objectid import ObjectId
from bson import json_util
from utils.jithu_helper import convertTimeStampToDate, generate_otp


def insertRecord(tableName, insertData):
    id = mongo.db[tableName].insert_one(insertData)
    if id.inserted_id is not None:
        return {"status": "valid", "message": "Data added successfully", "data": {'id': str(id.inserted_id)}}
    else:
        return {"status": "invalid", "message": "Data adding Failed.Try again..!"}

# update otp in database
def updateOtp(table, where):
    otp = generate_otp()  # Assuming this function generates the OTP
    updateDB = {
        "$set": {"otp":otp}
    }
    update = mongo.db[table].update_one(where, updateDB)
    if update.modified_count > 0:
        return True
    else:
        return False

def insertRecordReturnId(tableName, insertData):
    id = mongo.db[tableName].insert_one(insertData)
    if id.inserted_id is not None:
        return str(id.inserted_id)
    
def getCountWithWhere(table,where):
    total_items = mongo.db[table].count_documents(where)
    return total_items

def updateRecord(tableName, whereCondition, setData):
    updateDB = {
        "$set": setData
    }
    update = mongo.db[tableName].update_one(whereCondition, updateDB)
    if update.modified_count > 0:
        return {"status": "valid", "message": "Data Updated successfully"}
    else:
        return {"status": "valid", "message": "Data not updated.No Changes made."}
    
def updateRecordWithOutResponce(tableName, whereCondition, setData):
    updateDB = {
        "$set": setData
    }
    update = mongo.db[tableName].update_one(whereCondition, updateDB)
    if update.modified_count > 0:
        return True
    else:
        return False
def updateRecordWithOutResponceCustomSet(tableName, whereCondition, setData):
    updateDB = setData
    update = mongo.db[tableName].update_one(whereCondition, updateDB)
    if update.modified_count > 0:
        return True
    else:
        return False
def updateRecordForLoop(tableName, whereCondition, setData):
    updateDB = {
        "$set": setData
    }
    update = mongo.db[tableName].update_one(whereCondition, updateDB)
    if update.modified_count > 0:
        return True
    else:
        return False
def deleteRecordWithOutResponce(tableName, id):
    delete = mongo.db[tableName].delete_one({"_id": ObjectId(id)})
    if (delete.deleted_count > 0):
        return True
    else:
        return False

def deleteRecord(tableName, id):
    delete = mongo.db[tableName].delete_one({"_id": ObjectId(id)})
    if (delete.deleted_count > 0):
        return {"status": "valid", "message": "Deleted successfully"}
    else:
        return {"status": "invalid", "message": "Deleted Failed.Try again..!"}
    
def deleteAllRecords(tableName, whereC={}):
    delete = mongo.db[tableName].delete_many(whereC)
    if (delete.deleted_count > 0):
        return {"status": "valid", "message": "Deleted successfully"}
    else:
        return {"status": "invalid", "message": "Deleted Failed.Try again..!"}
    
 

def getSingleRecord(table_name, id,selectedFields=None):
    items = mongo.db[table_name].find_one({"_id": ObjectId(id)},selectedFields)
    return items
def getSingleRecordJson(table_name, id):
    result = mongo.db[table_name].find_one({"_id": ObjectId(id)})
    if result and '_id' in result:
        result['_id'] = str(result['_id'])
    return json.loads(json_util.dumps(result))

def getSingleRecordWithWhere(table_name, with_where, requiredJson=False,sortDefault=-1):
    items = mongo.db[table_name].find_one(with_where,sort=[('_id', sortDefault )])
    if requiredJson:
        items["_id"] = str(items["_id"])   
        items = json.loads(json_util.dumps(items))
    return items


def getAllRecords(table_name, where={}, requiredSOrt=False, columnName="", typeAsc=-1,selectedFields={}):
    columnName = columnName if columnName else "_id"

    packagesList = mongo.db[table_name].find(where,selectedFields)
    if requiredSOrt:
        packagesList = packagesList.sort(columnName, typeAsc)
  
    packages = [
        {**x, 
        "_id": str(x["_id"]), 
        "sno": index + 1,
        # "created_at_date": convertTimeStampToDate(x["created_at"]),
        } 
        for index, x in enumerate(packagesList)
    ]

    all_packages = list(json.loads(json_util.dumps(packages)))
    return all_packages


def getAllRecordsWithJoins(tableName, listOfJoinData, where={},selectedFields={}, thiredLevelEnable=False, thiredLevelJoinData={}, sortColumn="_id"):
    # listOfJoinData=[{"from":"packages_categories","localField":"category_id","as":"category","sort_enable":False,"sort_column":"_id""selected_fields":{}}]
    # print(":JITHU",j1)
    # return j1["title"]

    packagesList = mongo.db[tableName].find(where,selectedFields)
    packages = [dict(x, _id=str(x['_id'])) for x in packagesList]
    # adding the id here
    for index, x in enumerate(packages):
        if x is not None:
            x.update({"id": index + 1})
            # Join array start from here
            if listOfJoinData is not None:
                for joinTable in listOfJoinData:
                    if joinTable["type"] == "multiple_records":
                        res = getAllRecords(joinTable["from"], {
                                            joinTable["localField"]: (x["_id"])})
                        if res is not None:
                            for sub in res: 
                                if sub is not None:
                                    if thiredLevelEnable: 
                                        if thiredLevelJoinData is not None:
                                            thiredLevl = getAllRecords(thiredLevelJoinData["from"],
                                                                    {thiredLevelJoinData["localField"]: str(
                                                                        sub["_id"])},
                                                                        thiredLevelJoinData["required_sort"],
                                                                        thiredLevelJoinData["sort_column"],
                                                                        thiredLevelJoinData["sort_asc_desc"],
                                                                    )
                                            if thiredLevl is not None:
                                                sub.update(
                                                    {thiredLevelJoinData["as"]: thiredLevl})
                            x.update({joinTable["as"]: res})
                    else:
                        res = getSingleRecord(
                            joinTable["from"], (x[joinTable["localField"]]),{})
                        # query = str(res._CommandCursor__query)
                        # print(joinTable["from"], x[joinTable["localField"]])
                        # print(res)
                        if res is not None:
                            x.update({joinTable["as"]: res})

    all_packages = list(json.loads(json_util.dumps(packages)))
    return all_packages


def getAllRecordsWithJoinsCustomised(tableName, listOfJoinData, where={},selectedFields={}, thiredLevelEnable=False, thiredLevelJoinData={}, sortColumn="_id"):
    # listOfJoinData=[{"from":"packages_categories","localField":"category_id","as":"category","sort_enable":False,"sort_column":"_id""selected_fields":{}}]
    # print(":JITHU",j1)
    # return j1["title"]

    packagesList = mongo.db[tableName].find(where,selectedFields)
    packages = [dict(x, _id=str(x['_id'])) for x in packagesList]
    # adding the id here
    for index, x in enumerate(packages):
        if x is not None:
            x.update({"id": index + 1})
            # Join array start from here
            if listOfJoinData is not None:
                for joinTable in listOfJoinData:
                    if joinTable["type"] == "multiple_records":
                        res = getAllRecords(joinTable["from"], 
                                            {joinTable["localField"]:ObjectId(x["_id"])},
                                            joinTable['sort_enable'],
                                            joinTable['sort_column'],
                                            -1,
                                            joinTable['selected_fields']
                                            )
                        # return joinTable,res
                        if res is not None:
                            for sub in res: 
                                if sub is not None:
                                    if thiredLevelEnable: 
                                        if thiredLevelJoinData is not None:
                                            thiredLevl = getAllRecords(thiredLevelJoinData["from"],
                                                                    {thiredLevelJoinData["localField"]: str(
                                                                        sub["_id"])},
                                                                        thiredLevelJoinData["required_sort"],
                                                                        thiredLevelJoinData["sort_column"],
                                                                        thiredLevelJoinData["sort_asc_desc"],
                                                                    )
                                            if thiredLevl is not None:
                                                sub.update(
                                                    {thiredLevelJoinData["as"]: thiredLevl})
                            x.update({joinTable["as"]: res})
                    else:
                        res = getSingleRecord(
                            joinTable["from"], (x[joinTable["localField"]]),joinTable["selected_fields"],)
                        # query = str(res._CommandCursor__query)
                        # print(joinTable["from"], x[joinTable["localField"]])
                        # print(res)
                        if res is not None:
                            x.update({joinTable["as"]: res})

    all_packages = list(json.loads(json_util.dumps(packages)))
    return all_packages


def getAllRecordsWithJoinsPagination(tableName, listOfJoinData, where={},selectedFields={}, thiredLevelEnable=False, thiredLevelJoinData={}, sortColumn="_id",page = 1,per_page=2):
    # listOfJoinData=[{"from":"packages_categories","localField":"category_id","as":"category","sort_enable":False,"sort_column":"_id""selected_fields":{}}]
    # print(":JITHU",j1)
    # return j1["title"]
    # ,page,per_page
    skip = (page - 1) * per_page
    packagesList = mongo.db[tableName].find(where,selectedFields).skip(skip).limit(per_page)
    packages = [dict(x, _id=str(x['_id'])) for x in packagesList]
    # adding the id here
    for index, x in enumerate(packages):
        if x is not None:
            x.update({"id": index + 1})
            # Join array start from here
            if listOfJoinData is not None:
                for joinTable in listOfJoinData:
                    if joinTable["type"] == "multiple_records":
                        res = getAllRecords(joinTable["from"], 
                                            {joinTable["localField"]:ObjectId(x["_id"])},
                                            joinTable['sort_enable'],
                                            joinTable['sort_column'],
                                            -1,
                                            joinTable['selected_fields']
                                            )
                        # return joinTable,res
                        if res is not None:
                            for sub in res: 
                                if sub is not None:
                                    if thiredLevelEnable: 
                                        if thiredLevelJoinData is not None:
                                            thiredLevl = getAllRecords(thiredLevelJoinData["from"],
                                                                    {thiredLevelJoinData["localField"]: str(
                                                                        sub["_id"])},
                                                                        thiredLevelJoinData["required_sort"],
                                                                        thiredLevelJoinData["sort_column"],
                                                                        thiredLevelJoinData["sort_asc_desc"],
                                                                    )
                                            if thiredLevl is not None:
                                                sub.update(
                                                    {thiredLevelJoinData["as"]: thiredLevl})
                            x.update({joinTable["as"]: res})
                    else:
                        res = getSingleRecord(
                            joinTable["from"], (x[joinTable["localField"]]),joinTable["selected_fields"],)
                        # query = str(res._CommandCursor__query)
                        # print(joinTable["from"], x[joinTable["localField"]])
                        # print(res)
                        if res is not None:
                            x.update({joinTable["as"]: res})
    total_items = mongo.db[tableName].count_documents(where)
    total_pages = (total_items + per_page - 1) // per_page
    all_packages = list(json.loads(json_util.dumps(packages)))
    return ({
        'list': all_packages,
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'total_pages': total_pages
    })


def getPrivilegesDataWithAccessRights(table_name, role_id, list_of_join_data, where=None, theredLevelEnable=None):
    if where is None:
        where = {}
    packagesList = mongo.db[table_name].find(where)
    packages = [dict(x, _id=str(x['_id'])) for x in packagesList]
    # adding the id here
    for index, x in enumerate(packages):
        if x is not None:
            x.update({"id": index + 1})
            x.update({"access_rights": get_access_rights(x["_id"], role_id)})
            # Join array start from here
            if list_of_join_data is not None:
                for joinTable in list_of_join_data:
                    if joinTable["type"] == "multiple_records":
                        res = getAllRecords(joinTable["from"], {
                                            joinTable["localField"]: str(x["_id"])})
                        if res is not None:
                            for sub in res:
                                if sub is not None:
                                    sub.update(
                                        {"access_rights": get_access_rights(sub["_id"], role_id)})
                            x.update({joinTable["as"]: res})
                    else:
                        res = getSingleRecord(
                            joinTable["from"], (x[joinTable["localField"]]))
                        # query = str(res._CommandCursor__query)
                        print(joinTable["from"], x[joinTable["localField"]])
                        print(res)
                        if res is not None:
                            x.update({joinTable["as"]: res})

    all_packages = list(json.loads(json_util.dumps(packages)))
    return all_packages


def getPagenation(table,where={},selectedFields={},page=1,per_page=10):
    
    skip = page - 1 * per_page
    items = list(mongo.db[table].find(where,selectedFields,sort=[('_id', -1 )]).skip(skip).limit(per_page))
    
    for item in items:
        item['_id'] = str(item['_id'])
    
    total_items = mongo.db[table].count_documents(where)
    total_pages = (total_items + per_page - 1) // per_page
    items  = list(json.loads(json_util.dumps(items)))
    return ({
        'items': items,
        'page': page,
        'per_page': per_page,
        'total_items': total_items,
        'total_pages': total_pages
    })

def get_access_rights(module_id, role_id):
    check_access_rights = getSingleRecordWithWhere(
        "role_wise_access_rights", {"module_id": module_id, "role_id": role_id})
    if check_access_rights:
        check_access_rights = check_access_rights
    else:
        check_access_rights = {
            "role_id": role_id,
            "module_id": module_id,
            "view_permission": 0,
            "add_permission": 0,
            "edit_permission": 0,
            "delete_permission": 0,
            "all_permission": 0,
        }
    return check_access_rights
