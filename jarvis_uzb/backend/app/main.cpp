#include <iostream>
#include <string>
#include "language.h"
#include "regex_commands.h"
#include "utils.h"

int main(int argc, char* argv[]) {
    // Tilni aniqlash (default: uz)
    std::string langCode = "uz";
    std::string singleCommand = "";
    int argStart = 1;

    // Argumentlarni tekshirish
    if (argc > 1) {
        std::string arg1 = argv[1];
        // Agar birinchi argument til kodi bo'lsa
        if (arg1 == "uz" || arg1 == "en" || arg1 == "ru") {
            langCode = arg1;
            argStart = 2;
        }
    }

    // Qolgan argumentlarni yagona buyruq sifatida yig'ish
    for (int i = argStart; i < argc; ++i) {
        singleCommand += argv[i];
        if (i < argc - 1) singleCommand += " ";
    }

    loadLanguage(langCode);

    // Agar CLI orqali buyruq berilgan bo'lsa, uni bajarib chiqib ketamiz
    if (!singleCommand.empty()) {
        handleRegexCommand(singleCommand);
        return 0;
    }

    // --- Interaktiv Rejim (Terminal) ---
    std::string greeting = (LANG.count("greeting") ? LANG["greeting"] : "Ishga tushdi");
    std::cout << "----------------------------------------\n";
    std::cout << "JARVIS (" << langCode << ") - " << greeting << "\n";
    std::cout << "----------------------------------------\n";
    showNotification("Jarvis", greeting);

    while (true) {
        std::cout << "> ";
        std::string input;
        if (!std::getline(std::cin, input)) break; // EOF check
        
        if (input.empty()) continue;
        
        handleRegexCommand(input);
    }
    return 0;
}