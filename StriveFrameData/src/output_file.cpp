#include "output_file.h"
#include <json.hpp>

using json = nlohmann::json;

OutputFile::OutputFile()
: outFile("frame_data.json", std::ios::app) {}

void OutputFile::write(const json &j) {
  outFile << j.dump() << std::endl;
}

void OutputFile::clear() {
  outFile.close();
  outFile.open("frame_data.json", std::ios::trunc);
}
