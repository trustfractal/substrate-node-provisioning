import pulumi
import pulumi_aws as aws

# setting
config = pulumi.Config()
availability_zone = config.require("availability_zone")
instance_type = config.require("instance_type")
node_db_volume_size = int(config.require("node_db_volume_size"))
node_chain = config.require("node_chain")
ssh_public_key = config.require("ssh_public_key")
stack_name = pulumi.get_stack()

# setting ssh key
ssh_key = aws.ec2.KeyPair("pulumi01", public_key=ssh_public_key)

# choosing the latest ubuntu minimal 20.04 image
ubuntu_minimal = aws.get_ami(most_recent=True,
    filters=[
        aws.GetAmiFilterArgs(
            name="name",
            values=["ubuntu-minimal/images/hvm-ssd/ubuntu-focal-20.04-amd64-minimal*"],
        ),
        aws.GetAmiFilterArgs(
            name="virtualization-type",
            values=["hvm"],
        ),
    ],
    owners=["099720109477"])

security_group = aws.ec2.SecurityGroup('ssh and node public access',
    description='Enable SSH + node access',
    egress=[
        {'protocol': '-1', 'fromPort': 0, 'toPort': 0, 'cidrBlocks': ["0.0.0.0/0"]},
    ],
    ingress=[
        {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0']},
        {'protocol': 'tcp', 'from_port': 30333, 'to_port': 30333, 'cidr_blocks': ['0.0.0.0/0']}
    ])

# creating volume for db files
node_volume = aws.ebs.Volume("db_volume",
    availability_zone=availability_zone,
    size=node_db_volume_size)

# setting root file system
root_ebs = { "deleteOnTermination": True,
            "volume_size": 25,
            "volumeType": "gp2",
            "encrypted": False
          }

# creating ec2 instance
node = aws.ec2.Instance(
    f'{node_chain.upper()} validator Node - {stack_name}',
    ami=ubuntu_minimal.id,
    availability_zone=availability_zone,
    instance_type=instance_type,
    vpc_security_group_ids=[security_group.id],
    key_name=ssh_key.key_name,
    root_block_device=root_ebs,
    tags={
        "Name": f'{node_chain.upper()} validator Node ef- {stack_name}',
    })

# attaching volume to the node.
ebs_att = aws.ec2.VolumeAttachment("db_volume",
    device_name="/dev/xvdf",
    volume_id=node_volume.id,
    instance_id=node.id)



# creating and attaching elastic ip
static_ip = aws.ec2.Eip(f'{node_chain} Node', vpc=True)
eip_assoc = aws.ec2.EipAssociation("eipAssoc",
    instance_id=node.id,
    allocation_id=static_ip.id)

# exports
pulumi.export('elastic_ip', static_ip.public_ip)
# pulumi.export('public_ip', node.public_ip)
pulumi.export('db_volume_dev', ebs_att.device_name)
# pulumi.export('ssh_command', f'ssh@{static_ip.public_ip}')
pulumi.export('ssh_command', static_ip.public_ip.apply(lambda public_ip: 'ssh ubuntu@'+public_ip))
