#!/usr/bin/env python

import sys
import time
from datetime import datetime
from datetime import timedelta 
import socket
import websocket
import hashlib
import base64
import json
import mysql.connector
from mysql.connector import Error
try:
    import thread
except ImportError:
    import _thread as thread


#MariaDB settings. Port = 3306 or 3307
mysqlconfig = {
  'user': 'user',
  'password': 'pass',
  'host': '127.0.0.1',
  'port': '3306',
  'database': 'OBSdb',
  'raise_on_warnings': True
}

try:
	connection = mysql.connector.connect(**mysqlconfig)
	if connection.is_connected():
		db_Info = connection.get_server_info()
		print("Connected to MySQL Server version ", db_Info)
		mycursor = connection.cursor(dictionary=True)
		mycursor.execute("SELECT * FROM host")
		records = mycursor.fetchall()
		for row in records:
			host = row["hostname"]
			port = row["port"]
			password = row["pass"]
except Error as e:
	print("Error while connecting to MySQL", e)
	
try:
	connectionthread = mysql.connector.connect(**mysqlconfig)
	if connectionthread.is_connected():
		db_Info = connectionthread.get_server_info()
		print("Thread connected to MySQL Server version ", db_Info)
except Error as e:
	print("Error while connecting to MySQL", e)


StudioMode = False
obsconnected = False
exporttime = [0,1000,2000,3000,4000,5000]  # every hour at mmss. 100 = 1 minute after each hour, 1500 = 15 minutes after each hour.
#[0,1000,2000,3000,4000,5000] = export every 10 minutes
GetAuthRequired = {"request-type" : "GetAuthRequired" ,"message-id" : "1"};
GetStudioModeStatus = {"request-type" : "GetStudioModeStatus" , "message-id" : "GetStudioModeStatus"}
GetSceneList = {"request-type" : "GetSceneList" , "message-id" : "getSceneList"}
GetSourcesList = {"request-type" : "GetSourcesList" , "message-id" : "GetSourcesList"}
GetTransitionList = {"request-type": "GetTransitionList","message-id" : "GetTransitionList"}

while True:
	try:
		def on_message(ws, message):
			data = json.loads(message)
			#print (data["message-id"])
			#print (data)
			global obsconnected
			if "error" in data:
				if (data["error"] == "Authentication Failed."):
					print("Authentication Failed.")
					ws.keep_running = False
				else:
					print (data)
			elif "message-id" in data:
				if (data["message-id"] == "GetStudioModeStatus"):
					global StudioMode
					StudioMode = data["studio-mode"]
				elif (data["message-id"] == "getSceneList"):
					if not connection.is_connected():
							connection.reconnect(attempts=5, delay=0)
					mycursor = connection.cursor()
					mycursor.execute("TRUNCATE TABLE scenenames")
					connection.commit()
					mycursor = connection.cursor()
					mycursor.execute("TRUNCATE TABLE sourcenames")
					connection.commit()
					for i in data['scenes']:
						scene = i['name']
						if not connection.is_connected():
							connection.reconnect(attempts=5, delay=0)
						mycursor = connection.cursor()
						qry = "INSERT INTO scenenames(scene) VALUES('" + scene + "')"
						mycursor.execute(qry)
						connection.commit()
						for j in i['sources']:
							sourcename = j['name']
							mycursor = connection.cursor()
							qry = "INSERT INTO sourcenames(scene,source) VALUES('" + scene + "' , '" + sourcename + "')"
							if not connection.is_connected():
								connection.reconnect(attempts=5, delay=0)
							mycursor.execute(qry)
							connection.commit()
				elif (data["message-id"] == "GetTransitionList"):
					if not connection.is_connected():
							connection.reconnect(attempts=5, delay=0)
					mycursor = connection.cursor()
					mycursor.execute("TRUNCATE TABLE transitionnames")
					connection.commit()
					for i in data['transitions']:
						trans_type = i['name']
						if not connection.is_connected():
							connection.reconnect(attempts=5, delay=0)
						mycursor = connection.cursor()
						qry = "INSERT INTO transitionnames(transition) VALUES('" + trans_type + "')"
						mycursor.execute(qry)
						connection.commit()
				elif (data["message-id"] == "SetCurrentTransition"):
					print("SetCurrentTransition")
				elif (data["authRequired"]):
					print("Authentication required")
					secret = base64.b64encode(hashlib.sha256((password + data['salt']).encode('utf-8')).digest())
					auth = base64.b64encode(hashlib.sha256(secret + data['challenge'].encode('utf-8')).digest()).decode('utf-8')
					auth_payload = {"request-type": "Authenticate", "message-id": "2", "auth": auth}
					ws.send(json.dumps(auth_payload))
					obsconnected = True
				else:
					print(data)
					obsconnected = True
			elif "update-type" in message:
				if (data["update-type"] == "StudioModeSwitched"):
					StudioMode = data["new-state"]

		def on_error(ws, error):
			print(error)
			ws.close()

		def on_close(ws):
			print("On Close Connection error.")
			#stop on_open while loop
			global obsconnected
			obsconnected = False
			ws.keep_running = False
			time.sleep(30)

		def on_open(ws):
			def run(*args):
				ws.send(json.dumps(GetAuthRequired))
				time.sleep(2)
				if ws.sock:
					ws.send(json.dumps(GetStudioModeStatus))
					global obsconnected
					weekdays = ("ma","di","wo","do","vr","za","zo") #Dutch
					while obsconnected == True:
						try:
							dayrun = False
							currentdtime = time.strftime("%Y%m%d%H%M%S",time.localtime())
							timenow = time.strftime("%H:%M:%S",time.localtime())
							if not connectionthread.is_connected():
								connectionthread.reconnect(attempts=5, delay=0)
							mycursor = connectionthread.cursor(dictionary=True)
							mycursor.execute("SELECT * FROM scedules Where processed = 0")
							records = mycursor.fetchall()
							print(time.strftime("%H:%M:%S",time.localtime()))
							for row in records:
								id = row["id"]
								swtime = row["swtime"]
								swdate = row["swdate"]
								time_object = datetime.strptime(str(swtime), '%H:%M:%S').time()
								date_object = datetime.strptime(str(swdate), '%Y-%m-%d').date()
								datetime_str = datetime.combine(date_object , time_object)
								dtime = datetime_str.strftime("%Y%m%d%H%M%S")
								scene = row["scene"]
								trans_type = row["transition"]
								sourceoff = row["sourceoff"] #source in this scene to switch off
								sourceon = row["sourceon"] #source in this scene to switch on
								repeattime = row["repeattime"]
								if timenow == datetime_str.strftime("%H:%M:%S"):
									if weekdays[datetime.today().weekday()] in repeattime:
										dayrun = True
								if currentdtime == dtime or dayrun: 
									message={"request-type" : "SetCurrentTransition" , "message-id" : "SetCurrentTransition" ,"transition-name":trans_type};
									ws.send(json.dumps(message))
									message = {"request-type" : "SetCurrentScene" , "message-id" : "SetCurrentScene" , "scene-name" : scene};
									ws.send(json.dumps(message))
									if len(sourceoff) > 0:
										message={"request-type" : "SetSceneItemProperties" , "message-id" : "SetSceneItemProperties" , "scene-name" : scene , "item" : sourceoff , "visible": False };
										ws.send(json.dumps(message))
									if len(sourceon) > 0:
										message={"request-type" : "SetSceneItemProperties" , "message-id" : "SetSceneItemProperties" , "scene-name" : scene , "item" : sourceon , "visible": True };
										ws.send(json.dumps(message))
									if not connectionthread.is_connected():
										connectionthread.reconnect(attempts=5, delay=0)
									mycursor = connectionthread.cursor()
									if len(repeattime) > 0 and not dayrun:
										if "," in repeattime:
											repeattimenew = repeattime.split(',')[0]
											repeattimenumber = repeattime.split(',')[1]
											if repeattimenumber == "0": #continuous
												newdtime = datetime_str + timedelta(minutes=int(repeattimenew))
												new_time_object = datetime.time(newdtime)
												new_date_object = datetime.date(newdtime)
												qry = "UPDATE scedules SET swtime = '" + new_time_object.strftime("%H:%M:%S") + "', swdate ='" + new_date_object.strftime("%Y-%m-%d") + "' WHERE id = " + str(id) + ";"
											elif repeattimenumber == "1": #last run was done
												qry = "UPDATE scedules SET processed = 1 WHERE id = " + str(id) + ";"
											else:
												newdtime = datetime_str + timedelta(minutes=int(repeattimenew))
												repeattime = repeattimenew + "," + str(int(repeattimenumber) - 1)
												new_time_object = datetime.time(newdtime)
												new_date_object = datetime.date(newdtime)
												qry = "UPDATE scedules SET swtime = '" + new_time_object.strftime("%H:%M:%S") + "', swdate = '" + new_date_object.strftime("%Y-%m-%d") + "', repeattime = '" + repeattime + "' WHERE id = " + str(id) + ";"
										else:
											newdtime = datetime_str + timedelta(minutes=int(repeattime))
											new_time_object = datetime.time(newdtime)
											new_date_object = datetime.date(newdtime)
											qry = "UPDATE scedules SET swtime = '" + new_time_object.strftime("%H:%M:%S") + "', swdate ='" + new_date_object.strftime("%Y-%m-%d") + "' WHERE id = " + str(id) + ";"
									else:
										qry = "UPDATE scedules SET processed = 1 WHERE id = " + str(id) + ";"
									if not dayrun:
										mycursor.execute(qry)
										connectionthread.commit()
									print("Transition to: " + scene + " at " + time.strftime("%H:%M:%S",time.localtime()))
							connectionthread.close()
							time.sleep(0.25) #no need 100's loops a second
						except Exception:
							print("connectionthread error")
							connectionthread.close()
							time.sleep(10)
						timenow = int(time.strftime("%M%S",time.localtime()))
						if timenow in exporttime:
							print("export scenes")
							ws.send(json.dumps(GetSceneList))
							Updatescenes = False
							time.sleep(0.25)
						if timenow - 10 in exporttime:
							print("export transitions")
							ws.send(json.dumps(GetTransitionList))
							time.sleep(0.25)
			thread.start_new_thread(run, ())

		if __name__ == "__main__":
			#websocket.enableTrace(True)
			ws = websocket.WebSocketApp("ws://{}:{}".format(host, port),on_message = on_message,on_error = on_error,on_close = on_close)
			ws.on_open = on_open
			ws.run_forever()

	except Exception:
		print("Exception Connection error")
		time.sleep(10)





