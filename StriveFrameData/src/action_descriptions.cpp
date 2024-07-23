#include "action_descriptions.h"


// Initialize the actionDescriptions map
std::unordered_map<std::string, std::string> initializeActionDescriptions() {
  std::unordered_map<std::string, std::string> actionDescriptions;
  actionDescriptions["CmnActStand"] = "Stand";
  actionDescriptions["CmnActStandTurn"] = "Stand Turn";
  actionDescriptions["CmnActStand2Crouch"] = "Stand to Crouch";
  // Add more action descriptions here
  return actionDescriptions;
}
