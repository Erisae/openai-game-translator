#!/usr/bin/python3
# https://console.xfyun.cn/services/ost
# -*- coding:utf-8 -*-
import seve_file
import requests
import datetime
import hashlib
import base64
import hmac
import json
import os
import re

path_pwd = os.path.split(os.path.realpath(__file__))[0]
os.chdir(path_pwd)


# create and query
class get_result(object):
    def __init__(self, appid, apikey, apisecret):
        # POST request
        self.Host = "ost-api.xfyun.cn"
        self.RequestUriCreate = "/v2/ost/pro_create"
        self.RequestUriQuery = "/v2/ost/query"
        # url setting
        if re.match("^\d", self.Host):
            self.urlCreate = "http://" + self.Host + self.RequestUriCreate
            self.urlQuery = "http://" + self.Host + self.RequestUriQuery
        else:
            self.urlCreate = "https://" + self.Host + self.RequestUriCreate
            self.urlQuery = "https://" + self.Host + self.RequestUriQuery
        self.HttpMethod = "POST"
        self.APPID = appid
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"
        self.UserName = apikey
        self.Secret = apisecret

        # current time setting
        cur_time_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(cur_time_utc)
        # test file setting
        self.BusinessArgsCreate = {
            "language": "zh_cn",
            "accent": "mandarin",
            "language_type" : 1,
            "domain": "pro_ost_ed",
            # "callback_url": "http://IP:port/xxx/"
        }

    def img_read(self, path):
        with open(path, 'rb') as fo:
            return fo.read()

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).
        The supplied date must be in UTC.
        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest, uri):
        signature_str = "host: " + self.Host + "\n"
        signature_str += "date: " + self.Date + "\n"
        signature_str += self.HttpMethod + " " + uri \
                         + " " + self.HttpProto + "\n"
        signature_str += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode('utf-8')),
                             bytes(signature_str.encode('utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data, uri):
        digest = self.hashlib_256(data)
        sign = self.generateSignature(digest, uri)
        auth_header = 'api_key="%s",algorithm="%s", ' \
                      'headers="host date request-line digest", ' \
                      'signature="%s"' \
                      % (self.UserName, self.Algorithm, sign)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": auth_header
        }
        return headers

    def get_create_body(self, fileurl):
        post_data = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgsCreate,
            "data": {
                "audio_src": "http",
                "audio_url": fileurl,
                "encoding": "raw"
            }
        }
        body = json.dumps(post_data)
        return body

    def get_query_body(self, task_id):
        post_data = {
            "common": {"app_id": self.APPID},
            "business": {
                "task_id": task_id,
            },
        }
        body = json.dumps(post_data)
        return body

    def call(self, url, body, headers):

        try:
            response = requests.post(url, data=body, headers=headers, timeout=8)
            status_code = response.status_code
            interval = response.elapsed.total_seconds()
            if status_code != 200:
                info = response.content
                return info
            else:
                resp_data = json.loads(response.text)
                return resp_data
        except Exception as e:
              print("Exception ：%s" % e)

    def task_create(self):
        body = self.get_create_body(fileurl)
        headers_create = self.init_header(body, self.RequestUriCreate)
        task_id = gClass.call(self.urlCreate, body, headers_create)
        # print(task_id)
        return task_id

    def task_query(self, task_id):
        if task_id:
            body = self.get_create_body(fileurl)
            query_body = self.get_query_body(task_id)
            headers_query = self.init_header(body, self.RequestUriQuery)
            result = gClass.call(self.urlQuery, query_body, headers_query)
            return result

    def get_fileurl(self):
        # file upload
        api = seve_file.SeveFile(app_id=appid, api_key=apikey, api_secret=apisecret, upload_file_path=file_path)
        file_total_size = os.path.getsize(file_path)
        if file_total_size < 31457280:
            fileurl = api.gene_params('/upload')['data']['url']
        else:
            fileurl = api.gene_params('/mpupload/upload')
        return fileurl

    def get_result(self):
        task_id = gClass.task_create()['data']['task_id']
        while True:
            result = gClass.task_query(task_id)
            if isinstance(result, dict) and result['data']['task_status'] != '1' and result['data'][
                'task_status'] != '2':
                # with open("./test.json", 'w', encoding ='utf8') as json_file:
                #     json.dump(result, json_file, indent=6, ensure_ascii=False)

                print("transcription success···")
                for a in result["data"]["result"]["lattice"][0]["json_1best"]["st"]["rt"][0]["ws"]:
                    print(a["cw"][0]["w"], end="")
                print()
                break
            elif isinstance(result, bytes):
                print("transcription error···", result)
                break


if __name__ == '__main__':
    # appod apikey and apisecret from xunfeo
    appid = ""
    apikey = ""
    apisecret = ""
    file_path = r"./audio/audio_sample_little.wav"


    gClass = get_result(appid, apikey, apisecret)
    fileurl = gClass.get_fileurl()
    gClass.get_result()
