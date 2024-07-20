 #!/usr/bin/env python

import os
from configparser import ConfigParser
from exceptions import *
from requests_toolbelt.adapters.ssl import SSLAdapter
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests
import urllib.parse
import socketio


class Codequiry(object):
    def __init__(self,
                 api_key):
        if not api_key:
            raise ValueError("API Key is required and cannot be null")

        self.api_key = api_key

        parser = ConfigParser()
        parser.read('config.ini')
        self.API_BASE_URL = parser.get('config', 'api_base_url')
        self.API_UPLOAD_URL = parser.get('config', 'api_upload_url')
        self.SOCKETS_BASE_URL = parser.get('config', 'sockets_base_url')
        self.SDK_VERSION = parser.get('config', 'sdk_version')

        self.base_headers = {
            'apikey': api_key,
            'Content-Type': 'application/json'
        }

        session = requests.Session()
        session.mount(self.API_BASE_URL, SSLAdapter())
        session.headers = self.base_headers
        self.session = session

    def account(self):
        return self.__post('account', {})

    def checks(self):
        return self.__post('checks', {})

    def create_check(self, check_name, lang):
        return self.__post('check/create', {
            'name': check_name,
            'language': lang
        })

    def check_listen(self, job_id, callback_fn):
        if job_id == 0:
            return

        sio = socketio.Client()
        sio.connect(self.SOCKETS_BASE_URL)

        @sio.event
        def connect():
            sio.emit('job-check', {'jobid': job_id})

        @sio.on('job-status')
        def on_message(data):
            callback_fn(data)
            if data.error == 1 or data.percent == 100:
                sio.disconnect()

    def start_check(self, check_id):
        return self.__post('check/start', {
            'check_id': check_id
        })

    def get_check(self, check_id):
        return self.__post('check/get', {
            'check_id': check_id
        })

    def get_overview(self, check_id):
        return self.__post('check/overview', {
            'check_id': check_id
        })

    def get_results(self, check_id, sid):
        return self.__post('check/results', {
            'check_id': check_id,
            'submission_id': sid
        })

    def upload_file(self, check_id, file_path):
        _, file_name = os.path.split(file_path)
        mp_enc = MultipartEncoder(
            fields={
                'check_id': str(check_id),
                'file': (file_name, open(file_path, 'rb'))
            }
        )
        headers = self.base_headers
        headers['Content-Type'] = mp_enc.content_type
        response = requests.post(self.API_UPLOAD_URL, data=mp_enc, headers=headers).content
        return response

    def __post(self, url, data, headers=None):
        if headers is None:
            headers = self.base_headers
        try:
            response = self.session.request(
                method='POST',
                url=urllib.parse.urljoin(self.API_BASE_URL, url) if not url.startswith("http") else url,
                data=json.dumps(data),
                headers=headers
            )
        except Exception as e:
            raise CodequiryAPIException({
                'error': 'Could not connect to the server: {}'.format(e.args[0])
            })
        try:
            json_body = json.loads(response.content)
        except ValueError as e:
            raise CodequiryAPIException({
                'Invalid response: {}'.format(e.args[0])
            })

        return json_body
