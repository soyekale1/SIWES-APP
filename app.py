from flask import Flask, request, jsonify
import boto3
import uuid
from boto3.dynamodb.conditions import Key

app = Flask(__name__)

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('siwes_logs')


# POST: Save log
@app.route("/submit-log", methods=["POST"])
def submit_log():
    data = request.get_json()

    log_entry = {
        "log_id": str(uuid.uuid4()),
        "student_id": data.get("student_id"),
        "date": data.get("date"),
        "work_done": data.get("work_done")
    }

    table.put_item(Item=log_entry)

    return jsonify({
        "message": "Log submitted",
        "data": log_entry
    }), 201


# GET: Get logs for a student
@app.route("/logs/<student_id>", methods=["GET"])
def get_logs(student_id):
    response = table.query(
        KeyConditionExpression=Key('student_id').eq(student_id)
    )

    return jsonify(response["Items"])


# GET: Get all logs
@app.route("/all", methods=["GET"])
def get_all():
    response = table.scan()
    return jsonify(response["Items"])


# Home route
@app.route("/")
def home():
    return "SIWES Log API is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)