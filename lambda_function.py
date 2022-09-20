# import the JSON utility package since we will be working with a JSON object
import json
import sys
import os
import logging
import pymysql

host="mm-xpand1.mdb0001358.db.skysql.net"
port="5002"
user="DB00006940"
password="Admin777!"
database="patientDB"

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host='mm-xpand1.mdb0001358.db.skysql.net', port=5002, user='DB00006940',
                           passwd="Admin777!", db='patientDB', ssl={'ca':'/opt/python/skysql_chainXpand.pem'}, connect_timeout=10)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

# define the handler function that the Lambda service will use an entry point
def lambda_handler(event, context):
    
    # extract values from the event object we got from the Lambda service
    
    accountID = event['accountID']
    ipAddress = event['ipAddress']
    hardwareAddress = event['hardwareAddress']
    serialNumber = event['serialNumber']
    info = event['info']
    lastReported = event['lastReported']
    lastInfo = event['lastInfo']
    online = event['online']
    

    sqlString = """insert into heartMonitors (account_id , ip_address, hardware_address,serial_number, info, last_reported, last_info, online) VALUES (%s, %s, %s, %s, %s,%s,%s, %s );"""


    with conn.cursor() as cur:
        #cur.execute(sqlString)
        cur.execute(sqlString,(accountID,ipAddress,hardwareAddress, serialNumber, json.dumps(info), lastReported, lastInfo, online ))
        res1 = cur.fetchone()
        conn.commit()
    
# return a properly formatted JSON object
    return {
        
        'statusCode': 200,
        'body': json.dumps('A new record has been inserted')
    }