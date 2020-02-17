import sqlite3 as driver
connection = None
from threading import Lock

lock = Lock()

def get_user_id(username):
    global connection
    search_query = "select * from device_user_details where username = " + "'{}'".format(username)
    user_id = 0
    try:
        if connection:
            cursor = connection.cursor()
            cursor.execute(search_query)
            # find the record for the given username
            data = cursor.fetchone()
            if len(data) != 0:
                user_id = data[2]
            cursor.close()
    except Exception as error:
        print(error)

    return user_id


def get_device_details():
    global connection
    search_query = "select * from device_mgmt_details"
    try:
        if connection:
            cursor = connection.cursor()
            cursor.execute(search_query)
            # find the record for the given username
            data = cursor.fetchall()
            cursor.close()
    except Exception as error:
        print(error)
    return data


def get_dev_id():
    global connection
    search_query = "select * from device_mgmt_details where dev_id = (select max(dev_id) from device_mgmt_details)"
    user_id = 0
    try:
        if connection:
            cursor = connection.cursor()
            cursor.execute(search_query)
            # find the record for the given username
            data = cursor.fetchone()
            if len(data) != 0:
                user_id = data[0]
            cursor.close()
    except Exception as error:
        print(error)

    return user_id


def database_conn():
    global connection
    try:
        print("Trying to connect to Db")
        connection = driver.connect("device_mgmt_db", check_same_thread=False)
        return connection
    except (Exception, driver.Error) as error :
        print ("Error while connecting to Database", error)
        return None


def check_and_create_device_table():
    global connection
    table_query = '''SELECT count(*) FROM sqlite_master
        WHERE type='table' AND name='device_mgmt_details';'''
    cursor = connection.execute(table_query)
    count = cursor.fetchone()[0]
    if count == 1:
        print('Device table exists.')
    else:
        cursor = connection.execute('''CREATE TABLE device_mgmt_details
        (
        dev_id INTEGER PRIMARY KEY , 
        dev_name NOT NULL, 
	    dev_console TEXT,
	    dev_mgmt TEXT,
	    dev_power TEXT,
	    usedby TEXT,
	    topo TEXT
         );''')
        print("Table created")
    cursor.close()


def check_and_create_user_table():
    global connection
    table_query = '''SELECT count(*) FROM sqlite_master
        WHERE type='table' AND name='device_user_details';'''
    cursor = connection.execute(table_query)
    count = cursor.fetchone()[0]
    if count == 1:
        print('User table exists.')
    else:
        cursor = connection.execute('''CREATE TABLE device_user_details
        (
        username TEXT NOT NULL PRIMARY KEY,
	    email TEXT NOT NULL,
	    id INTEGER
         );''')
        print("User Table created")
    cursor.close()


def insert_user_data(local_user_instance):
    """
    insert into device_user_details(username, password) values('vinoth' ,'password')

    UPDATE device_user_details SET password = 'cisco' WHERE username ='vinoth'

    """
    return_str = ""
    search_query = "select * from device_user_details where username = " + "'{}'".format(local_user_instance.username)
    try:
        if connection:
            cursor = connection.cursor()
            cursor.execute(search_query)
            # find the record for the given username
            data = cursor.fetchall()
            print(len(data))
            if len(data) != 0:
                # if the user already exist.update the record
                    insert_query = "UPDATE device_user_details SET password = " + \
                    "'{}'".format(str(local_user_instance.email)) + \
                    " WHERE username =" + "'{}'".format(local_user_instance.username)
            else:
                #  Create new Record in the db.
                insert_query = ("insert into device_user_details(username, email ,id) "
                                "values("  "'{}'".format(str(local_user_instance.username)) + "," + \
                                "'{}'".format(str(local_user_instance.email))) + ", " + \
                               "(SELECT IFNULL(MAX(id), 0) + 1 FROM  device_user_details))"
            print(insert_query)
            with lock:
                cursor.execute(insert_query)
                connection.commit()
            cursor.close()
            print("Record inserted username:", local_user_instance.username)
        else:
            print("Connection Does not exist.Something wrong with db.")

    except driver.OperationalError:
        return_str = "Operational Error. Cannot Create User."
    except Exception as error:
        return_str = error
    return return_str


def add_update_device(device_details):
    global connection
    try:
        if connection:
            cursor = connection.cursor()
            if int(device_details.dev_id) !=0:
                insert_query  = "UPDATE device_mgmt_details set dev_name =  " + \
                                "'{}'".format(str(device_details.dev_name)) + ", dev_console = " + \
                                "'{}'".format(str(device_details.dev_console)) + ", dev_mgmt = " + \
                                "'{}'".format(str(device_details.dev_mgmt)) + ",  dev_power = " + \
                                "'{}'".format(str(device_details.dev_power)) + ", topo   =" + \
                                "'{}'".format(str(device_details.dev_topo)) + ", usedby = " + \
                                "'{}'".format(str(device_details.usedby)) + " where dev_id =" + \
                                "'{}'".format(str(device_details.dev_id))


            else:
                insert_query = ("insert into device_mgmt_details(dev_name, dev_console ,dev_mgmt ,  dev_power , topo , usedby) "
                        "values(" "'{}'".format(str(device_details.dev_name)) + "," + \
                            "'{}'".format(str(device_details.dev_console))) + ", " + \
                            "'{}'".format(str(device_details.dev_mgmt)) + ", " + \
                            "'{}'".format(str(device_details.dev_power)) + ", " + \
                            "'{}'".format(str(device_details.dev_topo)) + ", " \
                            "'{}'".format(str(device_details.usedby)) + ")"
            print(insert_query)
            with lock:
                cursor.execute(insert_query)
                connection.commit()
            cursor.close()
            if device_details.dev_id != 0:
                device_id = get_dev_id()
    except Exception as error:
        return error
    return device_id


def delete_device(dev_id):
    global connection
    try:
        if connection:
            cursor = connection.cursor()
            delete_query  = "DELETE FROM device_mgmt_details WHERE dev_id =" + \
                            "'{}'".format(str(dev_id))
            with lock:
                cursor.execute(delete_query)
                connection.commit()
            cursor.close()
    except Exception as error:
        return error
    return True


def login_user(user_detail):
    global connection
    try:
        if connection:
            get_query = "select * from device_user_details where username = " + "'{}'".format(user_detail.username)
            print(get_query)
            cursor = connection.cursor()
            cursor.execute(get_query)
            data = cursor.fetchone()
            if len(data) == 0:
               return False
            else:
                if data[0] == user_detail.username:
                    return True
                else:
                    return False
        else:
            print("Problem with connection")

    except Exception as error:
        print(error)

    return False
