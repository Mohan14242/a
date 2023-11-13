import boto3

# Replace with your AWS access key and secret key
aws_access_key = 'AKIAURISP2E6QRX54ANJ'
aws_secret_key = 'qSWHjeFTgXxeNcaplrBhnAc7YphQYSsF2FD2pFFE'
aws_region = 'us-east-1'

# Create an EC2 client


# Create an EC2 client
ec2_client = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

# Get all running EC2 instances
response = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

# Extract instance details (name and public IP)
instances = []

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_details = {
            'Name': [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name'][0],
            'PublicIpAddress': instance.get('PublicIpAddress', 'N/A')
        }
        instances.append(instance_details)

# Print and append to file
output_file_path = 'inventory.ini'

with open(output_file_path, 'w') as output_file:
    for instance in instances:
        output_file.write(f"[{instance['Name']}]\nansible_host={instance['PublicIpAddress']} ansible_user=centos ansible_ssh_pass=DevOps321 ansible_private_key=/home/centos/{instance['Name']}/private_key\n")
