import flask
from flask import render_template, Flask, redirect, json ,jsonify , url_for
from flask import request
import device_mgmt_class
from flask import jsonify
import database
import smtplib


device_detail_array = ['dev_id', 'dev_name' ,'dev_console', 'dev_mgmt','dev_power', 'used_by', 'dev_topo']

app = Flask(__name__)


app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['TESTING'] = False


@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        username = request.form['n_userid']
        local_user_detail = device_mgmt_class.User(username,"")
        ret_val = database.login_user(local_user_detail)
        if ret_val is True:
            ''' If the user is authenticated redirect the use
            to the device detail page
            '''
            print("coming here")
            resp = flask.make_response(redirect(url_for('get_device_page')))
            resp.set_cookie('user', username)
            return resp
        else:
            return render_template('login.html', error="Invalid Username or Password")
    else:
        #Get method
        username = request.cookies.get('user')
        if username is None:
            resp = flask.make_response(render_template('login.html', error=error))
            return resp
        else:
            '''
            The cookie is set, which means that the user is already authenticated
            redirect the user to device detail page'''
            resp = flask.make_response(redirect(url_for('get_device_page')))
            return resp


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
      username = request.form['n_reg_userid']
      email = request.form['n_reg_email']
      local_user_instance = device_mgmt_class.User(username, email)
      return_str = database.insert_user_data(local_user_instance)
      """
        Get the username and email and insert into the DB.
      """
      if len(return_str):
          error = return_str
      else:
          error="User created Successfully. \n Login to Continue.."
      return flask.make_response(redirect(url_for('login')))
    else:
        return render_template('login.html', error=error)


@app.route('/device_detail/reserve_device', methods=['POST'])
def reserve_device():
    if request.method == 'POST':
        jsondata = request.get_json()
        '''
            Reserve the device for the user requested for and update the DB.
        '''
        local_device_instance = device_mgmt_class.DeviceMgmt(jsondata['dev_id'],
                                                             jsondata['dev_name'],
                                                             jsondata['dev_console'],
                                                             jsondata['dev_mgmt'],
                                                             jsondata['dev_power'],
                                                             jsondata['dev_topo'],
                                                             jsondata['used_by'])
        database.add_update_device(local_device_instance)
        return render_template('device_detail.html')
    else:
        pass
    return 0


@app.route('/device_detail/request_device', methods=['POST'])
def request_device():
        if request.method == 'POST':
            jsondata = request.get_json()
            try:
                msg_to = jsondata['used_by'] + '@cisco.com'
                msg_sub = 'Device Request : ' + jsondata['dev_name']
                TEXT = 'User ' + request.cookies.get('user') + " is requesting device :" + jsondata['dev_name']
                message = 'Subject: {}\n\n{}'.format(msg_sub, TEXT)
                s = smtplib.SMTP('localhost')
                s.sendmail('dev_mgr', msg_to, message)
                s.quit()
                return render_template('device_detail.html')
            except:
                return render_template('device_detail.html', error="Error sending Email")
        else:
            return render_template('device_detail.html')



@app.route('/device_detail/save_edit_device', methods=['POST'])
def device_detail_operation():
    error = None
    if request.method == 'POST':
        jsondata = request.get_json()
        form_device_id = jsondata['dev_id']
        form_device_id = jsondata['dev_id']
        device_name = jsondata['dev_name']
        device_console = jsondata['dev_console']
        device_mgmt =  jsondata['dev_mgmt']
        device_power = jsondata['dev_power']
        device_topo = jsondata['dev_topo']
        used_by = None
        """
        Get the details from the form and update the DB.
        """
        local_device_instance = device_mgmt_class.DeviceMgmt(form_device_id, device_name,device_console,device_mgmt,
                                                             device_power, device_topo, used_by)
        device_id = database.add_update_device(local_device_instance)
        if form_device_id == 0:
            local_device_instance.dev_id = device_id
    return flask.make_response(redirect(url_for('get_device_page')))


@app.route('/device_detail/',methods=['GET'])
def get_device_page():
    '''
        If the user is directly trying to access the page
         without logging, re-direct to the login page.
    '''
    username = request.cookies.get('user')
    if username is None:
        error = "Please login to access this page"
        return redirect(url_for('login'))
    return render_template('device_detail.html')


@app.route('/device_detail/get_device', methods=['GET', 'POST','DELETE'])
def fetch_all_devices():
    '''

    Fetch all the device details and build json out of it
    and send it over to the UI.
    '''
    list_dict =[]
    if request.method == 'GET':
        data = database.get_device_details()
        for entry in data:
            local_copy = entry
            dev_dict = {}
            for index in range(len(device_detail_array)):
                dev_dict[device_detail_array[index]] = local_copy[index]
            list_dict.append(dev_dict)
        return jsonify(list_dict)
    elif request.method == 'DELETE':
        jsondata = request.get_json()
        database.delete_device(jsondata['dev_id'])
        return get_device_page()


@app.route('/logout',methods=["POST"])
def logout():
    '''
    Delete the cookie, this de-authenticates the user.
    :return:
    '''
    username = request.cookies.get('user')
    print(username)
    resp = flask.make_response(redirect('/login'))
    resp.delete_cookie('user' , username)
    return resp


def invoke_db_conn():
    '''
        Setup the DB connections and create the DB if they don't exist.

    '''
    print("Connecting to DB.....")

    connect = database.database_conn()
    if connect is None:
        print("No Db Connection")
    else:
        print("Connection Succeeded", "\n")
        database.check_and_create_device_table()
        database.check_and_create_user_table()


if __name__ == '__main__':
    invoke_db_conn()
    app.run(debug=True,host='0.0.0.0',port='5500')
