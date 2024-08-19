#!/usr/bin/env python3

from utils import *
from .modules.openstack_provider import OpenstackProvider
from pprint import pprint
import sys

def list_infra():
    print(list_folders("infra"))
    
def show_infra():

    existing_infras = list_folders("infra")
    if not existing_infras:
        print("No infra found!")
        return 
    
    selected_infra = input(f"Select one infra {existing_infras}: ")
    if not selected_infra in existing_infras:
        print("Select a valid infra!")
        return
    
    print("\ninfra.json:")
    print("----------\n")
    pprint(read_json_file(f"infra/{selected_infra}/infra.json"))
    
    print("\n\nterraform.tfstate:")
    print("-----------------\n")
    pprint(read_json_file(f"infra/{selected_infra}/terraform.tfstate"))
    
def create_infra():
    
    selected_infra_file = select_infra_file()
    if not select_infra_file:
        return
    
    print()
    
    infra = read_json_file(selected_infra_file)
    pprint(infra)
    
    create_infra_answer = input("\nThe following infra will be created, are you sure? (y/n): ")
    if not create_infra_answer.lower() in "y":
        print()
        sys.exit(1)
    
    print("\nCreating corresponding directory under infra/ ...")
    
    dest_folder = f"infra/{infra['name']}"
    create_directory(dest_folder)
    copy_file(selected_infra_file, f"{dest_folder}/infra.json")
    
    if infra['type'] == "openstack":
        driver = OpenstackProvider()

    driver.generate_tf_file()
    driver.create_tf_infra()

def update_infra():
    # Select the existing infra to update
    existing_infras = list_folders("infra")
    selected_infra = input(f"Select one infra {existing_infras}: ")
    if not selected_infra in existing_infras:
        print("Select a valid infra!")
        return
    
    # Select new infra file
    selected_infra_file = select_infra_file()
    if not select_infra_file:
        return
    
    infra = read_json_file(selected_infra_file)
    pprint(infra)
    
    create_infra_answer = input("\nThe new following infra will be used, are you sure? (y/n): ")
    if not create_infra_answer.lower() in "y":
        print()
        sys.exit(1)
    
    dest_folder = f"infra/{infra['name']}"
    print(f"\nUpdating {dest_folder}/infra.json ...")
    copy_file(selected_infra_file, f"{dest_folder}/infra.json")
    
    if infra['type'] == "openstack":
        driver = OpenstackProvider()

    driver.generate_tf_file(infra)
    driver.create_tf_infra(dest_folder)
    
def delete_infra():
    # Select the existing infra to delete
    existing_infras = list_folders("infra")
    selected_infra = input(f"Select the infra to be deleted {existing_infras}: ")
    if not selected_infra in existing_infras:
        print("Select a valid infra!")
        return
    
    dest_folder = f"infra/{selected_infra}"
    infra = read_json_file(f"{dest_folder}/infra.json")
    if infra['type'] == "openstack":
        driver = OpenstackProvider()

    driver.destroy_tf_infra(dest_folder)
    
    # Remove infra folder and its contents
    delete_folder(dest_folder)
    

def main():
    while True:
        print("\n========= Options: =========\n")
        print("1. List Infrastructure")
        print("2. Show Infraestructure")
        print("3. Create Infrastructure")
        print("4. Update Infrastructure")
        print("5. Delete Infrastructure")
        print("6. Exit")

        choice = input("\nEnter the number of your choice: ")
        print()

        if choice == "1":
            list_infra()
        elif choice == "2":
            show_infra() 
        elif choice == "3":
            create_infra()
        elif choice == "4":
            update_infra()
        elif choice == "5":
            delete_infra()
        elif choice == "6":
            print("Exiting program...\n")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()