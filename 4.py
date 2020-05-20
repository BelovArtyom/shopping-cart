double_bar_country = {"40": "Germany"}
triple_bar_country = {"471": "Taiwan"}


class Cart:

    def __init__(self, items, total=0):
        if items is Item:
            self.items = [items]
            self.total = items.price
        elif items is list:
            self.items = []
            self.total = 0
            for x in range(0, len(items)):
                self.items.append(items[x])
                self.total += items[x].price

    def addfromfile(self, impfile):
        with open(impfile) as file:
            filelines = file.readlines()
            for x in range(0, len(filelines)):
                iteminfo = filelines[x].split(" ")

                self.total += int(iteminfo[1])
                self.items.append(Item(iteminfo[0], iteminfo[1], iteminfo[2]))

    def exporttofile(self, filename):
        # setting in append mode to not erase previous data
        with open(filename, "a") as file:
            for x in range(0, len(self.items)):
                info = self.items[x]
                file.write("\n", info.title, " ", info.price, " ", info.barcode)


    def additem(self, item):
        self.items.append(item)
        self.total += item.price

    def deleteitem(self, item):
        if item in self.items:
            self.items.remove(item)
            self.total -= int(item[1])


class Item:

    def __init__(self, title, price, barcode):
        self.title = title
        self.price = price
        self.barcode = barcode
        barcode = int(barcode)

        # checking validity of barcode
        odd = []
        even = []
        for x in range(0, 12):
            if x % 2 != 0:
                odd.append(int(barcode[x]))
            else:
                even.append(int(barcode[x]))
        checksum = 0
        for x in range(0, 6):
            checksum += odd[x] * 3 + even[x]

        checknum = 0
        while checksum % 10 != 0:
            checksum += 1
            checknum += 1

        # applying country as of barcode
        if len(barcode) == 13 and checknum == int(barcode[13]):

            # applying countries with intervals
            if int(barcode[0]) == 0:
                self.country = "USA & Canada"
            elif int(barcode[0:1]) >= 20 and int(barcode[0:1]) <= 29:
                self.country = "In-store function"
            elif int(barcode[0:1]) >= 30 and int(barcode[0:1]) <= 37:
                self.country = "France"
            elif int(barcode[0:1]) >= 40 and int(barcode[0:1]) <= 44:
                self.country = "Germany"

            # applying countries from dicts
            elif barcode[0:1] in double_bar_country:
                self.country = double_bar_country[barcode[0:1]]
            elif barcode[0:2] in triple_bar_country:
                self.country = triple_bar_country[barcode[0:2]]
        else:
            # if not in list, most likely not included or not real
            raise ValueError


cart = Cart([])
cart.items = []

# start menu
success = None
while success != "yes":
    action = None
    actions = ["add", "remove", "importfile", "exportfile"]
    while action not in actions:
        print("Выберите действие над корзинкой ", actions, ":", sep="", end="")
        action = input()

    if action == "add":
        iteminfo = input("Наберите название, цену и штрихкод через пробелы:").split(" ")
        cart.additem(Item(iteminfo[0], iteminfo[1], iteminfo[2]))

    elif action == "remove":
        iteminfo = input("Наберите название, цену и штрихкод через пробелы:").split(" ")
        cart.deleteitem(Item(iteminfo[0], iteminfo[1], iteminfo[2]))

    elif action == "importfile":
        filename = input("Наберите имя файла с .txt:")
        cart.addfromfile(filename)

    elif action == "exportfile":
        filename = input("Наберите имя файла с .txt:")
        cart.exporttofile(filename)

    success = input("Напишите \"yes\", если закончили с этой корзинкой:")
