# Jarvis Linux Assistant

Professional C++ Assistant for Linux with Voice & AI capabilities.
Bu loyiha Linux tizimlari uchun mo'ljallangan, C++ da yozilgan tezkor va yengil ovozli yordamchi.

## Imkoniyatlar

- **Core:** C++ (Tez va resurs tejamkor)
- **Ovoz:** Python SpeechRecognition (Google STT)
- **AI:** ChatGPT Integration (Murakkab so'rovlar uchun)
- **UX:** Background Daemon + Hotkey Trigger + Native Notifications
- **Til:** Ko'p tilli qo'llab-quvvatlash (Default: O'zbek tili)
- **Media:** YouTube qidiruvi va lokal musiqa boshqaruvi

## O'rnatish

### 1. Kerakli kutubxonalar

Ubuntu/Debian uchun:

```bash
sudo apt update
sudo apt install g++ libcurl4-openssl-dev libnotify-bin python3-pip xbindkeys
pip3 install SpeechRecognition pyaudio
```

### 2. Loyihani yig'ish (Build)

```bash
chmod +x build.sh
./build.sh
```

### 3. Sozlash (.env)

Namuna faylidan nusxa oling va API kalitingizni kiriting:

```bash
cp .env.example .env
# .env faylini ochib OPENAI_API_KEY ni yozing
```

## Ishlatish

### Oddiy rejim (Terminal)

```bash
./build/jarvis uz
```

### Orqa fon rejimi (Daemon)

Jarvisni orqa fonda ishga tushirish:

```bash
chmod +x start_daemon.sh
./start_daemon.sh
```

### Ovozli boshqaruv (Hotkey)

`trigger.sh` faylini tizim sozlamalarida biror tugmaga (masalan, `Ctrl+Space`) bog'lang.
Tugma bosilganda Jarvis sizni eshitadi va bildirishnoma orqali javob qaytaradi.
