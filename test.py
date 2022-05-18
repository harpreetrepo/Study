from importlib.resources import path
from netmiko import ConnectHandler
net_connect = ConnectHandler(device_type="cisco_ios", host="sandbox-iosxe-latest-1.cisco.com", 
username="developer", password="C1sco12345")
net_connect.find_prompt()
output= net_connect.send_command("show run | in hostname")
output_backup = net_connect.send_command("show run")
file_name=(len(output))
output=(output[9:file_name])
print(output)
file = open("/Users/harpreetsingh/Desktop/python_study/study/"+output+".txt", "w")
file.write(output_backup)
file.close()

 