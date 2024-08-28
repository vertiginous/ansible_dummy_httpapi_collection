#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) 2024 [Your Name]
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: dummy_api_smtp
short_description: Manage SMTP configuration via REST API
description:
    - This module manages the SMTP configuration of a target system by interacting with its REST API.
    - It retrieves the current SMTP settings, compares them with the desired configuration, and updates them if necessary.
author:
  - Gordon Thiesfeld (gordon.thiesfeld@em.com)
options:
    enabled:
        description:
            - Enables or disables the SMTP service.
        type: bool
        required: false
    encrypted:
        description:
            - Enables or disables encryption for SMTP communication.
        type: bool
        required: false
    password:
        description:
            - The password for the SMTP user.
            - This value is not logged for security reasons.
        type: str
        required: false
        no_log: true
    port:
        description:
            - The port number used for SMTP communication.
        type: int
        required: false
    recipients:
        description:
            - A comma-separated list of recipient email addresses.
        type: str
        required: false
    sender_email:
        description:
            - The sender email address to be used for outgoing SMTP emails.
        type: str
        required: false
    server:
        description:
            - The SMTP server address.
        type: str
        required: false
    user:
        description:
            - The username used to authenticate with the SMTP server.
        type: str
        required: false
extends_documentation_fragment:
    - ansible.netcommon.httpapi
'''

EXAMPLES = '''
- name: Update SMTP Configuration on devapi device
  hosts: all
  connection: httpapi
  gather_facts: false
  tasks:
    - name: Configure SMTP settings
      local.dummy.dummy_smtp:  # Replace with the actual name of your module
        enabled: true
        encrypted: true
        port: 25
        recipients:
          - "hwadmin@domain.com"
          - "swadmin@domain.com"
          - "on-call@domain.com"
        sender_email: "root@dummy-device.domain.com"
        server: "smtp-server.domain.com"
## In inventory:
  vars:
    ansible_user: admin
    ansible_password: password
    ansible_connection: httpapi
    ansible_network_os: dummy
'''

RETURN = '''
changed:
    description: Whether the SMTP configuration was changed.
    type: bool
    returned: always
    sample: true
original_message:
    description: The original SMTP configuration retrieved from the API before any changes.
    type: str
    returned: always
message:
    description: A message indicating the result of the module's execution.
    type: str
    returned: always
    sample: "SMTP configuration updated"
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

def main():
    module_args = dict(
        enabled=dict(type='bool', required=False),
        encrypted=dict(type='bool', required=False),
        password=dict(type='str', required=False, no_log=True),
        port=dict(type='int', required=False),
        recipients=dict(type='str', required=False),
        sender_email=dict(type='str', required=False),
        server=dict(type='str', required=False),
        user=dict(type='str', required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )
  
    result = {
        'changed': False,
        'original_message': '',
        'message': ''
    }

    # Create HTTPAPI connection
    connection = Connection(module._socket_path)

    # Get the current SMTP configuration from the API
    current_smtp_config = connection.get('/api/v1/smtp')
    result['original_message'] = current_smtp_config

    # Desired SMTP configuration from the playbook
    desired_smtp_config = {
        'enabled': module.params['enabled'],
        'encrypted': module.params['encrypted'],
        'password': module.params['password'],
        'port': module.params['port'],
        'recipients': module.params['recipients'],
        'sender_email': module.params['sender_email'],
        'server': module.params['server'],
        'user': module.params['user']
    }

    # Compare the current configuration with the desired configuration
    if current_smtp_config != desired_smtp_config:
        if not module.check_mode:
            # Send a PUT request to update the SMTP configuration
            connection.put('/api/v1/smtp', data=desired_smtp_config)
            result['changed'] = True
            result['message'] = 'SMTP configuration updated'
        else:
            result['changed'] = True
            result['message'] = 'SMTP configuration would be updated'
    else:
        result['message'] = 'SMTP configuration is already up to date'

    module.exit_json(**result)

if __name__ == '__main__':
    main()
