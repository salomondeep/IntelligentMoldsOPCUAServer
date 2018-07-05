from flask import Flask, jsonify, make_response, request
import json
import jwt
import datetime
from opcua import Server
from random import randint

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AliceinWonderland'

server = Server()
url = "opc.tcp://192.168.137.250:4840"
server.set_endpoint(url)
name = "OPCUA_SIMULATION_SERVER"
addspace = server.register_namespace(name)

node = server.get_objects_node()

Param = node.add_object(addspace, "Parameters")

TaskID = Param.add_variable(addspace, "PieceTaskID", 0)
NodeID = Param.add_variable(addspace, "NodeID", 0)
Name = Param.add_variable(addspace, "DisplayName", 0)
Val = Param.add_variable(addspace, "Value", 0)
OPCString = Param.add_variable(addspace, "OPCString", 0)

TaskID.set_writable()
NodeID.set_writable()
Name.set_writable()
Val.set_writable()
OPCString.set_writable()

server.start()

@app.route("/api/opcdata", methods=['POST'])
def hello():
	data = request.json
	#print(data["PieceTaskID"])
	#print(data["NodeID"])
	#print(data["DisplayName"])
	#print(data["Value"])
	#TaskID.set_value(data["PieceTaskID"])
	#NodeID.set_value(data["NodeID"])
	#Name.set_value(data["DisplayName"])
	#Val.set_value(data["Value"])
	print(data)
	#teste = {teste: 123, value: 1738}"
	OPCString.set_value(json.dumps(data))
	return "OK"


@app.route('/protected')
def protected():
    return ''

@app.route('/login')
def login():
	auth = request.authorization
	if auth and auth.password == 'password':
		token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
		return jsonify({'token': token.decode('UTF-8')})
	return make_response('Could verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

if __name__ == '__main__':
	app.run(debug=False, host='0.0.0.0')
