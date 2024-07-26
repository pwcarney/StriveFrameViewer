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
    
    # Getting hit
    "CmnActNokezoriHighLv1": "Standing Hitstun lv1",
    "CmnActNokezoriHighLv2": "Standing Hitstun lv2",
    "CmnActNokezoriHighLv3": "Standing Hitstun lv3",
    "CmnActNokezoriHighLv4": "Standing Hitstun lv4",
    "CmnActNokezoriHighLv5": "Standing Hitstun lv5",
    
    "CmnActNokezoriCrouchLv1": "Crouching Hitstun lv1",
    "CmnActNokezoriCrouchLv2": "Crouching Hitstun lv2",
    "CmnActNokezoriCrouchLv3": "Crouching Hitstun lv3",
    "CmnActNokezoriCrouchLv4": "Crouching Hitstun lv4",
    "CmnActNokezoriCrouchLv5": "Crouching Hitstun lv5",
    
    "CmnActNokezoriCrouchLv5": "Hitstun lv5",
    
    "CmnActLockWait": "Animation Lock",
    "CmnActBlowoff": "Animation Lock",
    "CmnActZSpin": "Spinning Lock",
    "CmnActKorogari": "Tumbling Lock",
    
    "CmnActExDamage": "Hit for extra",
    
    "CmnActBDownUpper": "Falling",
    "CmnActBDownBound": "Falling",
    "CmnActBDownDown": "Falling",
    "CmnActBDownLoop": "Down",
    
    "CmnActFDownUpper": "Falling",
    "CmnActFDownBound": "Falling",
    "CmnActFDownLoop": "Down",

    "CmnActVDownUpper": "Falling",
    "CmnActVDownDown": "Falling",
    "CmnActVDownBound": "Knockdown",
    "CmnActVDownLoop": "Down",
    
    "CmnActBDown2Stand": "Getting up from knockdown",
    "CmnActFDown2Stand": "Getting up from knockdown",
    
    "CmnActQuickDown": "Soft knockdown",
    "CmnActQuickDown2Stand": "Soft knockdown recovery",
    
    "CmnActJitabataLoop": "Staggered",
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

# Load the JSON data from the specified file path
file_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\GUILTY GEAR STRIVE\\RED\\Binaries\\Win64\\frame_data.json"
with open(file_path, 'r') as file:
    data = [json.loads(line) for line in file.readlines()]

# Track unfound actions
unfound_actions = set()

# Replace esoteric action terms with human-readable text
for entry in data:
    if "p1" in entry and "action" in entry["p1"]:
        action_p1 = entry["p1"]["action"]
        if action_p1 in action_mappings:
            entry["p1"]["action"] = action_mappings[action_p1]
        else:
            if action_p1 not in unfound_actions:
                print(f"No mapping found for action: {action_p1}")
                unfound_actions.add(action_p1)

    if "p2" in entry and "action" in entry["p2"]:
        action_p2 = entry["p2"]["action"]
        if action_p2 in action_mappings:
            entry["p2"]["action"] = action_mappings[action_p2]
        else:
            if action_p2 not in unfound_actions:
                print(f"No mapping found for action: {action_p2}")
                unfound_actions.add(action_p2)

# Save the updated data back to a JSON file
output_file_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\GUILTY GEAR STRIVE\\RED\\Binaries\\Win64\\frame_data_readable.json"
with open(output_file_path, 'w') as file:
    for entry in data:
        file.write(json.dumps(entry) + '\n')