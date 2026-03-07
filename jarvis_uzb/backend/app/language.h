#ifndef LANGUAGE_H
#define LANGUAGE_H
#include <string>
#include <map>

extern std::map<std::string, std::string> LANG;
void loadLanguage(const std::string& code);

#endif