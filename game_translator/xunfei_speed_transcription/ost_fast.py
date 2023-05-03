"""
This module provides xunfei api linking function

Classes:
- xf_transcriptor

Author: Yuhan Xia
Copyright: Copyright (c) 2023
License: Apache-2.0
Version: 2.0
"""
import datetime
import hashlib
import base64
import hmac
import json
import os
import re
import requests

from .seve_file import SeveFile

LANGUAGE_MAPPING = {"english": "en_us", "chinese": "zh_cn"}


# create and query
class xf_transcriptor:
    """
    A class representing a xf_transcriptor.

    Attributes:
    """

    def __init__(self, appid, apikey, apisecret, file_path, input_language):
        # POST request
        self.Host = "ost-api.xfyun.cn"
        self.RequestUriCreate = "/v2/ost/pro_create"
        self.RequestUriQuery = "/v2/ost/query"
        # url setting
        if re.match(r"^\d", self.Host):
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
        self.FilePath = file_path

        # current time setting
        cur_time_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(cur_time_utc)
        # test file setting
        self.BusinessArgsCreate = {
            "language": LANGUAGE_MAPPING[input_language],
            "accent": "mandarin",
            "language_type": 1,
            "domain": "pro_ost_ed",
        }

    def hashlib_256(self, res):
        """
        A function to .

        """
        m = hashlib.sha256(bytes(res.encode(encoding="utf-8"))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding="utf-8")
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).
        The supplied date must be in UTC.
        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (
            weekday,
            dt.day,
            month,
            dt.year,
            dt.hour,
            dt.minute,
            dt.second,
        )

    def generateSignature(self, digest, uri):
        """
        A function to generate signature

        """
        signature_str = "host: " + self.Host + "\n"
        signature_str += "date: " + self.Date + "\n"
        signature_str += self.HttpMethod + " " + uri + " " + self.HttpProto + "\n"
        signature_str += "digest: " + digest
        signature = hmac.new(
            bytes(self.Secret.encode("utf-8")),
            bytes(signature_str.encode("utf-8")),
            digestmod=hashlib.sha256,
        ).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding="utf-8")

    def init_header(self, data, uri):
        """
        A function to init header

        """
        digest = self.hashlib_256(data)
        sign = self.generateSignature(digest, uri)
        auth_header = (
            'api_key="%s",algorithm="%s", '
            'headers="host date request-line digest", '
            'signature="%s"' % (self.UserName, self.Algorithm, sign)
        )
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": auth_header,
        }
        return headers

    def get_create_body(self):
        """
        A function to get create body

        """
        post_data = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgsCreate,
            "data": {"audio_src": "http", "audio_url": self.fileurl, "encoding": "raw"},
        }
        body = json.dumps(post_data)
        return body

    def get_query_body(self, task_id):
        """
        A function to get query body

        """
        post_data = {
            "common": {"app_id": self.APPID},
            "business": {
                "task_id": task_id,
            },
        }
        body = json.dumps(post_data)
        return body

    def call(self, url, body, headers):
        """
        A function to call xunfei

        """
        try:
            response = requests.post(url, data=body, headers=headers, timeout=8)
            status_code = response.status_code
            if status_code != 200:
                info = response.content
                return info
            else:
                resp_data = json.loads(response.text)
                return resp_data
        except Exception as e:
            print("Exception :%s" % e)

    def task_create(self):
        """
        A function to create task

        """
        body = self.get_create_body()
        headers_create = self.init_header(body, self.RequestUriCreate)
        task_id = self.call(self.urlCreate, body, headers_create)
        return task_id

    def task_query(self, task_id):
        """
        A function to query task

        """
        if task_id:
            body = self.get_create_body()
            query_body = self.get_query_body(task_id)
            headers_query = self.init_header(body, self.RequestUriQuery)
            result = self.call(self.urlQuery, query_body, headers_query)
            return result

    def get_fileurl(self):
        """
        A function to get file url

        """
        # file upload
        api = SeveFile(
            app_id=self.APPID,
            api_key=self.UserName,
            api_secret=self.Secret,
            upload_file_path=self.FilePath,
        )
        file_total_size = os.path.getsize(self.FilePath)
        if file_total_size < 31457280:
            self.fileurl = api.gene_params("/upload")["data"]["url"]
        else:
            self.fileurl = api.gene_params("/mpupload/upload")

    def get_result(self):
        """
        A function to get result

        """
        task_id = self.task_create()["data"]["task_id"]
        sentence = ""
        while True:
            result = self.task_query(task_id)
            if (
                isinstance(result, dict)
                and result["data"]["task_status"] != "1"
                and result["data"]["task_status"] != "2"
            ):
                # with open("./test.json", 'w', encoding ='utf8') as json_file:
                #     json.dump(result, json_file, indent=6, ensure_ascii=False)

                print("transcription success...")
                for a in result["data"]["result"]["lattice"][0]["json_1best"]["st"][
                    "rt"
                ][0]["ws"]:
                    sentence += a["cw"][0]["w"]
                print(sentence)
                break
            elif isinstance(result, bytes):
                print("transcription error···", result)
                break
        return sentence
