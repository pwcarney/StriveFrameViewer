#pragma once

#include "framebar_p.h"
#include <string>
#include <json.hpp>

struct PlayerFrameData {
  int hp;
  int risc;
  int burst;

  int positionX;
  int positionY;

  std::string currentAction;
  PlayerStateType state;

  int hitstun;
  int blockstun;

  std::string attackPhase;
  int attackFrame;

  int counterhitLevel;

  int combo;
  int combo_damage;
};

struct FrameData {
  int frameNumber;
  PlayerFrameData player1;
  PlayerFrameData player2;
  double distance;
};

void initOutputFile();
void logRoundStart();
void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2);
void outputUniqueActions();
void logEvent(const std::string &event);
