""" Port module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

import logging
import urllib3
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
        dellemc_ansible_vplex_utils as utils
from vplexapi.api import ExportsApi
from vplexapi.rest import ApiException
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = r'''
---
module: dellemc_vplex_port
version_added: '2.7'
short_description: Manage Ports on VPLEX Storage Object
description:
- Provisioning the storage port on VPLEX Storage System includes
  Get information about existing port,
  Enable existing port,
  Disable existing port
extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex
author: Sherene Jean Prathiba (sherene_jean_pratibh@dellteam.com)
        vplex.ansible@dell.com

options:
  cluster_name:
    description:
    - Name of the cluster
    type: str
    required: True

  port_name:
    description:
    - Name of the port
    type: str
    required: True

  enabled:
    description:
    - Enables/Disables the port
    type: bool

  state:
    description:
    - Presence of the port
    type: str
    choices: ["present", "absent"]
    required: True

'''

EXAMPLES = r'''
    - name: Get Port
      dellemc_vplex_port:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        port_name: "{{ port_name }}"
        state: "present"

    - name: Enable Port
      dellemc_vplex_port:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        port_name: "{{ port_name }}"
        enabled: true
        state: "present"

    - name: Disable Port
      dellemc_vplex_port:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{vplexpassword }}"
        cluster_name: "{{ cluster_name }}"
        port_name: "{{ port_name }}"
        enabled: false
        state: "present"

'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: bool

Port Details:
    description: Details of the port
    returned: For Get, Enable and Disable operation
    type: complex
    contains:
        director:
            description: Name of the director
            type: str
        director_id:
            description: The ID of the director where the port is exported
            type: str
        discovered_initiators:
            description: List of all initiator-ports visible from this port
            type: list
        enabled:
            description: Enabled status of the port
            type: bool
        export_status:
            description: Export status of the VPLEX port
            type: str
        exports:
            description: List of details of lun exported by the port
            type: list
        iscsi_name:
            description: ISCSI name of the port
            type: str
        name:
            description: Name of the port
            type: str
        node_wwn:
            description: node wwn for registering the port
            type: str
        port_wwn:
            description: WWN of the port to register
            type: str
'''

LOG = utils.get_logger('dellemc_vplex_port', log_devel=logging.INFO)
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexPort():  # pylint:disable=R0902
    """Class wth port operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_port_parameters())

        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
        )

        # Check for Python vplexapi sdk
        if HAS_VPLEXAPI_SDK is False:
            self.module.fail_json(msg="Ansible modules for VPLEX require "
                                      "the vplexapi python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")

        self.cl_name = self.module.params['cluster_name']
        self.port_nm = self.module.params['port_name']
        self.enabled = self.module.params['enabled']
        self.state = self.module.params['state']

        # Create the configuration instance to communicate with
        # vplexapi
        self.client = utils.config_vplexapi(self.module.params)

        # Validating the user inputs
        if isinstance(self.client, tuple):
            err_code, msg = self.client  # pylint: disable=W0612
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Checking if the cluster is reachable
        (status, msg) = utils.verify_cluster_name(self.client, self.cl_name)
        if status != 200:
            if "Resource not found" in msg:
                msg = "Could not find resource {0}".format(self.cl_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        # Create an instance to PortApi to communicate with
        # vplexapi
        self.port = ExportsApi(api_client=self.client)

        # result is a dictionary that contains changed status and
        # port details
        self.result = {"changed": False, "port_details": {}}

    def get_port(self):
        """
        Get port details
        """
        try:
            port_details = self.port.get_port(self.cl_name, self.port_nm)
            LOG.info("Obtained the port %s details in %s",
                     self.port_nm, self.cl_name)
            LOG.debug("Port Details:\n%s", port_details)
            return port_details
        except ApiException as err:
            err_msg = ("Could not get the Port {0} Details in {1} due to"
                       " error: {2}".format(
                           self.port_nm, self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None

    def en_dis_port(self):
        """
        Enable or Disable a port
        """
        en_dis = {'True': 'Enabled', 'False': 'Disabled'}
        try:
            port_patch_payload = [{'op': 'replace',
                                   'path': '/enabled',
                                   'value': self.enabled}]
            port_details = self.port.patch_port(self.cl_name, self.port_nm,
                                                port_patch_payload)
            LOG.info("Moved the port %s to %s state successfully in %s",
                     self.port_nm, en_dis[str(self.enabled)], self.cl_name)
            LOG.debug("Port Details:\n%s", port_details)
            return port_details
        except ApiException as err:
            err_msg = ("Could not set the Port {0} to {1} state in {2} due to"
                       " error: {3}".format(
                           self.port_nm, en_dis[str(self.enabled)],
                           self.cl_name, utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def perform_module_operation(self):
        """
        Perform different actions on the port based on user parameters
        specified in the playbook
        """
        port_details = None
        changed = False

        # Get port details
        port_details = self.get_port()
        if port_details is None and self.state == 'absent':
            msg = "Could not get the details of the port {0} from {1}"
            msg = msg.format(self.port_nm, self.cl_name)
            LOG.error(msg)
        elif port_details is None and self.state == 'present':
            msg = "Could not get the details of the port {0} from {1}"
            msg = msg.format(self.port_nm, self.cl_name)
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        elif port_details and self.enabled is not None:
            if self.enabled != port_details.enabled:
                port_details = self.en_dis_port()
                changed = True

        # Finally update the module changed state details
        self.result["changed"] = changed
        if port_details:
            port_details = utils.serialize_content(port_details)
        self.result["port_details"] = port_details
        self.module.exit_json(**self.result)


def get_vplex_port_parameters():
    """This method provide parameter required for the ansible port
    module on VPLEX"""
    return dict(
        cluster_name=dict(required=True, type='str'),
        port_name=dict(required=True, type='str'),
        enabled=dict(required=False, type='bool'),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """Create VplexPort object and perform action on it
        based on user input from playbook"""
    obj = VplexPort()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()