from flask                          import Flask,request,Response
from redis                          import StrictRedis
import json
import os

app = Flask(__name__)
r = StrictRedis(host="redis")
MESSAGEQUEUE = "queue-webhook"
ERRORQUEUE   = "queue-error"
PRODUCERTOKEN = os.environ['PRODUCERTOKEN']
CONSUMERTOKEN = os.environ['CONSUMERTOKEN']

@app.route('/', methods=['GET','POST'])
def default():
    return Response(json.dumps({"message" : "Invalid path. This service is a queue for webhook."}), 403 , mimetype='application/json')

@app.route('/status', methods=['GET','POST'])
def status():
    return Response(json.dumps({"message" : "Webhook queue is up and running."}), 200 , mimetype='application/json')

@app.route('/webhook-producer', methods=['GET','POST'])
def producer():
    if request.method == 'POST':
        if request.args.get('PRODUCERTOKEN') is None:
            return Response(json.dumps({"message" : "Please provide producer auth token"}), 401 , mimetype='application/json')

        if request.args.get('PRODUCERTOKEN') != PRODUCERTOKEN:
            return Response(json.dumps({"message" : "Invalid producer auth token"}), 401 , mimetype='application/json')

        payload = request.get_json()
        r.rpush(MESSAGEQUEUE, json.dumps(payload))
        return Response(json.dumps({"message" : "Message added to queue"}), 200 , mimetype='application/json')
    else:
        return Response(json.dumps({"message" : "This is a webhook receiver only."}), 403 , mimetype='application/json')

@app.route('/webhook-consumer', methods=['GET','POST'])
def consumer():
    if request.method == 'POST':
        if request.args.get('CONSUMERTOKEN') is None:
            return Response(json.dumps({"message" : "Please provide consumer auth token"}), 401 , mimetype='application/json')

        if request.args.get('CONSUMERTOKEN') != CONSUMERTOKEN:
            return Response(json.dumps({"message" : "Invalid consumer auth token"}), 401 , mimetype='application/json')

        payload = request.get_json()
        len = r.llen(MESSAGEQUEUE)
        resp = []
        while( len > 0 ):
            resp.append( json.loads(r.lpop(MESSAGEQUEUE)) )
            len = len -1;
        return Response(json.dumps({"result" : resp}), 200 , mimetype='application/json')

    else:
        return Response(json.dumps({"message" : "This is a webhook consumer only."}), 403 , mimetype='application/json')

@app.route('/webhook-error', methods=['GET','POST'])
def sserrors():
    if request.method == 'POST':
        if request.args.get('CONSUMERTOKEN') is None:
            return Response(json.dumps({"message" : "Please provide consumer auth token"}), 401 , mimetype='application/json')

        if request.args.get('CONSUMERTOKEN') != CONSUMERTOKEN:
            return Response(json.dumps({"message" : "Invalid consumer auth token"}), 401 , mimetype='application/json')

        payload = request.get_json()
        r.rpush(ERRORQUEUE, json.dumps(payload))
        return Response(json.dumps({"message" : "Message added to Error queue"}), 200 , mimetype='application/json')
    else:
        return Response(json.dumps({"message" : "This is a webhook error receiver only."}), 403 , mimetype='application/json')

if __name__ == '__main__':
    app.run()
