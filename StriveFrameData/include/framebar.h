#pragma once

#include "common.h"
#include "arcsys.h"


class FrameBar {
  PIMPL

public:
  ~FrameBar();
  FrameBar();
  void addFrame(AREDGameState_Battle *gameState);
  void reset();
  void draw();
};