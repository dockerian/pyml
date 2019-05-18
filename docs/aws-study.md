# AWS Study

> This page taken from the notes when studying AWS



## Content

* [EC2](#ec2)



</br><a name="ec2"></a>
## EC2

### Web Server

#### Creating Steps

1. request a EC2 instance from AWS, I used the free ubuntu server, storage 28, with SSH, HTTP, HTTPS protocols
2. use terminal ssh command to login to the server: ssh -i ~/.ssh/jiz148_ec2.pem ubuntu@"public_dns"
3. sudo apt-get update, sudo install apache2, install the web server pachage
4. change the owner and accessibility of the html directory that Apache2 is looking for
5. replace the htmls

### Commands

* chmod 400 jiz148_ec2.pem: manage the visibility of a file
* ssh -i \~/.ssh/jiz148_ec2.pem "user_name"[public dns]: login to the server with the ssh key in "\~/.ssh/jiz148_ec2.pem"; user_name can be ec2-user or ubuntu; eg. ssh -i "jiz148_ec2.pem" ubuntu@"public_dns"; -i for identity file (eg. private key)
* sudo apt-get update: get latest packges updated
* sudo apt-get install: install package; eg. sudo apt-get install apache2 (for web server)
* sudo chown -R ubuntu /var/www/html: change the user of the file to specific user, this time it is for changing the owner of html that ubuntu is looking for ubuntu is the user_name, -R means process of the files in the directory and its subdirectoreis
* sudo chmod -R 755 /var/www/html: chmod means changing a acessibility of a file or directory. three numbers ugo(u: user, g: group, o: others), 4 read, 2 write, 1 excute; here we are changing the acessibility of the Apache2 html file to all for user, read and execute for group and others
* sudo nano index.html: edit "index.html" using Nano, create on if there was not
* scp -i "pravite key" "file directory" "user_name"@"public_dns":"destination_on_ec2": secured copy file using TCP

### HTML

* ```<html> and </html>```: opening and closing
* ```<head> </head> and <body> </body>```: head and body, ```<br />``` means next line
* ```<title> and </title>```: web page title
* ```<h1></h1> to <h5></h5>```: bigger size
* ```<p></p>```: paragraph
* ```<img src="*path"```: display image of the indicated path, can have the property, width, alt for alternative text
* ```<hr />```: a horizontal line
