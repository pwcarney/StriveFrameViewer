#pragma once

#include "common.h"
#include "arcsys.h"


class FrameBar {
  PIMPL

public:
  ~FrameBar();
  FrameBar();
  void addFrame();
  void reset();
  void draw();
};