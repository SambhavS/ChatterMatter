from flask import Flask, render_template, request
import pickle
import json
app = Flask(__name__)
######
#Pickling helpers
def serialize(obj, path):
	with open(path, "wb") as pfile:
		pickle.dump(obj, pfile)
 
def deserialize(path):
	try:
		with open(path, "rb") as pfile:
			return pickle.load(pfile)
	except:
		serialize({"messages":[]},path)
		return deserialize(path)
#####	

@app.route('/<session>')
def hello_world(session):
	return render_template("each.html", number=str(session))

@app.route('/int/<session>', methods=["GET","POST"])
def add(session):
	path = "pickles/" + str(session)
	info = deserialize(path)
	messages = info["messages"]
	others_update = request.form.getlist('others[]')[0]
	if others_update == "false":
		user_info = request.form.getlist('wordlist[]')
		new_message = user_info[0]
		if new_message != "":
			messages.append(new_message)
		if len(messages) > 10:
			messages.pop(0)
		serialize(info, path)
	return json.JSONEncoder().encode(messages)





if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

