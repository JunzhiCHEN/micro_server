import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from flask import Flask
from flask_restful import Api
from api.receive_msg import ReceiveMsg
from api.im.add_im_user_info import AddImUser

def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ReceiveMsg, '/api/sky_server_data_app/im/receiveMsg')
    api.add_resource(AddImUser, '/api/sky_server_data_app/im/addImUser')
    return app


if __name__ == '__main__':
    create_app().run(host="0.0.0.0", port=8080, debug=True)