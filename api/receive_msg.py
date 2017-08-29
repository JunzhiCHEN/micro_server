import hashlib
import json
from flask_restful import Resource
from flask_restful import reqparse, request
from common.im import Im
from libs.util import Util
from const.const import APP_SERECT
class ReceiveMsg(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        # Token: first headers, second cookies, last args
        self.get_args.add_argument('Curtime', type=str, required=True, location=['headers', 'cookies', 'values'],
                                   help='CurTime cannot be blank!')
        self.get_args.add_argument('Md5', type=str, required=True, location=['headers', 'cookies', 'values'],
                                   help='MD5 cannot be blank!')
        self.get_args.add_argument('Checksum', type=str, required=True, location=['headers', 'cookies', 'values'],
                                   help='CheckSum cannot be blank!')
        self.args = self.get_args.parse_args()
    def post(self):
        json_str = request.data
        util_helper = Util()
        json_str = util_helper.encrypt(json_str.encode("utf-8"))
        AppSecret = APP_SERECT
        veryMD5 = hashlib.md5(request.data).hexdigest()
        veryChecksum = hashlib.sha1(AppSecret+self.args["Md5"]+self.args["Curtime"]).hexdigest()
        if self.args["Md5"] == veryMD5 and veryChecksum == self.args["Checksum"]:
            msg_id = Im().save_msg_to_db(json_str)
            if msg_id:
                return {"error_code": "200", "msg": "save sucess!"}
            else:
                return {"error_code": "400", "msg": "save Faild!"}
        else:
            print False
            return {"error_code": "2001", "msg": "no pass the check!"}
