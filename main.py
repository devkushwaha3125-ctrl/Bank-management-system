# Create an Account or Register
from pathlib import Path
import json
import random
import string

class Bank:
    database = "database.json"
    data = []
    try:
        if Path(database).exists():
            with open(database) as fs:  # fs is just a variable
                data = json.loads(fs.read())
    except Exception as err:
        print(f"An error occured as {err} try again")

    @classmethod
    def __update(cls):
        with open(cls.database, "w") as fs:
            fs.write(json.dumps(cls.data))

    @staticmethod
    def __generate_accountno():
        char = random.choices(string.ascii_uppercase, k = 4)
        digits = random.choices(string.digits, k = 8)
        acc = char + digits
        final = "".join(acc)
        return final

    def create_account(self):
        info = {
            "name": input("Enter your name :- "),
            "age": int(input("Enter your age :- ")),
            "mail": input("Enter your mail :- "),
            "balance": 0,
            "accountno.": Bank.__generate_accountno(),
            "number": int(input("Tell me your 10 digit number "))
        }

        try:
            while True:
                pin = int(input("Enter your 4 digit pin: "))
                if len(str(pin)) != 4:
                    print("Your pin must be of 4 digit, please try again :- ")
                else:
                    info['pin'] = pin
                    break

        except Exception as ValueError:  # We used this so that if user gives wrong input for this particular field i.e. pin then they don't want to start again and continue from where they make the mistake.
            print("You can only have 4 numbers try again")

        # Do the above thing for the number as well
        if info['age'] < 18:
            print("You are a minor")
            return
        else:
            Bank.data.append(info)
            Bank.__update()


    def deposite_money(self):
        acc_no = input("tell your account number:-")
        pin = int(input("tell your pin :-"))
        user = [i for i in Bank.data if i ['pin'] == pin and i['accountno.'] == acc_no]

        if user:
            money = int(input("how much money you want to deposite :- "))
            if money > 100000 or money<=0:
                print("you cannot deposite more than 100000 rs or less than 0rs")
            else:
                user[0] ['balance'] += money
                print("money added succesfully thanks visit again 💸")
                Bank.__update()

        else:
            print("invalid accountno. or pin ")


        
    def withdrawal_money(self):
        acc_no = input("tell your account number:-")
        pin = int(input("tell your pin :-"))
        user = [i for i in Bank.data if i ['pin'] == pin and i['accountno.'] == acc_no]

        if user:
            money = int(input("how much money you want to withdraw:- :- "))
            if money > user[0]['balance'] or money <= 0:
                print("insufficient balance 😒")
            else:
                user[0] ['balance'] -= money
                print("money debited from your account  💸") 
                Bank.__update()

        else:
            print("invalid accountno. or pin ")

    def check_details(self):
        acc_no = input("tell your account number:-")
        pin = int(input("tell your pin :-"))
        user = [i for i in Bank.data if i ['pin'] == pin and i['accountno.'] == acc_no]
        if user:
            print("your details are : \n ")
            for i in user[0]:
                if i !="pin":
                    print(f"{i} : {user[0] [i]}")
        else:
                print("invalid account no. or pin")

    def update_details():
        acc_no = input("tell your account number:-")
        pin = int(input("tell your pin :-"))
        user = [i for i in Bank.data if i ['pin'] == pin and i['accountno.'] == acc_no]
        
        if user == False:
            print("invalid number or pin ")
        else:
            newdata = {
                "name" : input("enter to skip or type your new name :"),
                "mail" : input("enter to skip or type your new mail :"),
                "number" : input("enter to skip or type your new number:"),
                "pin" :input("enter to skip or type your new pin :")

            }

            if newdata['name'] == "":
                newdata['name'] = user[0]['name']
            
            if newdata['mail'] == "":
                newdata['mail'] = user[0]['mail']
                
            if newdata['number'] == "":
                newdata['number'] = str(user[0]['number'])
            
            if newdata['pin'] == "":
                newdata['pin'] = user[0]['pin']

            newdata['pin'] = int(newdata['pin'])
            newdata['number'] = int(newdata['number'])
        for i in user[0]:
            if i in newdata:
                user[0][i]=newdata[i]


        Bank._update()

        
    def delete_user():
        acc_no = input("tell your account number:-")
        pin = int(input("tell your pin :-"))
        user = [i for i in Bank.data if i ['pin'] == pin and i['accountno.'] == acc_no]

        if user == False:
            print("invalid number or pin ")
            
        else:
            print("are you sure press y/n")
            check = input("press (y) or (N)")
            if check=="y" or check=='Y':
                index = Bank.data.index(user)
                Bank.data.pop(index)

                Bank.update()

            else:
                print('ok')

bank = Bank()

print("Press 01 for Creating an Account")
print("Press 02 for Depositing Money")
print("Press 03 for Withdrawal Money")
print("Press 04 for Checking Balance")
print("Press 05 for Updating some details")
print("Press 06 for deactivate your account")
print("Press 0 to exit")

check = int(input("How may I help you? Type any one option from below "))

if check == 1:
    bank.create_account()

if check == 2 :
    bank.deposite_money()

if check ==3 :
    bank.withdrawal_money()

if check == 4:
    bank.check_details()

if check == 5 :
    bank.update_details()

if check == 6 :
    bank.delete_user()