from subclasses.ATM import ATM, ATMException
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
                result, message = atm.withdraw(int(command[1]), token)

                if result:
                    print("Amount dispensed: {}".format(command[1]))
                print(message)

            if command[0] == "deposit":
                print(atm.deposit(float(command[1]), token)[1])

            if command[0] == "balance":
                print(atm.get_balance(token)[1])

            if command[0] == "history":
                result, history = atm.get_history(token)

                if result == False:
                    print(history)
                    continue

                for line in history:
                    try:
                        print("{} {} {}".format(line[0], line[1], line[2]))
                    except IndexError:
                        print("Failure to Parse History")

            if command[0] == "logout":
                print(atm.log_out(token)[1])

        except IndexError:
            print(command)
            print("Invalid Command")
        except ATMException as ex:
            print(ex)

        time.sleep(1)




if __name__ == "__main__":
    main_event_loop()
