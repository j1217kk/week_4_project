import re

class Property():
    def __init__(self, state, street, rent, expenses):
        self.state = state
        self.street = street
        self.rent = rent
        self.expenses = expenses
        self.roi = rent - expenses
    def __repr__(self):
        return f"\nState: {self.state}\nStreet: {self.street}\nRent: {self.rent}\nExpenses: {self.expenses}\n--------------"

class ROI_Calculator():
    def __init__(self):
        self.users = {}


    def add_user(self):
        '''
        Creates a user and adds a user to self.users
        '''
        name = input("What is your name?" ).lower()
        if name not in self.users:
            self.users[name] = []
            print(f"\nGlad to have you as a new user {name.title()}!\n")
        else:
            print("Sorry, this name is already associated with an existing account.")


    def delete_user(self):
        '''
        Removes user
        '''
        print("Sorry to see you go...")
        name = input("Please specify the name associated with the account you would like to delete: ").lower()
        del self.users[name]
        print(f"The account for {name.title()} has been deleted as well as all associated properties along with it.")
    

    def add_property(self):
        '''
        Adds a property with info (state, street, rent, expenses)
        Creates and adds new user if specified user is not in self.users already
        A user can add multiple properties under one user across different states
        '''
        name = input("Hello, which account/name are you adding properties for? (enter name): ").lower()
        if name not in self.users:
            print(f"Why hello new user! I have just created an account under '{name.title()}'. Welcome and enjoy looking at that beautiful ROI. Now let's continue...")
            self.users[name] = []
        state = input("In which state is your property located? (DO NOT USE ABBRV): ").lower()
        with open("grossrents.txt") as g:
            data = g.readlines()
        proceed = False
        for states in data:
            if state.title() in states:
                proceed = True
        if proceed == False:
            print("Sorry, that is not a valid state")
            return     
        street = input("What street is this property located on? ").lower()
        rent = int(input("What are you charging for monthly rent? "))
        expenses = int(input("What are the total expenses on this property? (Total expense includes tax, insurance, utlities, etc.) : "))
        property = Property(state, street, rent, expenses)
        self.users[name].append(property)
        print(f"Great. Your property in '{state.title()}' has been added under username '{name.title()}'.")
        
    
    def delete_property(self):
        '''
        Deletes a property from a user's properties
        '''
        check_name = input("Please enter name to see all associated properties: ").lower()
        if check_name in self.users:
            print(f"\nHere are the properties associated with {check_name.title()}: ")
            for prop in self.users[check_name]:
                print(prop)
        skreet = input("Please specify the STREET associated with the property you would like to DELETE: ").lower()
        for prop in self.users[check_name]:
            if prop.street == skreet:
                index = self.users[check_name].index(prop)
                print(f"...The property at {skreet.title()} has been removed. ")
                del self.users[check_name][index]

    

    def check_properties(self):
        '''
        Displays current properties associated with given user
        '''
        check_name = input("Please enter your name to see all associated properties: ").lower()
        self.name = check_name
        if check_name in self.users:
            print(f"\nHere are the properties associated with {check_name.title()}: ")
            for prop in self.users[check_name]:
                print(prop)


    def check_roi(self):
        '''
        Checks and returns the ROI for a given property identified by the street name
        ROI calculation is done in the Property object init
        '''
        total = 0
        check_name = input("Please enter the name associated with the property you would like to check the total ROI for: ").lower()
        if check_name in self.users:
            print(f"\nHere are the properties associated with {check_name.title()}: ")
            for prop in self.users[check_name]:
                print(prop)
                total += prop.roi
            print(f"Total ROI on all these properties combined is ${total} monthly.\n")
        get_specific = input("Would you like to see the ROI on a specific individual property (Y/N) ? ").lower()
        if get_specific == 'y':
            account = input("Please specify the STREET associated with the specific property you would like to check the ROI for: ").lower()
            for prop in self.users[check_name]:
                if account == prop.street:
                    print(f"\nThe total ROI (Return on Investment) for {check_name.title()}'s property in {prop.state.upper()} on {prop.street.title()} is ${prop.roi} a month.\n")
                    if total < 0:
                        print("Might want to try getting a better return on investment... just saying...")
        else:
            return
    
    def compare_rent(self):
        '''
        Uses regex to compare a property's rent to state-wide and national numbers
        source: "grossrents.txt"
        '''
        check = False
        with open("grossrents.txt") as g:
            data = g.readlines()
        # for states in data:
        #     print(states)
        check_name = input("Please enter your name to see all associated properties: ").lower()
        if check_name in self.users:
            print(f"\nHere are the properties associated with {check_name.title()}: ")
            for prop in self.users[check_name]:
                print(prop)
        account = input("Please specify the STREET associated with the specific property you would like to analyze: ").lower()
        for prop in self.users[check_name]:
                if account == prop.street:
                    current_prop = prop
                    check = True
        if check == True:
            print(current_prop.state.title())            
            for states in data:
                if current_prop.state.title() in states:
                    states_format = re.compile("([A-Z][a-z]* )*([A-Z][a-z]+)[\s]+[$]([0-9]+)")
                    state_info = states_format.search(states)
                    if state_info:
                        print(f"---For your property at {current_prop.street.title()}...---\n")
                        if state_info.group(1) == None:
                            print(f"Your current rent is ${current_prop.rent}. The current median gross rent in {state_info.group(2)} is ${state_info.group(3)}.")
                        else:
                            print(f"Your current rent is ${current_prop.rent}. The current median gross rent in {state_info.group(1)}{state_info.group(2)} is ${state_info.group(3)}.")
                        if current_prop.rent > int(state_info.group(3)):
                            print(f"You charge ${current_prop.rent - int(state_info.group(3))} higher rent than the state median.")
                            print("Greedy realtor. \n")
                        elif current_prop.rent < int(state_info.group(3)):
                            print(f"You charge ${int(state_info.group(3)) - current_prop.rent} less than the state median.")
                            print("Consider raising those Airbnb prices...\n")
                        else:
                            print("Look at that. You charge the exact same as the state median.\n")
                        if current_prop.rent > 602:
                            print(f"Your property's current rent is also ${current_prop.rent - 602} above the US National median gross rent.\n ")
                        elif current_prop.rent < 602:
                            print(f"Your property's current rent is also ${602 - current_prop.rent} lower than the US national median gross rent.\n ")
                        else:
                            print("Look at that. You also charge the exact same rent on this property as the US National median.\n ")
        elif check == False:
            print("This street is not associated with any of your properties. ")


    def run(self):
        '''
        run run run
        '''
        print("""
$$$$$$$\                                                     $$\                     $$$$$$$\   $$$$$$\  $$$$$$\        $$$$$$\            $$\                     $$\            $$\                                         
$$  __$$\                                                    $$ |                    $$  __$$\ $$  __$$\ \_$$  _|      $$  __$$\           $$ |                    $$ |           $$ |                                $$\    
$$ |  $$ | $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\   $$$$$$\ $$$$$$\   $$\   $$\       $$ |  $$ |$$ /  $$ |  $$ |        $$ /  \__| $$$$$$\  $$ | $$$$$$$\ $$\   $$\ $$ | $$$$$$\ $$$$$$\    $$$$$$\   $$$$$$\          $$ |   
$$$$$$$  |$$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\ $$  __$$\\_$$  _|  $$ |  $$ |      $$$$$$$  |$$ |  $$ |  $$ |        $$ |       \____$$\ $$ |$$  _____|$$ |  $$ |$$ | \____$$\\_$$  _|  $$  __$$\ $$  __$$\        $$$$$$$$\ 
$$  ____/ $$ |  \__|$$ /  $$ |$$ /  $$ |$$$$$$$$ |$$ |  \__| $$ |    $$ |  $$ |      $$  __$$< $$ |  $$ |  $$ |        $$ |       $$$$$$$ |$$ |$$ /      $$ |  $$ |$$ | $$$$$$$ | $$ |    $$ /  $$ |$$ |  \__|     \__$$  __|
$$ |      $$ |      $$ |  $$ |$$ |  $$ |$$   ____|$$ |       $$ |$$\ $$ |  $$ |      $$ |  $$ |$$ |  $$ |  $$ |        $$ |  $$\ $$  __$$ |$$ |$$ |      $$ |  $$ |$$ |$$  __$$ | $$ |$$\ $$ |  $$ |$$ |              $$ |   
$$ |      $$ |      \$$$$$$  |$$$$$$$  |\$$$$$$$\ $$ |       \$$$$  |\$$$$$$$ |      $$ |  $$ | $$$$$$  |$$$$$$\       \$$$$$$  |\$$$$$$$ |$$ |\$$$$$$$\ \$$$$$$  |$$ |\$$$$$$$ | \$$$$  |\$$$$$$  |$$ |              \__|   
\__|      \__|       \______/ $$  ____/  \_______|\__|        \____/  \____$$ |      \__|  \__| \______/ \______|       \______/  \_______|\__| \_______| \______/ \__| \_______|  \____/  \______/ \__|                      
                              $$ |                                   $$\   $$ |                                                                                                                                               
                              $$ |                                   \$$$$$$  |                                                                                                                                               
                              \__|                                    \______/                                                                                                                                                
        """)
        print("-----Welcome to ROI Calculator & Property Manager Plus-----")
        print("""
        What would you like to do? 
        (Please indicate which action by specifying the associated letter key.)
        [A] - Add new user
        [B] - Delete existing user
        [C] - Add property & property info
        [D] - Delete existing property
        [E] - Check all user's current properties & property info
        [F] - Calculate ROI for property
        [G] - Gross state rent comparison
        [Q] - Quit
        """)
        while True:
            choice = input("Please select from the given choices (enter 'H' for help): ").lower()
            if choice == 'a':
                self.add_user()
            elif choice == 'b':
                self.delete_user()
            elif choice == 'c':
                self.add_property()
            elif choice == 'd':
                self.delete_property()
            elif choice == 'e':
                self.check_properties()
            elif choice == 'f':
                self.check_roi()
            elif choice == 'g':
                self.compare_rent()
            elif choice == 'h':
                print("""
                What would you like to do? 
                (Please indicate which action by specifying the associated letter key.)
                [A] - Add new user
                [B] - Delete existing user
                [C] - Add property and property info
                [D] - Delete existing property
                [E] - Check all user's properties
                [F] - Calculate ROI for property
                [G] - Gross state rent comparison
                [Q] - Quit
                """)
            elif choice == 'q':
                print("\nThank you. Have a splendid day.")
                break
            else:
                print("\nNot a valid option.\n")

