from libs.db_conn import _mysql_config
import MySQLdb

class Im(object):
    def __init__(self):
        self.db_master = _mysql_config["im"]["master"]
        pass

    def save_msg_to_db(self, msg):

        result = self.db_master.insert("im_message_copy", json_data=msg)
        return result
    def add_im_user_info(self, data={}):

        result = self.db_master.insert("im_user_info", accid=data.get("accid",""),
                 name=data.get("name", ""), icon=data.get("icon", ""),
                 gender=data.get("gender", ""), email= data.get("email", ""),
                 birth=data.get("birth", ""), mobile=data.get("mobile", ""),
                 sign=data.get("sign", ""), ex=data.get("ex", "")
                 )
        if result:
            return True
        return False
    def update_im_user_info(self, data={}):
        if not data:
            return False
        set = ""
        for k,v in data.items():

            if set:
                if k != "gender" and k != 'accid':
                    value = MySQLdb.escape_string(v)
                    set = set + ", %s = '%s' " % (k,value)
                if k =="gender":
                    set = set + ", %s = %d " % (k, v)
            else:
                if k != "gender" and k != 'accid':
                    value = MySQLdb.escape_string(v)
                    set = set + "set %s = '%s' " % (k, value)
                if k == "gender":
                    set = set + "set %s = %d " % (k, v)
        sql = "update im_user_info "+ set + " where accid ='%s' " % data.get("accid", "")
        result = self.db_master.query(sql)
        if result:
            return True
        return False

    def check_accid(self, accid):
        db = _mysql_config["im"]["slave"]
        sql = '''
            select accid from im_user_info where accid='%s'
        ''' % MySQLdb.escape_string(accid)
        result = db.query(sql)
        if len(result) > 0:
            return True
        return False



if __name__ == '__main__':
    result = Im().save_msg_to_db("hahah")
    print result