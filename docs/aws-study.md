# AWS Study

> This page taken from the notes when studying AWS



## Content

  * [CloudFormation](#cf)
  * [RDS - MySQL](#rds)
  * [EC2](#ec2)



</br><a name="cf"></a>
## AWS CloudFormation

  * [Sceptre](https://github.com/Sceptre/sceptre) is a tool to drive
    [AWS CloudFormation](https://aws.amazon.com/cloudformation)


</br><a name="rds"></a>
## AWS RDS

### AWS RDS upgrade

  Here is an example of upgrading MySQL engine from 5.6 to 5.7.

  * Stop services (with notification)
  * Take a snapshot with timestamp suffix, e.g. `db-name-prod_YYMMDD-HHMM`
    - cluster and instance name
    - db instance class: e.g. `db.t2.medium` (prod)
    - connection port: `3306` (default);
    - vpc and subnet group
    - security group (**note**: this won't be in the snapshot)
    - db cluster parameter group: e.g. `default.aurora5.6` (engine 5.6.x)
    - encryption: disabled; no logging; maintenance: allow minor upgrade;
    - public: `none`; zone: e.g. "`us-east-1d`".
    - write down latest record, and counts for domains/rules tables
    - note: as incremental backup this should be very quick.
  * Rename the old cluster and instance with suffix, e.g. "-v56"
  * Restore the snapshot to a new cluster with
    - original instance name
    - original cluster name
    - a higher engine version, e.g. Aurora 2.x (MySQL 5.7)
      * parameter group: `default.aurora-mysql5.7`
    - other settings matching to the original one (where the snapshot taken from) as well as ensure the new instance and cluster keep the original names.
    - restoring operation could take up to, e.g. hours, depending on data storage volume in the database.
    - set "security group" manually to match the original one.
  * Finish up
    - Pending on test and verification.
    - Shutdown original database cluster/instance (which had been renamed after taking snapshot).
    - Delete experimental and old cluster/instance.
    - Delete old unused snapshots.


</br><a name="ec2"></a>
## EC2

### Web Server

#### Creating Steps

  1. request a EC2 instance from AWS, I used the free ubuntu server, storage 28, with SSH, HTTP, HTTPS protocols
  2. use terminal ssh command to login to the server: `ssh -i ~/.ssh/jiz148_ec2.pem ubuntu@<public_dns>`
  3. sudo apt-get update, sudo install apache2, install the web server package
  4. change the owner and accessibility of the html directory that Apache2 is looking for
  5. replace the htmls

### Commands

  * `chmod 400 jiz148_ec2.pem` manage the visibility of a file
  * `ssh -i ~/.ssh/jiz148_ec2.pem <user_name>@<public dns>`: login to the server with the ssh key in "\~/.ssh/jiz148_ec2.pem"; `user_name` can be `ec2-user` or `ubuntu`; eg. `ssh -i "jiz148_ec2.pem" ubuntu@<public_dns>`; "`-i`" for identity file (eg. private key)
  * `sudo apt-get update`: get latest packages updated
  * `sudo apt-get install`: install package; eg. `sudo apt-get install apache2` (for web server)
  * `sudo chown -R ubuntu /var/www/html`: change the user of the file to specific user, this time it is for changing the owner of html that ubuntu is looking for ubuntu is the user_name, `-R` means process of the files in the directory and its sub directories
  * `sudo chmod -R 755 /var/www/html`: chmod means changing a accessibility of a file or directory. three numbers ugo (u: user, g: group, o: others), 4: read, 2: write, 1: execute; here we are changing the accessibility of the Apache2 html file to all for user, read and execute for group and others
  * `sudo nano index.html`: edit "index.html" using Nano, create on if there was not
  * `scp -i <pravite key> <file directory> <user_name>@<public_dns>:<destination_on_ec2>`: secured copy file using TCP

### HTML

  * ```<html> and </html>```: opening and closing
  * ```<head> </head> and <body> </body>```: head and body, ```<br />``` means next line
  * ```<title> and </title>```: web page title
  * ```<h1></h1> to <h5></h5>```: bigger size
  * ```<p></p>```: paragraph
  * ```<img src="*path"```: display image of the indicated path, can have the property, width, alt for alternative text
  * ```<hr />```: a horizontal line
