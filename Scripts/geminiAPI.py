import json
import os
import google.generativeai as genai

def load_api_key(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()

def load_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def parse_frame_data(input_file_path, output_file_path, action_mappings, no_replace_actions):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file.readlines()]

    unfound_actions = set()

    for entry in data:
        for character, details in entry.items():
            if "action" in details:
                action = details["action"]
                if action in action_mappings:
                    details["action"] = action_mappings[action]
                elif action not in no_replace_actions and action not in unfound_actions:
                    print(f"No mapping found for action: {action}")
                    unfound_actions.add(action)

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for entry in data:
            file.write(json.dumps(entry) + '\n')

action_mappings = {
    # Generic Movement
    "CmnActBDash": "Backdash",
    "CmnActBWalk": "Walk Backwards",
    "CmnActBurst": "Burst",
    "CmnActCrouch": "Crouch",
    "CmnActCrouch2Stand": "Stand from crouch",
    "CmnActFDash": "Dash",
    "SpecialCancel_FDash": "Dash cancel from special",
    "CmnActFDashStop": "Dash Stop",
    "CmnActAirFDash": "Forward airdash",
    "CmnActAirBDash": "Back airdash",
    "CmnActAirGuardLoop": "Air blockstun",
    "CmnActAirGuardEnd": "Air blockstun ending",
    "CmnActFWalk": "Walk Forwards",
    "CmnActJump": "Jump",
    "CmnActJumpLanding": "Jump Land",
    "CmnActLandingStiff": "Exposed landing",
    "CmnActJumpPre": "Pre-Jump",
    "CmnActAirTurn": "Air turn",
    "CmnActStand": "Stand",
    "CmnActStand2Crouch": "Crouching",
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
    "CmnActExDamageLand": "Extra Damage",
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
    "WorldSideBreak_Master_DS": "Completed dust combo",
    
    "WSB_Slave_Down": "Put through wall",
    "WSB_Slave_Bound": "Put through wall",
    "WSB_Slave_Slide": "Put through wall",
    "WSB_Slave_Up": "Put through wall",
    "WorldSideBreak_Slave_DF": "Put through wall",
    "WorldSideBreak_Slave_DS": "Landing from hit dust combo",
    
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
    "ThrowExe": "Throw animation",
    "AirThrowExe": "Air throw animation",
    
    "CmnActRomanCancel": "Roman Cancel",
    "HomingJumpLoop": "Homing Jump",
    "DustFinish": "Dust Ender",
    
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
    "IrukasanEnd": "Dolphin End",
    "OverHeadKissExe": "Overhead Kiss Animation",
    
    # Ram
    "BajonetoC": "S Bajoneto",
    "BajonetoD": "H Bajoneto",
    "Morutobato": "Mortobato",
    
    # Bridget
    "KSMH": "Kick Start My Heart",
    "KSMH_P": "Kick Start My Heart Brake",
    "KSMH_K": "Kick Start My Heart Shoot",
    "LoopTheLoop": "Kick Start My Heart Shoot",
    "NmlAtk5CFar_2nd": "f.S followup",
    "NmlAtk5D_2nd": "5H followup",
    "YOYO_214S_Land": "Grounded Stop and Dash (Hit on return)",
    "YOYO_214S_Air": "Air Stop and Dash (Hit on return)",
    "YOYO_236S_Land": "Grounded Stop and Dash (Hit on send)",
    "YOYO_236S_Air": "Air Stop and Dash (Hit on send)",
    "YOYO_236S_Air": "Air Stop and Dash (Hit on send)",
    "Rolling": "Rolling movement",
    "KillMachine_Land": "Return of the Killing Machine",
    "KillMachine_Air": "Air Return of the Killing Machine",
    "RockTheBaby_Land": "Rock the Baby",
    "RockTheBaby_Air": "Air Rock the Baby",
    
    # Bedman?
    "AirMove": "Air Move",
    "AirMove7": "Air Move Up Back",
    "AirMove8": "Air Move Up",
    "AirMove9": "Air Move Up Forward",
    "AirMove4": "Air Move Back",
    "AirMove6": "Air Move Forward",
    "AirMove1": "Air Move Down Back",
    "AirMove2": "Air Move Down",
    "AirMove3": "Air Move Down Forward",
    "Ultimate1_Land": "Call 13C",
    "Ultimate1_Air": "Call 13C (air)",
    "Ultimate2": "Call 4CC",
    "Special1_Land": "call 4BA",
    "Special1_Air": "call 4BA (air)",
}

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
    
    # Ram
    "Ondo",
    "Dauro",
    "Erarurumo1",
    "Erarurumo2",
    "AgresaOrdono",
    "Sabrobato",
    
    # Bridget
    "LoopTheLoop",
}

class ChatEngine:
    @classmethod
    def generate_response(cls, prompt):
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        try:
            return response.text
        except ValueError:
            print("Response was blocked. Safety ratings:")
            for candidate in response.candidates:
                print(candidate.safety_ratings)
            return None

def main():
    api_key_path = 'gemini_key'
    genai.configure(api_key=load_api_key(api_key_path))
    
    input_file_path = r"C:\Program Files (x86)\Steam\steamapps\common\GUILTY GEAR STRIVE\RED\Binaries\Win64\frame_data.json"
    output_file_path = r"C:\Program Files (x86)\Steam\steamapps\common\GUILTY GEAR STRIVE\RED\Binaries\Win64\frame_data_readable.json"

    # Parse the frame data
    parse_frame_data(input_file_path, output_file_path, action_mappings, no_replace_actions)

    # Load JSON frame data
    frame_data = load_file(output_file_path)

    # Load character guide texts
    guide_paths = [
        r"D:\Git\StriveFrameViewer\Scripts\character_data\Slayer_Overview.txt",
        r"D:\Git\StriveFrameViewer\Scripts\character_data\Slayer_Starter_Guide.txt",
        r"D:\Git\StriveFrameViewer\Scripts\character_data\Slayer_Combos.txt",
        r"D:\Git\StriveFrameViewer\Scripts\character_data\Slayer_Strategy_Guide.txt"
    ]
    guide_texts = [load_file(path) for path in guide_paths]
    combined_guide_text = "\n\n".join(guide_texts)

    # Create the contextual prompt
    user_prompt = f"""
    The following is a json comprising the frame data of a game of Guilty Gear Strive:
    {frame_data}
    
    Please write a timeline events in the match. Each bit on the timeline should contain a few seconds of in game time, depending on how much interesting stuff is happening. Concatenate combos. A true combo 20 seconds long can just be one bit. Summarize which buttons were in the combo, how many hits and how much damage. Was the combo dropped? Reflect on the post-combo okizeme situation. 

    Here's a representative example of how to display what button hits in a combo sequence: 
    '''
    CH 2D, cS, [5D], cS, P Dandy Step, Pilebunker, cS, 2S, 2H, P Dandy Step, Pilebunker
    '''
    The above means the starter was a counterhit 2D, followed by cS and a charged 5D. The rest is pretty self explanatory. 

    Focus on the player decision points.
    """
    
    with open('test_prompt.txt', 'w', encoding='utf-8') as file:
        file.write(user_prompt)
        
    response = ChatEngine.generate_response(user_prompt)
    if response:
        print(response)

if __name__ == "__main__":
    main()
