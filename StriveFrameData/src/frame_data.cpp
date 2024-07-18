#include "frame_data.h"
#include <fstream>

using json = nlohmann::json;

double safeStringToDouble(const char *str) {
  try {
    return std::stod(str);
  } catch (const std::exception &) {
    return 0.0;
  }
}

PlayerFrameData getPlayerFrameData(const asw_player *player, const PlayerState &state) {
  PlayerFrameData data;

  data.hp = safeStringToDouble(player->move_datas.moves[77].get_name());
  data.meter = safeStringToDouble(player->move_datas.moves[109].get_name());
  data.risc = safeStringToDouble(player->move_datas.moves[258].get_name());

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

void outputFrameData(const asw_player *p1, const asw_player *p2, const PlayerState &s1, const PlayerState &s2) {

    static int frameCount = 0;
    static std::ofstream outFile("frame_data.json", std::ios::app);

    FrameData frameData;
    frameData.frameNumber = ++frameCount;
    frameData.player1 = getPlayerFrameData(p1, s1);
    frameData.player2 = getPlayerFrameData(p2, s2);

    json j = {
        {"frameNumber", frameData.frameNumber},
        {"player1", {
            {"hp", frameData.player1.hp},
            {"meter", frameData.player1.meter},
            {"risc", frameData.player1.risc},
            {"positionX", frameData.player1.positionX},
            {"positionY", frameData.player1.positionY},
            {"currentAction", frameData.player1.currentAction},
            {"isAttacking", frameData.player1.isAttacking},
            {"isBlocking", frameData.player1.isBlocking},
            {"isJumping", frameData.player1.isJumping},
            {"hitstun", frameData.player1.hitstun},
            {"blockstun", frameData.player1.blockstun},
            {"isProjectileActive", frameData.player1.isProjectileActive}
        }},
        {"player2", {
            {"hp", frameData.player2.hp},
            {"meter", frameData.player2.meter},
            {"risc", frameData.player2.risc},
            {"positionX", frameData.player2.positionX},
            {"positionY", frameData.player2.positionY},
            {"currentAction", frameData.player2.currentAction},
            {"isAttacking", frameData.player2.isAttacking},
            {"isBlocking", frameData.player2.isBlocking},
            {"isJumping", frameData.player2.isJumping},
            {"hitstun", frameData.player2.hitstun},
            {"blockstun", frameData.player2.blockstun},
            {"isProjectileActive", frameData.player2.isProjectileActive}
        }}
    };

    outFile << j.dump() << std::endl;
}