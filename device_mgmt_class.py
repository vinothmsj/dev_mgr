"""
This class defines the entities required for the device management app
    device Id  - This is internal and used to interact with DB for CURD operations.
    Name - User customisable device name
    Telnet - Device console details.
    Mgmt - Device management ip range
    power details - Device power console and port details.
    usedby - Username(CEC ID) of the user the device is assigned to.
"""


class DeviceMgmt:
    def __init__(self, dev_id, dev_name,dev_console, dev_mgmt,dev_power, dev_topo, usedby):
        self.dev_id = dev_id
        self.dev_name = dev_name
        self.dev_console = dev_console
        self.dev_mgmt = dev_mgmt
        self.dev_power = dev_power
        self.dev_topo = dev_topo
        self.usedby = usedby


class User():
    def __init__(self, username, email):
        self.username = username
        self.email = email

