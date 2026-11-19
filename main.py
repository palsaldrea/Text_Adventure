# Name: Andrea Palomeque Saldivar
# Date: 11/18/2026
# Description: Text adventure demo with 3 different endings.

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

# Variables
actionPoints = 6
day = 1
dayDone = False
metWalter = False
metElena = False
metSofia = False
knowSofia = False
backExplored = False
backUnlocked = False
frontExplored = False
# Number of time's we've talked to characters
cw = 0
ce = 0
cs = 0

# Functions

# Constantly checks player morbidity; if it reaches goal, override everything and trigger bad ending, to be added
def checkMorbidity(): 
    print("To be implemented")

# Formats the journal contents to look like an actual journal, to be added
def displayJounral():
    print("To be implemented")

# Prints narration for first day
def startDayOne():
    print()
    print(Align.center("[bold magenta]----- DAY ONE -----[/bold magenta]"))
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

# Takes in action points and lets players perform actions on the first day
def actionsDayOne(ap):
    global cw
    global ce
    global cs
    global dayDone
    while ap > 0:
        print()
        if not metSofia: # Sofia won't show up in the menu if the player hasn't met her
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
                    questionary.Choice(title = f"   3. Talk to {'Sofia' if knowSofia else 'the woman at the back of the train'}.\n", value = 7),
                    questionary.Choice(title = "   4. Explore the back of the train.\n", value = 3),
                    questionary.Choice(title = "   5. Explore the front of the train.\n", value = 4),
                    questionary.Choice(title = "   6. Look around your wagon.\n", value = 5),
                    questionary.Choice(title = "   7. Go back to sleep. (Ends the day)\n", value = 6),
                ]
            ).ask()

        match action:
            case 1: # Talk to Walter, max 2 times first day
                if cw >= 2 and day == 1:
                    print("\tWalter seems to be lost in thought, best to leave him alone.")
                else:
                    ap, cw = walter(ap, cw)

            case 2: # Talk to Elena, max 2 times first day
                if ce >= 2 and day == 1:
                    print("\tElena has closed her eyes, looks like she's trying to sleep.")
                else:
                    ap, ce = elena(ap, ce)

            case 3:
                if backExplored and metSofia: # Avoids repeated dialogue
                    print("\tYou make your way towards the back of the train once more. The wagon remains unlocked and everything inside appears just as you left it. With nothing")
                    print("\tnew to find, you return to your seat.")
                else:
                    ap = exploreBack(ap)

            case 4:
                if frontExplored: # Avoids repeating dialogue if the player explores front again
                    print("\tYou make your way towards the front of the train once more. The conductor's cabin remains firmly shut, just as before. There's nothing new to find")
                    print("\there, so you head back to your seat.")
                else:
                    ap = exploreFront(ap)

            case 5:
                ap = lookAround(ap)

            case 6: # Ends the day prematurely
                ap = endDay()

            case 7: # Talk to Sofia, max 2 times first day
                if cs >= 2 and day == 1:
                    print("\tYou try to approach Sofia once more, but she ignores you.")
                else:
                    ap, cs = sofia(ap, cs)

    if not dayDone: # Print ending day message if player runs out of action points
        print()
        print("\tYou're too tired to do anything else. Back in your seat, you try your best to get comfortable and allow a new day to come.")
        dayDone = True

    print()

# All possible Walter conversations
def walter(ap, cw):
    global metWalter
    metWalter = True
    if cw == 0:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou approach the man by the end of a wagon, he seems to be staring at the continuous snowstorm outide the window. When he finally looks at you, he")
        print("\toffers you a warm smile, yet you can see a hint of worry behind it.")
        print()
        print("\t???: \"Well good morning, I see you're finally awake.\"")
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
                print("\tso optimistic about the whole situation.")
                player["morbidity"] += 1 # Increases morbidity by pessimistic answer

        return ap - 1, cw + 1 # Decreases action point and increases conversation time
    
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
                print("\t         [green]a journey. Don't you worry about me though, mighty kind of you to ask.\"[/green]")
                print()
                print("\tYou return to your seat.")
                player["empathy"] += 1

        return ap - 1, cw + 1
    
    elif cw == 2 and day == 2:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou approach Walter. He's leaning forward in his seat, occasionally glancing towards the connecting door as if expecting someone to come through.")
        print("\tHis hands are clasped tightly together, and his usual welcoming expression has been replaced by a look of concern.")
        print("\tWhen he notices you, he quickly straightens himself.")
        print()
        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Is something bothering you?", value = 1),
                questionary.Choice(title = "   Have you figured out anything about our destination?", value = 2),
            ]
        ).ask()

        match choice:
            case 1:
                print()
                print("\tWalter: [green]\"I reckon there's something truly wrong around here. I've been hearing things at night. Footsteps, doors opening... but every time I go and[/green]")
                print("\t         [green]check, there's nobody there.\"[/green]")
                print()
                print("\tWalter looks towards the connecting door again and says nothing more, seemingly distracted by something you can't see. You decide to leave him to") 
                print("\this thoughts and return to your seat.")

            case 2:
                print()
                print("\tWalter: [green]\"That's just it. I've been thinking about the route, and none of it makes sense. I've seen plenty of railways in my time, kid, but this...[/green]")
                print("\t         [green]this ain't following any route I've ever known. I'm starting to think this train doesn't want us getting off.\"[/green]")
                print()
                print("\tWalter looks towards the connecting door again and says nothing more, seemingly distracted by something you can't see. You decide to leave him to") 
                print("\this thoughts and return to your seat.")
                print()
        return ap - 1, cw + 1

    elif cw == 3 and day == 2: # Only available on day 2
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou approach Walter, but something about him immediately catches your attention. He's no longer sitting comfortably in his seat. Instead, he's huddled")
        print("\tnear the window, repeatedly glancing towards the connecting door. His breathing is uneven, and his hands tremble slightly. As you get closer,")
        print("\the suddenly looks up at you.")
        print()
        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Walter, what's happened? You're frightening yourself.", value = 1),
                questionary.Choice(title = "   I know what's wrong Walter, just breathe.", value = 2, disabled = "Not enough information" if not knowSofia else None), # Can't select if not met Sofia
            ]
        ).ask()

        match choice:
            case 1:
                print()
                print("\tWalter: [green]\"They're coming. I know they're coming. I've heard them walking outside the wagon, stopping right behind that door. I can't stay here.[/green]")
                print("\t         [green]I need to get off this train. I need to get away before they find me.\"[/green]")
                print()
                print("\tHe grips the edge of his seat and looks around frantically. You try calming him down but to no avail, wondering what could've happened to get him") 
                print("\tlike this. After a few minutes, he appears to completely shut off. Defeated, you return to your seat, hoping it'll pass.")
                print()
            case 2:
                print()
                print("\tYou explain to him what you learned, about this place slowly changing people and the disappearances. At first, it seems to make him even more paranoid,")
                print("\tuntil you tell him about Sofia, who's been there a while and hasn't disappeared. You explain the best way to stay safe is to remain")
                print("\tcalm and hopeful.")
                print()
                print("\tHe nods along your words, as his breathing evens out eventually. He still seems a bit nervous, but no longer in a panic state. You decide to sit") 
                print("\twith him for a while until he's mostly recovered, then you return to your seat.")
                passenger1["saved"] = True # Walter won't disappear morning of day 3
        return ap - 1, cw + 1

# All possible Elena conversations
def elena(ap, ce):
    global metElena
    metElena = True
    if ce == 0:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou decide to approach the woman who is looking at you expectantly with a calm smile, almost as if she already knew you were planning on talking to")
        print("\ther. She moves aside so you can take a seat next to her, which you cautiously do.")
        print()
        print("\t???: [red]\"Good morning. I was beginning to wonder when someone would come by.\"[/red]")
        print()

        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Do you know where we are?", value = 1),
                questionary.Choice(title = "   You seem rather calm.", value = 2),
            ]
        ).ask()
        
        match choice:
            case 1:
                print()
                print("\tElena: [red]\"I'm afraid not, no idea where we might be going either. Though I suppose the destination isn't often the most important part.[/red]")
                print("\t        [red]My name's Elena, it's very nice to meet you.\"[/red]")
                print()
                print("\tShe smiles, you find her mindset extremely odd given the situation, yet you still give her your name. It is a little reassuring knowing someone in")
                print("\tthis train doesn't look alarmed.")

            case 2:
                print()
                print("\tShe sighs, a faint smile not leaving her face.")
                print()
                print("\tElena: [red]\"I suppose I've had some time to think. There are things I remember from before this moring, I believe there's a reason I'm here...[/red]")
                print("\t        [red]I just haven't quite figured it out yet. It's nice knowing I'm not in this alone, my name's Elena.[/red]")
                print()
                print("\tYou tell her your name, wondering what she could possibly mean by her words, does she know things you don't? You try your hardest, but can't seem to")
                print("\trecall anything. Eventually you go back to your seat")

        return ap - 1, ce + 1
    
    elif ce == 1:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou decide to approach Elena again, she seems as composed as before. Once again, she smiles when she sees you.")
        print()
        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   What do you remember?", value = 1),
                questionary.Choice(title = "   Do you think we'll get home?", value = 2),
            ]
        ).ask()

        match choice:
            case 1:
                print()
                print("\tElena: [red]\"It's a little hard to explain, I remember being somewhere familiar... the feeling, more than anything. After that, my mind goes blank.[/red]")
                print("\t        [red]It's strange, the memories don't frighten me as much as they probably should, I feel rather comforted here.[/red]")
                print()
                print("\tYou note that she doesn't remember getting on this train either, and think it rather weird she is not the least bit worried. You return to your seat.")

            case 2:
                print()
                print("\tElena: [red]\"I would like to think so. There must be a reason my memories of home stayed with me, I believe we're meant to return eventually.[/red]")
                print("\t        [red]Every journey has an end, even if you can't see it from where you're standing.\"[/red]")
                print()
                print("\tYou return to your seat.")

        return ap - 1, ce + 1

# All posible Sofia conversations
def sofia(ap, cs):
    global knowSofia
    if cs == 0:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou go to approach the young woman at the back of the train. She notices you almost immediately, watching you cautiously as you come closer.")
        print("\tShe doesn't seem particularly welcoming, but she doesn't ask you to leave either.")
        print()
        print("\t???: [cyan]\"Can I help you?\"[/cyan]")
        print()

        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Have you noticed anything strange about this train?", value = 1),
                questionary.Choice(title = "   How long have you been here?", value = 2),
            ]
        ).ask()
        
        match choice:
            case 1:
                print()
                print("\tSofia: [cyan]\"Strange is putting it mildly. I have been here longer than the rest, and every time new people arrive, it never takes long[/cyan]")
                print("\t       [cyan]before they start vanishing. I'm Sofia, you'd be better off not trusting everything you see here.\"[/cyan]")
                print()
                print("\tHer words leave you with more questions than answers. You decide not to press her further and make your way back to your seat, worried")
                print("\tabout her words. How long has this been going on, and what did she mean by disappearing?")

            case 2:
                print()
                print("\tSofia: [cyan]\"Longer than I can remember. I used to count the days, then I started counting the people who disappeared instead.[/cyan]")
                print("\t        [cyan]Funny thing is, I still look exactly the same. I'm Sofia, can't say it's nice to meet you.[/cyan]")
                print()
                print("\tYou get the feeling there's more to her story than she's willing to share. Deciding not to push your luck, you leave her to herself and")
                print("\treturn to your seat.")
        knowSofia = True
        return ap - 1, cs + 1
        
    elif cs == 1:
        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
        print()
        print("\tYou find Sofia sitting in her usual seat, quietly writing in a journal. She pauses when she notices you approaching.")
        print()
        choice = questionary.select(
            "",
            choices = [
                questionary.Choice(title = "   Tell me more about the disappearances", value = 1),
                questionary.Choice(title = "   I think I'll be the first to disappear", value = 2),
            ]
        ).ask()
    
        match choice:
            case 1:
                print()
                print("\tSofia: [cyan]\"Not much to tell, people slowly stop making sense or losing hope, and then one morning they're just gone. If you know of someone[/cyan]")
                print("\t        [cyan]acting strange, don't expect to see them much longer.[/cyan]")
                print()
                print("\tYou make note of her warning, feeling a little uneasy. It sounds like it has happened to many people before. With a heavy heart and a sense of dread")
                print("\tyou return to your seat.")

            case 2:
                print()
                print("\tSofia quickly shots her gaze up at you, giving you a stern look as if saying your comment wasn't funny. Not that you were trying to be.")
                print()
                print("\tSofia: [cyan]\"Don't say that.[/cyan]")
                print()
                print("\tShe stares at you for a few more seconds, not saying anything. You decide to return to your seat.")
                player["morbidity"] += 1
        return ap - 1, cs + 1

# Unlocks the back and introduces Sofia
def unlockBack(ap):
    global metSofia
    choice = questionary.select(
        f"What will you do? [{ap} action points remaining]",
        choices = [
            questionary.Choice(title = "   Go inside", value = 1),
            questionary.Choice(title = "   Return to your seat", value = 2),
        ]
    ).ask()

    match choice:
        case 1:
            if ap > 0: # Makes sure you have enough action points for the action
                print()
                print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
                ap = ap - 1
                print()
                print("\tYou hesitate for a moment before stepping inside. The wagon is dimly lit, with only a few faint lights illuminating the rows of empty seats. The air")
                print("\tfeels unusually still compared to the rest of the train.")
                print()
                print("\tAs you look around, you notice someone sitting near the far end of the carriage. A young woman, sitting quietly by the window. She doesn't seem to have")
                print("\tnoticed you yet, her attention fixed on the scenery outside.")
                print()
                choice = questionary.select(
                    f"Do you approach her? [{ap} action points remaining]",
                    choices = [
                        questionary.Choice(title = "   Yes", value = 1),
                        questionary.Choice(title = "   No", value = 2),
                    ]
                ).ask()

                match choice:
                    case 1:
                        print()
                        print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
                        ap = ap - 1
                        print()
                        print("\tYou decide to approach the young woman. She notices you almost immediately, her eyes following your every movement. She looks you over cautiously,")
                        print("\talmost as if trying to determine whether she can trust you. Before you have a chance to say anything, she speaks.")
                        print()
                        print("\t???: [cyan]\"You shouldn't be here\"[/cyan]")
                        print()
                        print("\tHer voice is quiet, but there's a hint of suspicion behind her words. She doesn't offer much else, and you decide not to press her any further")
                        print("\tfor now. You leave the wagon and make your way back to your seat.")
                        metSofia = True
                        return ap

                    case 2:
                        print()
                        print("\tThere's something rather unusual about finding someone tucked away in an otherwise empty wagon, but you decide not to disturb her. Perhaps you'll have")
                        print("\ta chance to speak with her another time.")
                        print()
                        print("\tYou leave the wagon and make your way back to your seat.") 
                        return ap

            else: 
                print("\tYou are too tired for that, so you return to your seat.")
                return ap
        case 2:
            print()
            print("\tYou peer inside, but the dimly lit wagon offers little reason to venture further. Deciding to leave it for another time, you close the door and make your way")
            print("\tback to your seat.")
            return ap

# Explores the back of the train and checks for key to unlock it
def exploreBack(ap):
    print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
    ap = ap - 1
    global backExplored
    global backUnlocked
    if not backExplored and not metSofia: # First time exploring the back
        print()
        print("\tYou make your way towards the back of the train, passing through the connecting doors between wagons. Unlike the others, this carriage is noticeably")
        print("\tquieter. At the very end, you find a single wagon with its door firmly locked.")
        print()
        backExplored = True
        if items["key"] in player["inventory"]:
            backUnlocked = True
            print("\tYou notice the small keyhole beneath the handle. Remembering the key in your inventory, you take it out and carefully slide it into the lock. It turns") 
            print("\twith a soft click, and the door creaks open.")
            print()
            ap = unlockBack(ap)
            return ap

        else:
            print("\tYou try the handle, but it doesn't budge. A small keyhole sits just beneath it. Whatever is inside, you'll need to find a key before you can get in.")
            print("\tWith no other way forward, you head back to your seat.")
            return ap

    elif backExplored and not backUnlocked: # If already explored but not yet unlocked
        print()
        print("\tYou make your way towards the back of the train once more, stopping in front of the locked wagon.")
        print()
        if items["key"] in player["inventory"]:
            backUnlocked = True
            print("\tYou notice the small keyhole beneath the handle. Remembering the key in your inventory, you take it out and carefully slide it into the lock. It turns") 
            print("\twith a soft click, and the door creaks open.")
            print()
            ap = unlockBack(ap)
            return ap

        else:
            print("\tUnfortunately, without the key, there's still no way to get inside, the door remains firmly shut. Deciding there's nothing more you can do for now,")
            print("\tyou return to your seat.")
            return ap

    elif backUnlocked and not metSofia: # If unlocked but haven't met Sofia yet
        print()
        print("\tYou stand once again at the entrance of the now unlocked door.")
        print()
        ap = unlockBack(ap)
        return ap

# Explore front of the train
def exploreFront(ap):
    print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
    ap = ap - 1
    global frontExplored
    frontExplored = True
    if day <= 2: # More will be available after day 2
        print()
        print("\tYou make your way towards the front of the train, passing through a few connecting doors. At the very front, you find the conductor's cabin. The door")
        print("\tis firmly shut, with no visible keyhole or handle.")
        print()
        print("\tWith no way forward, you make your way back to your seat.")
        print()
        return ap

# Looks around your wagon
def lookAround(ap):
    print("  [italic #ffa03e]-1 action point[/italic #ffa03e]")
    ap = ap - 1
    print()
    print("\tYou decide to take a closer look around your wagon. Most of the seats are empty, and a few pieces of unattended luggage have been left behind.")
    print("\tIt's strange that nobody seems to have come back for them. Perhaps there's something worth investigating.")
    print()
    choice = questionary.select(
        "",
        choices = [
            questionary.Choice(title = "   Look between the seats", value = 1), # Finds key
            questionary.Choice(title = "   Look inside abandoned luggage", value = 2), # Finds journal
        ]
    ).ask()

    match choice:
        case 1:
            if items["key"] not in player["inventory"]:
                print()
                print("\tYou carefully inspect the gaps between the seats, moving aside a few scraps of paper and dust. Something metallic catches your eye. Reaching")
                print("\tdown, you retrieve a small, worn key. You're not sure what it belongs to, but it might come in handy.")
                player["inventory"].append(items["key"])
                print()
                print(f"\t[bold magenta]You obtained: {items["key"]["name"]}")
                print()
                print("\tYou finish searching and return to your seat.")
                return ap
            else:
                print()
                print("\tYou check between the seats once more, not finding anything new. You return to your seat.")
                return ap

        case 2:
            if items["journal"] not in player["inventory"]:
                print()
                print("\tYou approach one of the unattended suitcases and carefully open it. Inside, among a few scattered belongings, you find a small journal. You") 
                print("\ttake the journal with you, wondering who it might belong to.")
                player["inventory"].append(items["journal"])
                print()
                print(f"\t[bold magenta]You obtained: {items["journal"]["name"]}")
                print()
                print("\tYou close the suitcase and return to your seat.")
                print()
                return ap
            else:
                print()
                print("\tYou check the luggage again, not finding anything new. You return to your seat.")
                print()
                return ap

# Returns 0 as the action points, ending the day prematurely
def endDay():
    print("\tYou choose to settle back into your seat. The steady rumbling of the train and its gentle rocking soon begin to lull you to sleep.")
    print("\tWhatever this place is, perhaps you'll find some answers tomorrow. You close your eyes and drift off.")
    global dayDone
    dayDone = True
    return 0

# Prints narration for second day
def startDayTwo():
    print()
    print(Align.center("[bold magenta]----- DAY TWO -----[/bold magenta]"))
    print()
    print("\tA gentle swaying motion gradually pulls you out of your sleep. The occasional rattle of the train's wheels provides a familiar")
    print("\tbackground noise as you slowly regain consciousness. You rub your eyes and sit up, taking a moment to gather your thoughts. For a")
    print("\tbrief second, you wonder where you might have ended up this time, but a quick glance around puts those worries to rest.")
    print()
    print("\tYou stretch your arms and look towards the window. The landscape remains hidden behind the thick snowfall, with little indication")
    print("\tof how far the train has travelled or how much time has passed.")
    print()

# Takes in action points and lets players perform actions on the second day
def actionsDayTwo(ap):
    global dayDone
    global cw
    global ce
    global cs
    while ap > 0:
        print()
        if not metSofia:
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
                    questionary.Choice(title = f"   3. Talk to {'Sofia' if knowSofia else 'the woman at the back of the train'}.\n", value = 7),
                    questionary.Choice(title = "   4. Explore the back of the train.\n", value = 3),
                    questionary.Choice(title = "   5. Explore the front of the train.\n", value = 4),
                    questionary.Choice(title = "   6. Look around your wagon.\n", value = 5),
                    questionary.Choice(title = "   7. Go back to sleep. (Ends the day)\n", value = 6),
                ]
            ).ask()

        match action:
            case 1:
                if cw >= 4 and day == 2:
                    print("\tWalter seems to be lost in thought, best to leave him alone.")
                else:
                    ap, cw = walter(ap, cw)

            case 2:
                if ce >= 2 and day == 2:
                    print("\tElena has closed her eyes, looks like she's trying to sleep.")
                else:
                    ap, ce = elena(ap, ce)
    
            case 3:
                if backExplored and metSofia:
                    print("\tYou make your way towards the back of the train once more. The wagon remains unlocked and everything inside appears just as you left it. With nothing")
                    print("\tnew to find, you return to your seat.")
                else:
                    ap = exploreBack(ap)

            case 4:
                if frontExplored:
                    print("\tYou make your way towards the front of the train once more. The conductor's cabin remains firmly shut, just as before. There's nothing new to find")
                    print("\there, so you head back to your seat.")
                else:
                    ap = exploreFront(ap)
    
            case 5:
                ap = lookAround(ap)
    
            case 6:
                ap = endDay()
    
            case 7:
                if cs >= 2 and day == 2:
                    print("\tYou try to approach Sofia once more, but she ignores you.")
                else:
                    ap, cs = sofia(ap, cs)
    
    if not dayDone:
        print()
        print("\tYou're too tired to do anything else. Back in your seat, you try your best to get comfortable and allow a new day to come.")
        dayDone = True
    
    print()

# Prints narration for bad ending
def badEnding():
    print()
    print("\tA strange sensation pulls you from your sleep. The familiar rumbling of the train seems unusually distant, and the wagon is almost")
    print("\tcompletely silent. Something feels terribly wrong. Your hands look strange. They're faint, almost transparent, as though you're")
    print("\tlooking through a reflection in a window.")
    print()
    print("\tConfused, you reach towards your arm, but your fingers seem to pass through it. A sudden wave of panic washes over you. You try")
    print("\tcalling for help, but your voice barely makes a sound. Your thoughts begin to scatter, and memories that once seemed so important")
    print("\tbecome increasingly difficult to recall.")
    print()
    print("\tThe passengers. The conversations. The strange things you've witnessed aboard this train. You remember all of it, but somehow,")
    print("\tit no longer feels like it belongs to you. You look towards the other seats, hoping someone will notice, but there's nobody around.")
    print()
    print("\tYour body grows lighter as the darkness begins to creep into the edges of your vision. You try to hold on to something, anything,")
    print("\tbut even your own name starts to feel unfamiliar.")
    print()
    print("\tFor a brief moment, you wonder whether anyone will remember you.")
    print()
    print("\tThen, everything goes quiet.")
    print()
    print("\t[italic]Another passenger has disappeared.[italic]")
    print()
    print(Align.center("[bold magenta]----- BAD ENDING -----[/bold magenta]"))
    print(Align.center("[bold magenta]----- END OF DEMO -----[/bold magenta]"))

# Prints narration for good ending
def goodEnding():
    print()
    print(Align.center("[bold magenta]----- DAY THREE -----[/bold magenta]"))
    print()
    print("\tThe gentle rocking of the train gradually wakes you from your sleep. You slowly open your eyes, adjusting to the pale light above you. For a moment,")
    print("\tyou lie still, recalling the events of yesterday. Walter's frightened expression and his desperate warnings about the train come to mind.")
    print()
    print("\tYou sit up and look around the wagon. Everything seems relatively normal. The familiar seats, the flickering lights, the endless snowfall outside.")
    print("\tYour eyes wander towards Walter's usual seat, and to your relief, he's still there. He notices you looking and gives you a small, somewhat tired smile.")
    print()
    print("\tIt's a strange feeling, knowing that something you did might have made a difference. For once, nobody seems to have disappeared overnight. Still,")
    print("\tplenty of questions remain unanswered. The train continues along its endless journey, and you have no idea how much longer you'll be aboard.")
    print("\tPerhaps today you'll finally find another clue about where this train is taking you.")
    print()
    print(Align.center("[bold magenta]----- GOOD ENDING -----[/bold magenta]"))
    print(Align.center("[bold magenta]----- END OF DEMO -----[/bold magenta]"))

# Prints narration for neutral ending
def neutralEnding():
    print()
    print(Align.center("[bold magenta]----- DAY THREE -----[/bold magenta]"))
    print()
    print("\tThe familiar rumbling of the train slowly brings you out of your sleep. You open your eyes and take a moment to gather your thoughts,")
    print("\tstill feeling somewhat tired from the previous day. The pale lights above you flicker softly as you sit up and look around the wagon.")
    print()
    print("\tEverything seems just as you left it, but something catches your attention. Walter's usual seat is empty. You glance around, expecting")
    print("\tto find him somewhere nearby, but there's no sign of him. His belongings are still in place, and the smell of death lingers in the air.")
    print()
    print("\tA strange uneasiness settles over you as yesterday's conversation comes rushing back. You remember how frightened he seemed, how convinced")
    print("\the was that something terrible was going to happen. You can't help but wonder whether his fears were justified after all.")
    print()
    print("\tYou look towards the other passengers, but nobody seems particularly surprised by his absence. The train continues moving as though")
    print("\tnothing has happened. Another passenger is gone, and you find yourself wondering how many more will disappear before this journey ends.")
    print()
    print(Align.center("[bold magenta]----- NEUTRAL ENDING -----[/bold magenta]"))
    print(Align.center("[bold magenta]----- END OF DEMO -----[/bold magenta]"))

# Checks conditions and triggers an ending
def triggerEnding():
    if player["morbidity"] > 1: # Made too many negative choices
        badEnding()

    elif passenger1["saved"]: # Saved Walter
        goodEnding()

    else:
        neutralEnding() # Default

# Main
def main():
    global dayDone
    global day

    startDayOne()
    actionsDayOne(ap = 6)
    dayDone = False # Resets the day
    day += 1 # Next day
    startDayTwo()
    actionsDayTwo(ap = 6)
    triggerEnding()

if __name__ == "__main__":
    main()