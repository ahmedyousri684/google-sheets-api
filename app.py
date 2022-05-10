from flask import Flask, redirect, url_for, request, jsonify
from work_sheet import turn_on_tracking, get_status
app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def work_sheet():
    if request.method == 'POST':
        phone = request.args.get('phone')
        psid = request.args.get('psid')
        print("DATA",phone,psid)
        if phone and psid != None:
            api_resp = turn_on_tracking(phone, psid)
            if api_resp == "Notification is turned on":
                resp = jsonify({'message': api_resp})
                resp.status_code = 201
            else:
                resp = jsonify({'message': api_resp})
                resp.status_code = 404
            return resp
        else:
            resp = jsonify({'message': 'No order '})
            resp.status_code = 405
            return resp
    elif request.method == 'GET':
        phone = request.args.get('phone')
        api_resp = get_status(phone)
        print(api_resp,"heree")
        if phone:
            if api_resp == "Ready to be deleiverd":
                resp = jsonify({'Status':api_resp })
                resp.status_code = 200
                return resp
            elif api_resp == "Not found":
                resp = jsonify({'message': 'Not found'})
                resp.status_code = 404
                return resp
            else:
                resp = jsonify({'Status':api_resp[0] })
                resp.status_code = 200
                return resp
        else:
            resp = jsonify({'message': 'Bad request'})
            resp.status_code = 405
            return resp

if __name__ == '__main__':
    app.run()

