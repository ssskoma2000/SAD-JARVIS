#include "chatgpt.h"
#include <curl/curl.h>
#include <cstdlib>
#include <iostream>
#include <regex>

// Curl javobini yozib olish uchun callback
static size_t writeCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

// Oddiy JSON parser (faqat content qismini olish uchun)
std::string extractContent(const std::string& json) {
    std::regex content_regex(R"("content":\s*"((?:[^"\\]|\\.)*))");
    std::smatch match;
    if (std::regex_search(json, match, content_regex)) {
        std::string result = match[1].str();
        // Unicode va escape belgilarni tozalash (soddalashtirilgan)
        result = std::regex_replace(result, std::regex(R"(\\n)"), "\n");
        result = std::regex_replace(result, std::regex(R"(\\")"), "\"");
        return result;
    }
    return json; // Agar parse qila olmasa, hammasini qaytaradi
}

std::string askChatGPT(const std::string& prompt) {
    CURL* curl = curl_easy_init();
    std::string response;

    const char* apiKey = getenv("OPENAI_API_KEY");
    if (!apiKey) return "Xatolik: OPENAI_API_KEY topilmadi. .env faylni tekshiring.";

    // JSON body tayyorlash (escape qilish kerak bo'lsa, murakkabroq logika kerak bo'ladi)
    // Hozircha oddiy matnlar uchun ishlaydi.
    std::string safe_prompt = prompt; 
    // Qo'shtirnoqlarni escape qilish
    safe_prompt = std::regex_replace(safe_prompt, std::regex("\""), "\\\"");

    std::string data =
        "{ \"model\": \"gpt-4o-mini\", \"messages\": ["
        "{ \"role\": \"system\", \"content\": \"Sen Jarvis ismli aqlli yordamchisan. Javoblarni qisqa va lo'nda qil.\" },"
        "{ \"role\": \"user\", \"content\": \"" + safe_prompt + "\" } ] }";

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, (std::string("Authorization: Bearer ") + apiKey).c_str());

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "https://api.openai.com/v1/chat/completions");
        curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, writeCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        CURLcode res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            response = "Internet xatoligi: " + std::string(curl_easy_strerror(res));
        }
        
        curl_easy_cleanup(curl);
        curl_slist_free_all(headers);
    } else {
        return "Curl init failed";
    }

    return extractContent(response);
}