#include "regex_commands.h"
#include "chatgpt.h"
#include "language.h"
#include "utils.h"
#include <iostream>
#include <string>
#include <vector>
#include <regex>
#include <ctime>
#include <cstdlib>

// Tizim buyruqlarini bajarish uchun yordamchi funksiya
void runSystemCommand(const std::string& cmd) {
    // Outputni yashirish uchun > /dev/null qo'shamiz
    system(cmd.c_str());
}

void handleRegexCommand(const std::string& input) {
    std::string cmd = input; // Nusxa olish
    std::smatch matches;
    
    // 1. Vaqt
    if (std::regex_search(cmd, std::regex("(vaqt|soat|hozir)", std::regex_constants::icase))) {
        time_t t = time(nullptr);
        char buf[100];
        strftime(buf, sizeof(buf), "%H:%M", localtime(&t));
        std::string msg = (LANG.count("time") ? LANG["time"] : "Vaqt") + std::string(": ") + buf;
        std::cout << "Jarvis: " << msg << std::endl;
        showNotification("Jarvis", msg);
    }
    // 2. Sana
    else if (std::regex_search(cmd, std::regex("(sana|bugun|kun)", std::regex_constants::icase))) {
        time_t t = time(nullptr);
        char buf[100];
        strftime(buf, sizeof(buf), "%d-%B, %Y", localtime(&t));
        std::string msg = (LANG.count("date") ? LANG["date"] : "Sana") + std::string(": ") + buf;
        std::cout << "Jarvis: " << msg << std::endl;
        showNotification("Jarvis", msg);
    }
    // 3. Chrome / Brauzer
    else if (std::regex_search(cmd, std::regex("(chrome|google|brauzer).*och", std::regex_constants::icase))) {
        std::string msg = (LANG.count("open") ? LANG["open"] : "Ochilyapti...") + std::string(" Chrome");
        std::cout << "Jarvis: " << msg << "\n";
        showNotification("Jarvis", msg);
        system("xdg-open https://google.com > /dev/null 2>&1 &");
    }
    // 4. Chiqish
    else if (std::regex_search(cmd, std::regex("(chiq|to'xta|yop|exit)", std::regex_constants::icase))) {
        std::cout << "Jarvis: " << (LANG.count("exit") ? LANG["exit"] : "Xayr!") << "\n";
        showNotification("Jarvis", (LANG.count("exit") ? LANG["exit"] : "Xayr!"));
        exit(0);
    }   
    
    // --- TIZIM BOSHQARUVI (REAL COMMANDS) ---

    // 5. Ovozni foizga qo'yish (Masalan: "ovozni 50 ga qo'y")
    else if (std::regex_search(cmd, matches, std::regex("(ovoz|musiqa|tovush).*?(\\d+)", std::regex_constants::icase))) {
        std::string level = matches[2];
        // Linux (PulseAudio/Alsa) uchun
        runSystemCommand("amixer -D pulse sset Master " + level + "% > /dev/null 2>&1");
        
        std::string msg = "Ovoz balandligi " + level + "% ga o'rnatildi.";
        std::cout << "Jarvis: " << msg << std::endl;
        showNotification("Jarvis", msg);
    }
    // 6. Ovozni ko'tarish/pasaytirish
    else if (std::regex_search(cmd, std::regex("(ovoz|musiqa).*?(oshir|ko'tar|balandlat)", std::regex_constants::icase))) {
        runSystemCommand("amixer -D pulse sset Master 10%+ > /dev/null 2>&1");
        std::cout << "Jarvis: Ovoz ko'tarildi (+10%)" << std::endl;
    }
    else if (std::regex_search(cmd, std::regex("(ovoz|musiqa).*?(pasaytir|tushir|kamaytir)", std::regex_constants::icase))) {
        runSystemCommand("amixer -D pulse sset Master 10%- > /dev/null 2>&1");
        std::cout << "Jarvis: Ovoz pasaytirildi (-10%)" << std::endl;
    }

    // 7. Ekran yorug'ligi (Masalan: "yorug'likni 70 ga qo'y")
    else if (std::regex_search(cmd, matches, std::regex("(yorug'lik|ekran|yarkost).*?(\\d+)", std::regex_constants::icase))) {
        std::string levelStr = matches[2];
        int level = std::stoi(levelStr);
        float brightness = level / 100.0f;
        if (brightness > 1.0) brightness = 1.0;
        if (brightness < 0.1) brightness = 0.1; // Qop-qora bo'lib qolmasligi uchun

        // Xrandr orqali birinchi ulangan monitorni topib yorug'ligini o'zgartiramiz
        std::string sysCmd = "xrandr --output $(xrandr | grep ' connected' | cut -d' ' -f1 | head -n 1) --brightness " + std::to_string(brightness) + " > /dev/null 2>&1";
        runSystemCommand(sysCmd);

        std::string msg = "Ekran yorug'ligi " + levelStr + "% ga o'rnatildi.";
        std::cout << "Jarvis: " << msg << std::endl;
        showNotification("Jarvis", msg);
    }

    // 8. Tizimni o'chirish / Restart
    else if (std::regex_search(cmd, std::regex("(kompyuter|tizim).*?(o'chir|sondir|shutdown)", std::regex_constants::icase))) {
        std::cout << "Jarvis: Kompyuter o'chirilmoqda..." << std::endl;
        showNotification("Jarvis", "Kompyuter o'chirilmoqda...");
        runSystemCommand("shutdown now"); // Root huquqi yoki to'g'ri sozlangan bo'lishi kerak
    }
    else if (std::regex_search(cmd, std::regex("(kompyuter|tizim).*?(qayta|restart|perezagruzka)", std::regex_constants::icase))) {
        std::cout << "Jarvis: Tizim qayta yuklanmoqda..." << std::endl;
        showNotification("Jarvis", "Tizim qayta yuklanmoqda...");
        runSystemCommand("reboot");
    }

    // 9. Skrinshot
    else if (std::regex_search(cmd, std::regex("(skrinshot|rasmga ol|screenshot)", std::regex_constants::icase))) {
        std::cout << "Jarvis: Skrinshot olinmoqda..." << std::endl;
        runSystemCommand("gnome-screenshot || scrot || import window root screenshot.png"); 
        showNotification("Jarvis", "Skrinshot olindi");
    }

    // 10. Musiqa qo'yish (Aniq qo'shiq - YouTube)
    else if (std::regex_search(cmd, matches, std::regex("musiqa qo'?y (.+)", std::regex_constants::icase))) {
        std::string song = matches[1];
        // URL uchun bo'shliqlarni + ga almashtirish
        std::string query = std::regex_replace(song, std::regex(" "), "+");
        std::string url = "https://www.youtube.com/results?search_query=" + query;

        std::string msg = "YouTube'da qidirilmoqda: " + song;
        std::cout << "Jarvis: " << msg << "\n";
        showNotification("Jarvis", msg);

        // Linux uchun (Windows uchun: start "" "URL")
        runSystemCommand("xdg-open \"" + url + "\" > /dev/null 2>&1 &");
    }
    // 11. Musiqa pleer (Umumiy - Lokal)
    else if (std::regex_search(cmd, std::regex("musiqa qo'?y$", std::regex_constants::icase))) {
        std::string msg = "Musiqa pleer ishga tushmoqda...";
        std::cout << "Jarvis: " << msg << "\n";
        showNotification("Jarvis", msg);

        // Linux uchun (Rhythmbox yoki VLC)
        runSystemCommand("rhythmbox-client --play || rhythmbox || vlc > /dev/null 2>&1 &");
    }
    
    // 12. AI Fallback (Agar hech qaysi buyruq tushmasa)
    else {
        std::string response = askChatGPT(cmd);
        std::cout << "Jarvis (AI): " << response << std::endl;
        showNotification("Jarvis AI", response);
    }
}