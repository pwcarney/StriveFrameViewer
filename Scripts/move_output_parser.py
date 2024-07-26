import json

# Mapping dictionary
action_mappings = {
    # Generic Movement
    "CmnActBDash": "Backdash",
    "CmnActBWalk": "Walk Backwards",
    "CmnActBurst": "Burst",
    "CmnActCrouch": "Crouch",
    "CmnActCrouch2Stand": "Stand from crouch",
    "CmnActFDash": "Dash",
    "CmnActFWalk": "Walk Forwards",
    "CmnActJump": "Jump",
    "CmnActJumpLanding": "Jump Land",
    "CmnActJumpPre": "Pre-Jump",
    "CmnActStand": "Stand",
    "CmnActStand2Crouch": "Stand to crouch",
    
    "CmnActLockWait": "Animation Lock",
    "CmnActBlowoff": "Animation Lock",
    "CmnActZSpin": "Spinning Lock",
    "CmnActKorogari": "Tumbling Lock",
    
    "CmnActExDamage": "Hit for extra",
    
    "CmnActFDownUpper": "Down in air",
    "CmnActFDownBound": "Knockdown",
    "CmnActFDownLoop": "Down, animation locked",

    "CmnActVDownUpper": "Down in air",
    "CmnActVDownBound": "Knockdown",
    "CmnActVDownLoop": "Down, animation locked",
    "CmnActFDown2Stand": "Getting up from knockdown",
    
    "CmnActQuickDown": "Soft knockdown",
    "CmnActQuickDown2Stand": "Soft knockdown recovery",
    
    "CmnActHizakuzure": "Collapsed kneeling",
    
    # Generic Attacks
    "NmlAtk2A": "2P",
    "NmlAtk6A": "6P",
    "NmlAtk2B": "2K",
    "NmlAtk6B": "6K",
    "NmlAtk2C": "2S",
    "NmlAtk6C": "6S",
    "NmlAtk2D": "2H",
    "NmlAtk6D": "6H",
    "NmlAtk2E": "2D",
    "NmlAtk5A": "5P",
    "NmlAtk5B": "5K",
    "NmlAtk5CFar": "f.S",
    "NmlAtk5CNear": "c.S",
    "NmlAtk5D": "5H",
    "NmlAtkAir5A": "j.P",
    "NmlAtkAir5B": "j.K",
    "NmlAtkAir5C": "j.S",
    "NmlAtkAir5D": "j.H",
    "NmlAtkAir5E": "j.D",
    "NmlAtkThrow": "Throw",
    "ThrowExe": "Throwing",
    
    # Slayer
    "sly_SP_01": "P Mappa Hunch",
    "sly_SP_02": "K Mappa Hunch",
    "sly_SP_03": "P Dandy Step",
    "sly_SP_04": "K Dandy Step",
    "sly_SP_05": "Pilebunker",
    "sly_SP_06": "Bump Ahead",
    "sly_SP_07": "It's Late",
    "sly_SP_08": "Master's Hammer",
    "sly_SP_09": "Bloodsucking Universe",
    "sly_SP_09_exe": "Bloodsucking Universe Throwing",
    "sly_SP_10": "Hand of Doom",
    "sly_ULT_01": "Last Horizon",
    "sly_ULT_01_exe": "Last Horizon Animation",
    "sly_ULT_02": "Super Mappa Hunch",
}

# Load the JSON data
with open('/mnt/data/frame_data.json', 'r') as file:
    data = [json.loads(line) for line in file.readlines()]

# Replace esoteric action terms with human-readable text
for entry in data:
    if "p1" in entry and "action" in entry["p1"]:
        entry["p1"]["action"] = action_mappings.get(entry["p1"]["action"], entry["p1"]["action"])
    if "p2" in entry and "action" in entry["p2"]:
        entry["p2"]["action"] = action_mappings.get(entry["p2"]["action"], entry["p2"]["action"])

# Save the updated data back to a JSON file
with open('/mnt/data/frame_data_readable.json', 'w') as file:
    for entry in data:
        file.write(json.dumps(entry) + '\n')
