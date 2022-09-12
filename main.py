from tkinter import *
from tkinter import messagebox
import random
import json
import pyperclip

YELLOW = "#f7f5dd"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]

    random.shuffle(password_list)
    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)        # copies the password automatically after creation


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {website: {
                    "email": email,
                    "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please fill all the fields")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                # loading old data
                data = json.load(data_file)
                # updating old data with new data
                data.update(new_data)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open("data.json", mode="w") as data_file:
                # saving the updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- Search Email and Password ------------------------------- #


def search():
    website = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)

        messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}\n"
                                                   f"password: {data[website]['password']}")
        email_entry.delete(0, END)
        password_entry.delete(0, END)

        email_entry.insert(0, data[website]['email'])
        password_entry.insert(0, data[website]['password'])

    except KeyError:
        messagebox.showerror(title="Error", message=f"No details of '{website}' exists!")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data file found!")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=70, pady=70, bg=YELLOW)

# Canvas
canvas = Canvas(width=200, height=200, bg=YELLOW, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Web site: ", bg=YELLOW)
email_label = Label(text="Email/User name: ", bg=YELLOW)
password_label = Label(text="Password: ", bg=YELLOW)

website_label.grid(row=1, column=0)
email_label.grid(row=2, column=0)
password_label.grid(row=3, column=0)

# Entry
website_entry = Entry(width=21)
website_entry.focus()
email_entry = Entry(width=40)
password_entry = Entry(width=21)

website_entry.grid(row=1, column=1)
email_entry.grid(row=2, column=1, columnspan=2)
password_entry.grid(row=3, column=1)

# Buttons
generate_pass_button = Button(text="generate password", width=15, command=generate_password)
search_button = Button(text="Search", width=15, command=search)
add_button = Button(text="Add", width=35, command=save)

generate_pass_button.grid(row=3, column=2)
add_button.grid(row=4, column=1, columnspan=2)
search_button.grid(row=1, column=2)

window.mainloop()


