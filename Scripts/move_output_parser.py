import json

# Mapping dictionary
action_mappings = {
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
    "NmlAtk2A": "2P",
    "NmlAtk2B": "2K",
    "NmlAtk2C": "2S",
    "NmlAtk2D": "2H",
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
