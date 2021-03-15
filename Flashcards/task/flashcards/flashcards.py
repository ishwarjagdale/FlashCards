import os
import json
import random
import argparse


class FlashCards:
    def __init__(self):
        self.cards = dict()
        self.logs = list()

    def exit(self):
        self.tolog("\nBye bye!")
        exit()

    def tolog(self, message, stream="print"):
        if stream == "input":
            inp = input(message)
            self.logs.append(message.strip())
            self.logs.append(inp.strip())
            return inp
        else:
            print(message)
            self.logs.append(message.strip())

    def dup_term(self, term):
        while term in self.cards.keys():
            self.tolog(f"\nThe term \"{term}\" already exists.")
            term = self.tolog("", stream="input")
        return term

    def dup_def(self, defn):
        for i in self.cards.values():
            if i[1] == defn:
                self.tolog(f"\nThe definition \"{defn}\" already exists.")
                defn = self.tolog("", stream="input")
        return defn

    def add(self):
        term = self.dup_term(self.tolog("The card:\n", stream="input").strip())
        definition = self.dup_def(self.tolog("The definition of the card:\n", stream="input").strip())
        self.cards[term] = [0, definition]
        self.tolog(f"The pair (\"{term}\": \"{definition}\") has been added.")

    def remove(self):
        card = self.tolog("Which card?\n", stream="input")
        try:
            self.cards.pop(card)
        except KeyError:
            self.tolog(f"Can't remove \"{card}\": there is no such card.\n")
        else:
            self.tolog("The card has been removed.\n")

    def to_file(self, func, **kwargs):
        # self.file = self.tolog("File name:\n", stream="input").strip()
        im_file, ex_file = None, None
        if func == "import":
            if "import_file" in kwargs:
                im_file = kwargs["import_file"]
            else:
                im_file = self.tolog("File name:\n", stream="input").strip()

            try:
                with open(os.path.abspath(im_file), 'r', encoding='utf-8') as file:
                    loaded = json.loads(file.read())
                    self.cards.update(loaded)
                    self.tolog(f"{len(loaded)} cards have been loaded.\n")
            except FileNotFoundError:
                self.tolog("File not found.\n")
        elif func == "export":
            if "export_file" in kwargs:
                ex_file = kwargs["export_file"]
            else:
                ex_file = self.tolog("File name:\n", stream="input").strip()

            try:
                with open(os.path.abspath(ex_file), 'w') as file:
                    json.dump(self.cards, file)
                    self.tolog(f"{len(self.cards)} cards have been saved.\n")
            except OSError as e:
                self.tolog(e)

    def ask(self):
        num = int(self.tolog("How many times to ask?\n", stream="input"))

        for _ in range(num):
            j = random.choice(list(self.cards.keys()))
            answer = self.tolog(f"Print the definition of \"{j}\":\n", stream="input")
            if answer == self.cards[j][1]:
                self.tolog("Correct!")
            else:
                self.cards[j][0] += 1
                if answer in list(map(lambda x: x[1], self.cards.values())):
                    term = list(filter(lambda x: x[0] if x[1][1] == answer else None, self.cards.items()))[0]
                    self.tolog(f"Wrong. The right answer is \"{self.cards[j][1]}\", "
                               f"but your definition is correct for \"{term[0]}\".\n")
                else:
                    self.tolog(f"Wrong. The right answer is \"{self.cards[j][1]}\".")

    def log(self):
        with open(os.path.abspath(self.tolog("File name:\n", stream="input").strip()), 'w') as logFile:
            logFile.write('\n'.join(self.logs))
        print("The log has been saved.")

    def hardest_card(self):
        hards = sorted(self.cards.values())
        li = list(filter(lambda x: self.cards[x][0] == hards[-1][0] if hards[-1][0] != 0 else None, self.cards))
        if len(li) == 0:
            self.tolog("There are no cards with errors.")
        else:
            self.tolog(f"The hardest {'cards are' if len(li) != 1 else 'card is'} " +
                       ", ".join([f"{x}" for x in
                                  li]) + f". You have {hards[-1][0]} errors answering {'them' if len(li) != 1 else 'it'}."
                       )

    def reset_stats(self):
        for i in self.cards:
            self.cards[i][0] = 0
        self.tolog("Card statistics have been reset.")


parser = argparse.ArgumentParser(description="Flash Cards")
parser.add_argument("--import_from", type=str)
parser.add_argument("--export_to", type=str)
args = parser.parse_args()


if __name__ == "__main__":
    app = FlashCards()
    if args.import_from:
        app.to_file("import", import_file=args.import_from)
    while True:
        action = app.tolog("Input the action (add, remove, import, export, ask, exit, log, hardest card, "
                           "reset stats):\n", stream="input").strip().lower()
        if action == "exit":
            app.tolog("Bye bye!")
            if args.export_to:
                app.to_file("export", export_file=args.export_to)
            exit()
        elif action == "add":
            app.add()
        elif action == "remove":
            app.remove()
        elif action in ["import", "export"]:
            app.to_file(action)
        elif action == "ask":
            app.ask()
        elif action == "log":
            app.log()
        elif action == "hardest card":
            app.hardest_card()
        elif action == "reset stats":
            app.reset_stats()
