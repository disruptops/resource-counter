# resource-counter
This command line tool counts the number of resources in different categories across Amazon regions.

This is a simple Python app that will count resources across different regions and display them on the command line. It first shows the dictionary of the results for the monitored services on a per-region basis, then it shows totals across all regions in a friendlier format. It tries to use the most-efficient query mechanism for each resource in order to manage the impact of API activity. I wrote this to help me scope out assessments and know where resources are in a target account.

The development plan is to upgrade the output (probably to CSV file) and to continue to add services. If you have a specific service you want to see added just add a request in the comments.

The current list incluides:

* Application and Network Load Balancers
* Autoscale Groups
* Classic Load Balancers
* CloudTrail Trails
* Cloudwatch Rules
* Config Rules
* Dynamo Tables
* Elastic IP Addresses
* Glacier Vaults
* IAM Groups
* Images
* Instances
* KMS Keys
* Lambda Functions
* Launch Configurations
* NAT Gateways
* Network ACLs
* IAM Policies
* RDS Instances
* IAM Roles
* S3 Buckets
* SAML Providers
* SNS Topics
* Security Groups
* Snapshots 
* Subnets
* IAM Users
* VPC Endpoints
* VPC Peering Connection
* VPCs
* Volumes

## Usage:

To install just copy it where you want it and instally the requirements:

	pip install -r ./requirements.txt

This was written in Python 3.6.

To run:

	python count_resources.py 

By default, it will use whatever AWS credentials are alerady configued on the system. You can also specify an access key/secret at runtime and this is not stored. It only neeeds read permissions for the listed services- I use the ReadOnlyAccess managed policy, but you should also be able to use the SecurityAudit policy.

	Usage: count_resources.py [OPTIONS]

	Options:
	  --access TEXT   AWS Access Key. Otherwise will use the standard credentials
                  path for the AWS CLI.
	  --secret TEXT   AWS Secret Key
	  --profile TEXT  If you have multiple credential profiles, use this option to
                  specify one.
	  --help          Show this message and exit.

## Sample Output:

Establishing AWS session using the profile- dev
Current account ID: xxxxxxxxxx
Counting resources across regions. This will take a few minutes...
 
Resources by region
{'ap-northeast-1': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'ap-northeast-2': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 2, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'ap-south-1': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 2, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'ap-southeast-1': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'ap-southeast-2': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'ca-central-1': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 2, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'eu-central-1': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'eu-west-1': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'eu-west-2': {'instances': 3, 'volumes': 3, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'eu-west-3': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'sa-east-1': {'instances': 0, 'volumes': 0, 'security_groups': 1, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'us-east-1': {'instances': 2, 'volumes': 2, 'security_groups': 19, 'snapshots': 0, 'images': 0, 'vpcs': 2, 'subnets': 3, 'peering connections': 0, 'network ACLs': 2, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 1, 'cloudtrail trails': 2, 'sns topics': 3, 'kms keys': 5, 'dynamo tables': 0, 'rds instances': 0}, 'us-east-2': {'instances': 0, 'volumes': 0, 'security_groups': 2, 'snapshots': 0, 'images': 0, 'vpcs': 1, 'subnets': 3, 'peering connections': 0, 'network ACLs': 1, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 0, 'dynamo tables': 0, 'rds instances': 0}, 'us-west-1': {'instances': 1, 'volumes': 3, 'security_groups': 14, 'snapshots': 1, 'images': 0, 'vpcs': 0, 'subnets': 0, 'peering connections': 0, 'network ACLs': 0, 'elastic IPs': 0, 'NAT gateways': 0, 'VPC Endpoints': 0, 'autoscale groups': 0, 'launch configurations': 0, 'classic load balancers': 0, 'application and network load balancers': 0, 'lambdas': 0, 'glacier vaults': 0, 'cloudwatch rules': 0, 'config rules': 0, 'cloudtrail trails': 1, 'sns topics': 0, 'kms keys': 1, 'dynamo tables': 0, 'rds instances': 0}, 'us-west-2': {'instances': 9, 'volumes': 29, 'security_groups': 76, 'snapshots': 171, 'images': 104, 'vpcs': 7, 'subnets': 15, 'peering connections': 1, 'network ACLs': 8, 'elastic IPs': 7, 'NAT gateways': 1, 'VPC Endpoints': 0, 'autoscale groups': 1, 'launch configurations': 66, 'classic load balancers': 1, 'application and network load balancers': 2, 'lambdas': 10, 'glacier vaults': 1, 'cloudwatch rules': 8, 'config rules': 1, 'cloudtrail trails': 1, 'sns topics': 6, 'kms keys': 7, 'dynamo tables': 1, 'rds instances': 0}}
 
Resource totals across all regions
Application and Network Load Balancers : 2
Autoscale Groups : 1
Classic Load Balancers : 1
CloudTrail Trails : 16
Cloudwatch Rules : 8
Config Rules : 2
Dynamo Tables : 1
Elastic IP Addresses : 7
Glacier Vaults : 1
Groups : 12
Images : 104
Instances : 15
KMS Keys : 13
Lambda Functions : 10
Launch Configurations : 66
NAT Gateways : 1
Network ACLs : 22
Policies : 15
RDS Instances : 0
Roles : 40
S3 Buckets : 31
SAML Providers : 1
SNS Topics : 9
Security Groups : 122
Snapshots : 172
Subnets : 51
Users : 14
VPC Endpoints : 0
VPC Peering Connections : 1
VPCs : 21
Volumes : 37

Total resources: 796

