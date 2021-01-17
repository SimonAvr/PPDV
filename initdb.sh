#!/bin/bash
export MAINDB=stepdb
export PASSWORD_OF_MYSQL_ROOT_USER='new_password'
export username=user;
export new_password=1234;
#echo "press root mysql password"
#read -s PASSWORD_OF_MYSQL_ROOT_USER
export con_root="mysql -uroot -p$PASSWORD_OF_MYSQL_ROOT_USER -e "
$con_root "create user '$username' identified by '$new_password';"
echo "user created\n"
$con_root "CREATE DATABASE $MAINDB";
echo "db creted\n"
$con_root "GRANT ALL PRIVILEGES ON $MAINDB.* TO '$username' IDENTIFIED BY '$new_password';"
echo "priledges granted\n"
export con_usr="mysql -u$username -p$new_password -e"
$con_usr "use stepdb; 
								create table patient
								(
								url_id int PRIMARY KEY,
								firstname varchar(255),
								lastname varchar(255),
								disabled bool
								);"
$con_usr "use stepdb; 
								create table measure
								(
								id int AUTO_INCREMENT PRIMARY KEY,
								ts TIMESTAMP,
								patient_id int,
								entry text,
									INDEX pat_ind (patient_id),
								foreign key (patient_id) references patient(url_id)
								);"



#mysql -u$username -p$new_password -e "use stepdb; 
#create table patient
#(
#								url_id int PRIMARY KEY,
#								firstname varchar(255),
#								lastname varchar(255),
#								disabled bool
#
#);
#create table measure
#(
#								id int AUTO_INCREMENT PRIMARY KEY,
#								L0 int,
#								L1 int,
#								L2 int,
#								R0 int,
#								R1 int,
#								R2 int,
#								anomaly bool,
#								ts TIMESTAMP,
#								patient_id int,
#									INDEX pat_ind (patient_id),
#								foreign key (patient_id) references patient(url_id)
#);"
