#!/bin/bash

# Configuration variables
LOG_SOURCE_DIR="/home/ubuntu/mera-satsang-api/Logs"
S3_BUCKET_NAME="baps-parivar-prod-app-logs"
S3_PATH_PREFIX="main-app/logs"

# Get EC2 instance ID
# Using IMDSv2 token-based method which works with both IMDSv1 and IMDSv2
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600") 2>/dev/null
if [ -n "$TOKEN" ]; then
    # IMDSv2 method (token available)
    EC2_INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id) 2>/dev/null
else
    # Fallback to IMDSv1 method (token not available)
    EC2_INSTANCE_ID=$(curl -s http://169.254.169.254/latest/meta-data/instance-id) 2>/dev/null
fi

if [ -z "$EC2_INSTANCE_ID" ]; then
    # Fallback in case instance metadata is not available
    EC2_INSTANCE_ID="unknown-instance"
    log_message "WARNING: Could not retrieve EC2 instance ID, using '$EC2_INSTANCE_ID' instead"
fi

# VPC Endpoint configuration
USE_VPC_ENDPOINT=true

# For S3 interface endpoint (most common for EC2 instances in private subnets)
VPC_ENDPOINT_URL="https://s3.ap-south-1.amazonaws.com"

# Log file for this script
SCRIPT_LOG="/var/log/log-backup.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$SCRIPT_LOG"
}

# Create log file if it doesn't exist
touch "$SCRIPT_LOG"

log_message "Starting log backup process"

# Check if source directory exists
if [ ! -d "$LOG_SOURCE_DIR" ]; then
    log_message "ERROR: Source directory $LOG_SOURCE_DIR does not exist. Exiting."
    exit 1
fi

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    log_message "ERROR: AWS CLI is not installed. Please install it first."
    exit 1
fi

# Create a timestamp for the current backup
TIMESTAMP=$(date '+%Y%m%d-%H%M%S')
log_message "Using timestamp: $TIMESTAMP"
log_message "EC2 Instance ID: $EC2_INSTANCE_ID"

# Sync logs to S3
log_message "Syncing logs from $LOG_SOURCE_DIR to s3://$S3_BUCKET_NAME/$S3_PATH_PREFIX/$EC2_INSTANCE_ID/"

if [ "$USE_VPC_ENDPOINT" = true ]; then
    log_message "Using VPC endpoint for S3 access"
    aws s3 sync "$LOG_SOURCE_DIR" "s3://$S3_BUCKET_NAME/$S3_PATH_PREFIX/$EC2_INSTANCE_ID/" \
        --storage-class STANDARD_IA \
        --no-progress \
        --endpoint-url "$VPC_ENDPOINT_URL"
else
    aws s3 sync "$LOG_SOURCE_DIR" "s3://$S3_BUCKET_NAME/$S3_PATH_PREFIX/$EC2_INSTANCE_ID/" \
        --storage-class STANDARD_IA \
        --no-progress
fi

# Check if sync was successful
if [ $? -eq 0 ]; then
    log_message "Log backup completed successfully"
else
    log_message "ERROR: Log backup failed"
    exit 1
fi

log_message "Log backup process completed"
exit 0