import hashlib
import urllib
from flask_restful import Resource
from flask_restful import reqparse
from common.im import Im
from const.const import APP_SERECT
class UpdateImUser(Resource):
    def __init__(self):
        self.get_args = reqparse.RequestParser()
        # Token: first headers, second cookies, last args
        self.get_args.add_argument('Curtime', type=str, required=True, location=['headers', 'cookies', 'values'],
                                   help='CurTime cannot be blank!')
        self.get_args.add_argument('Md5', type=str, required=True, location=['headers', 'cookies', 'values'],
                                   help='MD5 cannot be blank!')
        self.get_args.add_argument('Checksum', type=str, required=True, location=['headers', 'cookies', 'values'],
                                   help='CheckSum cannot be blank!')
        self.get_args.add_argument('accid', type=str, required=True, location=['values'], help="accid cannot be blank!")
        self.get_args.add_argument('name', type=str, required=True, location=['values'], help="name cannot be blank!")
        self.get_args.add_argument('gender', type=int, default=0, location=['values'])
        self.get_args.add_argument('icon', type=str, default="", location=['values'])
        self.get_args.add_argument('sign', type=str, default="", location=['values'])
        self.get_args.add_argument('email', type=str, default="", location=['values'])
        self.get_args.add_argument('birth', type=str, default="", location=['values'])
        self.get_args.add_argument('mobile', type=str, default="", location=['values'])
        self.get_args.add_argument('ex', type=str, default="", location=['values'])
        self.args = self.get_args.parse_args()
    def post(self):
        data = {}
        data["accid"] = self.args.get("accid", "")
        data["name"] = self.args.get("name", "")
        data["gender"] = self.args.get("gender", 0)
        data["icon"] = self.args.get("icon", "")
        data["sign"] = self.args.get("sign", "")
        data["email"] = self.args.get("email", "")
        data["birth"] = self.args.get("birth", "")
        data["mobile"] = self.args.get("mobile", "")
        data["ex"] = self.args.get("ex", "")
        verify_md5 = hashlib.md5(urllib.urlencode(data)).hexdigest()
        verify_checksum = hashlib.sha1(APP_SERECT + self.args["Md5"] + self.args["Curtime"]).hexdigest()
        if verify_md5 == self.args["Md5"] and self.args["Checksum"] == verify_checksum :
            im = Im()
            if im.check_accid(data.get("accid", "")):
                print "----------------------"
                update_data = self.get_update_data(data)
                try:
                    flag = im.update_im_user_info(update_data)
                    msg = "update success" if flag else "update failed"
                except (BaseException), x:
                    return {"error_code": 500, "msg": x, "result": False}
                else:
                    return {"error_code": 200, "msg": msg, "result": flag}
            else:
                try:
                    flag = Im().add_im_user_info(data)
                    msg = "save success" if flag else "save failed"
                except (BaseException), x:
                    return {"error_code": 500, "msg": x, "result": False}
                else:
                    return {"error_code": 200, "msg": msg, "result": flag}

        return {"error_code": 2001, "msg": "no pass the check!"}


    def get_update_data(self, data={}):
        update_data = {}
        if data["accid"]:
            update_data["accid"] = data.get("accid", "")
        if data["name"]:
            update_data["name"] = data.get("name", "")
        if data["gender"]:
            update_data["gender"] = data.get("gender", 0)
        if data["icon"]:
            update_data["icon"] = data.get("icon", "")
        if data["sign"]:
            update_data["sign"] = data.get("sign", "")
        if data["email"]:
            update_data["email"] = data.get("email", "")
        if data["birth"]:
            update_data["birth"] = data.get("birth", "")
        if data["mobile"]:
            update_data["mobile"] = data.get("mobile", "")
        if data["ex"]:
            update_data["ex"] = data.get("ex", "")
        return update_data
