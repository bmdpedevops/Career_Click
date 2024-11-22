import random
import string
import time
from datetime import date, datetime
import re

from bson import ObjectId

# Function to generate a random OTP (One Time Password)
def generate_otp():
    # return random.randrange(1111, 9999)
    return 1234 
def base_url(url=""):
    # return random.randrange(1111, 9999)
    mainUrl = "https://43.204.97.119/" 
    return "{}{}".format(mainUrl,url)


def random_string_digits(stringLength=24):
    """Generate a random string of letters and digits """
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join(random.choice(lettersAndDigits) for i in range(stringLength))


# Function to generate a random string of given length
def get_random_strings(noofString):
    # Use random.choices to generate a random string from uppercase letters, lowercase letters, and digits
    res = ''.join(random.choices(string.ascii_uppercase +
                  string.ascii_lowercase + string.digits, k=noofString))
    return str(res)

def date_to_timestamp(date_str):
    # Parse the date string into a datetime object
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    # Convert the datetime object to a timestamp
    timestamp = dt.timestamp()
    return timestamp

# Function to get the current timestamp
def getTimeStamp():
    # Use time.time() to get the current timestamp (in seconds since the epoch)
    timestamp = int(time.time())
    # print(timestamp)  # Print the timestamp for debugging or logging purposes
    return timestamp

def convertTimeStampToDate(timestamp):
    # timestamp = 1545730073
    dt_obj = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')
    # print("date_time:",dt_obj)
    # print("type of dt:",type(dt_obj))
    return dt_obj
def getTimestampToOnlyDate(timestamp):
    # timestamp = 1545730073
    dt_obj = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y')
    # print("date_time:",dt_obj)
    # print("type of dt:",type(dt_obj))
    return dt_obj

def convert_keys_data(data):
    new_data = {}
    for key, value in data.items():
        new_key = re.sub(r'[^a-zA-Z0-9]', '_', key.lower())
        new_data[new_key] = value
    return new_data

def convert_keys_to_strings(data):
    if isinstance(data, dict):
        return {str(key): convert_keys_to_strings(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_strings(item) for item in data]
    else:
        return data
    
# Check the mongo db has the Object or not 
def is_valid_objectid(object_id_str):
    try:
        ObjectId(object_id_str)
        return True
    except:
        return False
    
def subscription_calc(area):
    cal_val1 =  0.2
    cal_val2 =  0.1
    cal_val3 =  0.05
    condition_a = 150 
    condition_b = (condition_a + (cal_val1 * area) )
    condition_c = condition_a + ( condition_a + 10000 *cal_val1 ) +  (0.1 * area)
    condition_d = condition_a + ( condition_a + 10000 *cal_val1 ) +  ( condition_a+( condition_a + 10000 *cal_val1 ) +  (cal_val2 * 20000) )+  (cal_val3 * area)
    
    if area <= 1000:
        return condition_a
    elif area >  1000 and area <= 10000:
        return condition_b
    elif area >  10000 and area <= 20000:
        return condition_c
    elif area >  20000:
    #   print("Coming D")
        return condition_d
    
