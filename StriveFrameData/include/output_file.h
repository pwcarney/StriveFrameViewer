#pragma once

#include <fstream>
#include <json.hpp>

class OutputFile {
public:
    static OutputFile& getInstance() {
        static OutputFile instance;
        return instance;
    }

    void write(const nlohmann::json& j);
    void clear();

private:
    std::ofstream outFile;

    OutputFile(); // Private constructor

    // Delete copy constructor and assignment operator to prevent copying
    OutputFile(const OutputFile&) = delete;
    void operator=(const OutputFile&) = delete;
};
