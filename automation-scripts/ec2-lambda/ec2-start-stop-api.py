import json
import os
import boto3


def lambda_handler(event, context):
    # print('--- Event ---')
    # print(event)
    # print('--- Context ---')
    # print(context)

    apiKey = event["headers"].get("x-api-key", None)
    if apiKey is None:
        return {"statusCode": 403, "body": json.dumps({"message": "Unauthorized"})}
    # get api key from the environment variable
    expectedApiKey = os.environ["API_KEY"]

    if apiKey != expectedApiKey:
        return {"statusCode": 403, "body": json.dumps({"message": "Unauthorized"})}

    body = json.loads(event["body"])
    action = body["action"]
    instanceId = body["instanceId"]

    print("Action:", action)
    print("InstanceId:", instanceId)

    allowedInstanceIds = os.environ["INSTANCE_IDS"].split(",")
    print("Allowed Instance Ids:", allowedInstanceIds)

    if instanceId not in allowedInstanceIds:
        return {
            "statusCode": 403,
            "body": json.dumps({"message": "Provided id is not allowed"}),
        }

    region = os.environ["REGION"]
    ec2 = boto3.client("ec2", region_name=region)

    if action == "stop":
        print("Stopping instance:", instanceId)
        ec2.stop_instances(InstanceIds=[instanceId])

    elif action == "start":
        print("Starting instance:", instanceId)
        ec2.start_instances(InstanceIds=[instanceId])

    else:
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid action"})}

    return {"statusCode": 200, "body": json.dumps({"message": "Request Completed Successfully!"})}
