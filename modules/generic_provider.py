from abc import ABC, abstractmethod
import os
import subprocess
import sys

class GenericProvider(ABC):
    
    @abstractmethod
    def load_credentials(self) -> None:
        pass

    @abstractmethod
    def list_shared_risk_group(self) -> list:
        pass

    @abstractmethod
    def generate_tf_file(self) -> list:
        pass

    def create_tf_infra(self, infra_folder) -> bool:
        self.load_credentials()

        # Idempotent
        if subprocess.run(["terraform", "init"], cwd=infra_folder).returncode != 0:
            print("Error while initializing Terraform")
            sys.exit(1)
        
        result_terraform_plan = subprocess.run(["terraform", "plan"], cwd=infra_folder)
        if result_terraform_plan.returncode != 0:
            print("Error while creating the execution plan for the infra")
            sys.exit(1)
        
        result_terraform_apply = subprocess.run(["terraform", "apply"], cwd=infra_folder)
        if result_terraform_apply.returncode != 0:
            print("Error while creating the infra")
            sys.exit(1)

    def destroy_tf_infra(self, infra_folder):
        self.load_credentials()

        result_terraform_destroy = subprocess.run(["terraform", "destroy"], cwd=infra_folder)
        if result_terraform_destroy.returncode != 0:
            print("Error while destroying the infra")
            sys.exit(1)