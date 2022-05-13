print("hello")
from netmiko import ConnectHandler
net_connect = ConnectHandler(device_type="cisco_ios", host="sandbox-iosxe-latest-1.cisco.com", 
username="developer", password="C1sco12345")
net_connect.find_prompt()
output= net_connect.send_command("show ip int br")
print(output)
