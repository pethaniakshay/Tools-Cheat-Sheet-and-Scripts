import json
import os
import boto3
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

autoscaling = boto3.client('autoscaling')

def lambda_handler(event, context):
    """
    Updates an AWS Auto Scaling Group (ASG) to use a specified Launch Template
    version and initiates an instance refresh.

    This function is designed to be triggered by an AWS Lambda event.
    It reads the ASG name, Launch Template ID, and optionally the Launch
    Template version from environment variables.

    Args:
        event (dict): The event dictionary passed by AWS Lambda.
                    Contains event-specific information.
        context (object): The context object passed by AWS Lambda.
                    Contains runtime information (e.g., request ID,
                    log group name).

    Environment Variables:
        ASG_NAME (str): The name of the Auto Scaling Group to update.
        LAUNCH_TEMPLATE_ID (str): The ID of the Launch Template to use.
        LAUNCH_TEMPLATE_VERSION (str, optional): The version of the Launch
                                                Template to use. Defaults to '$Latest'.

    Returns:
        dict: A dictionary containing the HTTP status code and a JSON-formatted
            body. Possible status codes:
                - 200: Success. ASG updated and instance refresh started.
                - 400: Bad Request. Missing required environment variables.
                - 409: Conflict. Resource contention error (e.g., another operation
                    in progress).
                - 500: Internal Server Error. Service-linked role failure or other
                    unexpected error.

    Raises:
        ResourceContentionFault: If there is contention with another operation on the ASG.
        ServiceLinkedRoleFailure: If there is an issue with the service-linked role permissions.
        Exception: For any other unexpected errors during execution.
    """
    logger.info('--- Event ---')
    logger.info(event)
    logger.info('--- Context ---')
    logger.info(context)

    # Get environment variables
    asg_name = os.environ.get('ASG_NAME')
    launch_template_id = os.environ.get('LAUNCH_TEMPLATE_ID')
    launch_template_version = os.environ.get('LAUNCH_TEMPLATE_VERSION', '$Latest') # Default to $Latest if not specified

    if not asg_name or not launch_template_id:
        logger.error("Missing required environment variables: ASG_NAME and/or LAUNCH_TEMPLATE_ID")
        return {
            'statusCode': 400,
            'body': json.dumps('Missing required environment variables: ASG_NAME and/or LAUNCH_TEMPLATE_ID')
        }

    logger.info(f"Updating Auto Scaling Group '{asg_name}' with Launch Template ID '{launch_template_id}' version '{launch_template_version}'")

    try:
        # Update the Auto Scaling Group's Launch Template
        response_update = autoscaling.update_auto_scaling_group(
            AutoScalingGroupName=asg_name,
            LaunchTemplate={
                'LaunchTemplateId': launch_template_id,
                'Version': launch_template_version
            }
        )
        logger.info(f"Successfully updated Auto Scaling Group: {response_update}")

        # Start Instance Refresh
        logger.info(f"Starting Instance Refresh for Auto Scaling Group '{asg_name}'")
        response_refresh = autoscaling.start_instance_refresh(
            AutoScalingGroupName=asg_name,
            DesiredConfiguration={
                'LaunchTemplate': {
                    'LaunchTemplateId': launch_template_id,
                    'Version': launch_template_version
                }
            },
            Preferences={
                'MinHealthyPercentage': 100,
                'MaxHealthyPercentage': 110,
                'InstanceWarmup': 15
            }
        )
        logger.info(f"Successfully started Instance Refresh: {response_refresh}")

        return {
            'statusCode': 200,
            'body': json.dumps(f"Successfully updated ASG '{asg_name}' and started instance refresh.")
        }

    except autoscaling.exceptions.ResourceContentionFault as e:
        logger.error(f"Resource contention error: {e}. Another operation might be in progress.")
        return {
            'statusCode': 409, # Conflict
            'body': json.dumps(f"Resource contention error: {e}")
        }
    except autoscaling.exceptions.ServiceLinkedRoleFailure as e:
        logger.error(f"Service-linked role failure: {e}. Check IAM permissions.")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Service-linked role failure: {e}")
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"An unexpected error occurred: {e}")
        }
