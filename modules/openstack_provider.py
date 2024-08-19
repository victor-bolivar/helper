from .generic_provider import GenericProvider
from abc import ABC, abstractmethod
from utils import *
import openstack
import openstack.config.loader
import openstack.compute.v2.server
import os
import subprocess
import sys

class OpenstackProvider(GenericProvider):
    def __init__(self):
        pass

    def load_credentials(self) -> None:
        openrc_files = self.find_all_openrc()
        if not openrc_files:
            print("To ensure successful authentication against OpenStack, it's required to have at least one OpenRC file within this directory.")
            print("See this link if you don't know how to generate one: https://docs.openstack.org/newton/user-guide/common/cli-set-environment-variables-using-openstack-rc.html")
            sys.exit(1)
        selected_openrc = input(f"Select an openrc file to use {openrc_files}: ")
        if selected_openrc not in openrc_files:
            print("Select a existing openrc file")
            sys.exit(1)
        load_env_vars_from_bash(selected_openrc)
        print(f"Succesfully loaded {selected_openrc}")

        self.set_terraform_env_vars()

    def list_shared_risk_group(self) -> list:
        # Initialize connection
        conn = openstack.connect()

        azs = []
        for az in openstack.compute.v2.availability_zone.AvailabilityZone.list(session=conn.compute):
            azs.append(az.to_dict()['name'])
        return azs

    def assign_vms_to_shared_risk_groups(self, vms) -> list:
        azs = self.list_shared_risk_group()
        num_azs = len(azs)
        
        az_index = 0
        
        for i, vm in enumerate(vms):
            vms[i] += f'\n    availability_zone = "{ azs[az_index] }"\n'
            vms[i] += "\n}"

            az_index = (az_index + 1) % num_azs
        
        return vms
    
    def set_terraform_env_vars(self):
        openrc_vars = ["OS_AUTH_URL", "OS_PROJECT_NAME", "OS_USERNAME", "OS_PASSWORD", "OS_REGION_NAME" ]
        for openrc_var in openrc_vars:
            # For Terraform to environment variables, they must be in the format TF_VAR_<variable_name>
            os.environ["TF_VAR_"+openrc_var] = os.environ[openrc_var]
        print("Succesfully loaded required Terraform environment variables\n")

    def generate_tf_file(self, infra) -> None:
        """Generate .tf file

        Args:
            infra (dict): read from JSON file selected by the user
        """
        
        vms = []
        
        for vm_template in infra["nodes"]:
            
            if vm_template["count"] > 1:
                for i in range(vm_template["count"]):
                    multiline_text = f'''
resource "openstack_compute_instance_v2" "{infra['name']}-{vm_template['name']}-{i}" {{
    count             = 1
    name              = "{infra['name']}-{vm_template['name']}-{i}"
    image_id          = "{ vm_template['imageId'] }"
    flavor_id         = "{ vm_template['flavorId'] }"
    key_pair          = "{ vm_template['keypair'] }"
    security_groups   = [ {', '.join([f'"{sg}"' for sg in vm_template['securityGroups']])} ]

    '''
                    # Add network blocks on separate lines
                    for net_id in vm_template['networkIds']:
                        multiline_text += f"    network {{ uuid = \"{net_id}\" }}\n"
                    
                    vms.append(multiline_text)
            else:
                multiline_text = f'''
resource "openstack_compute_instance_v2" "{infra['name']}-{vm_template['name']}" {{
    count             = 1
    name              = "{infra['name']}-{vm_template['name']}"
    image_id          = "{ vm_template['imageId'] }"
    flavor_id         = "{ vm_template['flavorId'] }"
    key_pair          = "{ vm_template['keypair'] }"
    security_groups   = [ {', '.join([f'"{sg}"' for sg in vm_template['securityGroups']])} ]

    '''
                # Add network blocks on separate lines
                for net_id in vm_template['networkIds']:
                    multiline_text += f"    network {{ uuid = \"{net_id}\" }}\n"
                
                vms.append(multiline_text)
        
        # Put each VM in different AZs
        vms = self.assign_vms_to_shared_risk_groups(vms)
        
        dest_folder = f"infra/{infra['name']}"
        add_text_to_file("templates/infra.tf", f"{dest_folder}/infra.tf", '\n'.join(vms))

    def find_all_openrc(self) -> list:
        return find_files("./", "*-openrc.sh")