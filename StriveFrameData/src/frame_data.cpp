#include "frame_data.h"
#include "action_descriptions.h"
#include "output_file.h"
#include "sigscan.h"
#include <cmath>
#include <fstream>
#include <set>
#include <unordered_set>
#include <iostream>
#include <array>
#include <string>
#include <unordered_map>

using json = nlohmann::json;

static uintptr_t universalBaseAddress;
static int frameCount = 0;
static int identicalFrameCount = 0;
static json previousFrame;

static std::string p1CharacterName;
static std::string p2CharacterName;

// Previous state variables for both players
static int prevTensionPlayer1 = -1;
static int prevBurstPlayer1 = -1;
static int prevRiscPlayer1 = -1;
static int prevPosXPlayer1 = -1;
static std::string prevStatePlayer1 = "";
static std::string prevAtkPhasePlayer1 = "";

static int prevTensionPlayer2 = -1;
static int prevBurstPlayer2 = -1;
static int prevRiscPlayer2 = -1;
static int prevPosXPlayer2 = -1;
static std::string prevStatePlayer2 = "";
static std::string prevAtkPhasePlayer2 = "";

// Utility function to reset previous state values
void resetPreviousValues() {
    frameCount = 0;
    identicalFrameCount = 0;

    prevTensionPlayer1 = -10000;
    prevBurstPlayer1 = -10000;
    prevRiscPlayer1 = -10000;
    prevPosXPlayer1 = -10000;
    prevStatePlayer1 = "";
    prevAtkPhasePlayer1 = "";

    prevTensionPlayer2 = -10000;
    prevBurstPlayer2 = -10000;
    prevRiscPlayer2 = -10000;
    prevPosXPlayer2 = -10000;
    prevStatePlayer2 = "";
    prevAtkPhasePlayer2 = "";
}

// Function to log round start and reset previous values
void logRoundStart() {
    resetPreviousValues();
    logEvent("Round Start!");
}

// Define a mapping from PlayerStateType to string
std::string playerStateTypeToString(PlayerStateType state) {
    static const std::unordered_map<PlayerStateType, std::string> stateToString = {
        {PST_Idle, "Idle"},
        {PST_BlockStunned, "BlockStunned"},
        {PST_HitStunned, "HitStunned"},
        {PST_Busy, "Busy"},
        {PST_Attacking, "Attacking"},
        {PST_ProjectileAttacking, "ProjectileAttacking"},
        {PST_Recovering, "Recovering"},
        {PST_None, "None"},
        {PST_End, "End"}
    };

    auto it = stateToString.find(state);
    if (it != stateToString.end()) {
        return it->second;
    }
    else {
        return "Unknown";
    }
}

void addPlayerDataToJson(json& playerJson, const asw_player* player, const PlayerState& state, int tension, int burst, int& prevTension, int& prevBurst, int& prevRisc, int& prevPosX, std::string& prevState, std::string& prevAtkPhase) {
    playerJson["hp"] = player->hp;

    int roundedTension = std::round(tension / 100.0);
    if (roundedTension != prevTension) {
        playerJson["tension"] = roundedTension;
        prevTension = roundedTension;
    }

    int roundedBurst = std::round(burst / 100.0);
    if (roundedBurst != prevBurst) {
        playerJson["burst"] = roundedBurst;
        prevBurst = roundedBurst;
    }

    if (player->risc != prevRisc) {
        playerJson["risc"] = player->risc;
        prevRisc = player->risc;
    }

    if (player->pos_x_from_center != prevPosX) {
        playerJson["posX"] = std::round(player->pos_x_from_center / 1000.0);
        prevPosX = player->pos_x_from_center;
    }

    if (player->pos_y != 0) {
        playerJson["posY"] = std::round(player->pos_y / 1000.0);
    }

    playerJson["action"] = player->get_BB_state();

    if (player->blockstun != 0) {
        playerJson["blkstun"] = player->blockstun;
    }

    std::string attackPhase;
    if (state.type == PST_Busy) {
        attackPhase = "startup";
    }
    else if (state.type == PST_Attacking || state.type == PST_ProjectileAttacking) {
        attackPhase = "active";
    }
    else if (state.type == PST_Recovering) {
        attackPhase = "recovery";
    }
    else {
        attackPhase = "";
    }
    if (attackPhase != prevAtkPhase) {
        playerJson["atkPhase"] = attackPhase;
        prevAtkPhase = attackPhase;
    }
    playerJson["atkFrame"] = state.state_time;

    const char* counterhit_name = player->get_damage_effect_name();
    static const std::unordered_map<std::string, std::string> counterhitMap = {
        {"cmn_counterhit_small", "Small Counterhit"},
        {"cmn_counterhit_middle", "Counterhit"},
        {"cmn_counterhit_large", "Large Counterhit"},
        {"cmn_universehit", "Universe Counterhit"}
    };
    auto it = counterhitMap.find(counterhit_name);
    if (it != counterhitMap.end()) {
        playerJson["counterhit"] = it->second;
    }
}

std::string getCharacterNameFromValue(int value) {
    switch (value) {
    case 0: return "Sol Badguy";
    case 1: return "Ky Kiske";
    case 2: return "May";
    case 3: return "Axl Low";
    case 4: return "Chipp Zanuff";
    case 5: return "Potemkin";
    case 6: return "Faust";
    case 7: return "Millia Rage";
    case 8: return "Zato-1";
    case 9: return "Ramlethal Valentine";
    case 10: return "Leo Whitefang";
    case 11: return "Nagoriyuki";
    case 12: return "Giovanna";
    case 13: return "Anji Mito";
    case 14: return "I-No";
    case 15: return "Goldlewis Dickinson";
    case 16: return "Jack-O'";
    case 17: return "Happy Chaos";
    case 18: return "Baiken";
    case 19: return "Testament";
    case 20: return "Bridget";
    case 21: return "Sin Kiske";
    case 22: return "Bedman?";
    case 23: return "Asuka";
    case 24: return "Johnny";
    case 25: return "Elphelt Valentine";
    case 26: return "A.B.A.";
    case 27: return "Slayer";
    case 28: return "Queen Dizzy";
    case 29: return "Venom";
    case 30: return "Unika";
    case 31: return "Lucy";
    default: return "Unknown value: " + std::to_string(value);
    }
}

void logEvent(const std::string& event) {
    json eventLog = { {"event", event} };
    OutputFile::getInstance().write(eventLog);
}

// Helper function to read memory
uintptr_t readMemory(uintptr_t address) {
    return *reinterpret_cast<uintptr_t*>(address);
}

// Function to resolve the final address by following the pointer chain
uintptr_t resolvePointerChain(uintptr_t baseAddress, const std::vector<uintptr_t>& offsets) {
    uintptr_t currentAddress = baseAddress;
    for (uintptr_t offset : offsets) {
        currentAddress = readMemory(currentAddress) + offset;
    }
    return currentAddress;
}

void initOutputFile() {
    OutputFile::getInstance().clear();
    frameCount = 0;
    identicalFrameCount = 0;
    previousFrame.clear();

    // Log the base address of GGST-Win64-Shipping.exe dynamically using sigscan
    auto basePattern = "\x4D\x5A\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xFF\xFF\x00\x00";
    auto baseMask = "xxxxxxxxxxxxxxxx";
    uintptr_t ggstBaseAddress = sigscan::get().scan(basePattern, baseMask);
    if (ggstBaseAddress == 0) {
        logEvent("Error: GGST base address not found");
        return;
    }

    // Calculate the universal base address
    universalBaseAddress = ggstBaseAddress + 0x050ECC60;

    // Offsets to GameSettings
    std::vector<uintptr_t> gameSettingsOffsets = { 0x188, 0x520, 0x20, 0x1B0 };
    uintptr_t gameSettingsAddress = resolvePointerChain(universalBaseAddress, gameSettingsOffsets);

    // Offsets to Player 1 and Player 2
    uintptr_t player1Address = readMemory(gameSettingsAddress + 0x318);
    uintptr_t player2Address = readMemory(gameSettingsAddress + 0x320);

    // Offset to character name byte within player object
    uintptr_t characterOffset = 0x29;

    // Read the character values as bytes
    uint8_t p1CharacterValue = *reinterpret_cast<uint8_t*>(player1Address + characterOffset);
    uint8_t p2CharacterValue = *reinterpret_cast<uint8_t*>(player2Address + characterOffset);

    // Convert character values to names
    p1CharacterName = getCharacterNameFromValue(static_cast<int>(p1CharacterValue));
    p2CharacterName = getCharacterNameFromValue(static_cast<int>(p2CharacterValue));

    // Log the battle event
    std::string battleEvent = "P1:" + p1CharacterName + " vs P2:" + p2CharacterName;
    logEvent(battleEvent);
}

void outputFrameData(const asw_player* p1, const asw_player* p2, const PlayerState& s1, const PlayerState& s2) {
    static int prevTensionPlayer1 = -1;
    static int prevBurstPlayer1 = -1;
    static int prevRiscPlayer1 = -1;
    static int prevPosXPlayer1 = -1;
    static std::string prevStatePlayer1 = "";
    static std::string prevAtkPhasePlayer1 = "";

    static int prevTensionPlayer2 = -1;
    static int prevBurstPlayer2 = -1;
    static int prevRiscPlayer2 = -1;
    static int prevPosXPlayer2 = -1;
    static std::string prevStatePlayer2 = "";
    static std::string prevAtkPhasePlayer2 = "";

    static int prevComboDmgPlayer1 = 0;
    static int prevComboDmgPlayer2 = 0;

    // Get tension and burst values using consistent memory reading
    std::vector<uintptr_t> tbStateOffsets = { 0x130, 0xBB0, 0x0 };
    uintptr_t tbStateAddress = resolvePointerChain(universalBaseAddress, tbStateOffsets);

    // Directly read the tension and burst values without additional memory reads
    int p1tension = *reinterpret_cast<int*>(tbStateAddress + 0x48);
    int p2tension = *reinterpret_cast<int*>(tbStateAddress + 0x1A8);
    int p1burst = *reinterpret_cast<int*>(tbStateAddress + 0x1448);
    int p2burst = *reinterpret_cast<int*>(tbStateAddress + 0x144C);

    // Variables to track current combo damage
    int currentComboDmgPlayer1 = 0;
    int currentComboDmgPlayer2 = 0;

    // Read combo-related values
    int p1ComboCount = p1->combo_count;
    int p2ComboCount = p2->combo_count;

    // Update current combo damage
    if (p1ComboCount > 0) {
        currentComboDmgPlayer2 = p1->total_combo_damage;  // Player 2 is hitting Player 1
    }
    else if (prevComboDmgPlayer2 != 0) {
        logEvent("P2 combo ended with " + std::to_string(prevComboDmgPlayer2) + " damage");
        prevComboDmgPlayer2 = 0;
    }

    if (p2ComboCount > 0) {
        currentComboDmgPlayer1 = p2->total_combo_damage;  // Player 1 is hitting Player 2
    }
    else if (prevComboDmgPlayer1 != 0) {
        logEvent("P1 combo ended with " + std::to_string(prevComboDmgPlayer1) + " damage");
        prevComboDmgPlayer1 = 0;
    }

    // Update previous combo damage values
    if (p1ComboCount > 0) {
        prevComboDmgPlayer2 = currentComboDmgPlayer2;
    }
    if (p2ComboCount > 0) {
        prevComboDmgPlayer1 = currentComboDmgPlayer1;
    }

    // Sanity check: do not output if the frame number exceeds 10,000
    frameCount++;
    if (frameCount > 10000) {
        return;
    }

    // Write out
    json j;

    addPlayerDataToJson(j[p1CharacterName], p1, s1, p1tension, p1burst, prevTensionPlayer1, prevBurstPlayer1, prevRiscPlayer1, prevPosXPlayer1, prevStatePlayer1, prevAtkPhasePlayer1);
    addPlayerDataToJson(j[p2CharacterName], p2, s2, p2tension, p2burst, prevTensionPlayer2, prevBurstPlayer2, prevRiscPlayer2, prevPosXPlayer2, prevStatePlayer2, prevAtkPhasePlayer2);

    // Add combo fields to the JSON
    if (p1ComboCount > 0) {
        j[p2CharacterName]["combo"] = p1ComboCount;
    }
    if (p2ComboCount > 0) {
        j[p1CharacterName]["combo"] = p2ComboCount;
    }

    // Check for identical frame
    if (previousFrame == j) {
        ++identicalFrameCount;
    }
    else {
        if (identicalFrameCount > 0) {
            logEvent("Omitted " + std::to_string(identicalFrameCount) + " identical frames");
            identicalFrameCount = 0;
        }
        previousFrame = j;
        OutputFile::getInstance().write(j);
    }
}
