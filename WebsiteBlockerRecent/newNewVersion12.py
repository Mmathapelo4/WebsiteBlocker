from tkinter import *
from tkinter import messagebox
import customtkinter

host_path = 'C:\Windows\System32\drivers\etc\hosts'
ip_address = '127.0.0.1'

root = Tk()
root.geometry('650x500')
root.resizable(0, 0)
root.title("Website Blocker")

root['bg'] = "#E5F9DB"


# Heading
Label(root, text='WEBSITE BLOCKER', font='arial 20 bold' , bg='#E5F9DB').grid(row=0, column=1, pady=10)


# Enter Website label and text box
Label(root, text='Enter Website:', font='arial 13 bold' , bg='#E5F9DB').place(x=5 , y=175)

Websites = Text(root, font='arial 10', height=2, width=40 ,wrap=WORD, padx=5, pady=5)
# Websites.grid(row=1, column=1, columnspan=2, sticky=W)
Websites.place(x=200 , y=175)



Label(root, text='List of blocked Website:', font='arial 13 bold', bg='#E5F9DB').place(x=5 , y=300)

def block_website():
    website_lists = Websites.get(1.0, END)
    if not website_lists.strip():
        messagebox.showerror("Error", "Please enter website(s) to block.")
        return

    Website = list(website_lists.split(","))

    with open(host_path, 'r+') as host_file:
        file_content = host_file.read()
        for website in Website:
            if website in file_content:
                Label(root, text='Already Blocked', font='arial 12 bold').place(x=200, y=200)
                pass
            else:
                host_file.write(ip_address + " " + website + '\n')
                Label(root, text="Blocked", font='arial 12 bold').place(x=230, y=200)

    blocked_websites_listbox.insert(END, *Website)

def unblock_website():
    website_lists = Websites.get(1.0, END)
    if not website_lists.strip():
        messagebox.showerror("Error", "Please enter website(s) to unblock.")
        return

    Website = list(website_lists.split(","))

    with open(host_path, 'r+') as host_file:
        file_content = host_file.readlines()
        host_file.seek(0)
        for line in file_content:
            if not any(website in line for website in Website):
                host_file.write(line)
        host_file.truncate()
        Label(root, text="Unblocked", font='arial 12 bold').place(x=230, y=200)

    for website in Website:
        blocked_websites_listbox.delete(blocked_websites_listbox.get(0, END).index(website))



# Block and Unblock buttons
block = Button(root, text='Block', font='arial 12 bold', pady=5, command=block_website, width=8, bg='#AEE2FF', activebackground='#448AFF')
# block.grid(row=2, column=1, sticky=E, padx=(10, 5),pady=(10, 0))
block.place(x=235 , y=240)


unblock = Button(root, text='Unblock', font='arial 12 bold', pady=5, command=unblock_website, width=8, bg='#AEE2FF', activebackground='#448AFF')
# unblock.grid(row=2, column=2, sticky=W, padx=(5, 10), pady=(10, 0))
unblock.place(x=350 , y=240)

# Blocked Websites listbox
blocked_websites_listbox = Listbox(root, font='arial 10', height=6, width=41)
blocked_websites_listbox.place(x=201,  y=300)

def remove_website():
    if blocked_websites_listbox.size() == 0:
        messagebox.showerror("Error", "No website selected to remove.")
        return

    selected_items = blocked_websites_listbox.curselection()
    if not selected_items:
        # No item is selected
        return
    selected_website = blocked_websites_listbox.get(selected_items[0])
    with open(host_path, 'r+') as host_file:
        file_content = host_file.readlines()
        host_file.seek(0)
        for line in file_content:
            if not selected_website in line:
                host_file.write(line)
        host_file.truncate()
        Label(root, text="Website Removed", font='arial 12 bold').place(x=200, y=380)
    blocked_websites_listbox.delete(ANCHOR)

# Remove button
remove_button = Button(root, text='Remove', font='arial 12 bold', pady=5, command=remove_website, width=8, bg='#AEE2FF', activebackground='#448AFF')
# remove_button.grid(row=5, column=2, sticky=W, padx=(5, 10), pady=(10, 0))
remove_button.place(x=350 , y=420)

def save_blocked_websites():
    if blocked_websites_listbox.size() == 0:
        messagebox.showerror("Error", "No websites to save.")
        return

    with open('blocked_websites.txt', 'w') as file:
        for website in blocked_websites_listbox.get(0, END):
            file.write(website + '\n')
    Label(root, text="Blocked Websites Saved", font='arial 12 bold').place(x=190, y=420)

# Save button
save_button = Button(root, text='Save', font='arial 12 bold', pady=5, command=save_blocked_websites, width=8, bg='#AEE2FF', activebackground='#448AFF')
# save_button.grid(row=5, column=1, sticky=E, padx=(5, 10), pady=(10, 0))
save_button.place(x=235 , y=420)

def load_blocked_websites():
    blocked_websites_listbox.delete(0, END)
    with open('blocked_websites.txt', 'r') as file:
        for line in file:
            website = line.strip()
            blocked_websites_listbox.insert(END, website)
    Label(root, text="Blocked Websites Loaded", font='arial 12 bold').place(x=190, y=420)
    

def display_instructions():
    instructions = '''
    INSTRUCTIONS:
    1. Enter the website(s) you want to block in the text box.
    2. Click the "Block" button to block the entered website(s).
    3. To unblock a website, enter the website(s) in the text box and click the "Unblock" button.
    4. To remove a website from the list of blocked websites, select it from the list and click the "Remove" button.
    5. Click the "Save" button to save the list of blocked websites to a file.

    NOTE:
    - You need administrative privileges to modify the host file.
    - The blocked websites will be redirected to the IP address 127.0.0.1 (localhost).
    '''

    instruction_window = Toplevel(root)
    instruction_window.title('Instructions')
    instruction_window.geometry('800x300')
    instruction_window.resizable(0, 0)
    instruction_window['bg'] = "#E5F9DB"

    instruction_label = Label(instruction_window, text=instructions, font='arial 12', bg='#E5F9DB', justify=LEFT)
    instruction_label.pack(padx=10, pady=10)

help_button = Button(root, text='Need Help?', font='arial 12 bold', pady=5, command=display_instructions, width=9, bg='#AEE2FF', activebackground='#448AFF')
# help_button.grid(row=5, column=3, sticky=E, padx=(5, 10), pady=(10, 0))
help_button.place(x=550, y=0)

root.mainloop()

    
