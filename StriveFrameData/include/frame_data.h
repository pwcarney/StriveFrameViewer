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
    bool isAttacking;
    bool isBlocking;
    bool isJumping;
    int hitstun;
    int blockstun;
    bool isProjectileActive;
};

struct FrameData {
    int frameNumber;
    PlayerFrameData player1;
    PlayerFrameData player2;
};

PlayerFrameData getPlayerFrameData(const asw_player* player, const PlayerState& state);
void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2, AREDGameState_Battle *gameState);
