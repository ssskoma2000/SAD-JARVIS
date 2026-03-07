#include "language.h"
#include <fstream>
#include <iostream>

std::map<std::string, std::string> LANG;

void loadLanguage(const std::string& code) {
    std::string path = "languages/" + code + ".txt";
    std::ifstream f(path);
    
    if (!f.is_open()) {
        std::cerr << "Xatolik: " << path << " fayli topilmadi!\n";
        return;
    }

    std::string line;
    while (getline(f, line)) {
        auto p = line.find('=');
        if (p != std::string::npos)
            LANG[line.substr(0, p)] = line.substr(p + 1);
    }
}