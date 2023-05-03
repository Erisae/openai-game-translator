# -*- coding:utf-8 -*-

import json
import math
import os
import time
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlparse
import requests
from urllib3 import encode_multipart_formdata

lfasr_host = "http://upload-ost-api.xfyun.cn/file"
# request API Name
api_init = "/mpupload/init"
api_upload = "/upload"
api_cut = "/mpupload/upload"
api_cut_complete = "/mpupload/complete"
api_cut_cancel = "/mpupload/cancel"
# File chunk size 5MB
file_piece_sice = 5242880


# file upload
class SeveFile:
    def __init__(self, app_id, api_key, api_secret, upload_file_path):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.request_id = "0"
        self.upload_file_path = upload_file_path
        self.cloud_id = "0"

    # request_id processing
    def get_request_id(self):
        return time.strftime("%Y%m%d%H%M")

    # header processing
    def hashlib_256(self, data):
        m = hashlib.sha256(bytes(data.encode(encoding="utf-8"))).digest()
        digest = "SHA-256=" + base64.b64encode(m).decode(encoding="utf-8")
        return digest

    # header processing
    def assemble_auth_header(
        self, requset_url, file_data_type, method="", api_key="", api_secret="", body=""
    ):
        u = urlparse(requset_url)
        host = u.hostname
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        digest = "SHA256=" + self.hashlib_256("")
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1\ndigest: {}".format(
            host, date, method, path, digest
        )
        signature_sha = hmac.new(
            api_secret.encode("utf-8"),
            signature_origin.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding="utf-8")
        authorization = 'api_key="%s", algorithm="%s", headers="%s", signature="%s"' % (
            api_key,
            "hmac-sha256",
            "host date request-line digest",
            signature_sha,
        )
        headers = {
            "host": host,
            "date": date,
            "authorization": authorization,
            "digest": digest,
            "content-type": file_data_type,
        }
        return headers

    # post request api
    def call(self, url, file_data, file_data_type):
        api_key = self.api_key
        api_secret = self.api_secret
        headerss = self.assemble_auth_header(
            url,
            file_data_type,
            method="POST",
            api_key=api_key,
            api_secret=api_secret,
            body=file_data,
        )
        try:
            resp = requests.post(url, headers=headerss, data=file_data, timeout=8)
            # print("Chunk upload success. STATUS：", resp.status_code, resp.text)
            return resp.json()
        except Exception as e:
            print("Chunk upload failed! Exception :%s" % e)
            return False

    # chunk upload complete
    def upload_cut_complete(self, body_dict):
        file_data_type = "application/json"
        url = lfasr_host + api_cut_complete
        fileurl = self.call(url, json.dumps(body_dict), file_data_type)
        fileurl = fileurl["data"]["url"]
        # print("upload complete")
        return fileurl

    def gene_params(self, apiname):
        appid = self.app_id
        request_id = self.get_request_id()
        upload_file_path = self.upload_file_path
        cloud_id = self.cloud_id
        body_dict = {}
        # api to upload file
        if apiname == api_upload:
            try:
                with open(upload_file_path, mode="rb") as f:
                    file = {
                        "data": (upload_file_path, f.read()),
                        "app_id": appid,
                        "request_id": request_id,
                    }
                    # print('File：', upload_file_path, ' File size：', os.path.getsize(upload_file_path))
                    encode_data = encode_multipart_formdata(file)
                    # print("----",encode_data)
                    file_data = encode_data[0]
                    file_data_type = encode_data[1]
                url = lfasr_host + api_upload
                fileurl = self.call(url, file_data, file_data_type)
                # print("Upload params",file_data)
                return fileurl
            except FileNotFoundError:
                print("Sorry!The file " + upload_file_path + " can't find.")
            # api preprocess
        elif apiname == api_init:
            body_dict["app_id"] = appid
            body_dict["request_id"] = request_id
            body_dict["cloud_id"] = cloud_id
            url = lfasr_host + api_init
            file_data_type = "application/json"
            return self.call(url, json.dumps(body_dict), file_data_type)
        elif apiname == api_cut:
            # preprocess
            upload_prepare = self.prepare_request()
            if upload_prepare:
                upload_id = upload_prepare["data"]["upload_id"]
            # chunk upload
            self.do_upload(upload_file_path, upload_id)
            body_dict["app_id"] = appid
            body_dict["request_id"] = request_id
            body_dict["upload_id"] = upload_id
            # chunk upload complete
            fileurl = self.upload_cut_complete(body_dict)
            # print("chunk upload url：",fileurl)
            return fileurl

    # preprocess
    def prepare_request(self):
        return self.gene_params(apiname=api_init)

    # chunk upload
    def do_upload(self, file_path, upload_id):
        file_total_size = os.path.getsize(file_path)
        chunk_size = file_piece_sice
        chunks = math.ceil(file_total_size / chunk_size)
        appid = self.app_id
        request_id = self.get_request_id()
        upload_file_path = self.upload_file_path
        slice_id = 1

        # print('File：', file_path, ' File size：', file_total_size, ' Chunk size：', chunk_size, ' Chunk num：', chunks)

        with open(file_path, mode="rb") as content:
            while slice_id <= chunks:
                # print('chunk',slice_id )
                if (slice_id - 1) + 1 == chunks:
                    current_size = file_total_size % chunk_size
                else:
                    current_size = chunk_size

                file = {
                    "data": (upload_file_path, content.read(current_size)),
                    "app_id": appid,
                    "request_id": request_id,
                    "upload_id": upload_id,
                    "slice_id": slice_id,
                }

                encode_data = encode_multipart_formdata(file)
                file_data = encode_data[0]
                file_data_type = encode_data[1]
                url = lfasr_host + api_cut

                resp = self.call(url, file_data, file_data_type)
                count = 0
                while not resp and (count < 3):
                    # print("retry upload")
                    resp = self.call(url, file_data, file_data_type)
                    count = count + 1
                    time.sleep(1)
                if not resp:
                    quit()
                slice_id = slice_id + 1
