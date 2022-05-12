from flask import Flask, redirect, url_for, request, jsonify
from work_sheet import turn_on_tracking, get_status, get_phone_by_psid
app = Flask(__name__)


@app.route('/', methods=['POST','GET'])
def work_sheet():
    if request.method == 'POST':
        phone = request.args.get('phone')
        psid = request.args.get('psid')
        if phone and psid != None:
            api_resp = turn_on_tracking(phone, psid)
            if api_resp == "Notification is turned on":
                resp = jsonify({'message': api_resp})
                resp.status_code = 201
                
            else:
                resp = jsonify({'message': api_resp})
                resp.status_code = 200
            return resp
        else:
            resp = jsonify({'message': 'No order '})
            resp.status_code = 404
            return resp
    elif request.method == 'GET':
        phone = request.args.get('phone')
        api_resp = get_status(phone)
        if phone:
            if api_resp == "Ready to be deleiverd":
                resp = jsonify({'message':api_resp })
                resp.status_code = 200
                return resp
            elif api_resp == "Not found":
                resp = jsonify({'message': 'Not found'})
                resp.status_code = 404
                return resp
            else:
                resp = jsonify({'message':api_resp[0] })
                resp.status_code = 200
                return resp
        else:
            resp = jsonify({'message': 'Bad request'})
            resp.status_code = 405
            return resp

@app.route('/status-by-psid', methods=['GET'])
def get_status_psid():
    if request.method == 'GET':
        psid = request.args.get('psid')
        phone = get_phone_by_psid(psid)
        api_resp = get_status(phone)
        if psid:
            if api_resp == "Ready to be deleiverd":
                resp = jsonify({'message':api_resp })
                resp.status_code = 200
                return resp
            elif api_resp == "Not found":
                resp = jsonify({'message': 'Not found'})
                resp.status_code = 404
                return resp
            else:
                resp = jsonify({'message':api_resp[0] })
                resp.status_code = 200
                return resp
        else:
            resp = jsonify({'message': 'Bad request'})
            resp.status_code = 405
            return resp
if __name__ == '__main__':
    app.run()

