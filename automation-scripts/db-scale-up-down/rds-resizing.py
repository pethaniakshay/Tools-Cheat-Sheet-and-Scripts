import json
import os
import time
import boto3

autoscaling = boto3.client('autoscaling')
rds = boto3.client('rds')

def lambda_handler(event, context):
    print('--- Event ---')
    print(event)
    print('--- Context ---')
    print(context)

    asg_name = os.environ.get('ASG_NAME');
    rds_instance_id = os.environ.get('RDS_INSTANCE_ID');
    rds_instance_class = os.environ.get('RDS_INSTANCE_CLASS');


    if not asg_name or not rds_instance_id or not rds_instance_class:
        print("Error: ASG_NAME or RDS_INSTANCE_ID or RDS_INSTANCE_CLASS environment variable not set.")
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required environment variables: ASG_NAME, RDS_INSTANCE_ID, RDS_INSTANCE_CLASS')
        }

    try:
        # Get the current ASG instance counts from the ASG and store in a variable
        response = autoscaling.describe_auto_scaling_groups(
            AutoScalingGroupNames=[asg_name]
        )
        asg_instances = response['AutoScalingGroups'][0]
        min_instances = asg_instances['MinSize']
        max_instances = asg_instances['MaxSize']
        desired_capacity = asg_instances['DesiredCapacity']
        print(f"Current ASG instances: {min_instances}, {max_instances}, {desired_capacity}")

        # # Scale down ASG to 0 instances
        autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=0,
            DesiredCapacity=0,
            MaxSize=0
        )
        print(f"Successfully scaled down ASG {asg_name} to 0 instances.")

        # Pause the execution for 5 seconds
        time.sleep(5)

        # Modify the RDS instance to the new size
        response = rds.modify_db_instance(
            DBInstanceIdentifier=rds_instance_id,
            DBInstanceClass=rds_instance_class,
            ApplyImmediately=True
        )
        print("--- RDS Modify Response ---")
        print(response)

        # Scaleup EC2 to previous max min instances
        autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            MinSize=min_instances,
            DesiredCapacity=min_instances,
            MaxSize=max_instances
        )
        print(f"Successfully scaled up ASG {asg_name} to {min_instances} instances.")

        return {
            'statusCode': 200,
            'body': json.dumps(f'Successfully resized RDS instance {rds_instance_id} to {rds_instance_class}')
        }

    except Exception as e:
        error_message = str(e)
        print(f"Error in RDS resizing operation: {error_message}")

        # Provide more specific error context based on the operation
        if "DBInstance" in error_message or "RDS" in error_message:
            detailed_error = f'Error modifying RDS instance {rds_instance_id}: {error_message}'
        elif "AutoScaling" in error_message or "ASG" in error_message:
            detailed_error = f'Error updating Auto Scaling Group {asg_name}: {error_message}'
        else:
            detailed_error = f'Error in automation script (ASG: {asg_name}, RDS: {rds_instance_id}): {error_message}'

        return {
            'statusCode': 500,
            'body': json.dumps(detailed_error)
        }
