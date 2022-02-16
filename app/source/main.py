from subclasses.ATM import ATM
import time



def main_event_loop():
    atm = ATM()
    atm.insert_dummy_data()

    command = []
    token = ""
    while len(command) == 0 or command[0] != "end":
        command = input("").split()


        try:
            if command[0] == "authorize":
                response = atm.authorize(command[1], command[2])
                try:
                    token = response[2]
                except IndexError:
                    # no token
                    pass
                print(response[1])
            if command[0] == "withdraw":
                print(atm.withdraw(int(command[1]), token)[1])
            if command[0] == "deposit":
                print(atm.deposit(float(command[1]), token)[1])
            if command[0] == "balance":
                print(atm.get_balance(token)[1])
            if command[0] == "history":
                print(atm.get_history(token)[1])
            if command[0] == "logout":
                print(atm.log_out(token)[1])
        except IndexError:
            print(command)
            print("Invalid Command")

        time.sleep(1)




if __name__ == "__main__":
    main_event_loop()
