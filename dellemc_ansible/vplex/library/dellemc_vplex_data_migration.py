""" Data Migration module """

# !/usr/bin/python
# Copyright: (c) 2020, DellEMC

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.storage.dell import \
    dellemc_ansible_vplex_utils as utils

__metaclass__ = type    # pylint: disable=C0103
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_vplex_data_migration
version_added: '2.7'
short_description:  Manage data migration on VPLEX Storage System
description:
- Create a migration job,
  Get information about existing migration job,
  Update an existing migration job,
  Delete an existing migration job

extends_documentation_fragment:
  - dellemc_vplex.dellemc_vplex

author:
- Sherene Jean Prathiba (@sherenevinod-dell) <vplex.ansible@dell.com>

options:
  migration_name:
    description:
    - The name of the migration job
    required: true
    type: str

  cluster_name:
    description:
    - The name of the source VPLEX cluster
    type: str

  target_cluster:
    description:
    - The name of the target VPLEX cluster
    type: str

  source_name:
    description:
    - The name of the source device. The source device should contain a virtual
      volume
    type: str

  target_name:
    description:
    - The name of the target device. The target device should not contain
      a virtual
      volume
    type: str

  status:
    description:
    - The status of the migration job
    choices: ['pause', 'resume', 'cancel', 'commit']
    type: str

  transfer_size:
    description:
    - The transfer size of the migration job. Number in Bytes.
      Must be a multiple of 4K with range 40KB to 128M.
      Default value is 128KB
    type: int

  state:
    description:
    - Defines whether the migration job should exist or not
    required: true
    choices: ['absent', 'present']
    type: str
  '''
EXAMPLES = r'''

    - name: Create a device migration job across cluster
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        target_cluster: "cluster-2"
        source_name: "source_dev_1"
        target_name: "target_dev_1"
        migration_name: "mobility_job"
        state: "present"

    - name: Create a device migration job within cluster
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        cluster_name: "cluster-1"
        source_name: "source_dev_1"
        target_name: "target_dev_1"
        migration_name: "mobility_job"
        state: "present"

    - name: Get a device migration job
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        migration_name: "mobility_job"
        state: "present"

    - name: Update transfer size of a device migration job
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        migration_name: "mobility_job"
        transfer_size: "40960"
        state: "present"

    - name: Pause a device migration job
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        migration_name: "mobility_job"
        status: "pause"
        state: "present"

    - name: Resume a device migration job
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        migration_name: "mobility_job"
        status: "resume"
        state: "present"

    - name: Cancel a device migration job
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        migration_name: "mobility_job"
        status: "cancel"
        state: "present"

    - name: Commit a device migration job
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        migration_name: "mobility_job"
        status: "commit"
        state: "present"

    - name: Delete a device migration job
      dellemc_vplex_data_migration:
        vplexhost: "{{ vplexhost }}"
        vplexuser: "{{ vplexuser }}"
        vplexpassword: "{{ vplexpassword }}"
        verifycert: "{{ verifycert }}"
        migration_name: "mobility_job"
        state: "absent"
'''

RETURN = r'''

changed:
    description: Whether or not the resource has changed
    returned: always
    type: bool

job_details:
    description: Properties of the migration job
    returned: When migration job exists in VPLEX
    type: complex
    contains:
        name:
            description:
                - The name assigned to the mobility job
            type: str
        from_cluster:
            description:
                - The cluster that the data comes from
            type: str
        percentage_done:
            description:
                - Displays the percentage of the mobility job that is complete
            type: int
        source:
            description:
                - The name of the device from which the data is being moved
            type: str
        start_time:
            description:
                - The time at which the mobility job began
            type: date
        status:
            description:
                - The status of the mobility job
            type: str
        target:
            description:
                - The name of the device to which the data is being moved
            type: str
        to_cluster:
            description:
                - The cluster to which the mobility job is moving data
            type: str
        transfer_size:
            description:
                - The speed of the mobility job
            type: int
        type:
            description:
                - The type of mobility job
            type: str
        source_exported:
            description:
                - Whether the source device is exported
            type: bool
        target_exported:
            description:
                - Whether the target device is exported
            type: bool
'''

LOG = utils.get_logger('dellemc_vplex_data_migration')

HAS_VPLEXAPI_SDK = utils.has_vplexapi_sdk()


class VplexDataMigration():  # pylint: disable=R0902
    """Class with VPLEX Data migration operations"""

    def __init__(self):
        """Define all the parameters required by this module"""
        self.module_params = utils.get_vplex_management_host_parameters()
        self.module_params.update(get_vplex_data_migration_parameters())

        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False,
        )

        # Check for external libraries
        lib_status, message = utils.external_library_check()
        if not lib_status:
            LOG.error(message)
            self.module.fail_json(msg=message)

        # Check for Python vplexapi sdk
        if HAS_VPLEXAPI_SDK is False:
            self.module.fail_json(msg="Ansible modules for VPLEX require "
                                      "the vplexapi python library to be "
                                      "installed. Please install the library "
                                      "before using these modules.")

        # Create the configuration instance to communicate
        # with vplexapi
        self.client = utils.config_vplexapi(self.module.params)
        self.cl_name = self.module.params['cluster_name']
        self.target_cl = self.module.params['target_cluster']

        # Validating the user inputs
        if isinstance(self.client, tuple):
            _, msg = self.client
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        vplex_setup = utils.get_vplex_setup(self.client)
        LOG.info(vplex_setup)
        # Checking if the cluster is reachable
        clusters = []
        if self.cl_name is not None:
            clusters.append(self.cl_name)
        if (self.target_cl is not None and self.target_cl != self.cl_name):
            clusters.append(self.target_cl)

        for cluster in clusters:
            (err_code, msg) = utils.verify_cluster_name(self.client, cluster)
            if err_code != 200:
                if "Resource not found" in msg:
                    msg = "Could not find resource {0}".format(cluster)
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        # Create an instance to storageApi to communicate with
        # vplexapi
        api_obj = utils.VplexapiModules()
        self.data = api_obj.DataMigrationApi(api_client=self.client)
        self.device = api_obj.DevicesApi(api_client=self.client)
        LOG.info('Got the vplexapi instance for Mobility')

        self.storage = "device"
        self.storage_uri = "devices"

    def get_job_details(self, migration_name):
        """
        Get the details of a migration job
        """
        try:
            job_details = None
            if self.storage == "device":
                job_details = self.data.get_device_migration(migration_name)
            LOG.info("Got the %s migration job details %s ", self.storage,
                     migration_name)
            LOG.debug("%s migration job details:\n%s", self.storage,
                      job_details)
            job_details = utils.serialize_content(job_details)
            return job_details
        except utils.ApiException as err:
            err_msg = ("Could not get {0} migration job {1} details due to"
                       " error: {2}".format(self.storage, migration_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None

    def create_job(self, migration_name, cluster_name,  # pylint: disable=R0913
                   target_cluster, source_name, target_name, transfer_size,
                   status):
        """
        Create data migration job on VPLEX
        """

        # Validate the source and the target
        self.validate_src_target(cluster_name, target_cluster, source_name,
                                 target_name)
        try:
            src_uri = ("/vplex/v2/clusters/{0}/{1}/{2}"
                       .format(cluster_name, self.storage_uri, source_name))
            target_uri = ("/vplex/v2/clusters/{0}/{1}/{2}"
                          .format(target_cluster, self.storage_uri,
                                  target_name))
            data_payload = {'name': migration_name, 'source': src_uri,
                            'target': target_uri}
            if status == "pause":
                data_payload['paused'] = True
            if transfer_size:
                data_payload['transfer_size'] = transfer_size
            if self.storage == "device":
                job_details = self.data.create_device_migration(
                    data_payload)
            LOG.info("Created a %s migration job %s", self.storage,
                     migration_name)
            LOG.debug("%s migration job details:\n%s", self.storage,
                      job_details)
            job_details = utils.serialize_content(job_details)
            return job_details
        except utils.ApiException as err:
            err_msg = ("Could not create {0} migration job {1} due to"
                       " error: {1}".format(migration_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def delete_job(self, job_details):
        """
        Delete a data migration job on VPLEX
        """
        if job_details['status'] not in ['cancelled', 'committed']:
            msg = ("Could not remove {0} migration record for {1}. The "
                   "migration must first be cancelled or committed."
                   .format(self.storage, job_details['name']))
            LOG.error(msg)
            self.module.fail_json(msg=msg)

        try:
            if self.storage == "device":
                self.data.delete_device_migration(job_details['name'])
            LOG.info("Deleted the %s migration job %s", self.storage,
                     job_details['name'])
            return True
        except utils.ApiException as err:
            err_msg = ("Could not delete {0} migration job {1} due to"
                       " error: {2}".format(self.storage, job_details['name'],
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def update_migration_job(self, migration_name, data_patch_payload):
        """
        Update data migration job
        """

        try:
            LOG.info("Final payload: %s", data_patch_payload)
            if self.storage == "device":
                job_details = self.data.patch_device_migration(
                    migration_name, data_patch_payload)
            LOG.info("Updated the %s data migration job %s", self.storage,
                     migration_name)
            LOG.debug("%s migration job details:\n%s", self.storage,
                      job_details)
            job_details = utils.serialize_content(job_details)
            return job_details
        except utils.ApiException as err:
            err_msg = ("Could not update the migration job {0} due to"
                       " error: {1}".format(migration_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            self.module.fail_json(msg=err_msg)

    def get_device(self, cluster_name, device_name):
        """
        Get the details of a device
        """
        try:
            obj_device = self.device.get_device(cluster_name, device_name)
            LOG.info("Got device details for %s from %s", device_name,
                     cluster_name)
            LOG.debug("Device Details:\n%s", obj_device)
            device_details = utils.serialize_content(obj_device)
            return device_details
        except utils.ApiException as err:
            err_msg = ("Could not get device {0} details in {1} due to"
                       " error: {2}".format(device_name, cluster_name,
                                            utils.error_msg(err)))
            LOG.error("%s\n%s\n", err_msg, err)
            return None

    def validate_src_target(self, cluster_name, target_cluster, source_name,
                            target_name):
        """
        Check if the source and the target provided are valid
        """
        msg = None
        if self.storage == "device":
            src_details = self.get_device(cluster_name, source_name)
            target_details = self.get_device(target_cluster, target_name)

            if src_details is None:
                msg = ("Could not create a {0} migration job. "
                       "The source device {1} is not present in {2}"
                       .format(self.storage, source_name, cluster_name))
            elif target_details is None:
                msg = ("Could not create a {0} migration job. "
                       "The target device {1} is not present in {2}"
                       .format(self.storage, target_name, target_cluster))

            elif 'virtual_volume' not in src_details.keys():
                msg = ("Could not create a {0} migration job. The source "
                       "device {1} in {2} does not contain a virtual volume"
                       .format(self.storage, source_name, cluster_name))

            elif ('virtual_volume' in target_details.keys() and
                  target_details['virtual_volume'] is not None):
                msg = ("Could not create a {0} migration job. The target "
                       "device {1} in {2} contains a virtual volume"
                       .format(self.storage, target_name, target_cluster))

            elif src_details['capacity'] > target_details['capacity']:
                msg = ("Could not create a {0} migration job. The source "
                       "{0} {1} capacity is greater than the target {0} "
                       "{2}".format(self.storage, source_name, target_name))

        if msg:
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def validate_transfer_size(self, transfer_size):
        """
        Validate the transfer size
        """
        msg = None
        if transfer_size < 40960:
            msg = ("Specified transfer size {0} is too low"
                   .format(transfer_size))
        elif transfer_size > 134217728:
            msg = ("Specified transfer size {0} is too high"
                   .format(transfer_size))
        elif transfer_size % 4096 != 0:
            msg = ("The transfer size {0} should be in multiples "
                   "of 4K".format(transfer_size))
        if msg:
            LOG.error(msg)
            self.module.fail_json(msg=msg)

    def check_name_validity(self, migration_name, name):
        """
        Check if the migration job name is valid
        """
        char_len = "63"
        status, msg = utils.validate_name(migration_name, char_len, name)
        if not status:
            LOG.error(msg)
            self.module.fail_json(msg=msg)
        else:
            LOG.info(msg)

    def perform_module_operation(self):  # pylint: disable=R0915,R0914,R0912
        """
        Perform different actions on Device based on user parameters
        chosen in playbook
        """

        migration_name = self.module.params['migration_name']
        source_name = self.module.params['source_name']
        target_name = self.module.params['target_name']
        transfer_size = self.module.params['transfer_size']
        status = self.module.params['status']
        cluster_name = self.module.params['cluster_name']
        target_cluster = self.module.params['target_cluster']
        state = self.module.params['state']

        changed = False
        result = dict(
            changed=False,
            job_details=None
        )
        job_details = None
        data_patch_payload = []

        # Dictionary for the supported operations in a state
        operations = {"queues": ["cancel", "pause", "transfer size"],
                      "in-progress": ["cancel", "pause", "transfer size"],
                      "paused": ["resume", "cancel", "transfer size"],
                      "commit pending": ["commit", "cancel", "transfer size"],
                      "complete": ["commit", "cancel", "transfer size"],
                      "committed": ['transfer size'],
                      "partially-committed": ["commit"],
                      "error": ["cancel"],
                      "cancelled": ["transfer size"],
                      "partially-cancelled": ["cancel"]}

        operations_idem = {"commit": "committed",
                           "pause": "paused",
                           "resume": "in-progress",
                           "cancel": "cancelled"}

        self.check_name_validity(migration_name, "migration job name")

        # Get the migration job details
        job_details = self.get_job_details(migration_name)
        if transfer_size:
            self.validate_transfer_size(transfer_size)
        create_flag = 0

        if target_cluster is None:
            target_cluster = cluster_name

        # Create a migration job
        if (job_details is None and state == "present"):
            if (source_name and target_name and cluster_name):
                job_details = self.create_job(migration_name, cluster_name,
                                              target_cluster, source_name,
                                              target_name, transfer_size,
                                              status)
                create_flag = 1
                changed = True
            else:
                msg = ("Could not get the details of the {0} migration job"
                       " {1}".format(self.storage, migration_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        elif (job_details and state == "present" and source_name and
              target_name and cluster_name):
            src_uri = ("/vplex/v2/clusters/{0}/{1}/{2}"
                       .format(cluster_name, self.storage_uri, source_name))
            target_uri = ("/vplex/v2/clusters/{0}/{1}/{2}"
                          .format(target_cluster, self.storage_uri,
                                  target_name))
            if (job_details['source'] == src_uri and
                    job_details['target'] == target_uri):
                LOG.info("%s migration job %s is already present",
                         self.storage, migration_name)
            else:
                msg = ("Could not create {0} migration job {1}. The job is"
                       " already present with different {0}"
                       .format(self.storage, migration_name))
                LOG.error(msg)
                self.module.fail_json(msg=msg)

        # Validate the status field
        if ((job_details and create_flag == 1 and  # pylint: disable=R0916
             status not in ["pause", None]) or
                (job_details and create_flag == 0 and status)):
            if (status in operations_idem.keys() and
                    job_details['status'] == operations_idem[status]):
                msg = ("{0} migration job is already in the status {1}"
                       .format(self.storage, job_details['status']))
                LOG.info(msg)
            elif status not in operations[job_details['status']]:
                msg = ("Could not update status of the {0} migration job {1} "
                       "to {2} from {3}".format(self.storage, migration_name,
                                                status, job_details['status']))
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            else:
                patch_payload = {'op': 'replace', 'path': '/status',
                                 'value': status}
                data_patch_payload.append(patch_payload)

        if (job_details and create_flag == 0 and transfer_size
                and state == "present"):
            if transfer_size == job_details['transfer_size']:
                msg = ("The transfer size of the {0} migration job {1} is "
                       "already {2}".format(self.storage, migration_name,
                                            transfer_size))
                LOG.info(msg)
            elif "transfer size" not in operations[job_details['status']]:
                msg = ("Could not update transfer size of {0} migration job"
                       " {1} when the job is in {2} state"
                       .format(self.storage, migration_name,
                               job_details['status']))
                LOG.error(msg)
                self.module.fail_json(msg=msg)
            else:
                patch_payload = {'op': 'replace', 'path': '/transfer_size',
                                 'value': transfer_size}
                data_patch_payload.append(patch_payload)

        if len(data_patch_payload) > 0:
            job_details = self.update_migration_job(migration_name,
                                                    data_patch_payload)
            changed = True

        # Delete a data migration job
        if (job_details is None and state == "absent"):
            msg = ("Could not get the details of the {0} migration job {1}. "
                   "Job not present".format(self.storage, migration_name))
            LOG.info(msg)
            self.module.exit_json(**result)

        elif (job_details and state == "absent"):
            self.delete_job(job_details)
            result['changed'] = True
            self.module.exit_json(**result)

        result['changed'] = changed
        result['job_details'] = job_details
        self.module.exit_json(**result)


def get_vplex_data_migration_parameters():
    """This method provide the parameters required for the ansible
    device module on VPLEX
    """
    return dict(
        migration_name=dict(type='str', required=True),
        source_name=dict(type='str', required=False),
        target_name=dict(type='str', required=False),
        transfer_size=dict(type='int', required=False),
        status=dict(type='str', required=False,
                    choices=['pause', 'resume', 'cancel', 'commit']),
        cluster_name=dict(type='str', required=False),
        target_cluster=dict(type='str', required=False),
        state=dict(type='str', required=True, choices=['present', 'absent'])
    )


def main():
    """Create VplexDataMigration object and perform action on it
        based on user inputs from playbook"""
    obj = VplexDataMigration()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
