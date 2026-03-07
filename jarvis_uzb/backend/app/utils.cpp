#include "utils.h"
#include <cstdlib>
#include <string>
#include <regex>

void showNotification(const std::string& title, const std::string& message) {
    // Xavfsizlik uchun qo'shtirnoqlarni escape qilamiz
    std::string safe_title = std::regex_replace(title, std::regex("\""), "\\\"");
    std::string safe_message = std::regex_replace(message, std::regex("\""), "\\\"");
    
    // Linux notify-send buyrug'i
    std::string cmd = "notify-send \"" + safe_title + "\" \"" + safe_message + "\" -i dialog-information";
    
    // Tizim buyrug'ini bajarish
    system(cmd.c_str());
}