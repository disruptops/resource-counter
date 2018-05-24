import click
import boto3
import sys
resource_counts = {}
resource_totals = {}

@click.command()
@click.option('--access', help='AWS Access Key. Otherwise will use the standard credentials path for the AWS CLI.')
@click.option('--secret', help='AWS Secret Key')
@click.option('--profile', help='If you have multiple credential profiles, use this option to specify one.')
def controller(access, secret, profile):
    global session
    if access:
        click.echo('Access Key specified')
        if not secret:
            click.echo('Secret key not specified. A secret key must be provided when the command line access key option is provided.')
        else:
            click.echo('Establishing AWS session using the provided access key...')
            try:
                session = boto3.session.Session(aws_access_key_id=access, aws_secret_access_key=secret)
            except:
                click.echo('Error establishing AWS connection. Likely bad credentials provided.')
                sys.exit()
    elif profile:
        click.echo('Establishing AWS session using the profile- ' + profile)
        try:
            session = boto3.session.Session(profile_name=profile)
        except:
            click.echo('Error establishing AWS connection. Likely bad credentials provided.')
            sys.exit()
    else:
        click.echo('Establishing AWS session using default path credentials...')
        try:
            session = boto3.session.Session()
        except:
            click.echo('Error establishing AWS connection. Likely bad credentials provided.')
            sys.exit()

    # pull the account ID for use when needed for filtering
    iam = session.client('sts')

    # account_id = iam.CurrentUser().arn.split(':')[4]
    account_id = iam.get_caller_identity()["Account"]
    click.echo('Current account ID: ' + account_id)

    # Initialize dictionary to hold the counts. Pull the regions using EC2, since that is in every region.
    # Then build out the master list of regions to then fill in the service counts
    # Also build a separate dictionary for cross-region totals


    region_list = session.get_available_regions('ec2')
    for region in region_list:
        resource_counts[region] = {}


    # iterate through the various services to build the counts
    click.echo('Counting resources across regions. This will take a few minutes...')
    click.echo(' ')
    ec2_counter(account_id)
    autoscaling_counter()
    balancer_counter()
    s3_counter()
    iam_counter()
    lambda_counter()
    glacier_counter()
    cloudwatch_rules_counter()
    config_counter()
    cloudtrail_counter()
    sns_counter()
    kms_counter()
    dynamo_counter()
    rds_counter()

    # show results
    click.echo('Resources by region')
    click.echo(resource_counts)
    click.echo(' ')
    click.echo('Resource totals across all regions')
    for key, value in sorted(resource_totals.items()):
        click.echo("{} : {}".format(key, value))
    total = sum(resource_totals.values())
    click.echo('')
    click.echo('Total resources: ' + str(total))

# ec2 = boto3.client('ec2', region_name='us-west-2')

# ec2 = session.client('ec2', region_name='us-west-2')


def ec2_counter(account_id):
    # get list of regions supported by EC2 endpoint
    region_list = session.get_available_regions('ec2')

    # initialize cross region totals
    total_instances = 0
    total_groups = 0
    total_volumes = 0
    total_snapshots = 0
    total_images = 0
    total_vpcs = 0
    total_subnets = 0
    total_peering_connections = 0
    total_acls = 0
    total_IPs = 0
    total_NAT = 0
    total_endpoints = 0

    for region in region_list:
        ec2 = session.resource('ec2', region_name=region)
        ec2client = session.client('ec2', region_name=region)

        # build the collections to count
        instance_iterator = ec2.instances.all()
        volume_iterator = ec2.volumes.all()
        security_group_iterator = ec2.security_groups.all()
        snapshot_iterator = ec2.snapshots.filter(OwnerIds=[account_id])
        image_iterator = ec2.images.filter(Owners=[account_id])
        vpc_iterator = ec2.vpcs.all()
        subnet_iterator = ec2.subnets.all()
        vpc_peering_connection_iterator = ec2.vpc_peering_connections.all()
        network_acl_iterator = ec2.network_acls.all()
        vpc_address_iterator = ec2.vpc_addresses.all()
        nat_gateways = ec2client.get_paginator('describe_nat_gateways')
        nat_gateway_iterator = nat_gateways.paginate()
        endpoints = ec2client.describe_vpc_endpoints()


        # count resources
        instance_counter = len(list(instance_iterator))
        group_counter = len(list(security_group_iterator))
        volume_counter = len(list(volume_iterator))
        snapshot_counter = len(list(snapshot_iterator))
        image_counter = len(list(image_iterator))
        vpc_counter = len(list(vpc_iterator))
        subnet_counter = len(list(subnet_iterator))
        peering_counter = len(list(vpc_peering_connection_iterator))
        acl_counter = len(list(network_acl_iterator))
        ip_counter = len(list(vpc_address_iterator))
        gateway_counter = 0
        for gateway in nat_gateway_iterator:
            gateway_counter += len(gateway['NatGateways'])
        endpoint_counter = len(endpoints['VpcEndpoints'])

        # add to the cross region totals
        total_instances = total_instances + instance_counter
        total_groups += group_counter
        total_volumes += volume_counter
        total_snapshots += snapshot_counter
        total_images += image_counter
        total_vpcs += vpc_counter
        total_subnets += subnet_counter
        total_peering_connections += peering_counter
        total_acls += acl_counter
        total_IPs += ip_counter
        total_NAT += gateway_counter
        total_endpoints += endpoint_counter

        # Add the counts to the per-region counter
        resource_counts[region]['instances'] = instance_counter
        resource_counts[region]['volumes'] = volume_counter
        resource_counts[region]['security_groups'] = group_counter
        resource_counts[region]['snapshots'] = snapshot_counter
        resource_counts[region]['images'] = image_counter
        resource_counts[region]['vpcs'] = vpc_counter
        resource_counts[region]['subnets'] = subnet_counter
        resource_counts[region]['peering connections'] = peering_counter
        resource_counts[region]['network ACLs'] = acl_counter
        resource_counts[region]['elastic IPs'] = ip_counter
        resource_counts[region]['NAT gateways'] = gateway_counter
        resource_counts[region]['VPC Endpoints'] = endpoint_counter


    resource_totals['Instances'] = total_instances
    resource_totals['Volumes'] = total_volumes
    resource_totals['Security Groups'] = total_groups
    resource_totals['Snapshots'] = total_snapshots
    resource_totals['Images'] = total_images
    resource_totals['VPCs'] = total_vpcs
    resource_totals['Subnets'] = total_subnets
    resource_totals['VPC Peering Connections'] = total_peering_connections
    resource_totals['Network ACLs'] = total_acls
    resource_totals['Elastic IP Addresses'] = total_IPs
    resource_totals['NAT Gateways'] = total_NAT
    resource_totals['VPC Endpoints'] = total_endpoints

def iam_counter():
    iam = session.resource('iam', region_name='us-west-2')

    user_iterator = iam.users.all()
    group_iterator = iam.groups.all()
    role_iterator = iam.roles.all()
    policy_iterator = iam.policies.filter(Scope='Local')
    saml_provider_iterator = iam.saml_providers.all()

    total_users = len(list(user_iterator))
    total_groups = len(list(group_iterator))
    total_roles = len(list(role_iterator))
    total_policies = len(list(policy_iterator))
    total_saml = len(list(saml_provider_iterator))

    resource_totals['Users'] = total_users
    resource_totals['Groups'] = total_groups
    resource_totals['Roles'] = total_roles
    resource_totals['Policies'] = total_policies
    resource_totals['SAML Providers'] = total_saml

def autoscaling_counter():
    # get list of supported regions
    region_list = session.get_available_regions('autoscaling')

    # initialize cross region totals
    total_autoscaling_groups = 0
    total_launch_configurations = 0

    # iterate through regions and count
    for region in region_list:
        client = session.client('autoscaling', region_name=region)

        # pull data using paginators
        autoscaling = client.get_paginator('describe_auto_scaling_groups')
        configurations = client.get_paginator('describe_launch_configurations')
        autoscale_iterator = autoscaling.paginate()
        configurations_iterator = configurations.paginate()

        # initialize region counts
        autoscale_count = 0
        configuration_count = 0

        for autoscale in autoscale_iterator:
            autoscale_count += len(autoscale['AutoScalingGroups'])
        for configuration in configurations_iterator:
            configuration_count += len(configuration['LaunchConfigurations'])

        total_autoscaling_groups += autoscale_count
        total_launch_configurations += configuration_count


        resource_counts[region]['autoscale groups'] = autoscale_count
        resource_counts[region]['launch configurations'] = configuration_count


    resource_totals['Autoscale Groups'] = total_autoscaling_groups
    resource_totals['Launch Configurations'] = total_launch_configurations

def balancer_counter():
    # get list of supported regions
    elb_region_list = session.get_available_regions('elb')
    elbv2_region_list = session.get_available_regions('elbv2')

    # initalize cross region totals
    elb_total = 0
    elbv2_total = 0

    # First count up the classic ELBs
    for region in elb_region_list:
        elb = session.client('elb', region_name=region)

        # pull data using paginator
        elb_paginator = elb.get_paginator('describe_load_balancers')
        elb_iterator = elb_paginator.paginate()

        #initialize region count
        elb_counter = 0

        for balancer in elb_iterator:
            elb_counter += len(balancer['LoadBalancerDescriptions'])

        elb_total += elb_counter
        resource_counts[region]['classic load balancers'] = elb_counter

    # Now count up the application and network load balancers
    for region in elbv2_region_list:
        elb = session.client('elbv2', region_name=region)

        # pull data using paginator
        elb_paginator = elb.get_paginator('describe_load_balancers')
        elb_iterator = elb_paginator.paginate()

        #initialize region count
        elb_counter = 0

        for balancer in elb_iterator:
            elb_counter += len(balancer['LoadBalancers'])

        elbv2_total += elb_counter
        resource_counts[region]['application and network load balancers'] = elb_counter
    resource_totals['Classic Load Balancers'] = elb_total
    resource_totals['Application and Network Load Balancers'] = elbv2_total

def s3_counter():
    total_buckets = 0
    # S3 gives you a full count no matter what the region setting
    s3 = session.resource('s3', region_name='us-west-2')
    bucket_iterator = s3.buckets.all()
    bucket_counter = len(list(bucket_iterator))
    total_buckets += bucket_counter
    # resource_counts[region]['s3 buckets'] = bucket_counter
    resource_totals['S3 Buckets'] = total_buckets

def lambda_counter():
    region_list = session.get_available_regions('lambda')

    total_functions = 0

    for region in region_list:
        aws_lambda = session.client('lambda', region_name=region)
        function_counter = 0
        function_paginator = aws_lambda.get_paginator('list_functions')
        function_iterator = function_paginator.paginate()
        for function in function_iterator:
            function_counter += len(function['Functions'])
        total_functions += function_counter
        resource_counts[region]['lambdas'] = function_counter
    resource_totals['Lambda Functions'] = total_functions

def glacier_counter():
    region_list = session.get_available_regions('glacier')

    total_vaults = 0

    for region in region_list:
        glacier = session.resource('glacier', region_name=region)
        vault_iterator = glacier.vaults.all()
        vault_counter = len(list(vault_iterator))
        total_vaults += vault_counter
        resource_counts[region]['glacier vaults'] = vault_counter
    resource_totals['Glacier Vaults'] = total_vaults

def cloudwatch_rules_counter():
    region_list = session.get_available_regions('events')

    total_events = 0

    for region in region_list:
        cloudwatch = session.client('events', region_name=region)
        rules = cloudwatch.list_rules()
        events_counter = len(rules['Rules'])
        total_events += events_counter
        resource_counts[region]['cloudwatch rules'] = events_counter
    resource_totals['Cloudwatch Rules'] = total_events

def config_counter():
    region_list = session.get_available_regions('config')

    total_config_rules = 0

    for region in region_list:
        config = session.client('config', region_name=region)
        config_rules_counter = 0
        config_rules_paginator = config.get_paginator('describe_config_rules')
        config_rules_iterator = config_rules_paginator.paginate()
        for rule in config_rules_iterator:
            config_rules_counter += len(rule['ConfigRules'])
        total_config_rules += config_rules_counter
        resource_counts[region]['config rules'] = config_rules_counter
    resource_totals['Config Rules'] = total_config_rules

def cloudtrail_counter():
    region_list = session.get_available_regions('cloudtrail')

    total_trails = 0

    for region in region_list:
        cloudtrail = session.client('cloudtrail', region_name=region)
        trails = cloudtrail.describe_trails()
        trails_counter = len(trails['trailList'])
        total_trails += trails_counter
        resource_counts[region]['cloudtrail trails'] = trails_counter
    resource_totals['CloudTrail Trails'] = total_trails

def sns_counter():
    region_list = session.get_available_regions('sns')

    total_topics = 0

    for region in region_list:
        sns = session.resource('sns', region_name=region)
        topic_iterator = sns.topics.all()
        topic_counter = len(list(topic_iterator))
        total_topics += topic_counter
        resource_counts[region]['sns topics'] = topic_counter
    resource_totals['SNS Topics'] = total_topics

def kms_counter():
    region_list = session.get_available_regions('kms')

    total_keys = 0

    for region in region_list:
        kms = session.client('kms', region_name=region)
        keys_counter = 0
        kms_paginator = kms.get_paginator('list_keys')
        kms_iterator = kms_paginator.paginate()
        for key in kms_iterator:
            keys_counter += len(key['Keys'])
        total_keys += keys_counter
        resource_counts[region]['kms keys'] = keys_counter
    resource_totals['KMS Keys'] = total_keys

def dynamo_counter():
    region_list = session.get_available_regions('dynamodb')

    total_tables = 0

    for region in region_list:
        dynamodb = session.resource('dynamodb', region_name=region)
        table_iterator = dynamodb.tables.all()
        table_counter = len(list(table_iterator))
        total_tables += table_counter
        resource_counts[region]['dynamo tables'] = table_counter
    resource_totals['Dynamo Tables'] = total_tables

def rds_counter():
    region_list = session.get_available_regions('rds')

    total_dbinstances = 0

    for region in region_list:
        rds = session.client('rds', region_name=region)
        dbinstances_counter = 0
        rds_paginator = rds.get_paginator('describe_db_instances')
        rds_iterator = rds_paginator.paginate()
        for instance in rds_iterator:
            dbinstances_counter += len(instance['DBInstances'])
        total_dbinstances += dbinstances_counter
        resource_counts[region]['rds instances'] = dbinstances_counter
    resource_totals['RDS Instances'] = total_dbinstances

if __name__ == "__main__":
    controller()