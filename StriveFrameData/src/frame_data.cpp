#include "frame_data.h"
#include "output_file.h"
#include "action_descriptions.h"
#include "sigscan.h"
#include <cmath>
#include <fstream>
#include <set>
#include <unordered_set>

using json = nlohmann::json;

static std::unordered_set<std::string> uniqueActions;

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

  data.positionX = player->get_pos_x();
  data.positionY = player->get_pos_y();
  data.currentAction = player->get_BB_state();
  data.state = state.type;
  data.hitstun = player->hitstun;
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

  // Check for special move
  MoveData *currentMove = player->get_current_move();
  if (currentMove != nullptr) {
    data.currentAction = currentMove->get_name();
  }

  return data;
}

std::string getCharacterNameFromValue(int value) {
  switch (value) {
  case 1:
    return "Ky Kiske";
  case 27:
    return "Slayer";
  default:
    return "Unknown";
  }
}

double calculateDistance(double x1, double y1, double x2, double y2) {
  return std::sqrt(std::pow(x2 - x1, 2) + std::pow(y2 - y1, 2));
}

void addPlayerDataToJson(json &j, const std::string &playerKey, const PlayerFrameData &playerData, int tension, int burst) {
  json playerJson;
  addFieldIf(playerJson, "hp", playerData.hp);
  addFieldIf(playerJson, "tension", tension);
  addFieldIf(playerJson, "burst", burst);
  addFieldIf(playerJson, "risc", playerData.risc, 0);
  addFieldIf(playerJson, "positionX", playerData.positionX);
  addFieldIf(playerJson, "positionY", playerData.positionY);
  addFieldIf(playerJson, "currentAction", playerData.currentAction);
  addFieldIf(playerJson, "state", playerStateTypeToString(playerData.state), std::string{""});
  addFieldIf(playerJson, "hitstun", playerData.hitstun, 0);
  addFieldIf(playerJson, "blockstun", playerData.blockstun, 0);
  addFieldIf(playerJson, "attackPhase", playerData.attackPhase, std::string{""});
  addFieldIf(playerJson, "attackFrame", playerData.attackFrame, 0);

  j[playerKey] = playerJson;
}

bool shouldOutput(const PlayerFrameData &player1, const PlayerFrameData &player2, std::string &reason) {
    // Exclude certain actions from output
    static const std::set<std::string> excludedActions = {
        "WSB_Master_Wait", "WSB_Master_Slide", "WSB_Slave_Slide"};

    // Exclude wallbreak animation
    if (excludedActions.count(player1.currentAction) > 0 || excludedActions.count(player2.currentAction) > 0) {
    reason = "Wallbreak situation";
    return false;
    }

    return true;
}

void logEvent(const std::string &event, const nlohmann::json &details) {
  static int frameCount = 0;
  int frameNumber = ++frameCount;

  json eventLog = {
      {"gameFrameIndex", frameNumber},
      {"event", event}};

  if (!details.empty()) {
    eventLog["details"] = details;
  }

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
  static int frameCount = 0;
  frameCount = 0;

  // Log the base address of GGST-Win64-Shipping.exe dynamically using sigscan
  auto basePattern = "\x4D\x5A\x90\x00\x03\x00\x00\x00\x04\x00\x00\x00\xFF\xFF\x00\x00";
  auto baseMask = "xxxxxxxxxxxxxxxx";
  uintptr_t ggstBaseAddress = sigscan::get().scan(basePattern, baseMask);
  if (ggstBaseAddress == 0) {
    logEvent("Error", {{"message", "GGST base address not found"}});
    return;
  }

  // Calculate the universal base address
  static uintptr_t universalBaseAddress = ggstBaseAddress + 0x050ECC60;

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
  std::string battleEvent = "Battle: " + p1CharacterName + " vs " + p2CharacterName;
  logEvent(battleEvent, {});
}

void logSpecificEvent(const std::string &reason, const PlayerFrameData &player1, const PlayerFrameData &player2) {
  std::string eventDescription = reason;
  if (reason == "Wallbreak situation" && player2.currentAction == "CmnActBDownLoop") {
    eventDescription += " with a hard knockdown";
  }
  eventDescription += ".";

  json eventDetails = {
      {"player1Action", player1.currentAction},
      {"player2Action", player2.currentAction}};

  logEvent(eventDescription, eventDetails);
}

void outputUniqueActions() {
  auto actionDescriptions = initializeActionDescriptions();
  json j;
  for (const auto &action : uniqueActions) {
    std::string description = "MISSING ACTION DESCRIPTION";
    auto it = actionDescriptions.find(action);
    if (it != actionDescriptions.end()) {
      description = it->second;
    }
    j[action] = description;
  }
  OutputFile::getInstance().write(j);
}

void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2) {
  static int previousHPPlayer1 = p1->hp;
  static int previousHPPlayer2 = p2->hp;

  PlayerFrameData player1 = getPlayerFrameData(p1, s1);
  PlayerFrameData player2 = getPlayerFrameData(p2, s2);

  // Log unique actions
  uniqueActions.insert(player1.currentAction);
  uniqueActions.insert(player2.currentAction);

  std::string reason;
  if (!shouldOutput(player1, player2, reason)) {
    logSpecificEvent(reason, player1, player2);
    return;
  }

  // Get tension and burst values
  static uintptr_t universalBaseAddress;  // defined in init
  std::vector<uintptr_t> tbStateOffsets = {0x130, 0xBB0};
  uintptr_t tbStateAddress = resolvePointerChain(universalBaseAddress, tbStateOffsets);

  // Offset values from CheatEngine
  int p1tension = *reinterpret_cast<int *>(readMemory(tbStateAddress + 0x48));
  int p2tension = *reinterpret_cast<int *>(readMemory(tbStateAddress + 0x1A8));
  int p1burst = *reinterpret_cast<int *>(readMemory(tbStateAddress + 0x1448));
  int p2burst = *reinterpret_cast<int *>(readMemory(tbStateAddress + 0x144C));

  // Detect HP change (hit events)
  if (player1.hp < previousHPPlayer1) {
    int hpLoss = previousHPPlayer1 - player1.hp;
    logEvent("Player1 hit and lost " + std::to_string(hpLoss) + " hp");
  }
  if (player2.hp < previousHPPlayer2) {
    int hpLoss = previousHPPlayer2 - player2.hp;
    logEvent("Player2 hit and lost " + std::to_string(hpLoss) + " hp");
  }
  previousHPPlayer1 = player1.hp;
  previousHPPlayer2 = player2.hp;

  FrameData frameData;
  static int frameCount = 0;
  frameData.frameNumber = ++frameCount;
  frameData.player1 = player1;
  frameData.player2 = player2;

  double distance = calculateDistance(frameData.player1.positionX, frameData.player1.positionY, frameData.player2.positionX, frameData.player2.positionY);

  json j;
  j["gameFrameIndex"] = frameData.frameNumber;
  addPlayerDataToJson(j, "player1", frameData.player1, p1tension, p1burst);
  addPlayerDataToJson(j, "player2", frameData.player2, p2tension, p2burst);
  j["distance"] = distance;

  OutputFile::getInstance().write(j);
}
