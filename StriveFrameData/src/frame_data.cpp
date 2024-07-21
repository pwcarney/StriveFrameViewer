#include "frame_data.h"
#include "output_file.h"
#include <cmath>
#include <fstream>
#include <set>

using json = nlohmann::json;

template <typename T>
void addFieldIf(json &j, const std::string &key, const T &value, const T &defaultValue = T()) {
  if (value != defaultValue) {
    j[key] = value;
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

  return data;
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
  addFieldIf(playerJson, "positionY", playerData.positionY, 0);
  addFieldIf(playerJson, "currentAction", playerData.currentAction);
  addFieldIf(playerJson, "state", playerData.state);
  addFieldIf(playerJson, "hitstun", playerData.hitstun, 0);
  addFieldIf(playerJson, "blockstun", playerData.blockstun, 0);

  j[playerKey] = playerJson;
}

bool shouldOutput(const PlayerFrameData &player1, const PlayerFrameData &player2, std::string &reason) {
  static const std::set<std::string> excludedActions = {
      "WSB_Master_Wait", "WSB_Master_Slide", "WSB_Slave_Slide"};

  if (excludedActions.count(player1.currentAction) > 0 || excludedActions.count(player2.currentAction) > 0) {
    reason = "Wallbreak situation";
    return false;
  }

  // Add more conditions here if needed in the future
  // if (some_other_condition) {
  //   reason = "Some other reason";
  //   return false;
  // }

  return true;
}

void logEvent(const std::string &event, const nlohmann::json &details) {
  static int frameCount = 0;
  int frameNumber = ++frameCount;

  json eventLog = {
      {"frameNumber", frameNumber},
      {"event", event}};

  if (!details.empty()) {
    eventLog["details"] = details;
  }

  OutputFile::getInstance().write(eventLog);
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

void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2, AREDGameState_Battle *gameState) {
  static int frameCount = 0;

  PlayerFrameData player1 = getPlayerFrameData(p1, s1);
  PlayerFrameData player2 = getPlayerFrameData(p2, s2);

  std::string reason;
  if (!shouldOutput(player1, player2, reason)) {
    logSpecificEvent(reason, player1, player2);
    return;
  }

  FrameData frameData;
  frameData.frameNumber = ++frameCount;
  frameData.player1 = player1;
  frameData.player2 = player2;

  double distance = calculateDistance(frameData.player1.positionX, frameData.player1.positionY, frameData.player2.positionX, frameData.player2.positionY);

  json j;
  j["frameNumber"] = frameData.frameNumber;
  addPlayerDataToJson(j, "player1", frameData.player1, gameState->p1_tension, gameState->p1_burst);
  addPlayerDataToJson(j, "player2", frameData.player2, gameState->p2_tension, gameState->p2_burst);
  j["distance"] = distance;

  OutputFile::getInstance().write(j);
}
