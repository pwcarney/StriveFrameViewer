#include "frame_data.h"
#include "action_descriptions.h"
#include "output_file.h"
#include "sigscan.h"
#include <cmath>
#include <fstream>
#include <set>
#include <unordered_set>

using json = nlohmann::json;

static uintptr_t universalBaseAddress;
static int frameCount = 0;
static int identicalFrameCount = 0;
static json previousFrame;

// Previous state variables for both players
static int prevTensionPlayer1 = -1;
static int prevBurstPlayer1 = -1;
static int prevHPPlayer1 = -1;
static int prevRiscPlayer1 = -1;
static int prevPosXPlayer1 = -1;
static std::string prevStatePlayer1 = "";
static std::string prevAtkPhasePlayer1 = "";

static int prevTensionPlayer2 = -1;
static int prevBurstPlayer2 = -1;
static int prevHPPlayer2 = -1;
static int prevRiscPlayer2 = -1;
static int prevPosXPlayer2 = -1;
static std::string prevStatePlayer2 = "";
static std::string prevAtkPhasePlayer2 = "";

// Utility function to reset previous state values
void resetPreviousValues() {
  frameCount = 0;
  identicalFrameCount = 0;

  prevTensionPlayer1 = -1;
  prevBurstPlayer1 = -1;
  prevHPPlayer1 = -1;
  prevRiscPlayer1 = -1;
  prevPosXPlayer1 = -1;
  prevStatePlayer1 = "";
  prevAtkPhasePlayer1 = "";

  prevTensionPlayer2 = -1;
  prevBurstPlayer2 = -1;
  prevHPPlayer2 = -1;
  prevRiscPlayer2 = -1;
  prevPosXPlayer2 = -1;
  prevStatePlayer2 = "";
  prevAtkPhasePlayer2 = "";
}

// Function to log round start and reset previous values
void logRoundStart() {
  resetPreviousValues();
  logEvent("Round Start!");
}

template <typename T>
void addFieldIf(json &j, const std::string &key, const T &value, const T &defaultValue = T()) {
  if (value != defaultValue) {
    j[key] = value;
  }
}

// Specialization for std::string to handle empty string case
template <>
void addFieldIf<std::string>(json &j, const std::string &key, const std::string &value, const std::string &defaultValue) {
  if (!value.empty() && value != defaultValue) {
    j[key] = value;
  }
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
      {PST_End, "End"}};

  auto it = stateToString.find(state);
  if (it != stateToString.end()) {
    return it->second;
  } else {
    return "Unknown";
  }
}

PlayerFrameData getPlayerFrameData(const asw_player *player, const PlayerState &state) {
  PlayerFrameData data;

  data.hp = player->hp;
  data.risc = player->risc;

  // Divide position by 1000 and round to the nearest whole number
  data.positionX = std::round(player->pos_x_from_center / 1000.0);
  data.positionY = std::round(player->pos_y / 1000.0);

  data.currentAction = player->get_BB_state();
  //data.state = state.type;
  //data.hitstun = player->hitstun;
  data.blockstun = player->blockstun;

  // Determine the attack phase and frame number
  if (state.type == PST_Busy) {
    data.attackPhase = "startup";
    data.attackFrame = state.state_time;
  } else if (state.type == PST_Attacking || state.type == PST_ProjectileAttacking) {
    data.attackPhase = "active";
    data.attackFrame = state.state_time;
  } else if (state.type == PST_Recovering) {
    data.attackPhase = "recovery";
    data.attackFrame = state.state_time;
  } else {
    data.attackPhase = "";
    data.attackFrame = 0;
  }

  return data;
}

std::string getCharacterNameFromValue(int value) {
  switch (value) {
  case 0:
    return "Sol Badguy";
  case 1:
    return "Ky Kiske";
  case 2:
    return "May";
  case 3:
    return "Axl Low";
  case 4:
    return "Chipp Zanuff";
  case 5:
    return "Potemkin";
  case 6:
    return "Faust";
  case 7:
    return "Millia Rage";
  case 8:
    return "Zato-1";
  case 9:
    return "Ramlethal Valentine";
  case 10:
    return "Leo Whitefang";
  case 11:
    return "Nagoriyuki";
  case 12:
    return "Giovanna";
  case 13:
    return "Anji Mito";
  case 14:
    return "I-No";
  case 15:
    return "Goldlewis Dickinson";
  case 16:
    return "Jack-O'";
  case 17:
    return "Happy Chaos";
  case 18:
    return "Baiken";
  case 19:
    return "Testament";
  case 20:
    return "Bridget";
  case 21:
    return "Sin Kiske";
  case 22:
    return "Bedman?";
  case 23:
    return "Asuka";
  case 24:
    return "Johnny";
  case 25:
    return "Elphelt Valentine";
  case 26:
    return "A.B.A.";
  case 27:
    return "Slayer";
  case 28:
    return "Queen Dizzy";
  case 29:
    return "Venom";
  case 30:
    return "Unika";
  case 31:
    return "Lucy";
  default:
    return "Unknown value: " + std::to_string(value);
  }
}

void addPlayerDataToJson(json &j, const std::string &playerKey, const PlayerFrameData &playerData, int tension, int burst, int &prevTension, int &prevBurst, int &prevHP, int &prevRisc, int &prevPosX, std::string &prevState, std::string &prevAtkPhase) {
  json playerJson;

  if (playerData.hp != prevHP) {
    playerJson["hp"] = playerData.hp;
    prevHP = playerData.hp;
  }

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

  addFieldIf(playerJson, "risc", playerData.risc, prevRisc);
  prevRisc = playerData.risc;

  if (playerData.positionX != prevPosX) {
    playerJson["posX"] = playerData.positionX;
    prevPosX = playerData.positionX;
  }

  addFieldIf(playerJson, "posY", playerData.positionY);

  addFieldIf(playerJson, "action", playerData.currentAction);
  
  /* if (playerStateTypeToString(playerData.state) != prevState) {
    playerJson["state"] = playerStateTypeToString(playerData.state);
    prevState = playerStateTypeToString(playerData.state);
  }*/

  // Hitstun is kind of coded weird, omitted for now
  //addFieldIf(playerJson, "hitstun", playerData.hitstun, 0);

  addFieldIf(playerJson, "blkstun", playerData.blockstun, 0);
  if (playerData.attackPhase != prevAtkPhase) {
    playerJson["atkPhase"] = playerData.attackPhase;
    prevAtkPhase = playerData.attackPhase;
  }
  addFieldIf(playerJson, "atkFrame", playerData.attackFrame, 0);

  j[playerKey] = playerJson;
}

void logEvent(const std::string &event) {
  json eventLog = {
      {"frameInd", frameCount},
      {"event", event}};

  OutputFile::getInstance().write(eventLog);
}

// Helper function to read memory
uintptr_t readMemory(uintptr_t address) {
  return *reinterpret_cast<uintptr_t *>(address);
}

// Function to resolve the final address by following the pointer chain
uintptr_t resolvePointerChain(uintptr_t baseAddress, const std::vector<uintptr_t> &offsets) {
  uintptr_t currentAddress = baseAddress;
  for (uintptr_t offset : offsets) {
    currentAddress = readMemory(currentAddress) + offset;
  }
  return currentAddress;
}

void initOutputFile() {
  OutputFile::getInstance().clear();
  frameCount = 0;          // Reset frame count for new battle
  identicalFrameCount = 0; // Reset identical frame count
  previousFrame.clear();   // Clear previous frame for new battle

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
  std::vector<uintptr_t> gameSettingsOffsets = {0x188, 0x520, 0x20, 0x1B0};
  uintptr_t gameSettingsAddress = resolvePointerChain(universalBaseAddress, gameSettingsOffsets);

  // Offsets to Player 1 and Player 2
  uintptr_t player1Address = readMemory(gameSettingsAddress + 0x318);
  uintptr_t player2Address = readMemory(gameSettingsAddress + 0x320);

  // Offset to character name int within player object
  uintptr_t characterOffset = 0x29;

  // Read the character values
  int p1CharacterValue = *reinterpret_cast<int *>(player1Address + characterOffset);
  int p2CharacterValue = *reinterpret_cast<int *>(player2Address + characterOffset);

  // Convert character values to names
  std::string p1CharacterName = getCharacterNameFromValue(p1CharacterValue);
  std::string p2CharacterName = getCharacterNameFromValue(p2CharacterValue);

  // Log the battle event
  std::string battleEvent = "P1:" + p1CharacterName + " vs P2:" + p2CharacterName;
  logEvent(battleEvent);
}

void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2) {
  static int prevTensionPlayer1 = -1;
  static int prevBurstPlayer1 = -1;
  static int prevHPPlayer1 = p1->hp;
  static int prevRiscPlayer1 = -1;
  static int prevPosXPlayer1 = -1;
  static std::string prevStatePlayer1 = "";
  static std::string prevAtkPhasePlayer1 = "";

  static int prevTensionPlayer2 = -1;
  static int prevBurstPlayer2 = -1;
  static int prevHPPlayer2 = p2->hp;
  static int prevRiscPlayer2 = -1;
  static int prevPosXPlayer2 = -1;
  static std::string prevStatePlayer2 = "";
  static std::string prevAtkPhasePlayer2 = "";

  PlayerFrameData player1 = getPlayerFrameData(p1, s1);
  PlayerFrameData player2 = getPlayerFrameData(p2, s2);

  // Get tension and burst values using consistent memory reading
  std::vector<uintptr_t> tbStateOffsets = {0x130, 0xBB0, 0x0};
  uintptr_t tbStateAddress = resolvePointerChain(universalBaseAddress, tbStateOffsets);

  // Directly read the tension and burst values without additional memory reads
  int p1tension = *reinterpret_cast<int *>(tbStateAddress + 0x48);
  int p2tension = *reinterpret_cast<int *>(tbStateAddress + 0x1A8);
  int p1burst = *reinterpret_cast<int *>(tbStateAddress + 0x1448);
  int p2burst = *reinterpret_cast<int *>(tbStateAddress + 0x144C);

  // Detect HP change (hit events)
  if (player1.hp < prevHPPlayer1) {
    int hpLoss = prevHPPlayer1 - player1.hp;
    logEvent("Player1 hit and lost " + std::to_string(hpLoss) + " hp");
  }
  if (player2.hp < prevHPPlayer2) {
    int hpLoss = prevHPPlayer2 - player2.hp;
    logEvent("Player2 hit and lost " + std::to_string(hpLoss) + " hp");
  }
  prevHPPlayer1 = player1.hp;
  prevHPPlayer2 = player2.hp;

  // Sanity check: do not output if the frame number exceeds 10,000
  frameCount++;
  if (frameCount > 10000) {
    return;
  }

  // Write out
  FrameData frameData;
  frameData.frameNumber = frameCount;
  frameData.player1 = player1;
  frameData.player2 = player2;

  json j;
  addPlayerDataToJson(j, "p1", frameData.player1, p1tension, p1burst, prevTensionPlayer1, prevBurstPlayer1, prevHPPlayer1, prevRiscPlayer1, prevPosXPlayer1, prevStatePlayer1, prevAtkPhasePlayer1);
  addPlayerDataToJson(j, "p2", frameData.player2, p2tension, p2burst, prevTensionPlayer2, prevBurstPlayer2, prevHPPlayer2, prevRiscPlayer2, prevPosXPlayer2, prevStatePlayer2, prevAtkPhasePlayer2);

  // Check for identical frame
  if (previousFrame == j) {
    ++identicalFrameCount;
  } else {
    if (identicalFrameCount > 0) {
      logEvent("Omitted " + std::to_string(identicalFrameCount) + " identical frames");
      identicalFrameCount = 0;
    }
    previousFrame = j;
    OutputFile::getInstance().write(j);
  }
}