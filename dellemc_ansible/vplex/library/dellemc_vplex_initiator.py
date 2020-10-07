""" Initiator module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

import logging
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
        dellemc_ansible_vplex_utils as utils
from vplexapi.rest import ApiException
from vplexapi.api import ExportsApi
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_initiator
version_added: '2.7'
short_description: Manage Initiators on VPLEX Storage Object
description:
- Provisoning the initiator on VPLEX Storage System includes
  Register an initiator,
  Unregister an initiator,
  Get information about initiator (either registered/unregistered),
  Rename a registered initiator name,
  Rediscover Initiators
extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex
author: Mohana Priya Sivalingam (mohana_priya_sivalin@dellteam.com)
        vplex.ansible@dell.com
options:
  cluster_name:
    description:
    - Name of the cluster
    type: str
    required: True

  initiator_name:
    description:
    - Name of the initiator (Registered/Unregistered)
    type: str

  new_initiator_name:
    description:
    - Name of the initiator to be registered or renamed
    type: str

  iscsi_name:
    description:
    - ISCSI name of the port required for registering an initiator
      Mutually exclusive with port_wwn
    type: str

  port_wwn:
    description:
    - Port WWN of FC port required for registering an initiator
      Mutually exclusive with iscsi_name
    type: str

  host_type:
    description:
    - Host type for registering the port
    type: str
    choices: ["default", "hpux", "sun-vcs", "aix", "recoverpoint"]
    default: "default"

  registered:
    description:
    - State of the initiator used for Register/Unregister
    type: bool
    required: True
    choices: [True, False]

  state:
    description:
    - The presence of initiator
    type: str
    required: True
    choices: ["present", "absent"]

Notes:
- iscsi_name or port_wwn is required to register an initiator
- iscsi_name and port_wwn are mutually exclusive
'''

EXAMPLES = r'''
    - name: Register Initiator with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        initiator_name: "{{ initiator_name }}"
        port_wwn: "{{ port_wwn }}"
        host_type: "hpux"
        registered: true
        state: "present"

    - name: Get details of an Initiator with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        port_wwn: "{{ port_wwn }}"
        state: "present"

    - name: Get details of an Initiator with initiator_name
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        initiator_name: "{{ initiator_name }}"
        state: "present"

    - name: Rename a registered Initiator name with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        port_wwn: "{{ port_wwn }}"
        new_initiator_name: "{{ new_initiator_name }}"
        state: "present"

    - name: Rename a registered Initiator name with initiator_name
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        initiator_name: "{{ initiator_name }}"
        new_initiator_name: "{{ new_initiator_name }}"
        state: "present"

    - name: Unregister Initiator with port_wwn
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        port_wwn: "{{ port_wwn }}"
        registered: false
        state: "present"

    - name: Unregister Initiator with initiator_name
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        initiator_name: "{{ initiator_name }}"
        registered: false
        state: "present"

    - name: Rediscover Initiators
      dellemc_vplex_initiator:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "{{ cluster_name }}"
        state: "present"
'''

RETURN = r'''
changed:
    description: Status of the operation
    returned: End of all the operations
    type: boolean

Initiator Details:
    description: Details of the initiator
    returned: For Get, Add, Rename and Rediscover operations
    type: complex
    contains:
        bandwidth_limit:
            description: Bandwidth limit of the initiator port
            type: str
        iops_limit:
            description: IOPS limit of the initiator port
            type: int
        iscsi_name:
            description: iscsi_name of the port
            type: str
        name:
            description: Name of the initiator
            type: str
        node_wwn:
            description: Unique network identifier for the HBA's interface card
            type: str
        port_wwn:
            description: Unique network identifier for the port
            type: str
        target_ports:
            description: List of VPLEX ports visible to initiator
            type: list
        type:
            description: Host operating system
            type: str
'''

LOG = utils.get_logger('dellemc_vplex_initiator', log_devel=logging.INFO)
HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexInitiator():    # pylint:disable=R0902
    """Class with initiator operations"""

    def __init__(self):
        """Define all parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_initiator_parameters())

        mutually_exclusive = [
            ['iscsi_name', 'port_wwn']
        ]

        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
            mutually_exclusive=mutually_exclusive
        )

        # Check for Python vplexapi sdk
        if HAS_VPLEXAPI_SDK is False:
            self.module.fail_json(msg="Ansible modules for VPLEX require "
                                      "the vplexapi python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")

        self.cl_name = self.module.params['cluster_name']

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

        # Create an instance to InitiatorApi to communicate with
        # vplexapi
        self.initr = ExportsApi(api_client=self.client)

        # Module parameters
        self.init_name = self.module.params['initiator_name']
        self.new_init_name = self.module.params['new_initiator_name']
        self.port_wwn = self.module.params['port_wwn']
        self.iscsi_name = self.module.params['iscsi_name']
        self.registered = self.module.params['registered']
        self.temp_initiator = None
        self.flag = 0
        self.reg_flag = 0
        self.unreg_flag = 0
        self.rename_flag = 0

        # result is a dictionary that contains changed status and
        # initiator details
        self.result = {"changed": False, "initiator_details": {}}

    def get_initiator(self, initiator_name):
        """
        Get initiator port details
        """
        try:
            initiator_details = self.initr.get_initiator_port(
                self.cl_name, initiator_name)
            LOG.info("Got initiator details %s from %s", initiator_name,
                     self.cl_name)
            LOG.debug("Initiator Details:\n%s", initiator_details)
            return initiator_details
        except ApiException as err:
            err_msg = ("Could not get initiator {0} from {1} due to"
                       " error: {2}".format(initiator_name, self.cl_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None

    def rename_initiator(self, initiator_name, new_initiator_name):
        """
        Rename the initiator port
        """
        try:
            initiator_patch_payload = [{'op': 'replace',
                                        'path': '/name',
                                        'value': new_initiator_name}]
            initiator_details = self.initr.patch_initiator_port(
                self.cl_name, initiator_name, initiator_patch_payload)
            LOG.info("Renamed the initiator %s to %s in %s", initiator_name,
                     new_initiator_name, self.cl_name)
            LOG.debug("Initiator Details:\n%s", initiator_details)
            return initiator_details
        except ApiException as err:
            err_msg = ("Could not rename initiator {0} to {1} in {2} due to"
                       " error: {3}".format(initiator_name, new_initiator_name,
                                            self.cl_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def rediscover_initiator(self):
        """
        Rediscover initiator ports
        """
        try:
            initiator_details = self.initr.rediscover_initiator_ports(
                self.cl_name)
            LOG.info("Rediscovered initiators from %s", self.cl_name)
            LOG.debug("Initiator Details:\n%s", initiator_details)
            return initiator_details
        except ApiException as err:
            err_msg = ("Could not discover initiators from {0} due to"
                       " error: {1}".format(self.cl_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def unregister_initiator(self, initiator_name):
        """
        Unregister an initiator port
        """
        try:
            self.initr.unregister_initiator_port(
                self.cl_name, initiator_name)
            LOG.info("Unregistered initiator %s from %s", initiator_name,
                     self.cl_name)
            return True
        except ApiException as err:
            err_msg = ("Could not unregister initiator {0} from {1} due to"
                       " error: {2}".format(initiator_name, self.cl_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def register_initiator(self, initiator_payload):
        """
        Register an initiator port either with iscsi_name or port_wwn
        """
        try:
            det = self.initr.register_initiator_port(  # pylint: disable=E1121
                self.cl_name, initiator_payload)
            LOG.info("Registered initiator %s in %s", det.name, self.cl_name)
            LOG.debug("Initiator Details:\n%s", det)
            return det
        except ApiException as err:
            err_msg = ("Could not register initiator in {0} due to"
                       " error: {1}".format(self.cl_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def get_initiator_payload(self, iscsi_name,  # pylint: disable=R0913, R0201
                              port_wwn, host_type,
                              initiator_name):
        """
        Initiator payload required for registering an initiator
        """
        initiator_payload = dict()
        initiator_payload['iscsi_name'] = iscsi_name
        initiator_payload['port_wwn'] = port_wwn
        initiator_payload['port_name'] = initiator_name
        initiator_payload['type'] = host_type
        LOG.info("Final initiator payload: %s", initiator_payload)
        return initiator_payload

    def check_initiator_flag(self):    # pylint: disable=R0201
        """This method checks for the operation to be performed and sets the
        corresponding flag"""
        if not self.init_name and not self.port_wwn and not self.iscsi_name \
                and not self.new_init_name:
            self.flag = 1
        elif self.init_name and self.port_wwn and self.registered:
            self.reg_flag = 1
        elif self.init_name and self.iscsi_name and self.registered:
            self.reg_flag = 1
        elif self.init_name and self.new_init_name:
            self.rename_flag = 1
        elif self.new_init_name and self.port_wwn:
            self.rename_flag = 1
        elif self.new_init_name and self.iscsi_name:
            self.rename_flag = 1
        elif self.init_name and not self.registered and \
                self.registered is not None:
            self.unreg_flag = 1
        elif self.port_wwn and not self.registered and \
                self.registered is not None:
            self.unreg_flag = 1
        elif self.iscsi_name and not self.registered and \
                self.registered is not None:
            self.unreg_flag = 1
        return (self.flag, self.reg_flag, self.rename_flag, self.unreg_flag)

    def parse_data(self, object_data):    # pylint: disable=R0201
        """This method parses the fields in the object data and
        returns as a list"""
        parsed_list = []
        for initiator in object_data:
            init_list = []
            dic = {}
            if 'name' in initiator.keys():
                init_list.append('name')
            if 'type' in initiator.keys():
                init_list.append('type')
            if 'port_wwn' in initiator.keys():
                init_list.append('port_wwn')
            if 'iscsi_name' in initiator.keys():
                init_list.append('iscsi_name')
            dic = {init_list[i]: initiator[init_list[i]]
                   for i in range(len(init_list))}
            parsed_list.append(dic)
        return parsed_list

    def validate_name(self, name, field):    # pylint: disable=R0201
        """This method validates the name length and non-presence of
        special characters"""
        char_len = '36'
        status, msg = utils.validate_name(name, char_len, field)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def check_name(self, name, search_data):
        """This method checks for port_wwn/iscsi_name from initiators list"""
        for data in search_data:
            for _, val in data.items():
                if name == val:
                    self.temp_initiator = data['name']
                    LOG.info("Temp Initiator %s", self.temp_initiator)
                    return True
        return False

    def perform_module_operation(self):    # pylint: disable=R0912,R0914,R0915
        """
        Perform different actions on the initiator based on user parameters
        specified in the playbook
        """
        state = self.module.params['state']
        host_type = self.module.params['host_type']
        init_details = None
        initiator_details = None
        new_init_details = None
        temp_details = None
        init_dict = None
        changed = False

        def exit_module(changed, init_details):
            self.result["changed"] = changed
            if init_details:
                temp_itr = utils.serialize_content(init_details)
                init_details = temp_itr
                self.result["initiator_details"] = init_details
            self.module.exit_json(**self.result)

        # Perform rediscover initiators and keep it for idempotency
        details = self.rediscover_initiator()

        # Check for initiator relevant operation flag
        (self.flag, self.reg_flag, self.rename_flag, self.unreg_flag) = \
            self.check_initiator_flag()

        # Rediscover initiators if initiator_name is not present
        if self.flag and self.registered is None:
            exit_module(changed, details)

        # Collect the list of dictionaries with initiator names, port_wwn
        # and iscsi_name
        obj = utils.serialize_content(details)
        init_dict = self.parse_data(obj)

        # Validate the initiator_name
        if self.init_name:
            self.validate_name(self.init_name, 'initiator_name')

        # Validate the new initiator_name
        if self.new_init_name:
            self.validate_name(self.new_init_name, 'new_initiator_name')

        # Check for initiator/port_wwn/iscsi_name presence
        if self.flag:
            err_msg = ("Could not find initiator_name, port_wwn/iscsi_name"
                       " in user parameters. Required one of the options")
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        # Check for port_wwn is valid
        if state == "present" and self.port_wwn and not self.reg_flag \
                and not self.check_name(self.port_wwn, init_dict):
            err_msg = ("Could not match port_wwn {0} in {1}. Re-enter the"
                       " correct port_wwn".format(self.port_wwn,
                                                  self.cl_name))
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        # Check for iscsi_name is valid
        if state == "present" and self.iscsi_name and not self.reg_flag \
                and not self.check_name(self.iscsi_name, init_dict):
            err_msg = ("Could not match iscsi_name {0} in {1}. Re-enter the"
                       " correct iscsi_name".format(self.iscsi_name,
                                                    self.cl_name))
            LOG.error(err_msg)
            self.module.fail_json(msg=err_msg)

        # Get the details of given initiator
        if self.init_name:
            init_details = self.get_initiator(self.init_name)

        # Get the details of given new initiator
        if self.new_init_name:
            new_init_details = self.get_initiator(self.new_init_name)

        # Get the details of port_wwn/iscsi_name specific initiator
        if self.temp_initiator:
            temp_details = self.get_initiator(self.temp_initiator)

        # Register an initiator
        if state == "present" and self.reg_flag:
            # Check for idempotency
            if self.check_name(self.init_name, init_dict):
                if init_details.type is not None:
                    if self.port_wwn:
                        if self.port_wwn == init_details.port_wwn and \
                                host_type == init_details.type:
                            msg = ("Initiator {0} with port_wwn {1} in {2} is"
                                   " already registered".format(
                                       self.init_name, self.port_wwn,
                                       self.cl_name))
                            initiator_details = init_details
                            LOG.info(msg)
                            exit_module(changed, initiator_details)
                        elif self.port_wwn == init_details.port_wwn and \
                                host_type != init_details.type:
                            err_msg = ("Initiator {0} with port_wwn {1} in"
                                       " {2} is already registered with"
                                       " different host_type {3}".format(
                                           self.init_name, self.port_wwn,
                                           self.cl_name, init_details.type))
                            LOG.error(err_msg)
                            self.module.fail_json(msg=err_msg)
                        elif self.port_wwn != init_details.port_wwn:
                            err_msg = ("Initiator {0} is already registered"
                                       " with different port_wwn {1} in {2}."
                                       " Please enter any other valid"
                                       " initiator_name".format(
                                           self.init_name,
                                           init_details.port_wwn,
                                           self.cl_name))
                            self.module.fail_json(msg=err_msg)

                    elif self.iscsi_name:
                        if self.iscsi_name == init_details.iscsi_name and \
                                host_type == init_details.type:
                            msg = ("Initiator {0} with iscsi_name {1} in {2}"
                                   " is already registered".format(
                                       self.init_name, self.iscsi_name,
                                       self.cl_name))
                            initiator_details = init_details
                            LOG.info(msg)
                            exit_module(changed, initiator_details)
                        elif self.iscsi_name == init_details.iscsi_name and \
                                host_type != init_details.type:
                            err_msg = ("Initiator {0} with iscsi_name {1}"
                                       " in {2} is already registered with"
                                       " different host_type {3}".format(
                                           self.init_name, self.iscsi_name,
                                           self.cl_name, init_details.type))
                            LOG.error(err_msg)
                            self.module.fail_json(msg=err_msg)
                        elif self.iscsi_name != init_details.iscsi_name:
                            err_msg = ("Initiator {0} is already registered"
                                       " with different iscsi_name {1} in"
                                       " {2}. Please enter any other valid"
                                       " initiator_name".format(
                                           self.init_name,
                                           init_details.iscsi_name,
                                           self.cl_name))
                            self.module.fail_json(msg=err_msg)
                elif init_details.type is None:
                    err_msg = ("Could not register with initiator_name {0}"
                               " in {1} as it is already in use. Please"
                               " specify different initiator_name".format(
                                   self.init_name, self.cl_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
            # Perform registering the initiator
            else:
                initiator_payload = self.get_initiator_payload(
                    self.iscsi_name, self.port_wwn, host_type, self.init_name)
                initiator_details = self.register_initiator(
                    initiator_payload)
                changed = True

        # Renaming an initiator
        if state == "present" and self.rename_flag:
            if self.init_name and init_details is None:
                err_msg = ("Could not find initiator_name {0} from {1}".format(
                    self.init_name, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            elif self.init_name and self.new_init_name:
                if new_init_details is not None:
                    if self.init_name == self.new_init_name:
                        msg = ("initiator_name and new_initiator_name are"
                               " same")
                        initiator_details = init_details
                        LOG.info(msg)
                        exit_module(changed, initiator_details)
                    else:
                        err_msg = ("new_initiator_name {0} already exists in"
                                   " {1}. Specify a different name".format(
                                       self.new_init_name, self.cl_name))
                        LOG.error(err_msg)
                        self.module.fail_json(msg=err_msg)
                else:
                    self.temp_initiator = self.init_name
            elif self.port_wwn and self.new_init_name:
                if new_init_details is not None:
                    if self.port_wwn == new_init_details.port_wwn:
                        msg = ("Initiator is already visible with the same"
                               " new_initiator_name {0} in {1}".format(
                                   self.new_init_name, self.cl_name))
                        initiator_details = new_init_details
                        LOG.info(msg)
                        exit_module(changed, initiator_details)
                    else:
                        err_msg = ("new_initiator_name {0} already exists in"
                                   " {1}. Specify a different name".format(
                                       self.new_init_name, self.cl_name))
                        LOG.error(err_msg)
                        self.module.fail_json(msg=err_msg)
            elif self.iscsi_name and self.new_init_name:
                if new_init_details is not None:
                    if self.iscsi_name == new_init_details.iscsi_name:
                        msg = ("Initiator is already visible with the same"
                               " new_initiator_name {0} in {1}".format(
                                   self.new_init_name, self.cl_name))
                        initiator_details = new_init_details
                        LOG.info(msg)
                        exit_module(changed, initiator_details)
                    else:
                        err_msg = ("new_initiator_name {0} already exists in"
                                   " {1}. Specify a different name".format(
                                       self.new_init_name, self.cl_name))
                        LOG.error(err_msg)
                        self.module.fail_json(msg=err_msg)
            # Perform renaming the initiator
            initiator_details = self.rename_initiator(
                self.temp_initiator, self.new_init_name)
            changed = True

        # If state is absent for unregister and get initiator
        if state == "absent" and not self.reg_flag and not self.rename_flag:
            if self.port_wwn and not self.check_name(self.port_wwn, init_dict):
                exit_module(changed, initiator_details)
            elif self.iscsi_name and not self.check_name(
                    self.iscsi_name, init_dict):
                exit_module(changed, initiator_details)
            elif self.temp_initiator:
                temp_details = self.get_initiator(self.temp_initiator)

        # Unregister an initiator
        if self.unreg_flag:
            if self.init_name:
                if state == "absent" and init_details is None:
                    exit_module(changed, initiator_details)
                elif state == "present" and init_details is None:
                    err_msg = ("Could not find initiator_name {0} from"
                               " {1}".format(self.init_name, self.cl_name))
                    LOG.error(err_msg)
                    self.module.fail_json(msg=err_msg)
                elif init_details.type is None:
                    msg = ("Initiator {0} in {1} is already"
                           " unregistered".format(self.init_name,
                                                  self.cl_name))
                    LOG.info(msg)
                    exit_module(changed, initiator_details)
                else:
                    self.temp_initiator = self.init_name
            elif self.port_wwn or self.iscsi_name:
                if temp_details.type is None:
                    msg = ("Initiator {0} in {1} is already"
                           " unregistered".format(self.temp_initiator,
                                                  self.cl_name))
                    LOG.info(msg)
                    exit_module(changed, initiator_details)
            # Perform unregister initiator
            self.unregister_initiator(self.temp_initiator)
            changed = True
            initiator_details = None

        # Get initiator
        if not self.reg_flag and not self.unreg_flag \
                and not self.rename_flag:
            if state == "present" and self.port_wwn or self.iscsi_name and \
                    not self.init_name:
                init_details = temp_details
            elif state == "present" and init_details is None:
                err_msg = ("Could not get initiator {0} from {1}".format(
                    self.init_name, self.cl_name))
                LOG.error(err_msg)
                self.module.fail_json(msg=err_msg)
            elif state == "absent" and temp_details is not None:
                init_details = temp_details

            initiator_details = init_details

        # Finally call the exit module
        exit_module(changed, initiator_details)


def get_vplex_initiator_parameters():
    """This method provide parameter required for the ansible initiator
    module on VPLEX"""
    return dict(
        cluster_name=dict(required=True, type='str'),
        initiator_name=dict(required=False, type='str'),
        new_initiator_name=dict(required=False, type='str'),
        iscsi_name=dict(required=False, type='str'),
        port_wwn=dict(required=False, type='str'),
        host_type=dict(required=False, type='str', default='default',
                       choices=['default', 'hpux', 'sun-vcs', 'aix',
                                'recoverpoint']),
        registered=dict(required=False, type='bool'),
        state=dict(required=True, type='str', choices=['present', 'absent'])
    )


def main():
    """Create VplexInitiator object and perform action on it
        based on user input from playbook"""
    obj = VplexInitiator()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
