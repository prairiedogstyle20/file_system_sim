#! /usr/bin/env python3

import tkinter as tk
from tkinter import ttk

def print_data(virtual_tree, file_display_area):
    print_file_id = virtual_tree.focus(item=None)
    if print_file_id != None:
        text_to_print = virtual_tree.item(print_file_id, 'values'[0])
        #text_to_print = text_to_print['values']
        file_display_area.delete('1.0','4.0')
        file_display_area.insert('1.0',f'File Data: \n {text_to_print}\n')

def add_files(file_name, system_tree, virtual_tree, virtual_parent_node):

    sys_parent_node = check_system_file_space(system_tree)
    system_item_id = system_tree.insert(parent= sys_parent_node, index=1, text = file_name, open = False)
    virtual_tree.insert(parent=virtual_parent_node, index=1, iid=system_item_id, text=file_name, values=f'{system_item_id}')

def check_system_file_space(system_tree):
    locations = []

    for each in system_tree.get_children(item=None):
        locations.append(each)

    i = 0
    curr_pos = locations[i]
    while len(locations) > 0:
            if len(system_tree.get_children(curr_pos)) < 4:
                return curr_pos
            else:
                i += 1
                curr_pos = locations[i]

#returns the identifier for each of the three
# base drives on the main system in the order
# A, B, C
def generate_base_drives(system_tree):
    #parameters insert(parent, index, iid=None, **kw)
    drive_A = system_tree.insert(parent = "", index=0, text="A")
    drive_B = system_tree.insert(parent = "", index=1, text="B")
    drive_C = system_tree.insert(parent = "", index=2, text="C")
    #print(system_tree.column(0))

    return drive_A, drive_B, drive_C

def gen_virtual_drive(virtual_tree):
    usr_drive = virtual_tree.insert(parent="", index=0, text = "Usr")

    return usr_drive

def core_system_files(appRoot):
    core_file_system = ttk.Treeview(appRoot)
    system_label = tk.Label(appRoot, text="Core File System")
    drive_A,drive_B,drive_C = generate_base_drives(core_file_system)
    system_label.pack()
    core_file_system.pack()

    return drive_A, drive_B, drive_C, core_file_system

def user_virtual_files(appRoot):
    virtual_file_system = ttk.Treeview(appRoot)
    virtual_lable = tk.Label(appRoot,text="Virtual File System")
    drive_usr = gen_virtual_drive(virtual_file_system)
    virtual_lable.pack()
    virtual_file_system.pack()

    return drive_usr, virtual_file_system

def delete_file(system_tree, virtual_tree):
    deleted_file_id = virtual_tree.focus(item=None)
    files_to_delete = []
    if deleted_file_id != "":
        get_all_deleted_values(virtual_tree, deleted_file_id, files_to_delete)
        virtual_tree.delete(deleted_file_id)
        for each in files_to_delete:
            system_tree.delete(each)
            #remove_file_core_system(system_tree,each)
    else:
        return

def get_all_deleted_values(virtual_tree, file_id, files_to_delete):
    files_to_delete.append(file_id)

    for each in virtual_tree.get_children(file_id):
        if len(virtual_tree.get_children(each)) > 0:
            get_all_deleted_values(virtual_tree, each, files_to_delete)
        else:
            files_to_delete.append(each)

def remove_file_core_system(system_tree, file_id):
    fringe = []
    for each in system_tree.get_children():
        fringe.append(each)

        i = 0
        curr_pos = fringe[i]
    while len(fringe) > 0:
        for each in system_tree.get_children(curr_pos):
            if each == file_id:
                system_tree.delete(file_id)
                fringe.clear()
                break
            else:
                fringe.append(each)
        i += 1
        curr_pos = fringe[i]

def add_buttons(appRoot, system_tree, virtual_tree, file_display_area):
    entry_lable = tk.Label(appRoot,text="Enter File Name: ")
    add_file_entry = tk.Entry(appRoot)
    add_file_button = tk.Button(appRoot, text="Add File", command = lambda: add_files(add_file_entry.get(), system_tree, virtual_tree, virtual_tree.focus()))
    delete_file_button = tk.Button(appRoot, text="Delete File", command = lambda: delete_file(system_tree, virtual_tree))
    print_file_button = tk.Button(appRoot, text="Print File", command = lambda: print_data(virtual_tree, file_display_area))

    entry_lable.pack()
    add_file_entry.pack()
    add_file_button.pack()
    delete_file_button.pack()
    print_file_button.pack()

def main():
    root = tk.Tk()
    root.title("File System Sim")
    drive_A_ID, drive_B_ID,drive_C_ID, system_tree_reference = core_system_files(root)
    virtual_driver_ID, virtual_file_tree_reference = user_virtual_files(root)
    file_output = tk.Text(root, height = 5, width=40)
    file_output.pack()
    file_output.insert('1.0','File Data: \n')
    add_buttons(root, system_tree_reference, virtual_file_tree_reference, file_output)
    add_files("Kobe's Stats", system_tree_reference, virtual_file_tree_reference, virtual_driver_ID)
    root.mainloop()

main()
