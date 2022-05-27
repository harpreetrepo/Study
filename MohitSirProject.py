from netmiko import ConnectHandler
import os
import re
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_dispatcher import ConnectHandler
import time
#Funtion for creating a folder
def createfolder():
    try:
        folders= os.listdir("/Users/harpreetsingh/Desktop/python_study/Mohit_projects")
        print("*"* 100)
        print("Current folder in the directory")
        print("*"* 100)
        print(folders)
        print("*"* 100)
        if "cisco_ios" in folders and "juniper" in folders:
            print("Folders already exits")
            print("*"* 100)

        elif "cisco_ios" not in folders and "juniper" not in folders:
            os.makedirs("/Users/harpreetsingh/Desktop/python_study/Mohit_projects/cisco_ios")
            os.makedirs("/Users/harpreetsingh/Desktop/python_study/Mohit_projects/juniper")
            print("Cisco IOS and Juniper folder created!!!")
            print("*"* 100)

        elif "cisco_ios" not in folders:
            os.makedirs("/Users/harpreetsingh/Desktop/python_study/Mohit_projects/cisco_ios")
            print("Cisco IOS folder created!!!")
            print("*"* 100)

        else:
            os.makedirs("/Users/harpreetsingh/Desktop/python_study/Mohit_projects/juniper")
            print("Juniper folder created!!!")
            print("*"* 100)
        
        folders= os.listdir("/Users/harpreetsingh/Desktop/python_study/Mohit_projects")
        print(folders)
        print("*"* 100)
    except:
        print("Error occured while creating a folder.")
        print("*"* 100)

#Taking user device information and confirming if management interface is needs to be check.
Host = input("Please enter host details:")
User = input("Please provide user name:")
Password= input("Please provide password:")
Checkint = input("Do you want to check managment interface status(up/down) type Yes or No:")
print("*"* 100)
# Device class for checking the device type
class Device:
    def __init__(self, Host, User, Password):
        self.Host = Host
        self.User = User
        self.Password = Password
    
    def CheckDeviceType(self):
            remote_device = {
            'device_type' : 'autodetect',
        'host': self.Host,
        'username' : self.User,
            'password' : self.Password,
        }
            try:
                dev_type= SSHDetect(**remote_device)
                device= dev_type.autodetect()
                dev_type.connection.disconnect()
                return device
            except:
                print("Connection cannot be established with the host")
                print("*"* 100)
# Child class created to fetch the detials from parent class and does the device backup
class Devicebackup(Device):
    def __init__(self, Output):
        super().__init__(Host, User, Password)
        self.Output= Output
    def Backup(self):
        if self.Output == "cisco_ios":
            try:
                net_connect = ConnectHandler(device_type="cisco_ios", host=self.Host, 
                username=self.User, password=self.Password)
                net_connect.find_prompt()
            except:
                print("connection cannot formed with cisco router!!!!")
                print("*"* 100)
            try:
                output_interface=net_connect.send_command("show run interface Loopback 0")
                filename= re.search(r'ip address (.*) (.*)', output_interface)
                ip = filename.group(1)
            except:
                print("No management interface found to name the backup file!!!!")
                print("*"* 100)
            output= net_connect.send_command("show run")
            #print(output)
            print("*"* 100)
            file = open("/Users/harpreetsingh/Desktop/python_study/Mohit_projects/cisco_ios/"+ip+".txt","w")
            file.write(output)
            print("Device backup taken in master folder")
            print("*"* 100)
            file.close()
            net_connect.disconnect()

        else:
            try:
                net_connect = ConnectHandler(device_type="juniper", host=self.Host, 
                username=self.User, password=self.Password)
                net_connect.find_prompt()
            except:
                print("connection cannot formed with Juniper router!!!!")
                print("*"* 100)
            try:
                output_interface= net_connect.send_command("show interfaces lo0.0")
                print(output_interface)
                print("*"* 100)
                filename= re.search(r'Local: (.*)', output_interface)
                ip = filename.group(1)
                print(ip)
                print("*"* 100)
                output= net_connect.send_command("show configuration")
                #print(output)
                file = open("/Users/harpreetsingh/Desktop/python_study/Mohit_projects/juniper/"+ip+".txt","w")
                file.write(output)
                print("Device backup taken in master folder")
                print("*"* 100)
                file.close()
                net_connect.disconnect()
            except:
                print("No management interface found to name the backup file!!!!")
                print("*"* 100)
# Funtion created to check the management interface status and make the changes accordingly
def Mangint(Host, User, Password, output):

    if output == "cisco_ios":
        try:
            net_connect = ConnectHandler(device_type="cisco_ios", host=Host, 
            username=User, password=Password)
            net_connect.find_prompt()
            output= net_connect.send_command("show ip interface brief | in Loopback")
            print(output)
            print("*"* 100)
            if "down" in output:
                print("interface is down")
                print("*"* 100)
                commands=['interface Loopback 0',
                'no shut']
                check=net_connect.send_config_set(commands)
                print(check)
                print("*"* 100)
                print("Interface is up now")
                print("*"* 100)
            else:
                print("Management interface is already Up")
        except:
            print("Error occured when configuring Loopback 0 interface")
            print("*"* 100)
        
    else:
        try:
            net_connect = ConnectHandler(device_type="juniper", host=Host, 
            username=User, password=Password)
            net_connect.find_prompt()
            output_interface= net_connect.send_command("show interfaces terse | grep lo0.0")
            print(output_interface)
            print("*"* 100)
            if "down" in output_interface:
                print("interface is down")
                print("*"* 100)
                commands=[
                'delete interfaces lo0.0 disable',
                'commit']
                check=net_connect.send_config_set(commands)
                print(check)
                print("*"* 100)
                print("Interface is up now")
                print("*"* 100)
            else:
                print("Interface is already up!!!")
                print("*"* 100)
        except:
            print("Error occured when configuring Loopback 0 interface")
            print("*"* 100)


createfolder()
DeviceDetials= Device(Host,User,Password)
output=DeviceDetials.CheckDeviceType()
BackupStart=Devicebackup(output)
BackupStart.Backup()
time.sleep(3)
if Checkint == "yes":
     Mangint(Host, User, Password, output)
else:
    print("management interface check not required")
    print("*"* 100)
