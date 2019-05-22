import random
import math


class Player:
    player_list = {}
    
    def __init__(self, name, money=1500):
        self.name = name
        self.money = money
        self.jail = False
        self.jail_counter = 0
        self.position = 0
        # Colours, Utilities, Railroads
        self.properties = [[], [], []]
        self.jail_free = 0
        Player.player_list[self.name] = self

    def list_all(self):
        for x in self.properties[0]:
            print(x.name + ' '*(32-len(x.name)), end="")
            if x.houses > 0:
                print(str(x.houses) + " houses")
            elif x.hotel > 0:
                print(str(x.hotel) + " hotel")
            print("")
        print("\n")
        for x in self.properties[1]:
            print(x.name)
        print("\n")
        for x in self.properties[2]:
            print(x.name)

    def move_action(self):
        self.position = (self.position + Dice.roll[0] + Dice.roll[1]) ^ 40
        tiles[self.position].action(self)

    def roll_dice(self, counter=0):
        if not self.jail:
            Dice.throw()
            initial_position = self.position
            print(self.name + " rolled a " + str(Dice.roll[0] + Dice.roll[1]))
            if Dice.roll[0] == Dice.roll[1]:
                print("Rolled doubles.")
                if counter == 2:
                    self.jailed()
                    print("Double three times in a row. ", end="")
                else:
                    if initial_position > self.position > 0:
                        Go.action(self)
                    self.roll_dice(counter + 1)
                    self.move_action()
                    return
            else:
                if initial_position > self.position > 0:
                    Go.action(self)
                self.move_action()
        else:
            choice = input("Roll for doubles (R), pay fine (F), or use card (C).")
            if choice.lower == "r":
                Dice.throw()
                if Dice.roll[0] == Dice.roll[1]:
                    self.move_action()
                else:
                    if self.jail_counter == 2:
                        self.transaction(-50, "the Bank", True)
                        self.move_action()
                    else:
                        self.jail_counter += 1
            elif choice.lower == "f":
                self.transaction(-50, "the Bank", True)
                Dice.throw()
                self.move_action()
            elif choice.lower == "c":
                if self.jail_free > 0:
                    self.jail_free -= 1
                    Dice.throw()
                    self.move_action()
                else:
                    print("No get out of jail free cards. Try again.")
                    self.roll_dice()
                    return
            else:
                print("Invalid choice. Try again")
                self.roll_dice()
                return

        for x in Player.player_list:
            if x.money < 0:
                x.debt()

    def debt(self):
        while self.money < 0:
            print("Money = " + str(self.money))
            choice = input("Sell, mortgage, trade with another player, or declare bankruptcy?")
            if choice.lower() == "sell":
                for x in self.properties[0]:
                    if x.houses > 0 or x.hotel > 0:
                        print(x.name + ' ' * (32 - len(x.name)), end="")
                        if x.houses > 0:
                            print(str(x.houses) + " houses")
                        elif x.hotel > 0:
                            print(str(x.hotel) + " hotel")
                        print("")

                awef
            elif choice.lower() == "mortgage":
                for x in self.properties[0]:
                    if x.houses == 0:
                        print(x.name)
                print("\n")
                for x in self.properties[1]:
                    print(x.name)
                print("\n")
                for x in self.properties[2]:
                    print(x.name)
            elif choice.lower() == "trade":
                for x in Player.player_list:
                    print(x.name)


    def transaction(self, value, partner, trusted=False):
        if not trusted:
            if self.money + value >= 0 and Player.player_list[partner] - value >= 0:
                if value >= 0:
                    print(partner + " paid " + value + " to " + self.name)
                elif value < 0:
                    print(self.name + " paid " + value + " to " + partner)
            else:
                print("Not enough money!")
        else:
            self.money += value
            Player.player_list[partner].money -= value
            
            if self.money < 0:
                self.debt()
            elif Player.player_list[partner].money < 0:
                Player.player_list[partner].debt()

    def jailed(self):
        self.position = 10
        self.jail = True
        print("Sent to jail.")


class Tile:
    def __init__(self, name):
        self.name = name


class Go(Tile):
    def __init__(self, name="GO"):
        Tile.__init__(self, name)

    @staticmethod
    def action(player):
        print("For passing or landing on Go, ", end="")
        player.transaction(200, "the Bank")


class CommunityChest(Tile): 
    cards_list = {0: "Advance to \"GO\"", 1: "Bank error in your favour.", 2: "Doctor's fees.", 3: "Sale of stock.",
                  4: "Get out of jail free.", 5: "Go to jail.", 6: "Holiday fund matures.", 7: "Income tax refund.",
                  8: "It's your birthday.", 9: "Life insurance matures.", 10: "Hospital fees.", 11: "School fees.",
                  12: "Consultancy fee.", 13: "Street repairs.", 14: "2nd place in a beauty contest.",
                  15: "Inheritance."}

    def __init__(self, name="Community Chest"):
        Tile.__init__(self, name)

    @staticmethod
    def action(player):
        card = random.randint(0, len(CommunityChest.cards_list))
        print(CommunityChest.cards_list[card])
        if card == 0:
            player.position = 0
        elif card == 1:
            player.transaction(200, "the Bank", True)
        elif card == 2:
            player.transaction(-50, "the Bank", True)
        elif card == 3:
            player.transaction(50, "the Bank", True)
        elif card == 4:
            player.jail_free += 1
            del CommunityChest.cards_list[4]
        elif card == 5:
            player.position = 10
            player.jailed()
        elif card == 6:
            player.transaction(100, "the Bank", True)
        elif card == 7:
            player.transaction(20, "the Bank", True)
        elif card == 8:
            for payer in Player.player_list:
                player.transaction(10, Player.player_list[payer], True)
        elif card == 9:
            player.transaction(100, "the Bank", True)
        elif card == 10:
            player.transaction(-50, "the Bank", True)
        elif card == 11:
            player.transaction(-50, "the Bank", True)
        elif card == 12:
            player.transaction(25, "the Bank", True)
        elif card == 13:
            houses = 0
            hotels = 0
            for x in range(0, len(player.properties[0])):
                houses += player.properties[0][x].houses
                hotels += player.properties[0][x].hotel
            player.transaction(-40*houses-115*hotels, "the Bank", True)
        elif card == 14:
            player.transaction(10, "the Bank", True)
        elif card == 15:
            player.transaction(100, "the Bank", True)


class Chance(Tile):
    cards_list = {0: "Advance to \"GO\"", 1: "Advance to Illinois Avenue.", 2: "Advance to St. Charles Place.",
                  3: "Advance to nearest utility, and roll again to decide payment",
                  4: "Advance to nearest railroad. If owned, pay double to the owner.",
                  5: "Bank pays you.", 6: "Get out of jail free.", 7: "Go back three spaces.",
                  8: "Go to jail.", 9: "Make general repairs on your properties.", 10: "Pay poor tax.",
                  11: "Take a trip to Reading Railroad.", 12: "Go to Boardwalk.", 13: "Chairman. Pay each player $50.",
                  14: "Building loan matures.", 15: "You won a crosswords competition."}

    def __init__(self, name="CHANCE"):
        Tile.__init__(self, name)

    @staticmethod
    def action(player):
        card = random.randint(0, len(CommunityChest.cards_list))
        print(CommunityChest.cards_list[card])
        if card == 0:
            player.position = 0
        elif card == 1:
            player.position = 24
        elif card == 2:
            player.position = 11
        elif card == 3:
            if 13 < player.position < 29:
                player.position = 28
                Dice.throw()
        elif card == 4:
            if 15 > player.position >= 5:
                player.position = 15
            elif 25 > player.position >= 15:
                player.position = 25
            elif 35 > player.position >= 25:
                player.position = 35
            else:
                player.position = 5

            if tiles[player.position] is not None:
                tiles[player.position].action(player)
        elif card == 5:
            player.transaction(50, "the Bank", True)
        elif card == 6:
            player.jail_free += 1
            del Chance.cards_list[6]
        elif card == 7:
            player.position -= 3
        elif card == 8:
            player.position = 10
            player.jailed()
        elif card == 9:
            houses = 0
            hotels = 0
            for x in range(0, len(player.properties[0])):
                houses += player.properties[0][x].houses
                hotels += player.properties[0][x].hotel

            player.transaction(-25 * houses - 100 * hotels, "the Bank", True)
        elif card == 10:
            player.transaction(-15, "the Bank", True)
        elif card == 11:
            player.position = 5
        elif card == 12:
            player.position = 39
        elif card == 13:
            for payee in Player.player_list:
                player.transaction(-50, Player.player_list[payee], True)
        elif card == 14:
            player.transaction(150, "the Bank", True)
        elif card == 15:
            player.transaction(100, "the Bank", True)


class Property(Tile):
    def __init__(self, name, position, value, rent):
        self.position = position
        Tile.__init__(self, name)
        self.player = banker
        self.value = value
        self.rent = rent
        self.sold = False
        self.mortgaged = False

    def mortgage(self):
        if not self.mortgaged:
            self.player.transaction(self.value/2, "the Bank")
            print("Mortgaged " + self.name)
        else:
            if self.player.transaction(math.ceil((self.value/2)*1.1), "the Bank"):
                print("Un-mortgaged" + self.name)
            else:
                print(self.name + "remains mortgaged")
                self.mortgaged = not self.mortgaged
                # This inversion nullifies the inversion done in the next line
        self.mortgaged = not self.mortgaged

    def action(self, player):
        if not self.sold:
            self.sell(player)
        else:
            if not self.mortgaged:
                player.transaction(self.rent, self.player, True)

    def sell(self, player):
        option = input("Buy or auction property?")
        if option.lower() == "buy":
            if player.money < self.value:
                print("Not enough money. Please auction.")
                self.sell(player)
            else:
                player.transaction(-self.value, "the Bank")
                self.player.properties.remove(self)
                self.player = player
                player.properties.append(self)
        elif option.lower() == "auction":
            bid = 1
            player_list_copy = list(Player.player_list)
            while len(player_list_copy) != 1:
                for player_num in range(len(player_list_copy)):
                    choice = input("Bid or fold. Current bid: " + str(bid))
                    if choice == "fold":
                        del player_list_copy[player_num]
                    elif choice == "bid":
                        new_bid = input("Enter bid. Current bid: " + str(bid))
                        if bid < new_bid <= player_list_copy[player_num].money:
                            bid = new_bid
                        else:
                            print("Invalid bid. Try again.")
                            player_num -= 1
                    else:
                        print("Invalid input. Try again.")
                        player_num -= 1
            player_list_copy[0].transaction(-bid, "the Bank")
            self.player.properties.remove(self)
            self.player = player
            player.properties.append(self)
        else:
            print("Please choose to buy or auction.")
            self.sell(player)


class Colours(Property):
    def __init__(self, name, position, value, rent):
        Property.__init__(self, name, position, value, rent)
        self.houses = 0
        self.hotel = 0
        self.set = False
        self.change = True
        banker.properties[0].append(self)

        if value <= 120:
            self.house_value = 50
        elif value <= 200:
            self.house_value = 100
        elif value <= 280:
            self.house_value = 150
        else:
            self.house_value = 200

    def add_house(self):
        if self.hotel == 0:
            if self.player.money >= self.house_value:
                self.houses += 1
                self.player.transaction(-self.house_value, "the Bank")
                print("One house bought.")
            else:
                print("No houses bought.")
                return

            if self.houses == 5:
                print("Traded five houses in for a hotel.")
                self.hotel += 1

            self.change = True
        else:
            print("Already at maximum occupancy for this property.")

    def sell_house(self):
        if self.hotel > 0:
            self.hotel -= 1
            self.player.transaction(self.house_value/2, "the Bank")
            print("One hotel sold.")
            self.change = True
        elif self.houses > 0:

        else:
            print("No houses to sell. None sold.")

    def mortgage(self):
        if self.houses == 0 and self.hotel == 0:
            Property.mortgage(self)
        else:
            print("You own houses or hotels on this property. You must sell those before mortgaging.")

    def action(self, player):
        if self.player != player:
            if self.change:
                self.rent = self.set_rent()
                self.change = not self.change
            Property.action(self, player)

    def set_rent(self):
        if self.houses == 0:
            self.change = not self.change
            return self.rent*2 if self.set else self.rent
        elif self.houses == 1:
            if self.value == 320:
                # Pennsylvania Ave is the one outlier
                return 150
            else:
                return self.rent*5
        elif self.houses == 2:
            if self.value == 120:
                return self.rent*25/2
            elif self.value == 320:
                return self.value*225/14
            elif 180 <= self.value < 240 or self.value == 350:
                return math.floor(self.rent*10/7)*10
            else:
                return self.value*15
        elif self.houses == 3:
            if self.value == 120 or self.value == 200 or self.value == 240:
                return self.rent*37.5
            elif self.value < 120 or self.value == 140:
                return self.rent*45
            elif self.value <= 280:
                return math.ceil(self.value*85/1400)*50
            elif self.value <= 400:
                return math.floor(self.value*14/400-1)*100
        elif self.houses == 4:
            if self.value <= 60:
                return self.value*80
            elif self.value <= 120:
                return self.value/2*5+150
            elif self.value <= 140:
                return 625
            elif self.value <= 180:
                return math.floor(self.value*35/400)*50
            elif self.value == 200:
                return self.value*4
            elif self.value <= 280:
                return 5/2*self.value+325
            elif self.value <= 320:
                return 5*self.value-400
            elif self.value <= 400:
                return 8*self.value-1500
        elif self.hotel == 1:
            if self.name == "Mediterranean Avenue":
                return 250
            elif self.value <= 120:
                return 5/2*self.value+300
            elif self.value <= 160:
                return 7.5*self.value-300
            elif self.value <= 280:
                return 5/2*self.value+500
            elif self.value <= 320:
                return 25/4*self.value-600
            elif self.value <= 400:
                return 10*self.value-2000


class Utilities(Property):
    def __init__(self, name, position, value):
        Property.__init__(self, name, position, value, 0)
        self.set = False
        self.rent = 0
        banker.properties[1].append(self)

    def action(self, player):
        if self.player != player:
            self.rent = (Dice.roll[0] + Dice.roll[1])*(4 if self.set else 10)
            Property.action(self, player)


class Railroad(Property):
    def __init__(self, name, position):
        Property.__init__(self, name, position, 200, 25)
        banker.properties[2].append(self)

    def action(self, player):
        if self.player != player:
            self.rent = 25 * (2 ** len(self.player.properties[2]))
            Property.action(self, player)


class Tax(Tile):
    def __init__(self, name, rent):
        Tile.__init__(self, name)
        self.rent = rent

    def action(self, player):
        player.transaction(-self.rent, "the Bank", True)


class Dice:
    roll = [0, 1]

    @staticmethod
    def throw():
        Dice.roll[0] = random.randint(1, 6)
        Dice.roll[1] = random.randint(1, 6)


banker = Player("the Bank", 1000000)


tiles = [Go("GO"),
         Colours("Mediterranean Avenue", 1, 60, 2),
         Colours("Baltic Avenue", 2, 60, 4),
         CommunityChest("Community Chest"),
         Tax("Income Tax", 200),
         Railroad("Reading Railroad", 5),
         Colours("Oriental Avenue", 6, 100, 6),
         Chance("Chance"),
         Colours("Vermont Avenue", 8, 100, 6),
         Colours("Connecticut Avenue", 9, 120, 8),
         Tile("Jail"),
         Colours("St. Charles Place", 11, 140, 10),
         Utilities("Electric Company", 12, 150),
         Colours("States Avenue", 13, 140, 10),
         Colours("Virginia Avenue", 14, 160, 12),
         Railroad("Pennsylvania Railroad", 15),
         Colours("St. James Place", 16, 180, 14),
         CommunityChest(),
         Colours("Tennessee Avenue", 18, 180, 14),
         Colours("New York Avenue", 19, 200, 16),
         Tile("Free Parking"),
         Colours("Kentucky Avenue", 21, 220, 18),
         Chance(),
         Colours("Indiana Avenue", 23, 220, 18),
         Colours("Illinois Avenue", 24, 240, 20),
         Railroad("B. & O. Railroad", 25),
         Colours("Atlantic Avenue", 26, 260, 22),
         Colours("Ventnor Avenue", 27, 260, 22),
         Utilities("Water Works", 28, 150),
         Colours("Marvin Avenue", 29, 280, 24),
         # Go to Jail
         Colours("Pacific Avenue", 31, 300, 26),
         Colours("North Carolina Avenue", 32, 300, 26),
         CommunityChest(),
         Colours("Pennsylvania Avenue", 34, 320, 28),
         Railroad("Short Line", 35),
         Chance(),
         Colours("Park Place", 37, 350, 35),
         Tax("Luxury Tax", 100),
         Colours("Boardwalk", 39, 400, 50)]

banker.list_all()

