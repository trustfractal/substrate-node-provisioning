# AWS PULUMI substrate node (kusama/polkadot) simple provisioning script

## Pulumi script installation

Pulumi installation on Linux workstation: ```curl -fsSL https://get.pulumi.com | sh```

Pulumi installation on MAC workstation: ```brew install pulumi```

Installing:

```
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Setting AWS access keys:

```
export AWS_ACCESS_KEY_ID=<AWS Access Key>
export AWS_SECRET_ACCESS_KEY=<AWS Secret
```

## Creating a new stack

```
pulumi stack init kusama01
pulumi stack select kusama01
```

We have to set parameters for our node:

```
pulumi config set aws-python-substrate:availability_zone eu-central-1a
pulumi config set aws-python-substrate:instance_type t3.xlarge
pulumi config set aws-python-substrate:node_chain kusama
pulumi config set aws-python-substrate:node_db_volume_size 200
pulumi config set aws-python-substrate:ssh_public_key "ssh-rsa AAAAB3NzaC1yc2EAAAAxxxxxx"
``` 

Default zone config: ```pulumi config set aws:region eu-central-1```

Previewing pulumi installation: ```pulumi preview```

should give us the resources which will be initiated.

```
     Type                         Name                              Plan       
 +   pulumi:pulumi:Stack          aws-python-substrate-kusama01     create     
 +   ├─ aws:ec2:KeyPair           pulumi01                          create     
 +   ├─ aws:ec2:SecurityGroup     ssh and node public access        create     
 +   ├─ aws:ebs:Volume            db_volume                         create     
 +   ├─ aws:ec2:Eip               kusama Node                       create     
 +   ├─ aws:ec2:Instance          KUSAMA validator Node - kusama01  create     
 +   ├─ aws:ec2:EipAssociation    eipAssoc                          create     
 +   └─ aws:ec2:VolumeAttachment  db_volume                         create     
```

to initiate the provisioning: ```pulumi up ```

```
     Type                         Name                              Status      
 +   pulumi:pulumi:Stack          aws-python-substrate-kusama01     created     
 +   ├─ aws:ec2:KeyPair           pulumi01                          created     
 +   ├─ aws:ebs:Volume            db_volume                         created     
 +   ├─ aws:ec2:Eip               kusama Node                       created     
 +   ├─ aws:ec2:SecurityGroup     ssh and node public access        created     
 +   ├─ aws:ec2:Instance          KUSAMA validator Node - kusama01  created     
 +   ├─ aws:ec2:EipAssociation    eipAssoc                          created     
 +   └─ aws:ec2:VolumeAttachment  db_volume                         created     
 
Outputs:
    db_volume_dev: "/dev/xvdf"
    elastic_ip   : "34.203.109.221"

Resources:
    + 8 created

Duration: 1m16s
```

Now we can connect using ssh and proceed with software installation process. 
