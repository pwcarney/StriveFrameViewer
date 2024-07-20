#pragma once

#include "framebar_p.h"
#include <string>
#include <json.hpp>

struct PlayerFrameData {
  int hp;
  int risc;
  int positionX;
  int positionY;
  std::string currentAction;
  PlayerStateType state;
  int hitstun;
  int blockstun;
};

struct FrameData {
  int frameNumber;
  PlayerFrameData player1;
  PlayerFrameData player2;
  double distance;
};

PlayerFrameData getPlayerFrameData(const asw_player *player, const PlayerState &state);
double calculateDistance(double x1, double y1, double x2, double y2);
void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2, AREDGameState_Battle *gameState);
void logEvent(const std::string &event, const nlohmann::json &details = nlohmann::json());
