#!/usr/bin/env python3
"""Generate 1,207+ Uzbek commands for Jarvis.

Categories:
1. Time & Date (60+)
2. System Control (80+)
3. Media & Entertainment (150+)
4. Internet & Browser (100+)
5. Files & Folders (120+)
6. Communication (90+)
7. Productivity & Reminders (200+)
8. User Chat & Info (400+)

Output: commands.json and commands.csv
"""

import json
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def generate_commands():
    commands = {}
    
    # Category 1: Time & Date (60+)
    time_date_commands = [
        {"pattern": "what time is it", "synonyms": ["tell the time", "current time", "soat nechada", "qanday vaqt"], "intent": "show_time", "action": "show_time"},
        {"pattern": "today's date", "synonyms": ["tell me the date", "current date", "bugun sana", "bugun qaysi kun"], "intent": "show_date", "action": "show_time"},
        {"pattern": "show calendar", "synonyms": ["open calendar", "calendar view", "kalendarni ko'rsat"], "intent": "show_calendar", "action": "open_app", "args": {"app": "calendar"}},
        {"pattern": "what day is today", "synonyms": ["tell me the day", "bugun qaysi kun", "kun nomi"], "intent": "show_day", "action": "show_time"},
        {"pattern": "when is sunrise", "synonyms": ["sunrise time", "quyosh chiqish vaqti"], "intent": "show_sunrise", "action": "search_google", "args": {"query": "sunrise time"}},
        {"pattern": "when is sunset", "synonyms": ["sunset time", "quyosh botish vaqti"], "intent": "show_sunset", "action": "search_google", "args": {"query": "sunset time"}},
        {"pattern": "set alarm for {query}", "synonyms": ["create alarm {query}", "signal set {query}", "orali qo'y {query}"], "intent": "set_alarm", "action": "create_reminder"},
        {"pattern": "set timer {query}", "synonyms": ["timer for {query}", "sanigini qo'y {query}"], "intent": "set_timer", "action": "create_reminder"},
        {"pattern": "how many days until {query}", "synonyms": ["days remaining {query}", "yana nechta kun {query}"], "intent": "count_days", "action": "calculate"},
        {"pattern": "what is the current year", "synonyms": ["this year", "this year number", "yil nechasi"], "intent": "show_year", "action": "show_time"},
    ]
    
    # Category 2: System Control (80+)
    system_commands = [
        {"pattern": "shutdown computer", "synonyms": ["turn off system", "power off", "kompyuterni o'chir", "o'chirish"], "intent": "shutdown", "action": "blocked"},
        {"pattern": "restart computer", "synonyms": ["reboot", "restart system", "qayta yukla"], "intent": "restart", "action": "blocked"},
        {"pattern": "lock screen", "synonyms": ["lock computer", "block screen", "ekranni bloc qil"], "intent": "lock_screen", "action": "blocked"},
        {"pattern": "logout", "synonyms": ["log out", "sign out", "chiqib ket"], "intent": "logout", "action": "blocked"},
        {"pattern": "take screenshot", "synonyms": ["capture screen", "screenshot", "skrinshot olish"], "intent": "screenshot", "action": "screenshot"},
        {"pattern": "open task manager", "synonyms": ["task manager", "processes", "jarayon menejeri"], "intent": "open_task_manager", "action": "open_app"},
        {"pattern": "open settings", "synonyms": ["settings", "system settings", "sozlamalar"], "intent": "open_settings", "action": "open_app"},
        {"pattern": "open control panel", "synonyms": ["control panel", "system control"], "intent": "open_control_panel", "action": "open_app"},
        {"pattern": "check system updates", "synonyms": ["system updates", "check updates", "yangilanish tekshir"], "intent": "check_updates", "action": "open_app"},
        {"pattern": "open disk cleanup", "synonyms": ["disk cleanup", "clean disk", "diskni tozala"], "intent": "disk_cleanup", "action": "open_app"},
    ]
    
    # Category 3: Media & Entertainment (150+)
    media_commands = [
        {"pattern": "play music", "synonyms": ["start music", "play song", "musiqa qo'y", "qo'ymoq"], "intent": "play_music", "action": "play_music"},
        {"pattern": "play {query}", "synonyms": ["play song {query}", "start {query}", "qo'y {query}"], "intent": "play_specific", "action": "play_music"},
        {"pattern": "pause music", "synonyms": ["pause", "stop music", "to'xtat"], "intent": "pause_music", "action": "play_music"},
        {"pattern": "next track", "synonyms": ["skip song", "next song", "keyingi"], "intent": "next_track", "action": "play_music"},
        {"pattern": "previous track", "synonyms": ["prev song", "back track", "oldingi"], "intent": "prev_track", "action": "play_music"},
        {"pattern": "increase volume", "synonyms": ["turn up volume", "louder", "ovozni oshir"], "intent": "volume_up", "action": "set_volume"},
        {"pattern": "decrease volume", "synonyms": ["turn down volume", "quieter", "ovozni kamayt"], "intent": "volume_down", "action": "set_volume"},
        {"pattern": "mute audio", "synonyms": ["mute", "silence", "ovozsiz qil"], "intent": "mute", "action": "set_volume"},
        {"pattern": "unmute audio", "synonyms": ["unmute", "sound on", "ovozni yongi"], "intent": "unmute", "action": "set_volume"},
        {"pattern": "open YouTube", "synonyms": ["youtube", "youtube.com"], "intent": "open_youtube", "action": "open_url", "args": {"url": "https://www.youtube.com"}},
        {"pattern": "search YouTube for {query}", "synonyms": ["youtube search {query}", "youtube {query}"], "intent": "search_youtube", "action": "open_url", "template": "https://www.youtube.com/results?search_query={query}"},
        {"pattern": "open Netflix", "synonyms": ["netflix", "watch netflix"], "intent": "open_netflix", "action": "open_url", "args": {"url": "https://www.netflix.com"}},
        {"pattern": "open Spotify", "synonyms": ["spotify", "music spotify"], "intent": "open_spotify", "action": "open_url", "args": {"url": "https://www.spotify.com"}},
        {"pattern": "open Telegram", "synonyms": ["telegram", "open telegram"], "intent": "open_telegram", "action": "open_app"},
        {"pattern": "open WhatsApp", "synonyms": ["whatsapp", "open whatsapp"], "intent": "open_whatsapp", "action": "open_app"},
    ]
    
    # Category 4: Internet & Browser (100+)
    internet_commands = [
        {"pattern": "open Google", "synonyms": ["google", "google.com", "google ni aç"], "intent": "open_google", "action": "open_url", "args": {"url": "https://www.google.com"}},
        {"pattern": "search Google for {query}", "synonyms": ["google {query}", "search {query}"], "intent": "search_google", "action": "open_url", "template": "https://www.google.com/search?q={query}"},
        {"pattern": "open Gmail", "synonyms": ["gmail", "email"], "intent": "open_gmail", "action": "open_url", "args": {"url": "https://mail.google.com"}},
        {"pattern": "open Wikipedia", "synonyms": ["wikipedia"], "intent": "open_wikipedia", "action": "open_url", "args": {"url": "https://www.wikipedia.org"}},
        {"pattern": "search Wikipedia for {query}", "synonyms": ["wikipedia {query}"], "intent": "search_wikipedia", "action": "open_url", "template": "https://en.wikipedia.org/w/index.php?search={query}"},
        {"pattern": "open Reddit", "synonyms": ["reddit", "reddit.com"], "intent": "open_reddit", "action": "open_url", "args": {"url": "https://www.reddit.com"}},
        {"pattern": "open Stack Overflow", "synonyms": ["stackoverflow", "stack overflow"], "intent": "open_stackoverflow", "action": "open_url", "args": {"url": "https://stackoverflow.com"}},
        {"pattern": "open GitHub", "synonyms": ["github", "github.com"], "intent": "open_github", "action": "open_url", "args": {"url": "https://github.com"}},
        {"pattern": "open Twitter", "synonyms": ["twitter", "x.com"], "intent": "open_twitter", "action": "open_url", "args": {"url": "https://twitter.com"}},
        {"pattern": "open Facebook", "synonyms": ["facebook", "fb"], "intent": "open_facebook", "action": "open_url", "args": {"url": "https://www.facebook.com"}},
    ]
    
    # Category 5: Files & Folders (120+)
    file_commands = [
        {"pattern": "open file explorer", "synonyms": ["file manager", "open files", "fayl menijeri"], "intent": "open_file_explorer", "action": "open_app"},
        {"pattern": "create new file", "synonyms": ["new file", "create file", "fayl yarat"], "intent": "create_file", "action": "create_file"},
        {"pattern": "create new folder", "synonyms": ["new folder", "create folder", "jild yarat"], "intent": "create_folder", "action": "create_folder"},
        {"pattern": "delete file {query}", "synonyms": ["remove file {query}", "fayl o'chir {query}"], "intent": "delete_file", "action": "blocked"},
        {"pattern": "copy file {query}", "synonyms": ["copy {query}"], "intent": "copy_file", "action": "copy_file"},
        {"pattern": "move file {query}", "synonyms": ["move {query}"], "intent": "move_file", "action": "move_file"},
        {"pattern": "rename file {query}", "synonyms": ["rename {query}"], "intent": "rename_file", "action": "rename_file"},
        {"pattern": "open downloads folder", "synonyms": ["downloads", "download folder"], "intent": "open_downloads", "action": "open_app"},
        {"pattern": "open documents folder", "synonyms": ["documents", "my documents"], "intent": "open_documents", "action": "open_app"},
        {"pattern": "open desktop", "synonyms": ["show desktop", "desktop"], "intent": "open_desktop", "action": "open_app"},
    ]
    
    # Category 6: Communication (90+)
    communication_commands = [
        {"pattern": "send email to {query}", "synonyms": ["email {query}", "write email {query}"], "intent": "send_email", "action": "open_app"},
        {"pattern": "open email", "synonyms": ["check email", "email", "pochta"], "intent": "open_email", "action": "open_app"},
        {"pattern": "send message to {query}", "synonyms": ["message {query}"], "intent": "send_message", "action": "open_app"},
        {"pattern": "call {query}", "synonyms": ["call {query}", "ring {query}"], "intent": "call", "action": "blocked"},
        {"pattern": "open messaging app", "synonyms": ["messages", "text messages"], "intent": "open_messaging", "action": "open_app"},
        {"pattern": "open skype", "synonyms": ["skype", "skype call"], "intent": "open_skype", "action": "open_app"},
        {"pattern": "open zoom", "synonyms": ["zoom", "zoom meeting"], "intent": "open_zoom", "action": "open_app"},
        {"pattern": "open discord", "synonyms": ["discord", "discord chat"], "intent": "open_discord", "action": "open_app"},
        {"pattern": "open slack", "synonyms": ["slack", "slack chat"], "intent": "open_slack", "action": "open_app"},
        {"pattern": "open viber", "synonyms": ["viber", "viber call"], "intent": "open_viber", "action": "open_app"},
    ]
    
    # Category 7: Productivity & Reminders (200+)
    productivity_commands = [
        {"pattern": "create reminder {query}", "synonyms": ["set reminder {query}", "remind me {query}", "ozbek-reminder {query}"], "intent": "create_reminder", "action": "create_reminder"},
        {"pattern": "set reminder for {query}", "synonyms": ["remind me in {query}", "notification {query}"], "intent": "set_reminder_time", "action": "create_reminder"},
        {"pattern": "show reminders", "synonyms": ["list reminders", "my reminders"], "intent": "show_reminders", "action": "show_reminders"},
        {"pattern": "delete reminder {query}", "synonyms": ["remove reminder {query}"], "intent": "delete_reminder", "action": "delete_reminder"},
        {"pattern": "open notes", "synonyms": ["notes app", "notepad"], "intent": "open_notes", "action": "open_app"},
        {"pattern": "create note {query}", "synonyms": ["write note {query}", "add note {query}"], "intent": "create_note", "action": "create_note"},
        {"pattern": "open calculator", "synonyms": ["calculator", "calc"], "intent": "open_calculator", "action": "open_app"},
        {"pattern": "calculate {query}", "synonyms": ["math {query}", "solve {query}"], "intent": "calculate", "action": "calculate"},
        {"pattern": "open word processor", "synonyms": ["word", "libreoffice", "document"], "intent": "open_word", "action": "open_app"},
        {"pattern": "open spreadsheet", "synonyms": ["excel", "spreadsheet", "table"], "intent": "open_spreadsheet", "action": "open_app"},
        {"pattern": "open presentation", "synonyms": ["powerpoint", "slides"], "intent": "open_presentation", "action": "open_app"},
        {"pattern": "open to-do list", "synonyms": ["todo", "tasks"], "intent": "open_todo", "action": "open_app"},
        {"pattern": "add task {query}", "synonyms": ["create task {query}"], "intent": "add_task", "action": "create_reminder"},
        {"pattern": "mark task done {query}", "synonyms": ["complete task {query}"], "intent": "mark_task_done", "action": "update_task"},
        {"pattern": "show today's schedule", "synonyms": ["show schedule", "today schedule"], "intent": "show_schedule", "action": "show_reminders"},
    ]
    
    # Category 8: User Chat & Info (400+ - mix of Uzbek & English greetings, Q&A, jokes, etc.)
    chat_commands = [
        # Greetings
        {"pattern": "hello", "synonyms": ["hi", "hey", "salom", "assalomu aleykum", "qanday", "salom jarvis", "hi jarvis"], "intent": "greet", "action": "ai_response"},
        {"pattern": "goodbye", "synonyms": ["bye", "see you", "xayr", "bye bye", "farewell", "see you later"], "intent": "goodbye", "action": "ai_response"},
        {"pattern": "good morning", "synonyms": ["morning", "good morning jarvis", "saboh baxtubaxtliklar"], "intent": "greet_morning", "action": "ai_response"},
        {"pattern": "good evening", "synonyms": ["evening", "good evening jarvis", "kechqurun baxtubaxtliklar"], "intent": "greet_evening", "action": "ai_response"},
        {"pattern": "good night", "synonyms": ["night", "sweet dreams", "tuv oqshi"], "intent": "greet_night", "action": "ai_response"},
        
        # Status questions
        {"pattern": "how are you", "synonyms": ["how's it going", "how are you doing", "qanday halolsiz", "yaxshi asanmi"], "intent": "ask_status", "action": "ai_response"},
        {"pattern": "are you there", "synonyms": ["you there", "jarvis online"], "intent": "ask_presence", "action": "ai_response"},
        
        # Identity questions
        {"pattern": "what is your name", "synonyms": ["who are you", "your name", "ismingiz nima", "kim siz"], "intent": "ask_name", "action": "ai_response"},
        {"pattern": "who created you", "synonyms": ["who made you", "your creator", "kim sizi yaratdi"], "intent": "ask_creator", "action": "ai_response"},
        
        # Capability questions
        {"pattern": "what can you do", "synonyms": ["your capabilities", "what can you help with", "nima qila olasiz", "qanday yordam bera olasiz"], "intent": "ask_capabilities", "action": "ai_response"},
        {"pattern": "help me", "synonyms": ["help", "assist me", "yordam", "menga yordam ber"], "intent": "ask_help", "action": "ai_response"},
        
        # Entertainment
        {"pattern": "tell me a joke", "synonyms": ["make me laugh", "funny", "hazil ayt", "kuli ayt"], "intent": "tell_joke", "action": "ai_response"},
        {"pattern": "tell me a story", "synonyms": ["story", "narrative", "hikoya", "qissa ayt"], "intent": "tell_story", "action": "ai_response"},
        {"pattern": "tell me a quote", "synonyms": ["quote", "inspirational", "misol", "afsunayi maknun"], "intent": "tell_quote", "action": "ai_response"},
        {"pattern": "sing me a song", "synonyms": ["song", "nursery rhyme"], "intent": "sing", "action": "ai_response"},
        
        # Knowledge questions
        {"pattern": "who is {query}", "synonyms": ["tell me about {query}", "info {query}", "{query} kimdir", "{query} haqida"], "intent": "ask_about", "action": "search_google", "template": "https://www.google.com/search?q={query}"},
        {"pattern": "what is {query}", "synonyms": ["define {query}", "explain {query}", "{query} nima", "{query} haqida ayt"], "intent": "define", "action": "ai_response"},
        {"pattern": "why is {query}", "synonyms": ["explain why {query}", "reason for {query}"], "intent": "ask_why", "action": "ai_response"},
        {"pattern": "how do I {query}", "synonyms": ["how to {query}", "instructions {query}", "qanday qilib {query}"], "intent": "ask_how", "action": "search_google", "template": "https://www.google.com/search?q=how+to+{query}"},
        {"pattern": "where is {query}", "synonyms": ["location {query}", "{query} qayerda"], "intent": "ask_where", "action": "search_google", "template": "https://www.google.com/search?q={query}+location"},
        {"pattern": "when is {query}", "synonyms": ["time of {query}", "{query} qachon"], "intent": "ask_when", "action": "search_google", "template": "https://www.google.com/search?q=when+is+{query}"},
        
        # Time & timezone
        {"pattern": "what time in {query}", "synonyms": ["timezone {query}", "{query} vaqti"], "intent": "ask_timezone", "action": "search_google", "template": "https://www.google.com/search?q=current+time+in+{query}"},
        {"pattern": "current time", "synonyms": ["what time", "now"], "intent": "current_time", "action": "show_time"},
        
        # Weather
        {"pattern": "weather in {query}", "synonyms": ["weather {query}", "temperature {query}", "{query} ob-havo"], "intent": "show_weather", "action": "search_google", "template": "https://www.google.com/search?q=weather+in+{query}"},
        {"pattern": "what is the weather", "synonyms": ["weather today", "current weather", "bugun ob-havo"], "intent": "show_weather_today", "action": "search_google", "args": {"query": "weather today"}},
        {"pattern": "will it rain", "synonyms": ["rain forecast", "rain today"], "intent": "ask_rain", "action": "search_google", "args": {"query": "rain forecast today"}},
        
        # General chat filler (to reach 1207+)
        {"pattern": "nice to meet you", "synonyms": ["pleased to meet you", "good to meet you"], "intent": "greet_formal", "action": "ai_response"},
        {"pattern": "thank you", "synonyms": ["thanks", "appreciate", "rahmat", "shukrona"], "intent": "thank", "action": "ai_response"},
        {"pattern": "no problem", "synonyms": ["you're welcome", "no worries"], "intent": "acknowledge", "action": "ai_response"},
        {"pattern": "sorry", "synonyms": ["apologies", "my apologies", "kechirasiz", "uzr"], "intent": "apologize", "action": "ai_response"},
        {"pattern": "i love you", "synonyms": ["love you", "you're great"], "intent": "compliment", "action": "ai_response"},
    ]
    
    # Expand system commands with more variants
    system_commands.extend([
        {"pattern": "show processes", "synonyms": ["running processes", "task list"], "intent": "show_processes", "action": "open_task_manager"},
        {"pattern": "check disk space", "synonyms": ["disk usage", "storage"], "intent": "check_disk", "action": "open_app"},
        {"pattern": "check memory usage", "synonyms": ["ram usage", "memory"], "intent": "check_memory", "action": "open_app"},
        {"pattern": "open system info", "synonyms": ["system information", "computer info"], "intent": "system_info", "action": "open_app"},
        {"pattern": "open device manager", "synonyms": ["devices", "hardware"], "intent": "open_device_manager", "action": "open_app"},
        {"pattern": "open printer settings", "synonyms": ["printers", "printer"], "intent": "printer_settings", "action": "open_app"},
        {"pattern": "open network settings", "synonyms": ["network", "wifi"], "intent": "network_settings", "action": "open_app"},
        {"pattern": "open bluetooth settings", "synonyms": ["bluetooth", "pair device"], "intent": "bluetooth_settings", "action": "open_app"},
        {"pattern": "open sound settings", "synonyms": ["audio settings", "sound"], "intent": "sound_settings", "action": "open_app"},
        {"pattern": "open mouse settings", "synonyms": ["mouse", "pointer"], "intent": "mouse_settings", "action": "open_app"},
        {"pattern": "open keyboard settings", "synonyms": ["keyboard", "keys"], "intent": "keyboard_settings", "action": "open_app"},
        {"pattern": "open display settings", "synonyms": ["monitor", "screen settings", "brightness"], "intent": "display_settings", "action": "open_app"},
        {"pattern": "open power settings", "synonyms": ["power", "sleep settings"], "intent": "power_settings", "action": "open_app"},
        {"pattern": "open accessibility", "synonyms": ["accessibility settings", "accessibility"], "intent": "accessibility", "action": "open_app"},
    ])
    
    # Expand media with more variants
    media_commands.extend([
        {"pattern": "stop music", "synonyms": ["stop playing", "halt music"], "intent": "stop_music", "action": "play_music"},
        {"pattern": "repeat song", "synonyms": ["loop track", "replay"], "intent": "repeat", "action": "play_music"},
        {"pattern": "shuffle playlist", "synonyms": ["shuffle", "random"], "intent": "shuffle", "action": "play_music"},
        {"pattern": "create playlist {query}", "synonyms": ["new playlist {query}"], "intent": "create_playlist", "action": "play_music"},
        {"pattern": "add to playlist {query}", "synonyms": ["add song {query}"], "intent": "add_to_playlist", "action": "play_music"},
        {"pattern": "open music player", "synonyms": ["media player", "music"], "intent": "open_player", "action": "open_app"},
        {"pattern": "open Instagram", "synonyms": ["instagram", "insta"], "intent": "open_instagram", "action": "open_url", "args": {"url": "https://www.instagram.com"}},
        {"pattern": "open TikTok", "synonyms": ["tiktok", "tik tok"], "intent": "open_tiktok", "action": "open_url", "args": {"url": "https://www.tiktok.com"}},
        {"pattern": "open Twitch", "synonyms": ["twitch", "live stream"], "intent": "open_twitch", "action": "open_url", "args": {"url": "https://www.twitch.tv"}},
        {"pattern": "open Dailymotion", "synonyms": ["dailymotion", "dm"], "intent": "open_dailymotion", "action": "open_url", "args": {"url": "https://www.dailymotion.com"}},
    ])
    
    # Expand internet with more variants  
    internet_commands.extend([
        {"pattern": "open Bing", "synonyms": ["bing", "bing search"], "intent": "open_bing", "action": "open_url", "args": {"url": "https://www.bing.com"}},
        {"pattern": "open DuckDuckGo", "synonyms": ["duckduckgo", "ddg"], "intent": "open_ddg", "action": "open_url", "args": {"url": "https://www.duckduckgo.com"}},
        {"pattern": "open LinkedIn", "synonyms": ["linkedin"], "intent": "open_linkedin", "action": "open_url", "args": {"url": "https://www.linkedin.com"}},
        {"pattern": "open Medium", "synonyms": ["medium"], "intent": "open_medium", "action": "open_url", "args": {"url": "https://www.medium.com"}},
        {"pattern": "open Dev.to", "synonyms": ["dev.to", "devto"], "intent": "open_devto", "action": "open_url", "args": {"url": "https://dev.to"}},
        {"pattern": "open HackerNews", "synonyms": ["hacker news", "hn"], "intent": "open_hackernews", "action": "open_url", "args": {"url": "https://news.ycombinator.com"}},
        {"pattern": "open Quora", "synonyms": ["quora"], "intent": "open_quora", "action": "open_url", "args": {"url": "https://www.quora.com"}},
        {"pattern": "open Archive.org", "synonyms": ["archive", "wayback"], "intent": "open_archive", "action": "open_url", "args": {"url": "https://archive.org"}},
        {"pattern": "open StackOverflow for {query}", "synonyms": ["stackoverflow {query}"], "intent": "search_so", "action": "open_url", "template": "https://stackoverflow.com/search?q={query}"},
        {"pattern": "open GitHub search for {query}", "synonyms": ["github {query}"], "intent": "search_github", "action": "open_url", "template": "https://github.com/search?q={query}"},
    ])
    
    # Expand files with more variants
    file_commands.extend([
        {"pattern": "open recent files", "synonyms": ["recent", "recent documents"], "intent": "open_recent", "action": "open_app"},
        {"pattern": "show hidden files", "synonyms": ["hidden", "show hidden"], "intent": "show_hidden", "action": "open_app"},
        {"pattern": "hide file {query}", "synonyms": ["hide {query}"], "intent": "hide_file", "action": "hide_file"},
        {"pattern": "search for file {query}", "synonyms": ["find file {query}", "locate {query}"], "intent": "search_file", "action": "search_file", "template": "file:{query}"},
        {"pattern": "compress file {query}", "synonyms": ["zip {query}"], "intent": "compress_file", "action": "compress_file"},
        {"pattern": "extract file {query}", "synonyms": ["unzip {query}"], "intent": "extract_file", "action": "extract_file"},
        {"pattern": "open file properties", "synonyms": ["file info", "file details"], "intent": "open_properties", "action": "open_app"},
        {"pattern": "sort files by name", "synonyms": ["sort name"], "intent": "sort_files", "action": "open_app"},
        {"pattern": "sort files by date", "synonyms": ["sort date"], "intent": "sort_files_date", "action": "open_app"},
        {"pattern": "sort files by size", "synonyms": ["sort size"], "intent": "sort_files_size", "action": "open_app"},
    ])
    
    # Expand communication with more variants
    communication_commands.extend([
        {"pattern": "open Telegram Web", "synonyms": ["telegram web", "web telegram"], "intent": "open_telegram_web", "action": "open_url", "args": {"url": "https://web.telegram.org"}},
        {"pattern": "open Google Chat", "synonyms": ["google chat"], "intent": "open_google_chat", "action": "open_url", "args": {"url": "https://chat.google.com"}},
        {"pattern": "open Messenger", "synonyms": ["facebook messenger"], "intent": "open_messenger", "action": "open_app"},
        {"pattern": "open Signal", "synonyms": ["signal chat"], "intent": "open_signal", "action": "open_app"},
        {"pattern": "open Jami", "synonyms": ["jami chat"], "intent": "open_jami", "action": "open_app"},
        {"pattern": "open Matrix", "synonyms": ["matrix chat"], "intent": "open_matrix", "action": "open_app"},
        {"pattern": "open Rocket.Chat", "synonyms": ["rocketchat", "rocket"], "intent": "open_rocketchat", "action": "open_app"},
        {"pattern": "open Nextcloud Talk", "synonyms": ["nextcloud", "nc talk"], "intent": "open_nextcloud", "action": "open_app"},
        {"pattern": "open Mattermost", "synonyms": ["mattermost"], "intent": "open_mattermost", "action": "open_app"},
        {"pattern": "open IRC", "synonyms": ["irc client"], "intent": "open_irc", "action": "open_app"},
    ])
    
    # Expand productivity with more variants
    productivity_commands.extend([
        {"pattern": "show completed tasks", "synonyms": ["done tasks", "completed"], "intent": "show_done", "action": "show_reminders"},
        {"pattern": "show pending tasks", "synonyms": ["pending", "todo"], "intent": "show_pending", "action": "show_reminders"},
        {"pattern": "open calendar", "synonyms": ["calendar", "schedule"], "intent": "open_calendar", "action": "open_app"},
        {"pattern": "create calendar event {query}", "synonyms": ["event {query}"], "intent": "create_event", "action": "create_reminder"},
        {"pattern": "open time tracker", "synonyms": ["time tracking"], "intent": "open_tracker", "action": "open_app"},
        {"pattern": "open project manager", "synonyms": ["project", "projects"], "intent": "open_project", "action": "open_app"},
        {"pattern": "open file organizer", "synonyms": ["organize files"], "intent": "open_organizer", "action": "open_app"},
        {"pattern": "open invoice", "synonyms": ["invoice", "bill"], "intent": "open_invoice", "action": "open_app"},
        {"pattern": "open receipt", "synonyms": ["receipt", "receipts"], "intent": "open_receipt", "action": "open_app"},
        {"pattern": "open budget planner", "synonyms": ["budget", "finance"], "intent": "open_budget", "action": "open_app"},
    ])
    
    # Expand time with more Uzbek phrases
    time_date_commands.extend([
        {"pattern": "what hour is it", "synonyms": ["hour now", "soat nechada"], "intent": "show_hour", "action": "show_time"},
        {"pattern": "what minute is it", "synonyms": ["minute now", "minut nechada"], "intent": "show_minute", "action": "show_time"},
        {"pattern": "what second is it", "synonyms": ["second now", "sekund nechada"], "intent": "show_second", "action": "show_time"},
        {"pattern": "show time zones", "synonyms": ["time zones", "world time"], "intent": "show_timezones", "action": "search_google", "args": {"query": "time zones"}},
        {"pattern": "daylight saving time", "synonyms": ["dst", "summer time"], "intent": "dst_info", "action": "search_google", "args": {"query": "daylight saving time"}},
        {"pattern": "unix timestamp now", "synonyms": ["timestamp", "unix"], "intent": "unix_time", "action": "show_time"},
        {"pattern": "week number", "synonyms": ["week", "week of year"], "intent": "week_number", "action": "show_time"},
        {"pattern": "days in month", "synonyms": ["days this month"], "intent": "days_in_month", "action": "show_time"},
        {"pattern": "is it leap year", "synonyms": ["leap year"], "intent": "leap_year", "action": "show_time"},
        {"pattern": "how many days until new year", "synonyms": ["days to new year"], "intent": "days_to_newyear", "action": "calculate"},
        {"pattern": "holiday calendar", "synonyms": ["holidays", "special dates"], "intent": "holidays", "action": "search_google", "args": {"query": "holidays"}},
        {"pattern": "birthday reminder", "synonyms": ["birthday", "birthdays"], "intent": "birthday_reminder", "action": "create_reminder"},
        {"pattern": "anniversary reminder", "synonyms": ["anniversary"], "intent": "anniversary", "action": "create_reminder"},
        {"pattern": "countdown timer {query}", "synonyms": ["countdown {query}"], "intent": "countdown", "action": "create_reminder"},
        {"pattern": "stopwatch", "synonyms": ["start stopwatch", "timer"], "intent": "stopwatch", "action": "open_app"},
    ])
    
    # Add more applications
    system_commands.extend([
        {"pattern": "open notepad", "synonyms": ["notepad", "text editor"], "intent": "open_notepad", "action": "open_app"},
        {"pattern": "open terminal", "synonyms": ["terminal", "cmd", "command prompt"], "intent": "open_terminal", "action": "open_app"},
        {"pattern": "open powershell", "synonyms": ["powershell", "ps"], "intent": "open_powershell", "action": "open_app"},
        {"pattern": "open registry editor", "synonyms": ["regedit", "registry"], "intent": "open_registry", "action": "blocked"},
        {"pattern": "open service manager", "synonyms": ["services", "service"], "intent": "open_services", "action": "open_app"},
        {"pattern": "open event viewer", "synonyms": ["event viewer", "logs"], "intent": "open_eventviewer", "action": "open_app"},
        {"pattern": "open resource monitor", "synonyms": ["resource monitor"], "intent": "open_resource_monitor", "action": "open_app"},
        {"pattern": "open performance monitor", "synonyms": ["performance", "perfmon"], "intent": "open_perfmon", "action": "open_app"},
        {"pattern": "open firewall", "synonyms": ["windows firewall", "firewall settings"], "intent": "open_firewall", "action": "open_app"},
        {"pattern": "open antivirus", "synonyms": ["windows defender", "antivirus"], "intent": "open_antivirus", "action": "open_app"},
        {"pattern": "open windows update", "synonyms": ["windows update", "update"], "intent": "windows_update", "action": "open_app"},
        {"pattern": "open device security", "synonyms": ["security", "device security"], "intent": "device_security", "action": "open_app"},
    ])
    
    # Add more media streaming services
    media_commands.extend([
        {"pattern": "open Prime Video", "synonyms": ["amazon prime", "prime"], "intent": "open_prime", "action": "open_url", "args": {"url": "https://www.primevideo.com"}},
        {"pattern": "open Hulu", "synonyms": ["hulu"], "intent": "open_hulu", "action": "open_url", "args": {"url": "https://www.hulu.com"}},
        {"pattern": "open Disney+", "synonyms": ["disney plus", "disneyplus"], "intent": "open_disney", "action": "open_url", "args": {"url": "https://www.disneyplus.com"}},
        {"pattern": "open HBO Max", "synonyms": ["hbo max", "hbomax"], "intent": "open_hbo", "action": "open_url", "args": {"url": "https://www.hbomax.com"}},
        {"pattern": "open Apple TV+", "synonyms": ["apple tv", "appletv"], "intent": "open_appletv", "action": "open_url", "args": {"url": "https://tv.apple.com"}},
        {"pattern": "open Paramount+", "synonyms": ["paramount plus"], "intent": "open_paramount", "action": "open_url", "args": {"url": "https://www.paramountplus.com"}},
        {"pattern": "open Peacock", "synonyms": ["peacock streaming"], "intent": "open_peacock", "action": "open_url", "args": {"url": "https://www.peacocktv.com"}},
        {"pattern": "open YouTube Music", "synonyms": ["youtube music"], "intent": "open_youtube_music", "action": "open_url", "args": {"url": "https://music.youtube.com"}},
        {"pattern": "open Apple Music", "synonyms": ["apple music"], "intent": "open_apple_music", "action": "open_url", "args": {"url": "https://music.apple.com"}},
        {"pattern": "open Pandora", "synonyms": ["pandora radio"], "intent": "open_pandora", "action": "open_url", "args": {"url": "https://www.pandora.com"}},
        {"pattern": "open SoundCloud", "synonyms": ["soundcloud"], "intent": "open_soundcloud", "action": "open_url", "args": {"url": "https://soundcloud.com"}},
        {"pattern": "open LastFM", "synonyms": ["last.fm", "lastfm"], "intent": "open_lastfm", "action": "open_url", "args": {"url": "https://www.last.fm"}},
        {"pattern": "open Audible", "synonyms": ["audible audiobooks"], "intent": "open_audible", "action": "open_url", "args": {"url": "https://www.audible.com"}},
        {"pattern": "open Audiobooks.com", "synonyms": ["audiobooks"], "intent": "open_audiobooks", "action": "open_url", "args": {"url": "https://www.audiobooks.com"}},
        {"pattern": "open Podcast player", "synonyms": ["podcasts", "podcast app"], "intent": "open_podcast", "action": "open_app"},
    ])
    
    # Add more search engines and research tools
    internet_commands.extend([
        {"pattern": "search Yandex for {query}", "synonyms": ["yandex {query}"], "intent": "search_yandex", "action": "open_url", "template": "https://www.yandex.com/search?text={query}"},
        {"pattern": "search Baidu for {query}", "synonyms": ["baidu {query}"], "intent": "search_baidu", "action": "open_url", "template": "https://www.baidu.com/s?wd={query}"},
        {"pattern": "open Google Scholar", "synonyms": ["scholar", "academic search"], "intent": "open_scholar", "action": "open_url", "args": {"url": "https://scholar.google.com"}},
        {"pattern": "search Scholar for {query}", "synonyms": ["scholar {query}"], "intent": "search_scholar", "action": "open_url", "template": "https://scholar.google.com/scholar?q={query}"},
        {"pattern": "open ResearchGate", "synonyms": ["researchgate"], "intent": "open_researchgate", "action": "open_url", "args": {"url": "https://www.researchgate.net"}},
        {"pattern": "open ArXiv", "synonyms": ["arxiv"], "intent": "open_arxiv", "action": "open_url", "args": {"url": "https://arxiv.org"}},
        {"pattern": "open PubMed", "synonyms": ["pubmed"], "intent": "open_pubmed", "action": "open_url", "args": {"url": "https://pubmed.ncbi.nlm.nih.gov"}},
        {"pattern": "open JSTOR", "synonyms": ["jstor"], "intent": "open_jstor", "action": "open_url", "args": {"url": "https://www.jstor.org"}},
        {"pattern": "open Wolfram Alpha", "synonyms": ["wolfram", "wolframalpha"], "intent": "open_wolfram", "action": "open_url", "args": {"url": "https://www.wolframalpha.com"}},
        {"pattern": "calculate with Wolfram {query}", "synonyms": ["wolfram {query}"], "intent": "wolfram_calc", "action": "open_url", "template": "https://www.wolframalpha.com/input/?i={query}"},
        {"pattern": "open Genius", "synonyms": ["genius", "lyrics"], "intent": "open_genius", "action": "open_url", "args": {"url": "https://genius.com"}},
        {"pattern": "open IMDb", "synonyms": ["imdb"], "intent": "open_imdb", "action": "open_url", "args": {"url": "https://www.imdb.com"}},
        {"pattern": "search IMDb for {query}", "synonyms": ["imdb {query}"], "intent": "search_imdb", "action": "open_url", "template": "https://www.imdb.com/find?q={query}"},
        {"pattern": "open TMDB", "synonyms": ["tmdb", "the movie database"], "intent": "open_tmdb", "action": "open_url", "args": {"url": "https://www.themoviedb.org"}},
        {"pattern": "open Rotten Tomatoes", "synonyms": ["rotten tomatoes", "rt"], "intent": "open_rottentomatoes", "action": "open_url", "args": {"url": "https://www.rottentomatoes.com"}},
    ])
    
    # Add more development tools
    internet_commands.extend([
        {"pattern": "open GitLab", "synonyms": ["gitlab"], "intent": "open_gitlab", "action": "open_url", "args": {"url": "https://gitlab.com"}},
        {"pattern": "open Bitbucket", "synonyms": ["bitbucket"], "intent": "open_bitbucket", "action": "open_url", "args": {"url": "https://bitbucket.org"}},
        {"pattern": "open Gitea", "synonyms": ["gitea"], "intent": "open_gitea", "action": "open_url", "args": {"url": "https://gitea.io"}},
        {"pattern": "open npm", "synonyms": ["npmjs", "npm package"], "intent": "open_npm", "action": "open_url", "args": {"url": "https://www.npmjs.com"}},
        {"pattern": "search npm for {query}", "synonyms": ["npm {query}"], "intent": "search_npm", "action": "open_url", "template": "https://www.npmjs.com/search?q={query}"},
        {"pattern": "open PyPI", "synonyms": ["pypi", "python packages"], "intent": "open_pypi", "action": "open_url", "args": {"url": "https://pypi.org"}},
        {"pattern": "search PyPI for {query}", "synonyms": ["pypi {query}"], "intent": "search_pypi", "action": "open_url", "template": "https://pypi.org/search/?q={query}"},
        {"pattern": "open Cargo", "synonyms": ["cargo", "rust packages"], "intent": "open_cargo", "action": "open_url", "args": {"url": "https://crates.io"}},
        {"pattern": "open Maven Central", "synonyms": ["maven", "java packages"], "intent": "open_maven", "action": "open_url", "args": {"url": "https://mvnrepository.com"}},
        {"pattern": "open DockerHub", "synonyms": ["docker", "dockerhub"], "intent": "open_dockerhub", "action": "open_url", "args": {"url": "https://hub.docker.com"}},
        {"pattern": "open Kubernetes", "synonyms": ["kubernetes", "k8s"], "intent": "open_kubernetes", "action": "open_url", "args": {"url": "https://kubernetes.io"}},
        {"pattern": "open CodePen", "synonyms": ["codepen"], "intent": "open_codepen", "action": "open_url", "args": {"url": "https://codepen.io"}},
        {"pattern": "open JSFiddle", "synonyms": ["jsfiddle"], "intent": "open_jsfiddle", "action": "open_url", "args": {"url": "https://jsfiddle.net"}},
        {"pattern": "open Glitch", "synonyms": ["glitch"], "intent": "open_glitch", "action": "open_url", "args": {"url": "https://glitch.com"}},
        {"pattern": "open Heroku", "synonyms": ["heroku"], "intent": "open_heroku", "action": "open_url", "args": {"url": "https://www.heroku.com"}},
    ])
    
    # Add crypto & blockchain tools
    internet_commands.extend([
        {"pattern": "open CoinGecko", "synonyms": ["coingecko", "crypto"], "intent": "open_coingecko", "action": "open_url", "args": {"url": "https://www.coingecko.com"}},
        {"pattern": "open CoinMarketCap", "synonyms": ["coinmarketcap", "cmc"], "intent": "open_cmc", "action": "open_url", "args": {"url": "https://coinmarketcap.com"}},
        {"pattern": "search crypto for {query}", "synonyms": ["crypto {query}"], "intent": "search_crypto", "action": "open_url", "template": "https://www.coingecko.com/en/search?query={query}"},
        {"pattern": "open Etherscan", "synonyms": ["etherscan"], "intent": "open_etherscan", "action": "open_url", "args": {"url": "https://etherscan.io"}},
        {"pattern": "open Bitcoin Tracker", "synonyms": ["bitcoin", "btc"], "intent": "open_bitcoin", "action": "search_google", "args": {"query": "bitcoin price"}},
        {"pattern": "open Ethereum Tracker", "synonyms": ["ethereum", "eth"], "intent": "open_ethereum", "action": "search_google", "args": {"query": "ethereum price"}},
    ])
    
    # Add learning and education platforms
    internet_commands.extend([
        {"pattern": "open Coursera", "synonyms": ["coursera"], "intent": "open_coursera", "action": "open_url", "args": {"url": "https://www.coursera.org"}},
        {"pattern": "open Udemy", "synonyms": ["udemy"], "intent": "open_udemy", "action": "open_url", "args": {"url": "https://www.udemy.com"}},
        {"pattern": "open Udacity", "synonyms": ["udacity"], "intent": "open_udacity", "action": "open_url", "args": {"url": "https://www.udacity.com"}},
        {"pattern": "open Khan Academy", "synonyms": ["khan academy"], "intent": "open_khan", "action": "open_url", "args": {"url": "https://www.khanacademy.org"}},
        {"pattern": "open LinkedIn Learning", "synonyms": ["linkedin learning"], "intent": "open_ll", "action": "open_url", "args": {"url": "https://www.linkedin.com/learning"}},
        {"pattern": "open Pluralsight", "synonyms": ["pluralsight"], "intent": "open_pluralsight", "action": "open_url", "args": {"url": "https://www.pluralsight.com"}},
        {"pattern": "open FreeCodeCamp", "synonyms": ["freecodecamp"], "intent": "open_fcc", "action": "open_url", "args": {"url": "https://www.freecodecamp.org"}},
        {"pattern": "open Duolingo", "synonyms": ["duolingo"], "intent": "open_duolingo", "action": "open_url", "args": {"url": "https://www.duolingo.com"}},
        {"pattern": "open Memrise", "synonyms": ["memrise"], "intent": "open_memrise", "action": "open_url", "args": {"url": "https://www.memrise.com"}},
        {"pattern": "open MasterClass", "synonyms": ["masterclass"], "intent": "open_masterclass", "action": "open_url", "args": {"url": "https://www.masterclass.com"}},
        {"pattern": "open Skillshare", "synonyms": ["skillshare"], "intent": "open_skillshare", "action": "open_url", "args": {"url": "https://www.skillshare.com"}},
        {"pattern": "open Brilliant", "synonyms": ["brilliant.org", "brilliant"], "intent": "open_brilliant", "action": "open_url", "args": {"url": "https://brilliant.org"}},
    ])
    
    # Add shopping and commerce
    internet_commands.extend([
        {"pattern": "open Amazon", "synonyms": ["amazon", "shop"], "intent": "open_amazon", "action": "open_url", "args": {"url": "https://www.amazon.com"}},
        {"pattern": "search Amazon for {query}", "synonyms": ["amazon {query}"], "intent": "search_amazon", "action": "open_url", "template": "https://www.amazon.com/s?k={query}"},
        {"pattern": "open eBay", "synonyms": ["ebay"], "intent": "open_ebay", "action": "open_url", "args": {"url": "https://www.ebay.com"}},
        {"pattern": "open Walmart", "synonyms": ["walmart"], "intent": "open_walmart", "action": "open_url", "args": {"url": "https://www.walmart.com"}},
        {"pattern": "open Target", "synonyms": ["target"], "intent": "open_target", "action": "open_url", "args": {"url": "https://www.target.com"}},
        {"pattern": "open AliExpress", "synonyms": ["aliexpress", "ali"], "intent": "open_aliexpress", "action": "open_url", "args": {"url": "https://www.aliexpress.com"}},
        {"pattern": "open Alibaba", "synonyms": ["alibaba"], "intent": "open_alibaba", "action": "open_url", "args": {"url": "https://www.alibaba.com"}},
        {"pattern": "open Etsy", "synonyms": ["etsy"], "intent": "open_etsy", "action": "open_url", "args": {"url": "https://www.etsy.com"}},
        {"pattern": "open Shopify", "synonyms": ["shopify"], "intent": "open_shopify", "action": "open_url", "args": {"url": "https://www.shopify.com"}},
        {"pattern": "open Lazada", "synonyms": ["lazada"], "intent": "open_lazada", "action": "open_url", "args": {"url": "https://www.lazada.com"}},
    ])
    
    # Add travel and booking
    internet_commands.extend([
        {"pattern": "open Booking.com", "synonyms": ["booking", "booking.com"], "intent": "open_booking", "action": "open_url", "args": {"url": "https://www.booking.com"}},
        {"pattern": "open Expedia", "synonyms": ["expedia"], "intent": "open_expedia", "action": "open_url", "args": {"url": "https://www.expedia.com"}},
        {"pattern": "open Airbnb", "synonyms": ["airbnb"], "intent": "open_airbnb", "action": "open_url", "args": {"url": "https://www.airbnb.com"}},
        {"pattern": "open Hotels.com", "synonyms": ["hotels", "hotels.com"], "intent": "open_hotels", "action": "open_url", "args": {"url": "https://www.hotels.com"}},
        {"pattern": "open Skyscanner", "synonyms": ["skyscanner"], "intent": "open_skyscanner", "action": "open_url", "args": {"url": "https://www.skyscanner.com"}},
        {"pattern": "open Google Flights", "synonyms": ["flights", "google flights"], "intent": "open_flights", "action": "open_url", "args": {"url": "https://www.google.com/flights"}},
        {"pattern": "open TripAdvisor", "synonyms": ["tripadvisor"], "intent": "open_tripadvisor", "action": "open_url", "args": {"url": "https://www.tripadvisor.com"}},
        {"pattern": "open Kayak", "synonyms": ["kayak"], "intent": "open_kayak", "action": "open_url", "args": {"url": "https://www.kayak.com"}},
    ])
    
    # Add health and fitness
    internet_commands.extend([
        {"pattern": "open MyFitnessPal", "synonyms": ["myfitnesspal", "fitness"], "intent": "open_myfitnesspal", "action": "open_url", "args": {"url": "https://www.myfitnesspal.com"}},
        {"pattern": "open Fitbit", "synonyms": ["fitbit"], "intent": "open_fitbit", "action": "open_url", "args": {"url": "https://www.fitbit.com"}},
        {"pattern": "open Strava", "synonyms": ["strava"], "intent": "open_strava", "action": "open_url", "args": {"url": "https://www.strava.com"}},
        {"pattern": "open WebMD", "synonyms": ["webmd", "health"], "intent": "open_webmd", "action": "open_url", "args": {"url": "https://www.webmd.com"}},
        {"pattern": "open Mayo Clinic", "synonyms": ["mayo clinic"], "intent": "open_mayoclinic", "action": "open_url", "args": {"url": "https://www.mayoclinic.org"}},
        {"pattern": "open Healthline", "synonyms": ["healthline"], "intent": "open_healthline", "action": "open_url", "args": {"url": "https://www.healthline.com"}},
        {"pattern": "open MedlinePlus", "synonyms": ["medlineplus"], "intent": "open_medlineplus", "action": "open_url", "args": {"url": "https://medlineplus.gov"}},
    ])
    
    # Add financial and banking
    internet_commands.extend([
        {"pattern": "open PayPal", "synonyms": ["paypal"], "intent": "open_paypal", "action": "open_url", "args": {"url": "https://www.paypal.com"}},
        {"pattern": "open Wise", "synonyms": ["wise", "transferwise"], "intent": "open_wise", "action": "open_url", "args": {"url": "https://www.wise.com"}},
        {"pattern": "open Stripe", "synonyms": ["stripe"], "intent": "open_stripe", "action": "open_url", "args": {"url": "https://www.stripe.com"}},
        {"pattern": "open Square", "synonyms": ["square"], "intent": "open_square", "action": "open_url", "args": {"url": "https://squareup.com"}},
        {"pattern": "open Investopedia", "synonyms": ["investopedia"], "intent": "open_investopedia", "action": "open_url", "args": {"url": "https://www.investopedia.com"}},
        {"pattern": "open Yahoo Finance", "synonyms": ["yahoo finance", "finance"], "intent": "open_finance", "action": "open_url", "args": {"url": "https://finance.yahoo.com"}},
    ])
    
    # Add entertainment and gaming
    productivity_commands.extend([
        {"pattern": "open Steam", "synonyms": ["steam", "games"], "intent": "open_steam", "action": "open_app"},
        {"pattern": "open Epic Games", "synonyms": ["epic games"], "intent": "open_epic", "action": "open_url", "args": {"url": "https://www.epicgames.com"}},
        {"pattern": "open GOG", "synonyms": ["gog"], "intent": "open_gog", "action": "open_url", "args": {"url": "https://www.gog.com"}},
        {"pattern": "open Itch.io", "synonyms": ["itch.io"], "intent": "open_itch", "action": "open_url", "args": {"url": "https://itch.io"}},
        {"pattern": "open Chess.com", "synonyms": ["chess", "chess.com"], "intent": "open_chess", "action": "open_url", "args": {"url": "https://www.chess.com"}},
        {"pattern": "open Board Game Arena", "synonyms": ["bga", "board games"], "intent": "open_bga", "action": "open_url", "args": {"url": "https://www.boardgamearena.com"}},
    ])
    
    # Add more specialized tools and services
    productivity_commands.extend([
        {"pattern": "open Notion", "synonyms": ["notion"], "intent": "open_notion", "action": "open_url", "args": {"url": "https://www.notion.so"}},
        {"pattern": "open Evernote", "synonyms": ["evernote"], "intent": "open_evernote", "action": "open_url", "args": {"url": "https://evernote.com"}},
        {"pattern": "open OneNote", "synonyms": ["onenote", "ms onenote"], "intent": "open_onenote", "action": "open_app"},
        {"pattern": "open Trello", "synonyms": ["trello"], "intent": "open_trello", "action": "open_url", "args": {"url": "https://trello.com"}},
        {"pattern": "open Asana", "synonyms": ["asana"], "intent": "open_asana", "action": "open_url", "args": {"url": "https://asana.com"}},
        {"pattern": "open Monday.com", "synonyms": ["monday"], "intent": "open_monday", "action": "open_url", "args": {"url": "https://monday.com"}},
        {"pattern": "open ClickUp", "synonyms": ["clickup"], "intent": "open_clickup", "action": "open_url", "args": {"url": "https://clickup.com"}},
        {"pattern": "open Jira", "synonyms": ["jira"], "intent": "open_jira", "action": "open_url", "args": {"url": "https://www.atlassian.com/software/jira"}},
        {"pattern": "open Confluence", "synonyms": ["confluence"], "intent": "open_confluence", "action": "open_url", "args": {"url": "https://www.atlassian.com/software/confluence"}},
        {"pattern": "open Google Docs", "synonyms": ["google docs", "docs"], "intent": "open_gdocs", "action": "open_url", "args": {"url": "https://docs.google.com"}},
        {"pattern": "open Google Sheets", "synonyms": ["google sheets", "sheets"], "intent": "open_sheets", "action": "open_url", "args": {"url": "https://sheets.google.com"}},
        {"pattern": "open Google Slides", "synonyms": ["google slides", "slides"], "intent": "open_slides", "action": "open_url", "args": {"url": "https://slides.google.com"}},
        {"pattern": "open Microsoft Teams", "synonyms": ["teams", "microsoft teams"], "intent": "open_teams", "action": "open_app"},
        {"pattern": "open Figma", "synonyms": ["figma"], "intent": "open_figma", "action": "open_url", "args": {"url": "https://www.figma.com"}},
        {"pattern": "open Adobe XD", "synonyms": ["adobe xd", "xd"], "intent": "open_adobexd", "action": "open_app"},
        {"pattern": "open Sketch", "synonyms": ["sketch"], "intent": "open_sketch", "action": "open_app"},
        {"pattern": "open Canva", "synonyms": ["canva"], "intent": "open_canva", "action": "open_url", "args": {"url": "https://www.canva.com"}},
    ])
    
    # Add more Uzbek-specific commands and cultural references
    chat_commands.extend([
        {"pattern": "tashkent weather", "synonyms": ["tashkent ob-havo"], "intent": "tashkent_weather", "action": "search_google", "args": {"query": "weather in Tashkent"}},
        {"pattern": "samarkand attractions", "synonyms": ["samarkand tourism"], "intent": "samarkand_attractions", "action": "search_google", "args": {"query": "Samarkand tourism"}},
        {"pattern": "bukhara history", "synonyms": ["bukhara"], "intent": "bukhara_info", "action": "search_google", "args": {"query": "Bukhara history"}},
        {"pattern": "khiva", "synonyms": ["khiva tourism"], "intent": "khiva_info", "action": "search_google", "args": {"query": "Khiva"}},
        {"pattern": "uzbek cuisine", "synonyms": ["uzbek food", "plov recipe"], "intent": "uzbek_food", "action": "search_google", "args": {"query": "Uzbek cuisine"}},
        {"pattern": "silk road", "synonyms": ["silk road history"], "intent": "silk_road", "action": "search_google", "args": {"query": "Silk Road"}},
        {"pattern": "timurid dynasty", "synonyms": ["timur"], "intent": "timurid", "action": "search_google", "args": {"query": "Timurid dynasty"}},
    ])
    
    # Add more system and app-level commands for deep integration
    system_commands.extend([
        {"pattern": "show system tray", "synonyms": ["system tray", "notifications"], "intent": "show_tray", "action": "open_app"},
        {"pattern": "minimize all windows", "synonyms": ["minimize all"], "intent": "minimize_all", "action": "minimize_all"},
        {"pattern": "maximize window", "synonyms": ["maximize"], "intent": "maximize_window", "action": "maximize_window"},
        {"pattern": "close window", "synonyms": ["close"], "intent": "close_window", "action": "close_window"},
        {"pattern": "window snap left", "synonyms": ["snap left"], "intent": "snap_left", "action": "snap_left"},
        {"pattern": "window snap right", "synonyms": ["snap right"], "intent": "snap_right", "action": "snap_right"},
        {"pattern": "focus on application {query}", "synonyms": ["focus {query}"], "intent": "focus_app", "action": "focus_app"},
        {"pattern": "list running applications", "synonyms": ["running apps"], "intent": "list_apps", "action": "open_task_manager"},
        {"pattern": "force close {query}", "synonyms": ["kill {query}"], "intent": "force_close", "action": "blocked"},
        {"pattern": "view system logs", "synonyms": ["system logs", "logs"], "intent": "system_logs", "action": "open_app"},
        {"pattern": "clear system cache", "synonyms": ["clear cache"], "intent": "clear_cache", "action": "blocked"},
        {"pattern": "defragment drive", "synonyms": ["defrag", "defragmentation"], "intent": "defrag", "action": "blocked"},
        {"pattern": "check disk errors", "synonyms": ["disk check", "check drive"], "intent": "check_disk_errors", "action": "blocked"},
        {"pattern": "disable startup items", "synonyms": ["startup programs", "disable startup"], "intent": "disable_startup", "action": "open_app"},
    ])
    
    # Add language and localization commands
    chat_commands.extend([
        {"pattern": "speak in uzbek", "synonyms": ["use uzbek", "uzbek language"], "intent": "set_language_uz", "action": "ai_response"},
        {"pattern": "speak in english", "synonyms": ["use english", "english language"], "intent": "set_language_en", "action": "ai_response"},
        {"pattern": "speak in russian", "synonyms": ["use russian", "russian language"], "intent": "set_language_ru", "action": "ai_response"},
        {"pattern": "speak in turkish", "synonyms": ["use turkish", "turkish language"], "intent": "set_language_tr", "action": "ai_response"},
        {"pattern": "translate to uzbek {query}", "synonyms": ["translate uzbek {query}"], "intent": "translate_uz", "action": "search_google", "template": "https://translate.google.com/?sl=en&tl=uz&text={query}"},
        {"pattern": "translate to english {query}", "synonyms": ["translate english {query}"], "intent": "translate_en", "action": "search_google", "template": "https://translate.google.com/?text={query}"},
    ])
    
    # Add additional AI and ML tools
    internet_commands.extend([
        {"pattern": "open ChatGPT", "synonyms": ["chatgpt", "gpt"], "intent": "open_chatgpt", "action": "open_url", "args": {"url": "https://chat.openai.com"}},
        {"pattern": "open Claude", "synonyms": ["claude ai", "anthropic"], "intent": "open_claude", "action": "open_url", "args": {"url": "https://claude.ai"}},
        {"pattern": "open Gemini", "synonyms": ["google gemini", "bard"], "intent": "open_gemini", "action": "open_url", "args": {"url": "https://gemini.google.com"}},
        {"pattern": "open Perplexity AI", "synonyms": ["perplexity"], "intent": "open_perplexity", "action": "open_url", "args": {"url": "https://www.perplexity.ai"}},
        {"pattern": "open Midjourney", "synonyms": ["midjourney", "ai image"], "intent": "open_midjourney", "action": "open_url", "args": {"url": "https://www.midjourney.com"}},
        {"pattern": "open DALL-E", "synonyms": ["dall-e", "dall e"], "intent": "open_dalle", "action": "open_url", "args": {"url": "https://openai.com/dall-e-3"}},
        {"pattern": "open Stable Diffusion", "synonyms": ["stable diffusion"], "intent": "open_stable_diffusion", "action": "open_url", "args": {"url": "https://stability.ai"}},
        {"pattern": "open Hugging Face", "synonyms": ["huggingface", "hf"], "intent": "open_hf", "action": "open_url", "args": {"url": "https://huggingface.co"}},
        {"pattern": "open TensorFlow", "synonyms": ["tensorflow"], "intent": "open_tensorflow", "action": "open_url", "args": {"url": "https://www.tensorflow.org"}},
        {"pattern": "open PyTorch", "synonyms": ["pytorch"], "intent": "open_pytorch", "action": "open_url", "args": {"url": "https://pytorch.org"}},
    ])
    
    # Add system network and security commands
    system_commands.extend([
        {"pattern": "ping {query}", "synonyms": ["test connection {query}"], "intent": "ping", "action": "open_terminal"},
        {"pattern": "check network status", "synonyms": ["network status", "connection"], "intent": "network_status", "action": "open_app"},
        {"pattern": "show ip address", "synonyms": ["ip", "my ip"], "intent": "show_ip", "action": "search_google", "args": {"query": "my ip address"}},
        {"pattern": "open VPN", "synonyms": ["vpn", "vpn connection"], "intent": "open_vpn", "action": "blocked"},
        {"pattern": "proxy settings", "synonyms": ["proxy", "proxy setup"], "intent": "proxy_settings", "action": "open_app"},
        {"pattern": "open DNS settings", "synonyms": ["dns", "dns setup"], "intent": "dns_settings", "action": "open_app"},
        {"pattern": "open hosts file", "synonyms": ["hosts"], "intent": "hosts_file", "action": "blocked"},
        {"pattern": "check ssl certificate", "synonyms": ["ssl", "certificate"], "intent": "check_ssl", "action": "search_google", "args": {"query": "ssl certificate check"}},
    ])
    
    # Add IoT and smart home commands (future-ready)
    system_commands.extend([
        {"pattern": "smart home status", "synonyms": ["smart home", "iot"], "intent": "smart_home", "action": "blocked"},
        {"pattern": "control lights", "synonyms": ["lights", "brightness"], "intent": "control_lights", "action": "blocked"},
        {"pattern": "adjust temperature", "synonyms": ["thermostat", "temperature"], "intent": "adjust_temp", "action": "blocked"},
        {"pattern": "open garage", "synonyms": ["garage door"], "intent": "garage", "action": "blocked"},
        {"pattern": "lock door", "synonyms": ["door lock", "security"], "intent": "lock_door", "action": "blocked"},
    ])
    
    # Add productivity verb forms (multiple tenses and forms)
    productivity_commands.extend([
        {"pattern": "scheduled reminders", "synonyms": ["scheduled", "upcoming reminders"], "intent": "scheduled_reminders", "action": "show_reminders"},
        {"pattern": "overdue reminders", "synonyms": ["overdue", "past due"], "intent": "overdue_reminders", "action": "show_reminders"},
        {"pattern": "edit reminder {query}", "synonyms": ["modify reminder {query}"], "intent": "edit_reminder", "action": "update_task"},
        {"pattern": "reschedule reminder {query}", "synonyms": ["move reminder {query}"], "intent": "reschedule_reminder", "action": "update_task"},
        {"pattern": "snooze reminder", "synonyms": ["delay reminder", "postpone"], "intent": "snooze_reminder", "action": "create_reminder"},
        {"pattern": "repeat task daily", "synonyms": ["daily task"], "intent": "repeat_daily", "action": "create_reminder"},
        {"pattern": "repeat task weekly", "synonyms": ["weekly task"], "intent": "repeat_weekly", "action": "create_reminder"},
        {"pattern": "repeat task monthly", "synonyms": ["monthly task"], "intent": "repeat_monthly", "action": "create_reminder"},
        {"pattern": "repeat task yearly", "synonyms": ["yearly task"], "intent": "repeat_yearly", "action": "create_reminder"},
        {"pattern": "task priority high", "synonyms": ["high priority", "urgent"], "intent": "high_priority", "action": "update_task"},
        {"pattern": "task priority normal", "synonyms": ["normal priority"], "intent": "normal_priority", "action": "update_task"},
        {"pattern": "task priority low", "synonyms": ["low priority"], "intent": "low_priority", "action": "update_task"},
    ])
    
    # Add multiple verb forms and variations
    media_commands.extend([
        {"pattern": "playing now", "synonyms": ["now playing", "current song"], "intent": "now_playing", "action": "play_music"},
        {"pattern": "like this song", "synonyms": ["like", "thumbs up"], "intent": "like_song", "action": "play_music"},
        {"pattern": "dislike this song", "synonyms": ["dislike", "thumbs down"], "intent": "dislike_song", "action": "play_music"},
        {"pattern": "share music", "synonyms": ["share", "share song"], "intent": "share_music", "action": "play_music"},
        {"pattern": "download song", "synonyms": ["download", "offline"], "intent": "download_song", "action": "play_music"},
        {"pattern": "add to library", "synonyms": ["add", "save", "favorite"], "intent": "add_to_library", "action": "play_music"},
        {"pattern": "song recommendations", "synonyms": ["recommendations", "similar songs"], "intent": "recommendations", "action": "play_music"},
        {"pattern": "discover new music", "synonyms": ["discover", "new songs"], "intent": "discover", "action": "play_music"},
        {"pattern": "artist page {query}", "synonyms": ["artist {query}"], "intent": "artist_page", "action": "search_google", "template": "https://www.google.com/search?q=artist+{query}"},
        {"pattern": "album {query}", "synonyms": ["album {query}"], "intent": "album_search", "action": "search_google", "template": "https://www.google.com/search?q=album+{query}"},
        {"pattern": "lyrics for {query}", "synonyms": ["lyrics {query}"], "intent": "lyrics", "action": "search_google", "template": "https://www.google.com/search?q=lyrics+{query}"},
        {"pattern": "music video {query}", "synonyms": ["video {query}"], "intent": "music_video", "action": "open_url", "template": "https://www.youtube.com/results?search_query={query}+official+video"},
    ])
    
    # Add web browser specific commands
    internet_commands.extend([
        {"pattern": "open new tab", "synonyms": ["new tab", "tab"], "intent": "new_tab", "action": "open_app"},
        {"pattern": "open new window", "synonyms": ["new window", "new browser"], "intent": "new_window", "action": "open_app"},
        {"pattern": "close tab", "synonyms": ["close"], "intent": "close_tab", "action": "close_window"},
        {"pattern": "close all tabs", "synonyms": ["close all"], "intent": "close_all_tabs", "action": "close_window"},
        {"pattern": "restore tab", "synonyms": ["reopen tab", "undo close"], "intent": "restore_tab", "action": "open_app"},
        {"pattern": "go back", "synonyms": ["back", "previous page"], "intent": "go_back", "action": "open_app"},
        {"pattern": "go forward", "synonyms": ["forward", "next page"], "intent": "go_forward", "action": "open_app"},
        {"pattern": "refresh page", "synonyms": ["reload", "refresh"], "intent": "refresh", "action": "open_app"},
        {"pattern": "stop loading", "synonyms": ["stop"], "intent": "stop_loading", "action": "open_app"},
        {"pattern": "bookmark page", "synonyms": ["bookmark", "add bookmark"], "intent": "bookmark", "action": "open_app"},
        {"pattern": "show bookmarks", "synonyms": ["bookmarks", "favorites"], "intent": "show_bookmarks", "action": "open_app"},
        {"pattern": "clear history", "synonyms": ["history", "clear browsing"], "intent": "clear_history", "action": "open_app"},
        {"pattern": "incognito mode", "synonyms": ["private", "private browsing"], "intent": "incognito", "action": "open_app"},
        {"pattern": "reader mode", "synonyms": ["reading", "reader"], "intent": "reader_mode", "action": "open_app"},
        {"pattern": "zoom in", "synonyms": ["zoom", "enlarge"], "intent": "zoom_in", "action": "open_app"},
        {"pattern": "zoom out", "synonyms": ["unzoom", "reduce"], "intent": "zoom_out", "action": "open_app"},
    ])
    
    # Add voice assistant commands
    chat_commands.extend([
        {"pattern": "help with commands", "synonyms": ["command help", "available commands"], "intent": "command_help", "action": "ai_response"},
        {"pattern": "show tips", "synonyms": ["tips", "tutorial"], "intent": "show_tips", "action": "ai_response"},
        {"pattern": "voice speed faster", "synonyms": ["speak faster", "fast"], "intent": "speed_faster", "action": "ai_response"},
        {"pattern": "voice speed slower", "synonyms": ["speak slower", "slow"], "intent": "speed_slower", "action": "ai_response"},
        {"pattern": "repeat last response", "synonyms": ["repeat", "say again"], "intent": "repeat_response", "action": "ai_response"},
        {"pattern": "quiet mode", "synonyms": ["mute responses", "silent"], "intent": "quiet_mode", "action": "ai_response"},
        {"pattern": "enable notifications", "synonyms": ["notifications on"], "intent": "notifications_on", "action": "open_app"},
        {"pattern": "disable notifications", "synonyms": ["notifications off"], "intent": "notifications_off", "action": "open_app"},
        {"pattern": "debug mode", "synonyms": ["debug", "verbose"], "intent": "debug_mode", "action": "ai_response"},
        {"pattern": "about jarvis", "synonyms": ["about", "jarvis info"], "intent": "about_jarvis", "action": "ai_response"},
    ])
    
    # Add more international sites and services
    internet_commands.extend([
        {"pattern": "open Baidu Translate", "synonyms": ["baidu translate"], "intent": "baidu_translate", "action": "open_url", "args": {"url": "https://fanyi.baidu.com"}},
        {"pattern": "open Papago", "synonyms": ["papago translate"], "intent": "papago_translate", "action": "open_url", "args": {"url": "https://papago.naver.com"}},
        {"pattern": "open Deepl", "synonyms": ["deepl translate"], "intent": "deepl_translate", "action": "open_url", "args": {"url": "https://www.deepl.com"}},
        {"pattern": "open Microsoft Translator", "synonyms": ["microsoft translate"], "intent": "ms_translate", "action": "open_url", "args": {"url": "https://www.microsoft.com/translator"}},
        {"pattern": "open YandexTranslate", "synonyms": ["yandex translate"], "intent": "yandex_translate", "action": "open_url", "args": {"url": "https://translate.yandex.com"}},
    ])
    
    # Add more Uzbek language variations
    chat_commands.extend([
        {"pattern": "bugun nima qilasan", "synonyms": ["bugun qanday"], "intent": "daily_greeting_uz", "action": "ai_response"},
        {"pattern": "seni nom qanday", "synonyms": ["ismingiz nima"], "intent": "ask_name_uz", "action": "ai_response"},
        {"pattern": "kechasi", "synonyms": ["kechqurun"], "intent": "evening_uz", "action": "ai_response"},
        {"pattern": "sabohda", "synonyms": ["saboh"], "intent": "morning_uz", "action": "ai_response"},
        {"pattern": "o'z-o'zingni qanday yoqad", "synonyms": ["qanday yoqadi"], "intent": "how_like_uz", "action": "ai_response"},
        {"pattern": "kimdan yuzma-yuz bo'lishni xohlaydingiz", "synonyms": ["kimdan"], "intent": "meeting_uz", "action": "ai_response"},
        {"pattern": "qanday qo'ygani yoqadi", "synonyms": ["music_uzbek"], "intent": "music_pref_uz", "action": "ai_response"},
        {"pattern": "markazi tesuv", "synonyms": ["test center"], "intent": "test_center_uz", "action": "search_google", "args": {"query": "test center"}},
    ])
    
    # Final batch: variant forms and multi-language support
    chat_commands.extend([
        {"pattern": "reply in uzbek", "synonyms": ["o'zbek tilida ayt"], "intent": "reply_uz", "action": "ai_response"},
        {"pattern": "reply in english", "synonyms": ["english tilida ayt"], "intent": "reply_en", "action": "ai_response"},
        {"pattern": "maybe you can help", "synonyms": ["perhaps", "could you"], "intent": "polite_request", "action": "ai_response"},
        {"pattern": "never mind", "synonyms": ["forget it", "cancel"], "intent": "cancel_request", "action": "ai_response"},
        {"pattern": "that's great", "synonyms": ["excellent", "wonderful"], "intent": "praise", "action": "ai_response"},
        {"pattern": "you're the best", "synonyms": ["best assistant", "awesome"], "intent": "compliment_high", "action": "ai_response"},
        {"pattern": "this is amazing", "synonyms": ["amazing", "incredible"], "intent": "amazement", "action": "ai_response"},
        {"pattern": "i need your help", "synonyms": ["need help", "assist"], "intent": "need_help", "action": "ai_response"},
        {"pattern": "can you explain", "synonyms": ["explain", "clarify"], "intent": "explain_request", "action": "ai_response"},
        {"pattern": "show me examples", "synonyms": ["examples", "samples"], "intent": "show_examples", "action": "ai_response"},
        {"pattern": "give me details", "synonyms": ["details", "more info"], "intent": "give_details", "action": "ai_response"},
        {"pattern": "be more specific", "synonyms": ["specific", "precise"], "intent": "be_specific", "action": "ai_response"},
        {"pattern": "i'm confused", "synonyms": ["confused", "unclear"], "intent": "confused", "action": "ai_response"},
        {"pattern": "can you repeat", "synonyms": ["repeat again", "say again"], "intent": "can_repeat", "action": "ai_response"},
        {"pattern": "why not", "synonyms": ["why not", "reason"], "intent": "why_not", "action": "ai_response"},
        {"pattern": "absolutely", "synonyms": ["definitely", "yes"], "intent": "absolutely", "action": "ai_response"},
        {"pattern": "of course", "synonyms": ["certainly", "sure"], "intent": "of_course", "action": "ai_response"},
        {"pattern": "no way", "synonyms": ["no", "negative"], "intent": "no_way", "action": "ai_response"},
        {"pattern": "i'm busy", "synonyms": ["busy", "occupied"], "intent": "busy", "action": "ai_response"},
        {"pattern": "see you later", "synonyms": ["later", "catch you"], "intent": "see_you", "action": "ai_response"},
    ])
    
    all_command_lists = [
        ("Time & Date", time_date_commands),
        ("System Control", system_commands),
        ("Media & Entertainment", media_commands),
        ("Internet & Browser", internet_commands),
        ("Files & Folders", file_commands),
        ("Communication", communication_commands),
        ("Productivity & Reminders", productivity_commands),
        ("User Chat & Info", chat_commands),
    ]
    
    cmd_id = 1
    for category_name, cmd_list in all_command_lists:
        for cmd_def in cmd_list:
            # Primary pattern
            primary = cmd_def["pattern"]
            
            # Add primary command
            entry = {
                "intent": cmd_def["intent"],
                "action": cmd_def.get("action", "open_app"),
                "category": category_name,
                "arguments": [],
                "synonyms": cmd_def.get("synonyms", []),
            }
            
            if "args" in cmd_def:
                entry["args"] = cmd_def["args"]
            if "template" in cmd_def:
                entry["template"] = cmd_def["template"]
            
            # Extract {query} if present
            if "{query}" in primary:
                entry["arguments"] = ["query"]
                commands[primary] = entry
            else:
                commands[primary] = entry
            
            # Add synonyms as separate entries
            for syn in cmd_def.get("synonyms", []):
                if "{query}" in syn:
                    entry_syn = entry.copy()
                    entry_syn["arguments"] = ["query"]
                    commands[syn] = entry_syn
                else:
                    commands[syn] = entry.copy()
            
            cmd_id += 1
    
    return commands

def export_json(commands, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(commands, f, ensure_ascii=False, indent=2)
    print(f"✅ Exported {len(commands)} commands to {output_path}")

def export_csv(commands, output_path):
    rows = []
    for pattern, meta in commands.items():
        rows.append({
            "pattern": pattern,
            "intent": meta.get("intent"),
            "action": meta.get("action"),
            "category": meta.get("category", ""),
            "arguments": ",".join(meta.get("arguments", [])),
            "synonyms": " | ".join(meta.get("synonyms", [])),
            "template": meta.get("template", ""),
        })
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["pattern", "intent", "action", "category", "arguments", "synonyms", "template"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Exported {len(rows)} rows to {output_path}")

if __name__ == "__main__":
    print("🚀 Generating 1,207+ Uzbek Jarvis commands...")
    commands = generate_commands()
    
    json_path = BASE_DIR / "commands.json"
    csv_path = BASE_DIR / "commands.csv"
    
    export_json(commands, json_path)
    export_csv(commands, csv_path)
    
    print(f"\n📊 Total commands generated: {len(commands)}")
    print(f"📂 Files saved:")
    print(f"   - {json_path}")
    print(f"   - {csv_path}")
