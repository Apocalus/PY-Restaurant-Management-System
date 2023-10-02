from os import system, name #to clear screen
import json #for database
from getpass import getpass #to input password
import msvcrt as m #to wait till user presses a key
filename = "database.json" #database for user info
filename1 = "customeReviews.json" #database for feedback
filename2 = "orders.json" #database for orders
username_list = [] #all usernames from database
password_list = [] #all passwords from database
username = str()
items = {"CAKE": 50,"COFFEE": 30, "JUICE": 40, "MUFFINS": 100, "PIZZA": 200}
order_dict = dict()
exit = False
exit1 = False
exit2 = False
total = 0

with open(filename, "r") as read_file:
    data = json.load(read_file)        
for i in range(0, len(data)):
    username_list.append(data[i]["username"]) #adds all the usernames to list
    password_list.append(data[i]["password"]) #adds all the passwords to list 
    read_file.close()

def clear(): #clear screen
    # for windows
    if name == 'nt':
        _ = system('cls')

def wait(): #for delay
    m.getch()

def sign_up(): #if not a member
    clear()
    global username_list, username, password_list
    print("\033[3;34;40mSIGN UP PAGE\033[39m")
    print("_________________________________________________")
    username_bool = False
    while username_bool != True:
        username = input("Enter Username:\t")
        if username == "":
            print("\033[0;37;41m|Invalid Username.|\033[39;40m")
            wait()
        elif username in username_list:
            print("\033[0;37;41m|Username already exists.|\033[39;40m")
            wait()
        else:
            username_bool = False
            while username_bool != True:
                password = getpass("Enter Password:\t")
                if len(password) < 8:
                    print("\033[0;37;41m|Password strength: low\nLength of password should be 8 minimum|\033[39;40m")
                    wait(); username_bool = False
                else: 
                    confirm_pass = getpass("Confirm Password:\t")
                    if confirm_pass != password:
                        print("\033[0;37;41m|Passwords don't match.|\033[39;40m")
                        wait(); username_bool = False
                    else:
                        print("\033[0;33m|Account made successfully.|\033[39;40m"); wait()
                        username_bool = True
                        login_details = {}; username_list.append(username); password_list.append(password)
                        with open(filename, "r") as read_file:
                            data = json.load(read_file)
                            login_details["username"] = username
                            login_details["password"] = password
                        data.append(login_details) ; read_file.close()
                        with open(filename, "w") as write_file:
                            json.dump(data, write_file, indent = 4)
                            write_file.close(); return True

def login(): #if a member
    clear()
    global username, username_list, password_list
    print("\033[3;34;40mLOGIN PAGE\033[39m")
    print("_________________________________________________")
    username = input("Enter Username:\t")
    if username not in username_list:
        print("\033[0;37;41m|Username doesn't exist.|\033[39;40m")
        wait(); welcome(); exit  
    else:
        login_bool = False
        while login_bool != True:
            password = getpass("Enter Password:\t")
            with open(filename, "r") as read_file:
                data = json.load(read_file)
            for i in range(0, len(data)):   #searching for username : pair 
                if username == data[i]["username"] and password == data[i]["password"] and len(password) >= 8:
                    print("\033[2;30;43m WELCOME %s\033[39;40m"%username); wait()
                    login_bool = True; return True
            if login_bool != True:
                print("\033[0;37;41m|Wrong login|\033[39;40m")
                login_bool = False

def welcome(): #ask if member or not 
    welcome_bool = False
    while welcome_bool != True:
        clear() #clear
        user_input = input("Welcome to Mac's cafe Homepage\n\nAlready a member?\n1)Yes\n2)No\nEnter number:\t")
        if user_input == '1':
            return_value = login()
            if return_value == True:
                welcome_bool = True; return True
        elif user_input == '2':
            return_value = sign_up()
            if return_value == True:
                welcome_bool = True; return True
        elif user_input != '1' or user_input != '2':
            print("Oops!  That was no valid number.  Try again..."); wait()
            welcome_bool = False

def re_order(): #ordering more than once 
    global order_dict; exit = False
    print("_________________________________________________")
    if len(items) == 0:
        print("Looks like you ordered everything from our menu")
        confirmation()
    else:
        for item, price in items.items():
            print(item + "\t\t" + str(price) + "PKR")
        print("\n")
        order_item = input("What would you like?\t"); item_upper =  order_item.upper()
        if item_upper in items.keys():
            order_dict[item_upper] = items.get(item_upper)
            del items[order_item.upper()]
        else: 
            print("\n")
            print("Sorry, we do not have that.")
        while(exit != True):
            print("\n")
            order_input = input("Would you like to order again?\n1)Yes\n2)No\nPlease enter a number:\t")
            if order_input == '1':
                re_order(); exit = True
            elif order_input == '2':
                exit = True
                return True
            else:
                print("|Invalid|")
                exit = False

def confirmation(): #confirm order
    global exit1
    print("\t|ORDER|")
    print("ITEM\t\tPRICE\n")
    for item, price in order_dict.items():
        print(item + "\t\t" + str(price) + "PKR")
    while(exit1 != True):
        print("\n")
        user_input = input("Confirm order?\n1)Yes\n2)No\nPlease enter a number:\t")
        if user_input == '1':
            exit1 = True
        elif user_input == '2':
            print("|Have a good day!|"); quit()
        else: 
            print("|Invalid|")
            exit1 = False

start = welcome()
if start == True:
    clear()
    print("|Welcome to Mac's cafe|")
    print("_________________________________________________")
    for item, price in items.items():
        print(item + "\t\t" + str(price) + "PKR")
    print("\n")
    order_item = input("What would you like?\t"); item_upper =  order_item.upper() #asking user input 
    if item_upper in items.keys():
        order_dict[item_upper] = items.get(item_upper) #saving order to order_dict
        del items[order_item.upper()]
    else: 
        print("\n")
        print("Sorry, we do not have that.") #error message 
    while(exit != True):
        print("\n") 
        order_input = input("Would you like to order again?\n1)Yes\n2)No\nPlease enter a number:\t") #user input for ordering again
        if order_input == '1':
            re_order()
            confirmation()
            exit = True
        elif order_input == '2':
            if len(order_dict) != 0: #checking for existing orders
                confirmation()
            else: #no existing order
                print("\n")
                print("|Have a good day!|")
                quit()
            exit = True
        else:
            print("|Invalid|")
            exit = False
    clear()
    print("\t|BILL|")
    print("ITEM\t\tPRICE\n")
    for item, price in order_dict.items():
        print(item + "\t\t" + str(price) + "PKR")
        total += price #adds up prices of ordered items
    order_details = {}
    with open(filename2, "r") as read_file:
        data = json.load(read_file)
        order_details["username"] = username
        order_details["order"] = order_dict
    data.append(order_details) ; read_file.close()
    with open(filename2, "w") as write_file:
        json.dump(data, write_file, indent = 4)
        write_file.close()
    print("\n")
    print("Total: %dPKR" %total)
    while (exit2 != True):
        print("_________________________________________________")
        feedback = input("Feeling generous today? How about a feedback!\n1)Yes\n2)No\nEnter a number:\t") #asking for feedback
        if feedback == '1':
            take_feedback = input("|Feedback Column|\n") ; feedback_box = {} #taking feedback and saving to feedback_box 
            with open(filename1, "r") as read_file:
                data = json.load(read_file)
                feedback_box["username"] = username
                feedback_box["feedback"] = take_feedback
            data.append(feedback_box) #appending it to database
            with open(filename1, "w") as write_file:
                json.dump(data, write_file, indent = 4)
            print("\n")
            print("|Thanks for the feedback, we appreciate your co-operation - Have a great day!|")
            exit2 = True
        elif feedback == '2':
            print("\n")
            print("|Have a good day, %s!|"%username)
            exit2 = True
        else:
            print("\033[0;37;41m|Invalid|\033[39;40m")
            exit2 = False