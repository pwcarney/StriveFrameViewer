#include "frame_data.h"
#include "output_file.h"
#include "arcsys.h"
#include <cmath>
#include <fstream>
#include <framebar_p.h>

using json = nlohmann::json;

PlayerFrameData getPlayerFrameData(const asw_player *player, const PlayerState &state) {
  PlayerFrameData data;

  data.hp = player->hp;
  data.risc = player->risc;

  data.positionX = player->get_pos_x();
  data.positionY = player->get_pos_y();
  data.currentAction = player->get_BB_state();
  data.isAttacking = (state.type == PST_Attacking || state.type == PST_ProjectileAttacking);
  data.isBlocking = (state.type == PST_BlockStunned);
  data.isJumping = player->airborne;
  data.hitstun = player->hitstun;
  data.blockstun = player->blockstun;
  data.isProjectileActive = state.anyProjectiles();

  return data;
}

double calculateDistance(double x1, double y1, double x2, double y2) {
  return std::sqrt(std::pow(x2 - x1, 2) + std::pow(y2 - y1, 2));
}

void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2, AREDGameState_Battle *gameState) {
  static int frameCount = 0;

  FrameData frameData;
  frameData.frameNumber = ++frameCount;
  frameData.player1 = getPlayerFrameData(p1, s1);
  frameData.player2 = getPlayerFrameData(p2, s2);

  double distance = calculateDistance(frameData.player1.positionX, frameData.player1.positionY, frameData.player2.positionX, frameData.player2.positionY);

  json j = {
      {"frameNumber", frameData.frameNumber},
      {"player1", {{"hp", frameData.player1.hp}, {"tension", gameState->p1_tension}, {"risc", frameData.player1.risc}, {"positionX", frameData.player1.positionX}, {"positionY", frameData.player1.positionY}, {"currentAction", frameData.player1.currentAction}, {"isAttacking", frameData.player1.isAttacking}, {"isBlocking", frameData.player1.isBlocking}, {"isJumping", frameData.player1.isJumping}, {"hitstun", frameData.player1.hitstun}, {"blockstun", frameData.player1.blockstun}, {"isProjectileActive", frameData.player1.isProjectileActive}}},
      {"player2", {{"hp", frameData.player2.hp}, {"tension", gameState->p2_tension}, {"risc", frameData.player2.risc}, {"positionX", frameData.player2.positionX}, {"positionY", frameData.player2.positionY}, {"currentAction", frameData.player2.currentAction}, {"isAttacking", frameData.player2.isAttacking}, {"isBlocking", frameData.player2.isBlocking}, {"isJumping", frameData.player2.isJumping}, {"hitstun", frameData.player2.hitstun}, {"blockstun", frameData.player2.blockstun}, {"isProjectileActive", frameData.player2.isProjectileActive}}},
      {"distance", distance}};

  OutputFile::getInstance().write(j);
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
