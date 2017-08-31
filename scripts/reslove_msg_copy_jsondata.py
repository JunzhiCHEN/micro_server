#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
sys.path.insert(0,'/Users/chenjunzhi/PYProject/my_scripts/micro_server')
import json
import datetime
from libs.db_conn import _mysql_config

db_im = _mysql_config["im"]["master"]

def insert_to_msg_info_table(event_type, conv_type, from_accid, to_account, from_client_type,
                             msg_type, msg_timestamp, from_device_id, from_nick, body, attach, t_members,
                             ext, source, msg_copy_id):
    result = db_im.insert("im_message_info",event_type=event_type,  conv_type=conv_type, from_accid=from_accid, to_account=to_account,
               from_client_type=from_client_type, msg_type=msg_type, msg_timestamp=msg_timestamp,
               from_device_id=from_device_id, from_nick=from_nick, body=body, attach=attach, t_members=t_members,
               ext=ext, source=source, msg_copy_id=msg_copy_id)
    print result

    return result


def resolve_json_data(msg_copy_id, json_data):
    msg_object = json.loads(json_data)

    event_type = msg_object.get("eventType", "")
    if event_type == "1":
        conv_type = msg_object.get("convType", "")
        from_accid = msg_object.get("fromAccount", "")
        to_account = msg_object.get("to", "")
        from_client_type = msg_object.get("fromClientType", "")
        msg_type = msg_object.get("msgType", "")

        msg_timestamp_str = msg_object.get("msgTimestamp", "")

        d = datetime.datetime.fromtimestamp(float(msg_timestamp_str) / 1000)
        msg_timestamp = d.strftime("%y-%m-%d %H:%M:%S")

        from_device_id = msg_object.get("fromDeviceId", "")
        from_nick = msg_object.get("fromNick", "")
        body = msg_object.get("body", "")  # .replace('"','\\"')

        attach = msg_object.get("attach", "")  # .replace('\\"','"').replace('"','\\"')
        t_members = msg_object.get("tMembers", "")  # .replace('"','\\"')

        ext = msg_object.get("ext", "")  # .replace('"','\\"')

        source = ""
        if ext:
            ext_obj = json.loads(ext)  # .replace('\\"','"'))
            source = ext_obj.get("v", "")

        result = insert_to_msg_info_table(event_type, conv_type, from_accid, to_account, from_client_type,
                                          msg_type, msg_timestamp, from_device_id, from_nick, body, attach,
                                          t_members, ext, source, msg_copy_id)
        return True
    return False

def get_max_msg_copy_id_in_msg_info():
    sql = '''
        select max(msg_copy_id) as msg_copy_id  from im_message_info
    '''
    result = db_im.query(sql)
    max_id = 0
    for one in result:
        if one["msg_copy_id"]:
            max_id = one["msg_copy_id"]
    return max_id

def get_msg_json_data():
    start_msg_copy_id = get_max_msg_copy_id_in_msg_info()
    sql = '''
        select id, json_data from im_message_copy where id>%d limit 1000
    '''% start_msg_copy_id
    result = db_im.query(sql)
    msg_list = []
    for one in result:
        flag = resolve_json_data(one["id"], one["json_data"])
        print flag


if __name__ == '__main__':
    max_id = get_max_msg_copy_id_in_msg_info()
    print max_id
    get_msg_json_data()