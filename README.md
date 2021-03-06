# Ansible Modules for Dell EMC VPLEX

The Ansible Modules for Dell EMC VPLEX allow to provision the storage volume.

The capabilities of Ansible modules are managing storage views, initiators, ports, consistency groups, virtual volumes, devices, extents, data migration jobs and storage volumes and to get information of recently configured resources through gather facts. The options available for each capability are list, show, create, delete and modify. These tasks can be executed by running simple playbooks written in yaml syntax.

## Support
Ansible modules for VPLEX are supported by Dell EMC and are provided under the terms of the license attached to the source code.
Dell EMC does not provide support for any source code modifications.
For any Ansible module issues, questions or feedback, join the [Dell EMC Automation community](https://www.dell.com/community/Automation/bd-p/Automation).

## Supported Platforms
  * Dell VPLEX GeoSynchrony 6.2

## Prerequisites
  * Ansible 2.7, 2.8, 2.9
  * Python 2.7.18, 3.6.9
  * Red Hat Enterprise Linux 7.5, 7.6, 8.1
  * VPLEX Python SDK 6.2

## Idempotency
The modules are written in such a way that all requests are idempotent. It essentially means that the result of a successfully performed request is independent of the number of times it is executed.

## List of Ansible Modules for Dell VPLEX
  * Storage View module
  * Initiator module
  * Port module
  * Consistency Group module
  * Distributed Consistency Group module
  * Virtual Volume module
  * Distributed Virtual Volume module
  * Device module
  * Distributed Device module
  * Extent module
  * Storage Volume module
  * Rediscover Array module
  * Gather facts module
  * Data migration module

## Installation of SDK

  * git clone https://github.com/dell/python-vplex.git  
  
  * Export the python path with vplexapi
      export PYTHONPATH="{$PYTHONPATH}:<complete path of vplexapi>”
  * The above command works only on the current execution terminal. In order to make it persistent, we need to update the same export command in $HOME/.bashrc file followed by system reboot

## Installation of Ansible Modules

  * git clone https://github.com/dell/ansible-vplex.git

  * Make ansible-vplex as the current working directory
    * cd ansible-vplex

  * Determine the current ansible and python versions by executing the command
      "ansible --version"

  * Based on the listed python version along with location displayed in the above command, configure the ansible modules with the below steps

    For e.g: 
    * [root@<user>~]# mkdir -p /usr/lib/python2.7/site-packages/ansible/modules/storage/dellemc
    * [root@<user>~]# mkdir -p /usr/lib/python2.7/site-packages/ansible/module_utils/storage/dell
    * [root@<user>~]# touch /usr/lib/python2.7/site-packages/ansible/modules/storage/dellemc/__init__.py
    * [root@<user>~]# touch /usr/lib/python2.7/site-packages/ansible/module_utils/storage/__init__.py
    * [root@<user>~]# touch /usr/lib/python2.7/site-packages/ansible/module_utils/storage/dell/__init__.py
    * [root@<user>~]# cp -rf dellemc_ansible/utils/dellemc_ansible_vplex_utils.py /usr/lib/python2.7/site-packages/ansible/module_utils/storage/dell/dellemc_ansible_vplex_utils.py
    * [root@<user>~]# cp -rf dellemc_ansible/vplex/library/* /usr/lib/python2.7/site-packages/ansible/modules/storage/dellemc/
    * For ansible 2.7 version,
      [root@<user>~]# cp -rf dellemc_ansible/doc_fragments/dellemc_vplex.py /usr/lib/python2.7/site-packages/ansible/utils/module_docs_fragments/dellemc_vplex.py
    * For ansible 2.8 or higher,
      [root@<user>~]# cp -rf dellemc_ansible/doc_fragments/dellemc_vplex.py /usr/lib/python2.7/site-packages/ansible/plugins/doc_fragments/dellemc_vplex.py

## VPlex log collection script

Whenever a task fails the script vplexlog_collection.py collects the vplexapi logs, ansible module logs, the system logs and saves them in a folder Logs/Logs_<timestamp> in the current execution path.

## Prerequisites
  * Copy tools/vplexlog_collection.py to the path of the playbook
  * Add a block for rescue in the playbook like shown in tools/log_collection.yml
  * Install sshpass
  * Add the Vplex server IP to the file ~/.ssh/known_hosts in the test system
  * Set the python path for vplexapi
    export PYTHONPATH="{$PYTHONPATH}:/<vplexapi_PATH>"
