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
    "CmnActFDashStop": "Dash Stop",
    "CmnActAirFDash": "Forward airdash",
    "CmnActAirBDash": "Back airdash",
    "CmnActAirGuardLoop": "Air blockstun",
    "CmnActFWalk": "Walk Forwards",
    "CmnActJump": "Jump",
    "CmnActJumpLanding": "Jump Land",
    "CmnActLandingStiff": "Exposed landing",
    "CmnActJumpPre": "Pre-Jump",
    "CmnActStand": "Stand",
    "CmnActStand2Crouch": "Stand to crouch",
    "CmnActFaultlessPressureLand": "Faultless defense",
    
    # Getting hit
    "CmnActNokezoriHighLv1": "Standing Hitstun lv1",
    "CmnActNokezoriHighLv2": "Standing Hitstun lv2",
    "CmnActNokezoriHighLv3": "Standing Hitstun lv3",
    "CmnActNokezoriHighLv4": "Standing Hitstun lv4",
    "CmnActNokezoriHighLv5": "Standing Hitstun lv5",
    
    "CmnActNokezoriBottomLv1": "Hitstun lv1",
    "CmnActNokezoriBottomLv2": "Hitstun lv2",
    "CmnActNokezoriBottomLv3": "Hitstun lv3",
    "CmnActNokezoriBottomLv4": "Hitstun lv4",
    "CmnActNokezoriBottomLv5": "Hitstun lv5",
    
    "CmnActNokezoriLowLv1": "Low Hitstun lv1",
    "CmnActNokezoriLowLv2": "Low Hitstun lv2",
    "CmnActNokezoriLowLv3": "Low Hitstun lv3",
    "CmnActNokezoriLowLv4": "Low Hitstun lv4",
    "CmnActNokezoriLowLv5": "Low Hitstun lv5",
    
    "CmnActNokezoriCrouchLv1": "Crouching Hitstun lv1",
    "CmnActNokezoriCrouchLv2": "Crouching Hitstun lv2",
    "CmnActNokezoriCrouchLv3": "Crouching Hitstun lv3",
    "CmnActNokezoriCrouchLv4": "Crouching Hitstun lv4",
    "CmnActNokezoriCrouchLv5": "Crouching Hitstun lv5",
    
    "CmnActKirimomiUpper": "Hitstunned",
    
    "CmnActUkemi": "Recovering",
    "CmnActCrouchTurn": "Crouching turn",
    "CmnActStandTurn": "Standing turn",
    
    "CmnActHighGuardLoop": "Standing blockstunned",
    "CmnActCrouchGuardLoop": "Crouching blockstunned",
    "CmnActCrouchGuardEnd": "Crouching blockstunned ending",
    "CmnActMidGuardLoop": "Blockstunned",
    "CmnActMidGuardEnd": "Blockstun ending",
    "CmnActGuardLanding": "Landing from air blockstun",
    "CmnActHighGuardEnd": "Blockstun ending",
    
    "CmnActLockWait": "Animation Lock",
    "CmnActBlowoff": "Animation Lock",
    "CmnActZSpin": "Spinning Lock",
    "CmnActKorogari": "Tumbling Lock",
    
    "CmnActExDamage": "Hit for extra",
    
    "CmnActFloatDamage": "Falling",
    
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
    "CmnActHajikareCrouch": "Staggered crouch",
    "CmnActHajikareStand": "Staggered standing",
    "CmnActHajikareAir": "Staggered in air",
    "CmnActHizakuzure": "Collapsed kneeling",
    
    "CmnActWallBound": "Wall bounced",
    "CmnActWallBoundDown": "Wall bounced falling",
    
    "CmnActWallHaritsuki": "Wallstick",
    "WSB_Master_Wait": "Sent opponent through wall",
    "WorldSideBreak_Master_DF": "Sent opponent through wall",
    "WSB_Master_Down": "Sent opponent through wall",
    "WSB_Master_Up": "Sent opponent through wall",
    "WSB_Master_Bound": "Sent opponent through wall",
    "WSB_Master_Slide": "Sent opponent through wall",
    
    "WSB_Slave_Down": "Put through wall",
    "WSB_Slave_Bound": "Put through wall",
    "WSB_Slave_Slide": "Put through wall",
    "WSB_Slave_Up": "Put through wall",
    "WorldSideBreak_Slave_DF": "Put through wall",
    
    "CmnActMatchWin": "Match win",
    
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
    "NmlAtk5E": "5D",
    "NmlAtkAir5A": "j.P",
    "NmlAtkAir5B": "j.K",
    "NmlAtkAir5C": "j.S",
    "NmlAtkAir5D": "j.H",
    "NmlAtkAir5E": "j.D",
    "NmlAtkThrow": "Throw",
    "NmlAtkAirThrow": "Air throw",
    "ThrowExe": "Throwing",
    
    "CmnActRomanCancel": "Roman Cancel",
    "HomingJumpLoop": "Homing Jump Landing",
    
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
    
    # Potemkin
    "HeatKnucle": "HeatKnuckle",
    "PotemkinBusterExe": "Potemkin Buster Animation",
    
    # Giovanna
    "Special1": "Sepultura",
    "Special2_land": "Grounded Sol Poente", 
    "Special2_air": "Aerial Sol Poente",  
    "Special3": "Sol Nascente",  
    "Special4": "Trovão", 
    "Shervi": "Chave", 
    "LandUltimate": "Ventania", 
    "AirUltimate": "Tempestade", 
    
    # A.B.A.
    "ABA_SP1_Land": "Grounded Bonding and Dissolving", 
    "ABA_SP1_Air": "Aerial Bonding and Dissolving", 
    "ABA_SP2": "Changing and Swaying", 
    "ABA_SP3": "Haul and Heed", 
    "ABA_SP4": "Intertwine and Tilt", 
    "ABA_SP5": "Menace and Groan", 
    "ABA_SP6": "Restriction and Constraint", 
    "ABA_SP7": "Frenzy and Astonishment",
    "ABA_SP1_Land_Moroha": "Grounded Bonding and Dissolving (Moroha)",
    "ABA_SP1_Air_Moroha": "Aerial Bonding and Dissolving (Moroha)",
    "ABA_SP2_Moroha": "Changing and Swaying (Moroha)",
    "ABA_SP3_Moroha": "Haul and Heed (Moroha)",
    "ABA_SP4_Moroha": "Intertwine and Tilt (Moroha)",
    "ABA_SP5_Moroha": "Menace and Groan (Moroha)",
    "ABA_SP6_Moroha": "Restriction and Constraint (Moroha)",
    "ABA_SP7_Moroha": "Frenzy and Astonishment (Moroha)",
    "ABA_SP8": "Judgment and Sentiment", 
    "ABA_Moroha_End": "Moroha Mode End", 
    "ABA_Moroha_End": "Moroha Mode End", 
    "ABA_ULT1": "The Law is Key, Key is King", 
    "ABA_ULT1_Moroha": "The Law is Key, Key is King (Moroha)", 
    "ABA_ULT1_Moroha_exe": "The Law is Key, Key is King (Moroha) Animation", 
    "ABA_ULT1_exe": "The Law is Key, Key is King Animation", 
    "ABA_ULT2": "Keeper of the Key", 
    "ABA_ULT2_Moroha": "Keeper of the Key (Moroha)", 
    
    # Johnny
    "MistFiner_FWalk": "MistFiner stance forward walk", 
    "MistFiner_BWalk": "MistFiner stance back walk", 
    "MistFiner_FDash": "MistFiner stance forward dash", 
    "MistFiner_BDash": "MistFiner stance back dash", 
    
    # Leo
    "NmlAtk5CFar_Guard": "Guard stance",
    "NmlAtk5D_Guard": "Guard stance",
    "GuardAttack": "Guard stance attack",
    "Semuke": "Standing (Brynhildr Stance)",
    "SemukeReverse": "Brynhildr Stance Canceled",
    "Semuke5A": "bt.P",
    "Semuke5B": "bt.K",
    "Semuke5C": "bt.S",
    "Semuke5D": "bt.H",
    "Semuke5E": "bt.D",
    "SemukeFWalk": "Forward Walk (Brynhildr Stance)",
    "SemukeFDashStep": "Forward Dash Step (Brynhildr Stance)",
    "SemukeBWalk": "Back Walk (Brynhildr Stance)",
    "SemukeBDashStep": "Back Dash Step (Brynhildr Stance)",
    "GraviertWurdeC": "Gravierte Würde S",
    "GraviertWurdeD": "Gravierte Würde H",
    "EisenSturmC": "Eisensturm S",
    "EisenSturmD": "Eisensturm H",
    "ErstWind": "Erstes Kaltes Gestöber",
    "ZweitWind": "Zweites Kaltes Gestöber",
    "GlaenzenDunkel": "Glänzendes Dunkel",
    "GlaenzenDunkelExe": "Glänzendes Dunkel Animation",
    "SchildBrechen": "Glänzendes Dunkel",
    
    # Asuka (I need to rethink my structure for him)
    "Magic": "Spell Cast",
    "Magic_air": "Spell Cast in air",
    "ASK_Ultimate1": "High Compression Submicron Particle Sphere",
    "ASK_Ultimate2": "Bookmark (Full Order)",
    
    # Sol
    "BukkirabouNiNageru": "Wild Throw",
    "BukkiraExe": "Wild Throw Animation",
    "HMC": "Heavy Mob Cemetary",
    "HMCExe": "Heavy Mob Cemetary Animation",
    "Fefnir": "Fafnir",
    "Vortex": "Night Raid Vortex",
    
    # Ky
    "VaporThrustC": "Vapor Thrust S",
    "VaporThrustD": "Vapor Thrust H",
    "AirVaporThrustC": "Air Vapor Thrust S",
    "AirVaporThrustD": "Air Vapor Thrust H",
    "StunEdge1": "Stun Edge S",
    "AirStunEdge1": "Air Stun Edge S",
    "StunEdge2": "Stun Edge H",
    "AirStunEdge2": "Air Stun Edge H",
    "Diaekura": "Dire Eclat",
    "FadulArc": "Foudre Arc",
    
    # May
    "NmlAtk3B": "3K",
    "NmlAtkAir2D": "j.2H",
    "IrukasanYokoC": "S Dolphin Horiz",
    "IrukasanTateC": "S Dolphin Vert",
    "IrukasanYokoD": "H Dolphin Horiz",
    "IrukasanTateD": "H Dolphin Vert",
    "IrukasanJump": "Split Jump Off Dolphin",
    "OverHeadKissExe": "Overhead Kiss Animation",
}

# Some actions are basically the same as the human-readable version so
no_replace_actions = {
    # Generic
    "WildAssault",
    "HomingJump",

    # Potemkin
    "HammerFall",
    "HammerFallBrake",
    "GarudaImpact",
    "SlideHead",
    "MegaFistFront",
    "MegaFistBack",
    "PotemkinBuster",
    "FDB",
    
    # Johnny
    "MistFiner_Stance",
    "AirMistFiner_Stance",
    "MistFiner_Cancel",
    "AirMistFiner_Cancel",
    "Ensenga",
    
    # Leo
    "Turbulenz",
    
    # Asuka
    "Draw_or_Discard",
    "Draw_or_Discard_air",
    "Change_deck",
    "Change_deck_air",
    
    # Sol
    "GunFlame",
    "GunFlameFeint",
    "VolcanicViperLandS",
    "VolcanicViperAirS",
    "VolcanicViperLandHS",
    "VolcanicViperAirHS",
    "BanditRevolver_Land",
    "BanditRevolver_Air",
    "BanditBringer_Land",
    "BanditBringer_Air",
    "TyrantRave",
    
    # Ky
    "StunDipper",
    "AirRideTheLightning",
    "RideTheLightning",
    "SacredEdge",
    "DragonInstall",
    
    # May
    "OverHeadKiss",
    "Arisugawa",
    "Goshogawara",
    "AirGoshogawara",
    "Yamada",
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
        elif action_p1 not in no_replace_actions and action_p1 not in unfound_actions:
            print(f"No mapping found for action: {action_p1}")
            unfound_actions.add(action_p1)

    if "p2" in entry and "action" in entry["p2"]:
        action_p2 = entry["p2"]["action"]
        if action_p2 in action_mappings:
            entry["p2"]["action"] = action_mappings[action_p2]
        elif action_p2 not in no_replace_actions and action_p2 not in unfound_actions:
            print(f"No mapping found for action: {action_p2}")
            unfound_actions.add(action_p2)

# Save the updated data back to a JSON file
output_file_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\GUILTY GEAR STRIVE\\RED\\Binaries\\Win64\\frame_data_readable.json"
with open(output_file_path, 'w') as file:
    for entry in data:
        file.write(json.dumps(entry) + '\n')