# Welcome to Codemon, a game inspired by Pokemon and made solely for Python practice.
# Author: ns1017
# Version: 1.1
# Start Date: 07/22/2025
# Todo: add ascii art, expand attack capabilities, editable save.

import random
import pickle
import os
import time

# Codemon data
codemon_list = ["Codeachu", "Codemander", "Codeasaur", "Codelypuff", "Codetle", "Codegon", "Codequatic", "Codesteel", "Codeowl", "Codrill", "Codice", "Codflare"]
codemon_type = ["Electric", "Fire", "Grass", "Fairy", "Bug", "Dragon", "Water", "Steel", "Flying", "Ground", "Ice", "Fire"]
codemon_base_hp = [33, 35, 40, 38, 32, 60, 36, 42, 34, 39, 37, 38]
codemon_atk = [10, 12, 8, 7, 9, 20, 9, 11, 8, 10, 9, 12]
heavy_attacks = {
    "Electric": "Thunderbolt",
    "Water": "Hydro Pump",
    "Steel": "Iron Slam",
    "Flying": "Air Slash",
    "Ground": "Earth Quake",
    "Ice": "Frost Beam",
    "Fire": "Fire Spin",
    "Fire": "Flamethrower",
    "Grass": "Razor Leaf",
    "Fairy": "Moonblast",
    "Bug": "Bug Buzz",
    "Dragon": "Dragon Pulse"
}

# ASCII art for Codemon
codemon_ascii = {
    "Codeachu": """
     ⚡
    (o o)
   z(")(")
    """,
    "Codemander": """
     🔥
    (o o)
    > ^ <
    """,
    "Codeasaur": """
     🌱
    (o o)
    > - <
    """,
    "Codelypuff": """
     ✨
    (o o)
    > v <
    """,
    "Codetle": """
     🐞
    (o o)
    > ^ <
    """,
        "Codequatic": """
     💧
    (o o)
    ~~~~ 
    """,
    "Codesteel": """
     ⚙️
    (o o)
   [||||]
    """,
    "Codeowl": """
     🦉
    (o o)
    /)  )
    """,
    "Codrill": """
     ⛏️
    (o o)
   /====\
    """,
    "Codice": """
     ❄️
    (o o)
   (~~~)
    """,
    "Codflare": """
     🔥
    (o o)
    \ ^ /
    """,
    "Codegon": """
     🐉
    (o o)
   ==^==
    """
}

# ASCII animations for Heavy Attacks
heavy_attack_animations = {
    "Hydro Pump": ["⋅⋅⋅⋅⋅", "🌊🌊", "🌊🌊🌊", "🌊"],
    "Iron Slam": ["<--> ", "⚙️ ", "⚙️⚙️", "💥 "],
    "Air Slash": ["~~ ", "~~🪽 ", "~🪽~~🪽 ", "~~~🪽~~~~~🪽~🪽 "],
    "Earth Quake": ["!!", "▒▒▒", "▒▒▒▒", "▒▒💥▒▒▒💥▒"],
    "Frost Beam": ["❄️", "❄️❄️-->", "❄️❄️❄️❄️"],
    "Fire Spin": ["🔥🔥", "🔥>>=>🔥","🔥>=>🔥🔥"],
    "Thunderbolt": ["~~~ ", "~~~>⚡️ ", "~⚡️⚡️⚡️⚡️"],
    "Flamethrower": ["*** ", "***> 🔥 ", "🔥🔥🔥🔥🔥"],
    "Razor Leaf": ["~~~ ", "-🍃-🍃", "-🍃🍃"],
    "Moonblast": ["🌑 ", "🌑++", "🌑💥💥💥", ],
    "Bug Buzz": ["~~~ ", "~~zzz~~", "~~zzz~~zzz", "~~~zzz~~~t"],
    "Dragon Pulse": ["=== ", "<<==>>====", "====>>===", "====>>====>"]
}

# Type effectiveness
type_effectiveness = {
    "Water": "Fire",
    "Steel": "Fairy",
    "Flying": "Bug",
    "Ground": "Electric",
    "Ice": "Grass",
    "Electric": "Bug",
    "Fire": "Grass",
    "Grass": "Bug",
    "Fairy": "Dragon",
    "Bug": "Grass",
    "Dragon": "Dragon"
}

# NPC trainers
npc_list = ["Smith", "Showers", "Reeve", "Trich"]

# Save file
save_file = "codemon_save.pkl"

# Load or initialize game
if os.path.exists(save_file):
    with open(save_file, "rb") as f:
        data = pickle.load(f)
        captured_codemon = data["captured_codemon"]
else:
    print("No save file found. Let's choose your starter Codemon!")
    print("Choose your starting Codemon:")
    for i in range(len(codemon_list) - 1):  # Exclude Codegon
        print(f"{i + 1}. {codemon_list[i]} ({codemon_type[i]} Type, HP: {codemon_base_hp[i]}, ATK: {codemon_atk[i]})")
    choice = int(input("Enter the number of your starter: ")) - 1
    if choice < 0 or choice >= len(codemon_list) - 1:
        print("Invalid choice, defaulting to Codeachu.")
        choice = 0
    starter_name = codemon_list[choice]
    starter_base_hp = codemon_base_hp[choice]
    captured_codemon = [{"name": starter_name, "level": 1, "current_hp": starter_base_hp}]
    print(f"You chose {starter_name}! Let's start your adventure!")

# Main game loop
while True:
    print("\nWhat would you like to do?")
    print("1. Battle with a Codemon")
    print("2. Hunt for a new Codemon")
    print("3. Heal all Codemon")
    print("4. Exit")
    choice = input("Choose an option (1/2/3/4): ")

    if choice == "1":
        # Battle
        if all(codemon["current_hp"] <= 0 for codemon in captured_codemon):
            print("All your Codemon are fainted! Please heal them first.")
            continue

        print("\nChoose a Codemon to battle with:")
        available_codemon = [c for c in captured_codemon if c["current_hp"] > 0]
        for i, codemon in enumerate(available_codemon):
            name = codemon["name"]
            level = codemon["level"]
            base_hp = codemon_base_hp[codemon_list.index(name)]
            max_hp = base_hp + (level - 1) * 5
            print(f"{i + 1}. {name} (Lv {level}, HP {codemon['current_hp']}/{max_hp})")
        selection = int(input("Enter the number of the Codemon: ")) - 1
        if selection < 0 or selection >= len(available_codemon):
            print("Invalid choice, defaulting to first available Codemon.")
            selection = 0
        selected_codemon = available_codemon[selection]

        # Get player Codemon stats
        name = selected_codemon["name"]
        level = selected_codemon["level"]
        current_hp = selected_codemon["current_hp"]
        base_hp = codemon_base_hp[codemon_list.index(name)]
        max_hp = base_hp + (level - 1) * 5
        attack = codemon_atk[codemon_list.index(name)] + (level - 1) * 2
        player_type = codemon_type[codemon_list.index(name)]
        print(f"\nYou selected {name} (Lv {level}) - {player_type} Type")
        print(codemon_ascii[name])
        print(f"HP: {current_hp}/{max_hp}, Attack: {attack}")

        # NPC setup
        npc_index = random.randint(0, len(codemon_list) - 1)
        npc_name = codemon_list[npc_index]
        npc_type = codemon_type[npc_index]
        npc_level = level
        npc_base_hp = codemon_base_hp[npc_index]
        npc_max_hp = npc_base_hp + (npc_level - 1) * 5
        npc_current_hp = npc_max_hp
        npc_attack = codemon_atk[npc_index] + (npc_level - 1) * 2
        trainer_name = random.choice(npc_list)
        print(f"\nTrainer {trainer_name} challenges you with {npc_name} (Lv {npc_level}, {npc_type} Type, HP {npc_current_hp})")
        print(codemon_ascii[npc_name])

        # Battle loop
        while current_hp > 0 and npc_current_hp > 0:
            print(f"\n{name} (HP: {current_hp}) vs {npc_name} (HP: {npc_current_hp})")
            print("1. Attack")
            print("2. Do nothing")
            print("3. Flee")
            action = input("Choose an action (1/2/3): ")

            if action == "1":
                print("\nChoose an attack:")
                print("1. Tackle")
                print(f"2. {heavy_attacks[player_type]}")
                attack_choice = input("Choose an attack (1/2): ")
                
                if attack_choice == "1":
                    damage = attack + random.randint(-5, 5)
                    if type_effectiveness[player_type] == npc_type:
                        damage *= 2
                        print(f"{name} used Tackle! It's super effective! Deals {damage} damage!")
                    else:
                        print(f"{name} used Tackle! Deals {damage} damage!")
                    npc_current_hp -= damage
                elif attack_choice == "2":
                    if random.randint(1, 100) <= 70:
                        damage = int(attack * 1.5) + random.randint(-5, 5)
                        if type_effectiveness[player_type] == npc_type:
                            damage *= 2
                            print(f"{name} used {heavy_attacks[player_type]}! It's super effective!")
                        else:
                            print(f"{name} used {heavy_attacks[player_type]}!")
                        for frame in heavy_attack_animations[heavy_attacks[player_type]]:
                            os.system("cls" if os.name == "nt" else "clear")
                            print(codemon_ascii[name])
                            print(frame)
                            print(codemon_ascii[npc_name])
                            time.sleep(0.5)
                        print(f"Deals {damage} damage!")
                        npc_current_hp -= damage
                    else:
                        print(f"{name} used {heavy_attacks[player_type]}! It missed!")
                        for frame in heavy_attack_animations[heavy_attacks[player_type]]:
                            os.system("cls" if os.name == "nt" else "clear")
                            print(codemon_ascii[name])
                            print(frame)
                            print(codemon_ascii[npc_name])
                            time.sleep(0.5)
                        print("No damage dealt!")
                else:
                    print("Invalid attack choice. Try again.")
                    continue
            elif action == "2":
                print("You do nothing...")
            elif action == "3":
                print("You fled the battle!")
                break
            else:
                print("Invalid input. Try again.")
                continue

            # NPC attack
            if npc_current_hp <= 0:
                print(f"\nYou defeated {npc_name}!")
                print("🎉 Your Codemon leveled up!")
                selected_codemon["level"] += 1
                new_max_hp = base_hp + (selected_codemon["level"] - 1) * 5
                selected_codemon["current_hp"] = new_max_hp
                print(f"{name} is now Level {selected_codemon['level']}! HP restored to {new_max_hp}.")
                break

            npc_damage = npc_attack + random.randint(-5, 5)
            current_hp -= npc_damage
            selected_codemon["current_hp"] = current_hp
            print(f"{npc_name} attacks and deals {npc_damage} damage!")

            if current_hp <= 0:
                print(f"\nYour {name} fainted... You lose!")
                selected_codemon["current_hp"] = 0
                break

    elif choice == "2":
        # Hunt
        current_hour = time.localtime().tm_hour
        if 6 <= current_hour <= 11:
            time_slot = "morning"
            available_codemon = ["Codeachu", "Codetle", "Codequatic", "Codeowl", "Codflare"]
        elif 12 <= current_hour <= 17:
            time_slot = "afternoon"
            available_codemon = ["Codemander", "Codeasaur", "Codequatic", "Codrill", "Codflare"]
        elif 18 <= current_hour <= 23:
            time_slot = "evening"
            available_codemon = ["Codelypuff", "Codeasaur", "Codrill", "Codesteel"]
        else:
            time_slot = "night"
            available_codemon = ["Codelypuff", "Codetle", "Codeowl", "Codesteel", "Codice"]

        legendary_chance = random.randint(1, 100)
        if legendary_chance == 1:
            wild_codemon = "Codegon"
            wild_type = "Dragon"
            wild_base_hp = 60
            wild_atk = 20
            is_legendary = True
        else:
            wild_codemon = random.choice(available_codemon)
            wild_index = codemon_list.index(wild_codemon)
            wild_type = codemon_type[wild_index]
            wild_base_hp = codemon_base_hp[wild_index]
            wild_atk = codemon_atk[wild_index]
            is_legendary = False

        print(f"\n🌄 It's currently {time_slot.upper()} (hour {current_hour}).")
        print(f"A wild {wild_codemon} appears! ({wild_type} Type, HP {wild_base_hp}, ATK {wild_atk})")
        print(codemon_ascii[wild_codemon])
        try_catch = input("Try to catch it? (yes/no): ").lower()

        if try_catch == "yes":
            max_level = max([c["level"] for c in captured_codemon]) if captured_codemon else 1
            if is_legendary:
                catch_chance = min(100, 50 + max_level * 2)
            else:
                catch_chance = min(100, 75 + max_level * 5)
            catch_roll = random.randint(1, 100)
            if catch_roll <= catch_chance:
                print(f"🎉 You caught {wild_codemon}!")
                captured_codemon.append({"name": wild_codemon, "level": 1, "current_hp": wild_base_hp})
            else:
                print(f"{wild_codemon} escaped!")
        else:
            print("You let it go.")

    elif choice == "3":
        # Heal all Codemon
        for codemon in captured_codemon:
            name = codemon["name"]
            level = codemon["level"]
            base_hp = codemon_base_hp[codemon_list.index(name)]
            max_hp = base_hp + (level - 1) * 5
            codemon["current_hp"] = max_hp
        print("All your Codemon have been healed!")

    elif choice == "4":
        # Exit and save
        with open(save_file, "wb") as f:
            pickle.dump({"captured_codemon": captured_codemon}, f)
        print("🔒 Progress saved. Thanks for playing Codemon!")
        break

    else:
        print("Invalid choice. Please try again.")