# Author: ns1017 on Github, Data Analyst GPT (for help with comments and structure) 
# Date: 2025-09-16
# Codemon v4 (technically will be v2 on github) - A text-based monster capturing and battling game
import random
import pickle
import os
import time
from copy import deepcopy

SAVE_FILE = "codemon_save_v4.pkl"

# ----------------- Utilities -----------------
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def delay(game_data, sec):
    """Respect battle speed toggle: 'normal' waits, 'fast' skips small waits."""
    if game_data.get("battle_speed","normal") == "normal":
        time.sleep(sec)

# ----------------- ASCII art & animations  -----------------
codemon_ascii = {
    "Codeachu": """
     ⚡
    (o o)
   z(")(")
    """,
    "Codetron": """
     ⚡⚡
    (o o)/
    /(  )\\
    """,
    "Codebolt": """
     ⚡⚡⚡
    (o_o)⚡
   <(   )>
    """,
    "Codemander": """
     🔥
    (o o)
    > ^ <
    """,
    "Codezard": """
     🔥🔥
    (O O)
   <  ^  >
    """,
    "Codelord": """
     🔥👑
    (O_O)
   /  ^  \\
    """,
    "Codeasaur": """
     🌱
    (o o)
    > - <
    """,
    "Codebloom": """
     🌸
    (o o)/
   /(   )\\
    """,
    "Codetree": """
     🌳
   /(o o)\\
   /(   )\\
    """,
    "Codelypuff": """
     ✨
    (o o)
    > v <
    """,
    "Codeballad": """
     🎵✨
    (o o)
   /( v )\\
    """,
    "Codiva": """
     🎤
    (O o)
   <( v )>
    """,
    "Codetle": """
     🐞
    (o o)
    > ^ <
    """,
    "Codecrawler": """
     🪲
   /(o o)\\
   <  ^  >
    """,
    "Codecoloss": """
     🐛🛡️
   (O O)
  /  ||  \\
    """,
    "Codequatic": """
     💧
    (o o)
    ~~~~ 
    """,
    "Codewave": """
     🌊
    (o o)/
    ~~~~~~
    """,
    "Codesea": """
     🌊🌊
    (O O)
   <~~~~~>
    """,
    "Codesteel": """
     ⚙️
    (o o)
   [||||]
    """,
    "Coderon": """
     🛠️
    (O O)
   /||||\\
    """,
    "Codetitan": """
     🏗️
    (O O)
  /|||||||\\
    """,
    "Codeowl": """
     🦉
    (o o)
    /)  )
    """,
    "Coderoost": """
     🪶
    (o o)/
   /( )\\
    """,
    "Codemperor": """
     👑🦉
    (O O)
   /(   )\\
    """,
    "Codrill": """
     ⛏️
    (o o)
   /====\\
    """,
    "Codeminer": """
     ⛏️⚒️
    (O o)
   <====>
    """,
    "Codequake": """
     🌍⚡
    (O O)
   /====\\
    """,
    "Codice": """
     ❄️
    (o o)
   (~~~)
    """,
    "Codefrost": """
     ❄️❄️
    (O o)
   ( ~~~ )
    """,
    "Codestorm": """
     ❄️🌪️
    (O O)
   ( ~~~~ )
    """,
    "Codflare": """
     🔥
    (o o)
    \\ ^ /
    """,
    "Codeinferno": """
     🔥🔥
    (O O)
    / ^ \\
    """,
    "Codemagma": """
     🌋🔥
    (O O)
   /  ^  \\
    """,
    "Codegon": """
     🐉
    (o o)
   ==^==
    """
}

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
    "Moonblast": ["🌑 ", "🌑++", "🌑💥💥💥"],
    "Bug Buzz": ["~~~ ", "~~zzz~~", "~~zzz~~zzz", "~~~zzz~~~t"],
    "Dragon Pulse": ["=== ", "<<==>>====", "====>>===", "====>>====>"]
}

light_attack_animations = {
    "Tackle": ["*", "-*-", "*"],
    "Quick Zap": [". . ⚡", ". ⚡ .", "⚡ . ."],
    "Ember": [".🔥", " .🔥", "  .🔥"],
    "Razor Leaf": [" ~🍃", "~🍃~", " ~🍃"],
    "Splash Taps": [".~.", ".~~.", "..~.."],
}

heavy_attacks = {
    "Electric": "Thunderbolt",
    "Water": "Hydro Pump",
    "Steel": "Iron Slam",
    "Flying": "Air Slash",
    "Ground": "Earth Quake",
    "Ice": "Frost Beam",
    "Fire": "Flamethrower",
    "Grass": "Razor Leaf",
    "Fairy": "Moonblast",
    "Bug": "Bug Buzz",
    "Dragon": "Dragon Pulse"
}

# ----------------- Species & Base stats -----------------
codemon_list = ["Codeachu", "Codemander", "Codeasaur", "Codelypuff",
                "Codetle", "Codegon", "Codequatic", "Codesteel",
                "Codeowl", "Codrill", "Codice", "Codflare"]
codemon_type = ["Electric", "Fire", "Grass", "Fairy", "Bug", "Dragon",
                "Water", "Steel", "Flying", "Ground", "Ice", "Fire"]
codemon_base_hp = [33, 35, 40, 38, 32, 60, 36, 42, 34, 39, 37, 38]
codemon_atk = [10, 12, 8, 7, 9, 20, 9, 11, 8, 10, 9, 12]
codemon_base_spd = [14, 12, 10, 11, 9, 13, 11, 8, 13, 9, 10, 12]

SPECIES = {}
for i, name in enumerate(codemon_list):
    SPECIES[name] = {
        "type": codemon_type[i],
        "base_hp": codemon_base_hp[i],
        "base_atk": codemon_atk[i],
        "base_spd": codemon_base_spd[i],
    }

# ----------------- Type chart -----------------
TYPE_CHART = {
    "Normal": {},
    "Fire":    {"Grass": 2.0, "Water": 0.5, "Fire": 0.5, "Ice": 2.0, "Steel": 0.5},
    "Water":   {"Fire": 2.0, "Grass": 0.5, "Ground": 2.0, "Water": 0.5, "Dragon": 0.5},
    "Electric":{"Water": 2.0, "Ground": 0.0, "Flying": 2.0, "Electric": 0.5},
    "Grass":   {"Water": 2.0, "Fire": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5},
    "Bug":     {"Grass": 2.0, "Fire": 0.5, "Flying": 0.5, "Steel": 0.5},
    "Dragon":  {"Dragon": 2.0},
    "Steel":   {"Fairy": 0.5, "Ice": 2.0},
    "Fairy":   {"Dragon": 2.0, "Steel": 0.5},
    "Ground":  {"Electric": 2.0, "Fire": 2.0, "Flying": 0.0},
    "Flying":  {"Bug": 2.0, "Grass": 2.0},
    "Ice":     {"Grass": 2.0, "Ground": 2.0, "Dragon": 0.5},
}

def type_multiplier(attacker_type, defender_type):
    return TYPE_CHART.get(attacker_type, {}).get(defender_type, 1.0)

# ----------------- Moves DB  -----------------
# Add a 'pp' and 'max_pp' value per move
MOVE_DB = {
    "Tackle": {"name":"Tackle","type":"Normal","power":5,"accuracy":100,"kind":"light","desc":"Simple hit.","pp":35},
    "Quick Zap": {"name":"Quick Zap","type":"Electric","power":6,"accuracy":100,"kind":"light","desc":"Fast electric jolt.","pp":30},
    "Thunderbolt": {"name":"Thunderbolt","type":"Electric","power":16,"accuracy":85,"kind":"heavy","desc":"Powerful bolt; may miss.","pp":15},
    "Charge Up": {"name":"Charge Up","type":"Electric","power":0,"accuracy":100,"kind":"utility","desc":"Raise own ATK by 1 stage.","pp":10},
    "Ember": {"name":"Ember","type":"Fire","power":6,"accuracy":100,"kind":"light","desc":"A small flame.","pp":30},
    "Flamethrower": {"name":"Flamethrower","type":"Fire","power":16,"accuracy":80,"kind":"heavy","desc":"Heavy fire attack.","pp":15},
    "Scorch": {"name":"Scorch","type":"Fire","power":0,"accuracy":100,"kind":"utility","desc":"Lower enemy ATK by 1 stage.","pp":10},
    "Razor Leaf": {"name":"Razor Leaf","type":"Grass","power":7,"accuracy":95,"kind":"light","desc":"Sharp leaves.","pp":25},
    "Leaf Blade": {"name":"Leaf Blade","type":"Grass","power":15,"accuracy":90,"kind":"heavy","desc":"Powerful grass blade.","pp":15},
    "Root Guard": {"name":"Root Guard","type":"Grass","power":0,"accuracy":100,"kind":"utility","desc":"Raise own DEF stage.","pp":10},
    "Splash Taps": {"name":"Splash Taps","type":"Water","power":6,"accuracy":100,"kind":"light","desc":"A watery tap.","pp":30},
    "Hydro Pump": {"name":"Hydro Pump","type":"Water","power":17,"accuracy":75,"kind":"heavy","desc":"Massive water burst.","pp":10},
    "Soak": {"name":"Soak","type":"Water","power":0,"accuracy":100,"kind":"utility","desc":"Lower enemy SPD by 1 stage.","pp":12},
    "Iron Slam": {"name":"Iron Slam","type":"Steel","power":16,"accuracy":85,"kind":"heavy","desc":"Heavy metallic strike.","pp":15},
    "Air Slash": {"name":"Air Slash","type":"Flying","power":14,"accuracy":90,"kind":"heavy","desc":"Slashing air.","pp":15},
    "Earth Quake": {"name":"Earth Quake","type":"Ground","power":18,"accuracy":80,"kind":"heavy","desc":"Massive ground attack.","pp":10},
    "Frost Beam": {"name":"Frost Beam","type":"Ice","power":14,"accuracy":85,"kind":"heavy","desc":"Icy beam.","pp":15},
    "Bug Buzz": {"name":"Bug Buzz","type":"Bug","power":13,"accuracy":90,"kind":"heavy","desc":"Loud, damaging buzz.","pp":15},
    "Dragon Pulse": {"name":"Dragon Pulse","type":"Dragon","power":18,"accuracy":80,"kind":"heavy","desc":"Dragon energy.","pp":10},
    "Moonblast": {"name":"Moonblast","type":"Fairy","power":16,"accuracy":85,"kind":"heavy","desc":"Fairy energy impact.","pp":10},
    "Intimidate": {"name":"Intimidate","type":"Normal","power":0,"accuracy":100,"kind":"utility","desc":"Lower enemy ATK by 1 stage.","pp":10},
    "Agility": {"name":"Agility","type":"Normal","power":0,"accuracy":100,"kind":"utility","desc":"Raise own SPD by 2 stages.","pp":10},
}

# ----------------- Move unlocks / evolutions (same structure as v3) -----------------
MOVE_UNLOCKS = {
    "Codeachu": {1:["Quick Zap","Tackle"], 5:["Thunderbolt"], 10:["Charge Up"]},
    "Codemander": {1:["Ember","Tackle"], 5:["Flamethrower"], 12:["Scorch"]},
    "Codeasaur": {1:["Razor Leaf","Tackle"], 6:["Leaf Blade"], 14:["Root Guard"]},
    "Codelypuff": {1:["Tackle"], 8:["Moonblast"], 16:["Agility"]},
    "Codetle": {1:["Tackle"], 4:["Bug Buzz"], 10:["Iron Slam"]},
    "Codegon": {1:["Dragon Pulse","Tackle"], 20:["Earth Quake"]},
    "Codequatic": {1:["Splash Taps"], 6:["Hydro Pump"], 14:["Soak"]},
    "Codesteel": {1:["Tackle"], 5:["Iron Slam"], 13:["Intimidate"]},
    "Codeowl": {1:["Tackle"], 7:["Air Slash"], 15:["Agility"]},
    "Codrill": {1:["Tackle"], 6:["Earth Quake"], 12:["Bug Buzz"]},
    "Codice": {1:["Tackle"], 5:["Frost Beam"], 11:["Root Guard"]},
    "Codflare": {1:["Ember","Tackle"], 7:["Flamethrower"], 14:["Scorch"]},
}

EVOLUTIONS = {
    "Codeachu": {"to":"Codetron", "level":10, "stat_changes":{"base_hp":+15,"base_atk":+6,"base_spd":+3}},
    "Codetron": {"to":"Codebolt", "level":20, "stat_changes":{"base_hp":+20,"base_atk":+8,"base_spd":+4}},
    "Codemander": {"to":"Codezard", "level":12, "stat_changes":{"base_hp":+10,"base_atk":+8}},
    "Codezard": {"to":"Codelord", "level":22, "stat_changes":{"base_hp":+15,"base_atk":+12}},
    "Codeasaur": {"to":"Codebloom", "level":14, "stat_changes":{"base_hp":+12,"base_atk":+4}},
    "Codebloom": {"to":"Codetree", "level":25, "stat_changes":{"base_hp":+25,"base_atk":+6}},
    "Codelypuff": {"to":"Codeballad", "level":15, "stat_changes":{"base_hp":+8,"base_spd":+3}},
    "Codeballad": {"to":"Codiva", "level":28, "stat_changes":{"base_hp":+12,"base_atk":+6}},
    "Codetle": {"to":"Codecrawler", "level":12, "stat_changes":{"base_hp":+10,"base_atk":+3}},
    "Codecrawler": {"to":"Codecoloss", "level":22, "stat_changes":{"base_hp":+20,"base_atk":+8}},
    "Codequatic": {"to":"Codewave", "level":14, "stat_changes":{"base_hp":+10,"base_atk":+5}},
    "Codewave": {"to":"Codesea", "level":25, "stat_changes":{"base_hp":+20,"base_atk":+8}},
    "Codesteel": {"to":"Coderon", "level":16, "stat_changes":{"base_hp":+15,"base_atk":+6}},
    "Coderon": {"to":"Codetitan", "level":30, "stat_changes":{"base_hp":+30,"base_atk":+10}},
    "Codeowl": {"to":"Coderoost", "level":15, "stat_changes":{"base_spd":+4,"base_atk":+3}},
    "Coderoost": {"to":"Codemperor", "level":27, "stat_changes":{"base_hp":+12,"base_atk":+8}},
    "Codrill": {"to":"Codeminer", "level":14, "stat_changes":{"base_hp":+10,"base_atk":+6}},
    "Codeminer": {"to":"Codequake", "level":26, "stat_changes":{"base_hp":+15,"base_atk":+9}},
    "Codice": {"to":"Codefrost", "level":12, "stat_changes":{"base_spd":+3,"base_atk":+3}},
    "Codefrost": {"to":"Codestorm", "level":24, "stat_changes":{"base_atk":+12,"base_spd":+4}},
    "Codflare": {"to":"Codeinferno", "level":16, "stat_changes":{"base_atk":+8,"base_hp":+10}},
    "Codeinferno": {"to":"Codemagma", "level":28, "stat_changes":{"base_atk":+12,"base_hp":+20}},
}

LOCATIONS = {
    "Forest":    {"locked_by_badge": None, "pool":["Codeachu","Codeasaur","Codetle","Codelypuff"]},
    "Cave":      {"locked_by_badge": None, "pool":["Codesteel","Codrill","Codice"]},
    "Lake":      {"locked_by_badge": "Tide Badge", "pool":["Codequatic","Codetle","Codeowl"]},
    "Mountain":  {"locked_by_badge": "Blaze Badge", "pool":["Codemander","Codflare","Codrill"]},
}

NPC_TRAINERS = ["Smith", "Showers", "Reeve", "Trich", "Avery", "Mira"]

GYMS = [
    {"name":"Flame Gym","leader":"Ignis","type":"Fire","badge":"Blaze Badge","locked":False},
    {"name":"Wave Gym","leader":"Marina","type":"Water","badge":"Tide Badge","locked":False},
]

# ----------------- World map (ASCII grid) -----------------
# Simple map: each char symbolizes location; P will indicate player
WORLD_MAP = [
    list("###########"),
    list("#S..F...M.#"),
    list("#...|..|..#"),
    list("#T-+-C-L..#"),
    list("#...|..|..#"),
    list("#...H...D.#"),
    list("###########"),
]
# Legend:
# S = Start, T = Town, F = Forest, C = Cave, L = Lake, M = Mountain, H = House/Heal, D = League

MAP_LEGEND = {
    "S":"Start", "T":"Town", "F":"Forest", "C":"Cave", "L":"Lake", "M":"Mountain", "H":"House", "D":"League", ".":"Path", "-":"+"
}

# Walkable tiles
WALKABLE = set(".S T F C L M H D - +".split())

# ----------------- Helpers for stats, moves, etc. -----------------
def get_species_stats(species_name):
    if species_name in SPECIES:
        return deepcopy(SPECIES[species_name])
    else:
        return {"type":"Normal","base_hp":30,"base_atk":8,"base_spd":8}

def calc_max_hp(base_hp, level):
    return base_hp + (level - 1) * 5

def calc_attack(base_atk, level, atk_stage=0):
    base = base_atk + (level - 1) * 2
    multiplier = 1.0 + 0.20 * atk_stage
    return int(base * multiplier)

def calc_spd(base_spd, level, spd_stage=0):
    base = base_spd + (level - 1) * 1
    multiplier = 1.0 + 0.20 * spd_stage
    return int(base * multiplier)


def display_name(mon):
    """Return a human-friendly display name including Rare prefix and nickname."""
    if not mon:
        return ""
    prefix = "Rare " if mon.get("rare") else ""
    return prefix + (mon.get('nickname') or mon.get('name') or "Unknown")

def assign_moves_for_species_with_pp(species_name, level):
    """Return list of move dicts with current pp and max_pp."""
    names = []
    unlock_map = MOVE_UNLOCKS.get(species_name, {})
    for lvl in sorted(unlock_map.keys()):
        if level >= lvl:
            names.extend(unlock_map[lvl])
    # ensure Tackle present
    if "Tackle" not in names:
        names.insert(0,"Tackle")
    # dedupe while preserving order
    seen = set(); result=[]
    for n in names:
        if n not in seen and n in MOVE_DB:
            seen.add(n)
            mv = deepcopy(MOVE_DB[n])
            mv["max_pp"] = mv.get("pp", 10)
            mv["pp_current"] = mv["pp"]
            result.append(mv)
    # if still <2 moves, add a same-type move
    if len(result) < 2:
        species_type = SPECIES.get(species_name, {}).get("type","Normal")
        for mvn, mv in MOVE_DB.items():
            if mv["type"] == species_type and mvn not in seen:
                nmv = deepcopy(mv)
                nmv["max_pp"] = nmv.get("pp",10)
                nmv["pp_current"] = nmv["pp"]
                result.append(nmv)
                break
    return result[:4]

def ensure_move_pp_struct(captured_mon):
    """Make sure captured codemon have 'moves' as list of dicts with pp_current."""
    if not captured_mon.get("moves"):
        captured_mon["moves"] = assign_moves_for_species_with_pp(captured_mon["name"], captured_mon["level"])
        return
    # If moves are stored as names, convert
    if isinstance(captured_mon["moves"][0], str):
        new_moves = []
        for nm in captured_mon["moves"]:
            if nm in MOVE_DB:
                mv = deepcopy(MOVE_DB[nm])
                mv["max_pp"] = mv.get("pp",10)
                mv["pp_current"] = mv.get("pp",10)
                new_moves.append(mv)
        captured_mon["moves"] = new_moves

# ----------------- Default game state -----------------
DEFAULT_GAME = {
    "captured": [],
    "codedex": {name:{"seen":False,"caught":False} for name in codemon_list},
    "badges": [],
    "story_stage": 0,
    "rival_team": [],
    "storage": [],  # box storage
    "battle_speed": "normal",  # "normal" or "fast"
    # persist player map position as (row,col)
    "player_pos": (1,1),
}

def load_game():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            data = pickle.load(f)
            #migrate or ensure keys
            data.setdefault("storage", [])
            data.setdefault("battle_speed", "normal")
            data.setdefault("rival_team", [])
            data.setdefault("story_stage", 0)
            data.setdefault("player_pos", (1,1))
            #codedex includes all species
            for s in codemon_list:
                data.setdefault("codedex", {}).setdefault(s, {"seen":False,"caught":False})
            #move structures
            for c in data.get("captured", []):
                ensure_move_pp_struct(c)
            return data
    return deepcopy(DEFAULT_GAME)

def save_game(data):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(data, f)

# ----------------- Starter selection -----------------
def choose_starter(game_data):
    clear_screen()
    print("Choose your starting Codemon:")
    starters = [s for s in codemon_list if s != "Codegon"]
    for i, s in enumerate(starters):
        sp = get_species_stats(s)
        print(f"{i+1}. {s} ({sp['type']} Type, HP: {sp['base_hp']}, ATK: {sp['base_atk']})")
    try:
        choice = int(input("Enter the number of your starter: ")) - 1
    except:
        choice = 0
    if choice < 0 or choice >= len(starters):
        starter = "Codeachu"
    else:
        starter = starters[choice]
    starter_level = 1
    sp = get_species_stats(starter)
    starter_hp = calc_max_hp(sp["base_hp"], starter_level)
    starter_moves = assign_moves_for_species_with_pp(starter, starter_level)
    new = {"name": starter, "base_species": starter, "level": starter_level, "current_hp": starter_hp, "moves": starter_moves,
        "atk_stage": 0, "spd_stage": 0, "status": None, "status_counter": 0, "nickname": None, "rare": False}
    game_data["captured"].append(new)
    game_data["codedex"].setdefault(starter, {"seen":False,"caught":False})["seen"] = True
    game_data["codedex"][starter]["caught"] = True
    # rival starter
    rivals = [s for s in codemon_list if s != starter and s != "Codegon"]
    rival_choice = random.choice(rivals)
    game_data["rival_team"] = [{"name":rival_choice, "level":1}]
    print(f"You chose {starter}! Rival picked {rival_choice}!")

# ----------------- Status effects -----------------
def apply_status_start_of_turn(mon, game_data):
    """
    Apply passive status effects at the start of mon's turn.
    Returns True if mon can act this turn, False if it is incapacitated.
    """
    status = mon.get("status")
    if not status:
        return True
    name = mon.get("nickname") or mon["name"]
    if status == "Burn":
        dmg = max(1, mon["level"])
        mon["current_hp"] -= dmg
        print(f"{name} is hurt by burn for {dmg} HP!")
    elif status == "Poison":
        dmg = max(1, mon["level"] // 2)
        mon["current_hp"] -= dmg
        print(f"{name} is hurt by poison for {dmg} HP!")
    elif status == "Paralyze":
        # 25% chance to be fully paralyzed and skip turn
        if random.random() < 0.25:
            print(f"{name} is paralyzed and can't move!")
            return False
    elif status == "Freeze":
        # small chance to thaw each turn
        if random.random() < 0.2:
            mon["status"] = None
            print(f"{name} thawed out!")
            return True
        else:
            print(f"{name} is frozen solid!")
            return False
    # decrement status_counter if present and clear when 0
    if mon.get("status_counter", 0) > 0:
        mon["status_counter"] -= 1
        if mon["status_counter"] <= 0:
            mon["status"] = None
    return True

def inflict_status(target, status_name, duration=5):
    """Inflict a status if target has none; returns success flag."""
    if not target.get("status"):
        target["status"] = status_name
        target["status_counter"] = duration
        return True
    return False

# ----------------- Damage and moves -----------------
def calc_damage(attacker, defender, move):
    """
    returns (damage, multiplier, critical_flag)
    move is a move dict (with 'power', 'type', 'pp_current', etc.)
    """
    if move["kind"] == "utility":
        return 0, 1.0, False
    # attacker base stats
    sp_att = get_species_stats(attacker.get("base_species", attacker["name"]))
    sp_def = get_species_stats(defender.get("base_species", defender["name"]))
    atk = calc_attack(sp_att["base_atk"], attacker["level"], attacker.get("atk_stage",0))
    base = atk + move["power"]
    variance = random.uniform(0.85, 1.0)
    mult = type_multiplier(move["type"], sp_def["type"])
    dmg = int(base * variance * mult)
    # critical hit chance (10% default)
    crit = False
    if random.random() < 0.10:
        crit = True
        dmg = int(dmg * 2)
    if dmg < 1: dmg = 1
    return dmg, mult, crit

# ----------------- Move usage helper -----------------
def use_move_on(attacker, defender, move, game_data):
    """Consumes PP, applies damage or utility. Returns (action_result_str, did_defeat)"""
    # check PP
    if move.get("pp_current",0) <= 0:
        return f"{move['name']} has no PP left!", False
    move["pp_current"] -= 1
    # Display heavy or light attack ASCII/animation frames when available
    if move.get("kind") == "heavy":
        frames = heavy_attack_animations.get(move.get("name"))
        if frames:
            for frame in frames:
                print(frame)
                delay(game_data, 0.18)
    elif move.get("kind") == "light":
        frames = light_attack_animations.get(move.get("name"))
        if frames:
            for frame in frames:
                print(frame)
                delay(game_data, 0.10)
    if move["kind"] == "utility":
        # simple utilities implemented
        if move["name"] == "Charge Up":
            attacker["atk_stage"] = attacker.get("atk_stage",0) + 1
            return f"{attacker.get('nickname') or attacker['name']} used {move['name']} and raised its ATK!", False
        elif move["name"] == "Scorch":
            defender["atk_stage"] = defender.get("atk_stage",0) - 1
            return f"{attacker.get('nickname') or attacker['name']} used {move['name']}! Enemy ATK fell!", False
        elif move["name"] == "Soak":
            defender["spd_stage"] = defender.get("spd_stage",0) - 1
            return f"{attacker.get('nickname') or attacker['name']} used {move['name']}! Enemy SPD fell!", False
        elif move["name"] == "Intimidate":
            defender["atk_stage"] = defender.get("atk_stage",0) - 1
            return f"{attacker.get('nickname') or attacker['name']} used Intimidate! Enemy ATK fell!", False
        elif move["name"] == "Agility":
            attacker["spd_stage"] = attacker.get("spd_stage",0) + 2
            return f"{attacker.get('nickname') or attacker['name']} used Agility! SPD rose sharply!", False
        else:
            return f"{attacker.get('nickname') or attacker['name']} used {move['name']}!", False
    else:
        dmg, mult, crit = calc_damage(attacker, defender, move)
        defender["current_hp"] -= dmg
        s = f"{attacker.get('nickname') or attacker['name']} used {move['name']}! (x{mult:.1f})"
        if crit:
            s += " CRITICAL HIT!"
        s += f" It dealt {dmg} damage."
        # bonus: inflict status by certain moves
        if move["name"] == "Frost Beam" and random.random() < 0.15:
            if inflict_status(defender, "Freeze", duration=3):
                s += f" {defender.get('nickname') or defender['name']} was frozen!"
        if move["name"] == "Flamethrower" and random.random() < 0.10:
            if inflict_status(defender, "Burn", duration=4):
                s += f" {defender.get('nickname') or defender['name']} was burned!"
        if move["name"] == "Thunderbolt" and random.random() < 0.10:
            if inflict_status(defender, "Paralyze", duration=5):
                s += f" {defender.get('nickname') or defender['name']} was paralyzed!"
        return s, defender["current_hp"] <= 0

# ----------------- NPC move choices (use PP-aware moves) -----------------
def npc_move_choices(npc):
    ensure_move_pp_struct(npc)
    # prefer damaging moves with PP left
    moves_with_pp = [m for m in npc["moves"] if m.get("pp_current",0) > 0]
    if not moves_with_pp:
        return [ {"name":"Tackle","power":5,"type":"Normal","accuracy":100,"kind":"light","pp_current":0} ]
    # weight heavies slightly higher
    weights = []
    for m in moves_with_pp:
        w = 2 if m["kind"] == "heavy" else 1
        weights.append(w)
    return [random.choices(moves_with_pp, weights=weights, k=1)[0]]

# ----------------- Battle function (with switch & statuses) -----------------
def do_battle(game_data, is_gym=False, gym=None, npc_override=None, trainer_name=None):
    clear_screen()
    party = [c for c in game_data["captured"] if c["current_hp"] > 0]
    if not party:
        print("All your Codemon have fainted. Heal before battling.")
        return False

    # choose active
    print("Choose a Codemon to send out:")
    for i, c in enumerate(game_data["captured"]):
        base = c.get("base_species", c["name"])
        sp = get_species_stats(base)
        max_hp = calc_max_hp(sp["base_hp"], c["level"])
        print(f"{i+1}. {display_name(c)} (Lv {c['level']}) HP {c['current_hp']}/{max_hp}")
    try:
        sel = int(input("Enter number: ")) - 1
    except:
        sel = 0
    if sel < 0 or sel >= len(game_data["captured"]):
        sel = 0
    player = game_data["captured"][sel]
    ensure_move_pp_struct(player)

    # Setup NPC
    avg_level = max(1, sum(c["level"] for c in game_data["captured"]) // max(1, len(game_data["captured"])))
    if npc_override:
        npc = deepcopy(npc_override)
    else:
        if is_gym and gym:
            npc_level = avg_level + 2 + len(game_data["badges"])
        else:
            npc_level = random.randint(max(1, avg_level-1), avg_level+1)
        species = random.choice(codemon_list)
        npc = {"name":species, "level":npc_level, "current_hp":calc_max_hp(get_species_stats(species)["base_hp"], npc_level), "atk_stage":0, "spd_stage":0, "moves": assign_moves_for_species_with_pp(species, npc_level), "status":None, "status_counter":0}
    trainer_name = trainer_name or (gym["leader"] if gym else random.choice(NPC_TRAINERS))
    print(f"{trainer_name} sends out {npc['name']} (Lv {npc['level']})!")
    # codedex seen
    game_data["codedex"].setdefault(npc["name"], {"seen":False,"caught":False})["seen"] = True

    # battle loop
    while player["current_hp"] > 0 and npc["current_hp"] > 0:
        clear_screen()
        # display art
        print(f"{display_name(player)} (Lv {player['level']})  HP {player['current_hp']}/{calc_max_hp(get_species_stats(player.get('base_species',player['name']))['base_hp'], player['level'])}")
        if player["name"] in codemon_ascii:
            print(codemon_ascii.get(player["name"]))
        print("VS")
        print(f"{display_name(npc)} (Lv {npc['level']})  HP {npc['current_hp']}/{calc_max_hp(get_species_stats(npc['name'])['base_hp'], npc['level'])}")
        if npc["name"] in codemon_ascii:
            print(codemon_ascii.get(npc["name"]))
        print("\n-- Battle Menu --")
        print("1. Attack")
        print("2. Switch")
        print("3. Do Nothing")
        print("4. Flee")
        action = input("Choose: ").strip()

        # Determine speed order each round (including SPD stages)
        p_spd = calc_spd(get_species_stats(player.get("base_species",player["name"]))["base_spd"], player["level"], player.get("spd_stage",0))
        n_spd = calc_spd(get_species_stats(npc["name"])["base_spd"], npc["level"], npc.get("spd_stage",0))
        order = ["player","npc"] if p_spd > n_spd else (["npc","player"] if n_spd > p_spd else random.choice([["player","npc"],["npc","player"]]))

        # Player action resolution happens first if chosen and player is first in order
        for actor in order:
            if player["current_hp"] <= 0 or npc["current_hp"] <= 0:
                break
            if actor == "player":
                # Re-evaluate action if player chose switch earlier
                if action == "1":
                    # Attack flow
                    can_act = apply_status_start_of_turn(player, game_data) # Apply status start-of-turn effects
                    if not can_act:
                        delay(game_data, 0.5); continue
                    # list moves with PP
                    print("\nChoose a move:")
                    for idx,mv in enumerate(player["moves"]):
                        print(f"{idx+1}. {mv['name']} (PP {mv.get('pp_current',0)}/{mv.get('max_pp',mv.get('pp',0))})")
                    try:
                        mchoice = int(input("Move #: ")) - 1
                    except:
                        mchoice = 0
                    if mchoice < 0 or mchoice >= len(player["moves"]):
                        mchoice = 0
                    move = player["moves"][mchoice]
                    # Accuracy check
                    if random.randint(1,100) > move.get("accuracy",100):
                        print(f"{player.get('nickname') or player['name']}'s {move['name']} missed!")
                        delay(game_data, 0.8)
                    else:
                        out, defeated = use_move_on(player, npc, move, game_data)
                        print(out)
                        delay(game_data, 0.8)
                        if defeated:
                            print(f"{npc['name']} fainted!")
                            # award level up
                            player["level"] += 1
                            # learn moves and possibly evolve
                            new_moves = [m["name"] for m in assign_moves_for_species_with_pp(player.get("base_species",player["name"]), player["level"])]
                            for nm in new_moves:
                                if nm not in [m["name"] for m in player["moves"]]:
                                    # add new move from MOVE_DB with PP
                                    mv = deepcopy(MOVE_DB[nm])
                                    mv["max_pp"] = mv.get("pp",10)
                                    mv["pp_current"] = mv.get("pp",10)
                                    player["moves"].append(mv)
                                    print(f"{player.get('nickname') or player['name']} learned {nm}!")
                            # evo check
                            if player["name"] in EVOLUTIONS:
                                evo = EVOLUTIONS[player["name"]]
                                if player["level"] >= evo["level"]:
                                    new_name = evo["to"]
                                    print(f"✨ {player['name']} is evolving into {new_name}!")
                                    if new_name not in SPECIES:
                                        base = get_species_stats(player["name"])
                                        changes = evo.get("stat_changes", {})
                                        SPECIES[new_name] = {
                                            "type": base["type"],
                                            "base_hp": max(10, base["base_hp"] + changes.get("base_hp",0)),
                                            "base_atk": max(1, base["base_atk"] + changes.get("base_atk",0)),
                                            "base_spd": max(1, base["base_spd"] + changes.get("base_spd",0)),
                                        }
                                    player["name"] = new_name
                                    # refresh moves to new species' unlocks
                                    player["moves"] = assign_moves_for_species_with_pp(player["name"], player["level"])
                            # restore hp
                            sp_new = get_species_stats(player.get("base_species",player["name"]))
                            player["current_hp"] = calc_max_hp(sp_new["base_hp"], player["level"])
                            # update codedex seen
                            game_data["codedex"].setdefault(npc["name"],{"seen":False,"caught":False})["seen"] = True
                            break
                elif action == "2":
                    # Switch mechanic
                    print("\nChoose a Codemon to switch to:")
                    for i, c in enumerate(game_data["captured"]):
                        status = "(fainted)" if c["current_hp"] <= 0 else ""
                        print(f"{i+1}. {c.get('nickname') or c['name']} Lv{c['level']} {status}")
                    try:
                        sw = int(input("Switch to #: ")) - 1
                    except:
                        sw = -1
                    if 0 <= sw < len(game_data["captured"]) and game_data["captured"][sw]["current_hp"] > 0:
                        if game_data["captured"][sw] is player:
                            print("Already in!")
                        else:
                            player = game_data["captured"][sw]
                            ensure_move_pp_struct(player)
                            print(f"You switched to {player.get('nickname') or player['name']}!")
                            delay(game_data, 0.6)
                    else:
                        print("Can't switch there.")
                elif action == "3":
                    print("You do nothing.")
                elif action == "4":
                    # flee chance uses SPD difference
                    can_flee = 60 + (calc_spd(get_species_stats(player.get("base_species",player["name"]))["base_spd"], player["level"], player.get("spd_stage",0)) - calc_spd(get_species_stats(npc["name"])["base_spd"], npc["level"], npc.get("spd_stage",0))) * 5
                    can_flee = max(5, min(95, can_flee))
                    if random.randint(1,100) <= can_flee:
                        print("You fled successfully!")
                        return False
                    else:
                        print("Failed to flee.")
                else:
                    print("Invalid action.")
            else:
                # NPC turn
                can_act = apply_status_start_of_turn(npc, game_data)
                if not can_act:
                    delay(game_data, 0.5); continue
                # NPC chooses move
                mv = npc_move_choices(npc)[0]
                # accuracy check
                if random.randint(1,100) > mv.get("accuracy",100):
                    print(f"{npc['name']}'s {mv['name']} missed!")
                    delay(game_data, 0.8)
                else:
                    out, defeated = use_move_on(npc, player, mv, game_data)
                    print(out)
                    delay(game_data, 0.8)
                    if defeated:
                        print(f"Your {player.get('nickname') or player['name']} fainted!")
                        player["current_hp"] = 0
                        break
        # end round checks
        if player["current_hp"] <= 0:
            print("You have no usable Codemon left.")
            return False
        if npc["current_hp"] <= 0:
            print("You won the battle!")
            return True
    return True

# ----------------- Capture / Hunt (updated) -----------------
def add_captured(game_data, species, level=1, is_rare=False):
    sp = get_species_stats(species)
    hp = calc_max_hp(sp["base_hp"], level)
    moves = assign_moves_for_species_with_pp(species, level)
    # Store canonical species in 'name' and mark rarity via 'rare' flag. Use rec_label for messages.
    rec_label = ("Rare " if is_rare else "") + species
    rec = {"name": species, "base_species": species, "level": level, "current_hp": hp, "moves": moves, "atk_stage": 0, "spd_stage": 0, "status": None, "status_counter": 0, "nickname": None, "rare": is_rare}
    # party limit 6
    if len([c for c in game_data["captured"]]) < 6:
        game_data["captured"].append(rec)
        print(f"{rec_label} added to your party (Lv {level}).")
    else:
        # storage default capacity 50
        if len(game_data["storage"]) < 50:
            game_data["storage"].append(rec)
            print(f"Party full. {rec_label} sent to storage.")
        else:
            print("Storage full! Could not add captured codemon.")
    # update codedex
    game_data["codedex"].setdefault(species, {"seen":False,"caught":False})["caught"] = True

def hunt(game_data, location=None):
    """Hunt for codemon. If 'location' is provided, use it (map-initiated hunt).
    Otherwise prompt the player for a location from accessible LOCATIONS."""
    clear_screen()
    if location:
        loc_name = location
        print(f"You hunt at the {loc_name} (from map)...")
        pool = LOCATIONS.get(loc_name, {}).get("pool", [])
    else:
        print("Choose hunting location or current map location:")
        accessible = []
        for name, info in LOCATIONS.items():
            locked_by = info.get("locked_by_badge")
            if not locked_by or locked_by in game_data["badges"]:
                accessible.append(name)
        for i, loc in enumerate(accessible):
            print(f"{i+1}. {loc}")
        try:
            choice = int(input("Choose location number: ")) - 1
        except:
            choice = 0
        if choice < 0 or choice >= len(accessible):
            choice = 0
        loc_name = accessible[choice]
        print(f"You head to the {loc_name}...")
        pool = LOCATIONS[loc_name]["pool"]
    time_slot = current_time_slot()
    # legendary chance
    legendary_roll = random.randint(1,100)
    if legendary_roll == 1:
        wild = "Codegon"
        is_legend = True
    else:
        wild = random.choice(pool)
        is_legend = False
    sp = get_species_stats(wild)
    wild_level = max(1, (max((c["level"] for c in game_data["captured"]), default=1) + random.randint(-1,1)))
    is_rare = random.randint(1,100) <= 5
    label = ("Rare " if is_rare else "") + wild
    clear_screen()
    print(f"A wild {label} (Lv {wild_level}) appears! Type: {sp['type']}")
    if wild in codemon_ascii:
        print(codemon_ascii[wild])
    # If called from map, keep interactive capture flow but ensure message clarity
    ans = input("Try to catch it? (yes/no): ").strip().lower()
    if ans != "yes":
        print("You let it go.")
        return
    player_max_level = max((c["level"] for c in game_data["captured"]), default=1)
    if is_legend:
        initial_catch = min(95, 30 + player_max_level * 2)
        second_catch = min(95, 15 + player_max_level)
    else:
        initial_catch = min(95, 60 + player_max_level * 4)
        second_catch = min(95, 40 + player_max_level * 2)
    print("You attempt a capture...")
    if random.randint(1,100) <= initial_catch:
        print(f"🎉 You caught {label} on the first try!")
        add_captured(game_data, wild, wild_level, is_rare)
        return
    else:
        print(f"{label} resisted the first catch attempt!")
        escape_chance = 30
        if random.randint(1,100) <= escape_chance:
            print(f"{label} escaped!")
            return
        else:
            print(f"{label} is still here... second attempt!")
            if random.randint(1,100) <= second_catch:
                print(f"🎉 You caught {label} on the second try!")
                add_captured(game_data, wild, wild_level, is_rare)
                return
            print(f"{label} escaped after the second attempt!")
            return

def current_time_slot():
    h = time.localtime().tm_hour
    if 6 <= h <= 11:
        return "morning"
    elif 12 <= h <= 17:
        return "afternoon"
    elif 18 <= h <= 23:
        return "evening"
    else:
        return "night"

# ----------------- Storage & swap -----------------
def storage_menu(game_data):
    while True:
        clear_screen()
        print("=== Storage Menu ===")
        print("Party:")
        for i, c in enumerate(game_data["captured"]):
            status = "(fainted)" if c["current_hp"] <= 0 else ""
            print(f"{i+1}. {c.get('nickname') or c['name']} Lv{c['level']} {status}")
        print("\nStorage:")
        for i, c in enumerate(game_data["storage"]):
            print(f"S{i+1}. {c['name']} Lv{c['level']}")
        print("\nOptions: (m)ove party->storage, (s)wap storage<->party, (b)ack")
        cmd = input("Choice: ").strip().lower()
        if cmd == "b":
            return
        elif cmd == "m":
            # move from party to storage
            try:
                idx = int(input("Party index to move to storage: ")) - 1
            except:
                idx = -1
            if 0 <= idx < len(game_data["captured"]) and len(game_data["storage"]) < 50:
                mon = game_data["captured"].pop(idx)
                game_data["storage"].append(mon)
                print(f"Moved {mon.get('nickname') or mon['name']} to storage.")
            else:
                print("Invalid or storage full.")
            input("Press Enter...")
        elif cmd == "s":
            try:
                pidx = int(input("Party index to swap (1..): ")) - 1
                sidx = int(input("Storage index to swap (1..): ")) - 1
            except:
                pidx = sidx = -1
            if 0 <= pidx < len(game_data["captured"]) and 0 <= sidx < len(game_data["storage"]):
                # swap
                game_data["captured"][pidx], game_data["storage"][sidx] = game_data["storage"][sidx], game_data["captured"][pidx]
                print("Swap complete.")
            else:
                print("Invalid indices.")
            input("Press Enter...")
        else:
            print("Unknown command.")

# ----------------- Codemon renaming -----------------
def rename_codemon(game_data):
    clear_screen()
    print("Rename a Codemon:")
    for i, c in enumerate(game_data["captured"]):
        print(f"{i+1}. {c.get('nickname') or c['name']} (original: {c['name']})")
    try:
        idx = int(input("Which # to rename? ")) - 1
    except:
        idx = -1
    if 0 <= idx < len(game_data["captured"]):
        new = input("Enter new nickname (empty to clear): ").strip()
        if new == "":
            game_data["captured"][idx]["nickname"] = None
            print("Nickname cleared.")
        else:
            game_data["captured"][idx]["nickname"] = new
            print("Nickname set.")
    else:
        print("Invalid choice.")
    input("Press Enter to continue...")

# ----------------- Other menus -----------------
def heal_all(game_data):
    for c in game_data["captured"]:
        base = c.get("base_species", c["name"])
        sp = get_species_stats(base)
        c["current_hp"] = calc_max_hp(sp["base_hp"], c["level"])
        c["atk_stage"] = 0
        c["spd_stage"] = 0
        c["status"] = None
        c["status_counter"] = 0
    print("All Codemon healed and statuses cleared.")

def view_codemon(game_data):
    clear_screen()
    if not game_data["captured"]:
        print("No codemon.")
    else:
        for i, c in enumerate(game_data["captured"]):
            base = c.get("base_species", c["name"])
            sp = get_species_stats(base)
            maxhp = calc_max_hp(sp["base_hp"], c["level"])
            print(f"{i+1}. {c.get('nickname') or c['name']} (Orig: {c['name']}) Lv{c['level']} HP {c['current_hp']}/{maxhp} Status: {c.get('status')}")
            print("   Moves:")
            for mv in c["moves"]:
                print(f"    - {mv['name']} (PP {mv.get('pp_current',0)}/{mv.get('max_pp',mv.get('pp',0))})")
    input("Press Enter...")

def view_codedex(game_data):
    clear_screen()
    print("Codedex:")
    for name, entry in sorted(game_data["codedex"].items()):
        if entry["caught"]:
            status = "CAUGHT"
        elif entry["seen"]:
            status = "SEEN"
        else:
            status = "UNKNOWN"
        print(f"{name}: {status}")
    input("Press Enter...")

def gym_menu(game_data):
    clear_screen()
    print("Gyms:")
    for i, g in enumerate(GYMS):
        cleared = g["badge"] in game_data["badges"]
        print(f"{i+1}. {g['name']} - Leader: {g['leader']} - Badge: {g['badge']} - {'CLEARED' if cleared else 'Available'}")
    try:
        choice = int(input("Choose gym to challenge (number) or 0 to go back: ")) - 1
    except:
        choice = -1
    if choice < 0 or choice >= len(GYMS):
        return
    gym = GYMS[choice]
    if gym["badge"] in game_data["badges"]:
        print("Already cleared.")
        input("Enter to continue...")
        return
    print(f"Challenge {gym['name']} led by {gym['leader']}? (y/n)")
    if input().strip().lower() != "y":
        return
    success = do_battle(game_data, is_gym=True, gym=gym)
    if success:
        print(f"You defeated {gym['leader']}! Badge {gym['badge']} earned.")
        game_data["badges"].append(gym["badge"])
    else:
        print("You lost the gym challenge.")
    input("Press Enter...")

def toggle_battle_speed(game_data):
    s = game_data.get("battle_speed","normal")
    new = "fast" if s == "normal" else "normal"
    game_data["battle_speed"] = new
    print(f"Battle speed set to {new}.")
    input("Press Enter...")

# ----------------- Story system -----------------
def show_intro(game_data):
    clear_screen()
    print("Professor Code: Welcome to the world of Codemon!")
    if not game_data.get("rival_team"):
        player_first = game_data["captured"][0]["name"] if game_data["captured"] else None
        choices = [s for s in codemon_list if s != player_first and s != "Codegon"]
        rival_starter = random.choice(choices) if choices else "Codemander"
        game_data["rival_team"] = [{"name":rival_starter, "level":1}]
        print(f"A rival trainer appears — they picked {rival_starter} as their starter!")
    input("Press Enter...")

def show_codegon_legend():
    clear_screen()
    print("Elder: Tales of Codegon whisper among trainers. Collect all badges and face your destiny.")
    input("Press Enter...")

def unlock_league():
    clear_screen()
    print("🏆 The Codemon League is now open!")
    input("Press Enter...")

def show_endgame():
    clear_screen()
    print("🎉 You become Champion! The world still hides secrets - keep exploring!")
    input("Press Enter...")

def trigger_rival_battle(game_data, stage=1, champion=False):
    clear_screen()
    print("Your rival challenges you!")
    avg_level = max(1, sum(c["level"] for c in game_data["captured"]) // max(1,len(game_data["captured"])))
    base_level = avg_level + stage + (3 if champion else 0)
    # build team depending on stage
    if stage == 1:
        rival_species = [game_data["rival_team"][0]["name"]]
    elif stage == 2:
        rival_species = [game_data["rival_team"][0]["name"], "Codeasaur"]
    else:
        rival_species = ["Codezard","Codetree","Codemagma"]
    rival_team = []
    for sp in rival_species:
        lvl = max(1, base_level + random.randint(-1,1))
        rival_team.append({"name":sp, "level":lvl, "current_hp":calc_max_hp(get_species_stats(sp)["base_hp"], lvl)})
    for opp in rival_team:
        print(f"Rival sends {opp['name']} (Lv {opp['level']})")
        res = do_battle(game_data, npc_override=opp, trainer_name="Rival")
        if not res:
            print("Rival defeated you.")
            input("Press Enter...")
            return
    print("You defeated your rival!")
    input("Press Enter...")

def trigger_codegon_event(game_data):
    clear_screen()
    print("Atop the League, the sky parts and Codegon descends...")
    level = max(30, sum(c["level"] for c in game_data["captured"]) // max(1,len(game_data["captured"])) + 5)
    legendary = {"name":"Codegon","level":level,"current_hp":calc_max_hp(get_species_stats("Codegon")["base_hp"], level), "moves": assign_moves_for_species_with_pp("Codegon", level), "status":None}
    res = do_battle(game_data, npc_override=legendary, trainer_name="Legendary")
    if res:
        print("You faced Codegon.")
    else:
        print("Codegon escaped.")
    input("Press Enter...")

def check_story_progress(game_data):
    stage = game_data.get("story_stage", 0)
    if stage == 0:
        show_intro(game_data); game_data["story_stage"]=1
    elif stage == 1 and len(game_data["badges"]) >= 1:
        trigger_rival_battle(game_data, stage=1); game_data["story_stage"]=2
    elif stage == 2 and len(game_data["badges"]) >= 3:
        show_codegon_legend(); trigger_rival_battle(game_data, stage=2); game_data["story_stage"]=3
    elif stage == 3 and len(game_data["badges"]) >= len(GYMS):
        unlock_league(); game_data["story_stage"]=4
    elif stage == 4:
        trigger_rival_battle(game_data, stage=3, champion=True); game_data["story_stage"]=5
    elif stage == 5:
        trigger_codegon_event(game_data); game_data["story_stage"]=6

# ----------------- Map functions -----------------
def display_world(player_pos):
    clear_screen()
    for r, row in enumerate(WORLD_MAP):
        line = ""
        for c, ch in enumerate(row):
            if (r, c) == player_pos:
                line += "P"
            else:
                line += ch
        print(line)
    print("\nLegend: S=Start, T=Town, F=Forest, C=Cave, L=Lake, M=Mountain, H=House, D=League")

def map_menu(game_data):
    # load start position from save (persisted)
    player_pos = tuple(game_data.get("player_pos", (1,1)))
    while True:
        display_world(player_pos)
        print("\nMap options: W/A/S/D to move, (h)unt here, (b)ack to main menu")
        cmd = input("Command: ").strip().lower()
        if cmd == "b":
            # persist current map position into save structure
            game_data["player_pos"] = player_pos
            # save immediately so map position persists and inform player
            save_game(game_data)
            print("Map position saved.")
            input("Press Enter to continue...")
            return
        elif cmd in ("w","a","s","d"):
            r,c = player_pos
            if cmd == "w": nr, nc = r-1, c
            elif cmd == "s": nr, nc = r+1, c
            elif cmd == "a": nr, nc = r, c-1
            else: nr, nc = r, c+1
            if 0 <= nr < len(WORLD_MAP) and 0 <= nc < len(WORLD_MAP[0]) and WORLD_MAP[nr][nc] != "#":
                player_pos = (nr, nc)
            else:
                print("Can't move there.")
        elif cmd == "h":
            # check tile under player and convert to location if relevant
            r,c = player_pos
            ch = WORLD_MAP[r][c]
            # map characters to loc names
            map_to_loc = {"F":"Forest","C":"Cave","L":"Lake","M":"Mountain"}
            if ch in map_to_loc:
                # call hunt at that location (pass location so hunt is dynamic)
                loc_name = map_to_loc[ch]
                print(f"You hunt at the {loc_name} (time: {current_time_slot()})")
                hunt(game_data, loc_name)
                # after a map-initiated hunt, persist state and pause so player sees the outcome
                game_data["player_pos"] = player_pos
                save_game(game_data)
                input("Press Enter to continue...")
            else:
                print("No hunting here.")
        else:
            print("Unknown command.")

# ----------------- Main loop -----------------
def main():
    game_data = load_game()
    clear_screen()
    print("Welcome to Codemon v4!")
    if not game_data["captured"]:
        choose_starter(game_data)
    while True:
        clear_screen()
        check_story_progress(game_data)
        print("\nMain Menu:")
        print("1. Battle a trainer")
        print("2. Hunt for a new Codemon")
        print("3. Map (explore)")
        print("4. Storage / Box")
        print("5. Heal all Codemon")
        print("6. View Codemon")
        print("7. View Codedex")
        print("8. Gyms & Badges")
        print("9. Rename a Codemon")
        print("10. Toggle Battle Speed (normal/fast)")
        print("11. Save and Exit")
        choice = input("Choose (1-11): ").strip()
        if choice == "1":
            do_battle(game_data)
            input("Press Enter...")
        elif choice == "2":
            hunt(game_data)
            input("Press Enter...")
        elif choice == "3":
            map_menu(game_data)
        elif choice == "4":
            storage_menu(game_data)
        elif choice == "5":
            heal_all(game_data); input("Press Enter...")
        elif choice == "6":
            view_codemon(game_data)
        elif choice == "7":
            view_codedex(game_data)
        elif choice == "8":
            gym_menu(game_data)
        elif choice == "9":
            rename_codemon(game_data)
        elif choice == "10":
            toggle_battle_speed(game_data)
        elif choice == "11":
            save_game(game_data); print("Saved. Bye!"); break
        else:
            print("Invalid choice.")
            input("Press Enter...")

if __name__ == "__main__":
    main()
