import json
import os
import boto3

autoscaling = boto3.client('autoscaling')

def lambda_handler(event, context):
    print('--- Event ---')
    print(event)
    print('--- Context ---')
    print(context)

    asg_name = os.environ.get('ASG_NAME')
    min_instances_str = os.environ.get('MIN_INSTANCES')

    if not asg_name or not min_instances_str:
        print("Error: ASG_NAME or MIN_INSTANCES environment variable not set.")
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required environment variables: ASG_NAME, MIN_INSTANCES')
        }

    try:
        min_instances = int(min_instances_str)
    except ValueError:
        print(f"Error: Invalid value for MIN_INSTANCES: {min_instances_str}. Must be an integer.")
        return {
            'statusCode': 400,
            'body': json.dumps(f'Invalid MIN_INSTANCES value: {min_instances_str}')
        }

    try:
        print(f"Updating Auto Scaling Group: {asg_name} - Setting MinSize and DesiredCapacity to {min_instances}")
        response = autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=min_instances,
            DesiredCapacity=min_instances
        )
        print("--- Boto3 Response ---")
        print(response)
        print(f"Successfully updated ASG {asg_name}.")
        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully updated ASG {asg_name} MinSize and DesiredCapacity to {min_instances}')
        }
    except Exception as e:
        print(f"Error updating Auto Scaling Group {asg_name}: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error updating ASG {asg_name}: {str(e)}')
        }
