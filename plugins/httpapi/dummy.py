from ansible.plugins.httpapi import HttpApiBase
from urllib.parse import urljoin
from functools import wraps
import json


DOCUMENTATION = '''
---
module: dummy
author:
  - Gordon Thiesfeld (gordon.thiesfeld@em.com)

short_description: HTTPAPI Plugin for interacting with a Dummy REST API
description:
  - This plugin provides methods to interact with a Dummy REST API.
  - It supports standard CRUD operations (GET, PUT, DELETE) and handles authentication.
options:
'''

EXAMPLES = '''
- name: Login to the API and perform a GET request
  ansible.builtin.httpapi:
  connection: httpapi
  tasks:
    - name: Get user details
      ansible.builtin.uri:
        url: /api/v1/user/details
        method: GET
        headers:
          x-auth-token: "{{ ansible_httpapi_token }}"
'''

RETURN = '''
response:
  description: The HTTP response received from the API.
  type: dict
  returned: always
  sample: 
    {
      "status": "success",
      "data": {}
    }
'''

EMPTY_DATA = object()

class HttpApi(HttpApiBase):

    def send_request(self, path, data=EMPTY_DATA, method="GET", **message_kwargs):
        # set headers for body
        headers = {'Accept-Encoding': 'application/json'}
        if not data or data == EMPTY_DATA:
            data = {}
        else:
            headers['Content-Type'] = 'application/json'

        data = json.dumps(data).encode('utf-8')  # Ensure data is bytes

        # actually send the connection
        response, response_data = self.connection.send(path=path, data=data, method=method, headers=headers)

        # Parse the response data
        response_data_serialisable = json.loads(response_data.read().decode("utf-8"))

        # Return a tuple
        return response, response_data_serialisable

    def login(self, username, password):
        path = '/api/v1/login'
        data = {
            'username': username,
            'password': password
        }
        response, response_data = self.send_request(path, data=data, method='POST')
        token = response_data.get('token')
        refresh_token = response_data.get('refreshToken')
        self.connection._auth = {'x-auth-token': token, 'refresh-token': refresh_token}  

    def logout(self):
        path = '/api/v1/logout'
        headers = {
            'x-auth-token': self.connection._auth['x-auth-token'],
            'refresh-token': self.connection._auth['refresh-token']
        }
        response, response_data = self.send_request(path, headers=headers, method='POST')
        return response_data

    def get(self, path):
        response, response_data = self.send_request(path, method='GET')
        return response_data

    def put(self, path, data):
        response, response_data = self.send_request(path, data=data, method='PUT')
        return response_data

    def delete(self, path):
        response, response_data = self.send_request(path, method='DELETE')
        return response_data
