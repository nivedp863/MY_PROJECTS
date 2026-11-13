

class BusPass:
    def __init__(self,passenger_name,age,source,destination,pass_type):
        self.passenger_name = passenger_name
        self.age = age
        self.source = source
        self.destination = destination
        self.pass_type = pass_type
        self.status = "Active"

        if pass_type.lower() == "monthly":
            self.fee = 500
        elif pass_type.lower() == "quarterly":
            self.fee = 1000
        elif pass_type.lower() == "yearly":
            self.fee = 2000
        else:
            self.fee = 0

    def display_pass(self):
        print("\n----BUS PASS DETAILS----")
        print("Passenger Name:",self.passenger_name)
        print("Age:",self.age)
        print("Source:",self.source)
        print("Destination:",self.destination)
        print("Pass Type:",self.pass_type)
        print("Fee:",self.fee)
        print("Status:",self.status)

    def renew_pass(self):
        self.status = "Renewed"
        print("\n Bus Pass Renewed Successfully")

    def cancel_pass(self):
        self.status = "Cancelled"
        print("\n Bus Pass Cancelled Successfully")

class BusPassReservation:
    def __init__(self):
        self.passes = []

    def reserve_pass(self):
        print("\n----BUS PASS RESERVATION----")

        name = input("enter passenger name:")
        age = int(input("enter age:"))
        source = input("enter source:")
        destination = input("enter destination:")
        pass_type = input("enter pass type (Monthly/Quarterly/Yearly):")

        Bus_pass = BusPass(name,age,source,destination,pass_type)
        self.passes.append(Bus_pass)

        print("\n Bus pass reserved successfully!")
        Bus_pass.display_pass()

    def view_passes(self):
        if len(self.passes) == 0:
            print("\n No bus passes available!!!")
        else:
           for bus_pass in self.passes:
               bus_pass.display_pass()

system = BusPassReservation()

while True:
    print("\n---- BUS PASS RESERVATION SYSTEM----")
    print("1. Reserve Bus Pass")
    print("2. View Bus Passes")
    print("3. Renew Bus Pass")
    print("4. Cancel Bus Pass")
    print("5. Exit")

    choice = int(input("enter your choice:"))
    if choice == 1:
        system.reserve_pass()
    elif choice == 2:
        system.view_passes()
    elif choice == 3:
        if len(system.passes) > 0:
            system.passes[0].renew_pass()
        else:
            print("No pass available")
    elif choice == 4:
        if len(system.passes) > 0:
            system.passes[0].cancel_pass()
        else:
            print("No pass available")
    elif choice == 5:
        print("Thank you!")
        break
    else:
        print("Invalid choice!!!")