# Name: Andrea Palomeque Saldivar
# Date: 11/18/2026
# Description: Simple text adventure game with 5 different endings.

from rich import print
from rich.align import Align
import questionary

# Dictionaries

player = {
    "name": "John Doe",
    "inventory": [],
    "observation": 0,
    "empathy": 0,
    "morbidity": 0
}

passenger1 = {
    "name": "Walter",
    "trust": 0,
    "saved": False,
    "disappeared": False
}

passenger2 = {
    "name": "Elena",
    "trust": 0,
    "saved": False,
    "disappeared": False
}

passenger3 = {
    "name": "Sofia",
    "trust": 0,
    "saved": False,
    "disappeared": False
}

items = {
    "key": {
        "name": "Rusty key",
        "description": "Old rusty key, looks like it would fit in a wagon's lock."
    },

    "journal": {
        "name": "Leather journal",
        "description": "Contains many entries regarding the train and its past passengers, the letter S is engraved at the front."
    },

    "map": {
        "name": "Railway Map",
        "description": "A map of what appears to be railway routes."
    }
}

# Functions

# Constantly checks player morbidity; if it reaches goal, override everything and trigger bad ending
def checkMorbidity(): 
    print("To be implemented")

# Formats the journal contents to look like an actual journal
def displayJounral():
    print("To be implemented")

def startDayOne():
    print()
    print(Align.center("[bold blue]----- DAY ONE -----[/bold blue]"))
    print()
    print("\tA faint, rhythmic rumbling stirs you from your sleep. Brain still foggy, you can't exactly remember where you are or how you got there.")
    print("\tYou slowly open your eyes.")
    print()
    print("\tAbove you is a ceiling you don't recognize; the pale lights flicker once as you straighten your posture, noticing a slight cramp in your neck, you")
    print("\twonder how long you've been asleep for. Somewhere nearby, a steady mechanical hum sparks a sense of recognition: a train.")
    print()
    print("\tThe train's whistle roars all around you. Outside, a blizzard conceals the scenery, painting the windows white. Your memories feel strangely distant.")
    print("\tYou don't recall boarding the train or where you're supposed to be going.")
    print("\tThen, you remember. Your name.")
    print()
    player["name"] = input("\tWhat is your name?: ").capitalize()
    print()
    print("\tYou look around at the other passengers. An older man with a confused look in his eyes sits near the end of the wagon, while a middle aged woman sits")
    print("\tcalmly near him. Besides them, the train appears to be completely empty.")

def actionsDayOne(ap):
    cw = 0
    ce = 0
    while ap > 0:
        print()
        if not backUnlocked:
            action = questionary.select(
                f" What will you do? [{ap} action points remaining.]",
                choices = [
                    questionary.Choice(title = f"   1. Talk to {'Walter' if metWalter else 'the man'}.\n", value = 1),
                    questionary.Choice(title = f"   2. Talk to {'Elena' if metElena else 'the woman'}.\n", value = 2),
                    questionary.Choice(title = "   3. Explore the back of the train.\n", value = 3),
                    questionary.Choice(title = "   4. Explore the front of the train.\n", value = 4),
                    questionary.Choice(title = "   5. Look around your wagon.\n", value = 5),
                    questionary.Choice(title = "   6. Go back to sleep. (Ends the day)\n", value = 6),
                ]
            ).ask()

        else:
            action = questionary.select(
                f" What will you do? [{ap} action points remaining.]",
                choices = [
                    questionary.Choice(title = f"   1. Talk to {'Walter' if metWalter else 'the man'}.\n", value = 1),
                    questionary.Choice(title = f"   2. Talk to {'Elena' if metElena else 'the woman'}.\n", value = 2),
                    questionary.Choice(title = f"   3. Talk to {'Sofia' if metSofia else 'the woman at the back of the train'}.\n", value = 7),
                    questionary.Choice(title = "   4. Explore the back of the train.\n", value = 3),
                    questionary.Choice(title = "   5. Explore the front of the train.\n", value = 4),
                    questionary.Choice(title = "   6. Look around your wagon.\n", value = 5),
                    questionary.Choice(title = "   7. Go back to sleep. (Ends the day)\n", value = 6),
                ]
            ).ask()

        match action:
            case 1:
                if cw < 2:
                    ap, cw = walterDayOne(ap, cw)
                else:
                    print("\tWalter seems to be lost in thought, best to leave him alone.")

            case 2:
                if ce < 2:
                    ap, ce = elenaDayOne(ap, ce)
                else:
                    print("\tElena has closed her eyes, looks like she's trying to sleep.")
            case _:
                print("To be implemented.")
                ap = 0

def walterDayOne(ap, cw):
    global metWalter
    metWalter = True
    if cw == 0:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou approach the man by the end of a wagon, he seems to be staring at the continuous snowstorm outide the window. When he finally looks at you, he")
        print("\toffers you a warm smile, yet you can see a hint of worry behind it.")
        print()
        print("\tWalter: \"Well good morning, I see you're finally awake.\"")
        print()

        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Do you know where we are?", value = 1),
                questionary.Choice(title = "   I don't really want to be.", value = 2),
            ]
        ).ask()
        
        match choice:
            case 1:
                print()
                print("\tHe shakes his head, looking just as lost as you.")
                print()
                print("\tWalter: [green]\"Wish I could tell you, I haven't the faintest idea. Don't remember getting on this train, either, strange bussiness, ain't it?[/green]")
                print("\t         [green]Name's Walter, by the way. Pleased to meet you.\"[/green]")
                print()
                print("\tHe extends his hand and you shake it hesitantly, introducing yourself as well, it's nice knowing you're not alone in this. After a while you return")
                print("\tto your seat.")

            case 2:
                print()
                print("\tThe man gives you an awkward smile, not knowing how to reply to your comment. After a brief silence, he adds.")
                print()
                print("\tWalter: [green]\"Ain't exactly the most pleasant way to start the morning, still might as well make the most of being awake. Name's Walter, by the way.[/green]")
                print("\t         [green]Pleased to meet you.[/green]")
                print()
                print("\tYou give him your name and immediately return to your seat. You get the sense Walter is just as confused as you, and you have no idea how he can seem")
                print("\tso optimistic about the whole situation")
                player["morbidity"] += 1

        return ap - 1, cw + 1
    
    elif cw == 1:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou decide to approach Walter again, he's still looking out the window, you notice his leg bouncing anxiously.")
        print()
        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Do you remember anything from before this?", value = 1),
                questionary.Choice(title = "   Are you okay?", value = 2),
            ]
        ).ask()

        match choice:
            case 1:
                print()
                print("\tWalter: [green]\"Funnily enough I remember working on the railway. Spent the better part of forty years driving trains, as a matter of fact. But if you're[/green]")
                print("\t         [green]asking where I was before waking up here? Couldn't tell you. It's all a little hazy.[/green]")
                print()
                print("\tYou nod, agreeing that you can't remember where you were either, and then return to your seat.")

            case 2:
                print()
                print("\tWalter looks at his restless leg, quickly placing a hand on it to stop it from bouncing.")
                print()
                print("\tWalter: [green]\"Well would you look at that, didn't even realize I was doing that. Forty years driving trains and not once have I been this uncertain about[/green]")
                print("\t         [green]a journey. Don't you worry about me though, mighty kind of you to ask.")
                print()
                print("\tYou return to your seat.")
                player["empathy"] += 1

        return ap - 1, cw + 1

def elenaDayOne(ap, ce):
    global metElena
    metElena = True
    if ce == 0:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou decide to approach the woman who is looking at you expectantly with a calm smile, almost as if she already knew you were planning on talking to")
        print("\ther. She moves aside so you can take a seat next to her, which you cautiously do.")
        print()
        print("\tElena: [red]\"Well good morning, I see you're finally awake.\"")
        print()

        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Do you know where we are?", value = 1),
                questionary.Choice(title = "   I don't really want to be.", value = 2),
            ]
        ).ask()
        
        match choice:
            case 1:
                print()
                print("\tHe shakes his head, looking just as lost as you.")
                print()
                print("\tWalter: [green]\"Wish I could tell you, I haven't the faintest idea. Don't remember getting on this train, either, strange bussiness, ain't it?[/green]")
                print("\t         [green]Name's Walter, by the way. Pleased to meet you.\"[/green]")
                print()
                print("\tHe extends his hand and you shake it hesitantly, introducing yourself as well, it's nice knowing you're not alone in this. After a while you return")
                print("\tto your seat.")

            case 2:
                print()
                print("\tThe man gives you an awkward smile, not knowing how to reply to your comment. After a brief silence, he adds.")
                print()
                print("\tWalter: [green]\"Ain't exactly the most pleasant way to start the morning, still might as well make the most of being awake. Name's Walter, by the way.[/green]")
                print("\t         [green]Pleased to meet you.[/green]")
                print()
                print("\tYou give him your name and immediately return to your seat. You get the sense Walter is just as confused as you, and you have no idea how he can seem")
                print("\tso optimistic about the whole situation")
                player["morbidity"] += 1

        return ap - 1, ce + 1
    
    elif ce == 1:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou decide to approach Walter again, he's still looking out the window, you notice his leg bouncing anxiously.")
        print()
        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Do you remember anything from before this?", value = 1),
                questionary.Choice(title = "   Are you okay?", value = 2),
            ]
        ).ask()

        match choice:
            case 1:
                print()
                print("\tWalter: [green]\"Funnily enough I remember working on the railway. Spent the better part of forty years driving trains, as a matter of fact. But if you're[/green]")
                print("\t         [green]asking where I was before waking up here? Couldn't tell you. It's all a little hazy.[/green]")
                print()
                print("\tYou nod, agreeing that you can't remember where you were either, and then return to your seat.")

            case 2:
                print()
                print("\tWalter looks at his restless leg, quickly placing a hand on it to stop it from bouncing.")
                print()
                print("\tWalter: [green]\"Well would you look at that, didn't even realize I was doing that. Forty years driving trains and not once have I been this uncertain about[/green]")
                print("\t         [green]a journey. Don't you worry about me though, mighty kind of you to ask.")
                print()
                print("\tYou return to your seat.")
                player["empathy"] += 1

        return ap - 1, ce + 1

# Variables

actionPoints = 6
metWalter = False
metElena = False
metSofia = False
backUnlocked = False

# Main
def main():
    startDayOne()
    actionsDayOne(actionPoints)


if __name__ == "__main__":
    main()