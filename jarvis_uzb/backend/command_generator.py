import random
import zipfile

# Buyruqlar uchun kategoriyalar va andozalar
COMMANDS_BLUEPRINT = {
    "fayl_ochish": [
        "{papka} papkasidagi {fayl_turi}ni och",
        "{papka}dagi {fayl_nomi} nomli faylni ochib ber",
        "Menga {papka} ichidagi {fayl_turi}ni ko'rsat",
    ],
    "dastur_ochish": [
        "{dastur}ni ishga tushur",
        "Zudlik bilan {dastur}ni och",
        "{dastur} dasturini ochib yubor",
    ],
    "tizim_boshqaruvi": [
        "Kompyuterni {holat}",
        "Tizimni {holat} holatiga o'tkaz",
    ],
    "ovoz_boshqaruvi": [
        "Ovozni {daraja} foizga {yo'nalish}",
        "Musiqani {daraja}% {yo'nalish}",
        "Ovoz balandligini {yo'nalish}",
    ],
    "oyna_boshqaruvi": [
        "Joriy oynani {harakat}",
        "Oynani {harakat} qil",
        "Aktiv oynani {harakat} holatiga keltir",
    ],
    "brauzer_boshqaruvi": [
        "Brauzerda yangi {element} och",
        "{sayt} saytini och",
        "Chrome'da {qidiruv_sozi}ni qidir",
    ],
    "suhbat": [
        "Salom, ishlaring qalay?",
        "Ertak aytib ber",
        "Bugungi ob-havo qanday?",
        "Vaqt nechi bo'ldi?",
        "O'zingni tanishtir",
    ]
}

# To'ldiruvchilar
ENTITIES = {
    "papka": ["Downloads", "Documents", "Ish stoli", "Rasmlar", "Musiqa"],
    "fayl_turi": ["oxirgi rasmni", "hujjatlarni", "videoni", "taqdimotni"],
    "fayl_nomi": ["hisobot.docx", "logo.png", "main.py", "presentation.pptx"],
    "dastur": ["Chrome", "Telegram", "Terminal", "VS Code", "Fayl menejeri"],
    "holat": ["o'chir", "qayta yukla", "uxlat"],
    "daraja": [10, 20, 30, 50],
    "yo'nalish": ["oshir", "pasaytir", "ko'tar", "tushir"],
    "harakat": ["yop", "pastga tushur", "kattalashtir", "yashir"],
    "element": ["oyna", "vkladka"],
    "sayt": ["kun.uz", "daryo.uz", "google.com", "youtube.com"],
    "qidiruv_sozi": ["ob-havo", "Python darslari", "yangi kinolar"],
}

def generate_commands(num_commands):
    """Belgilangan miqdorda unikal buyruqlar generatsiya qiladi."""
    generated_commands = set()
    
    while len(generated_commands) < num_commands:
        category = random.choice(list(COMMANDS_BLUEPRINT.keys()))
        template = random.choice(COMMANDS_BLUEPRINT[category])
        
        command = template
        # Andozadagi to'ldiruvchilarni almashtirish
        placeholders = [p.strip('{}') for p in template.split() if '{' in p and '}' in p]
        
        # Agar suhbat kategoriyasi bo'lsa, to'ldiruvchilar kerak emas
        if category == "suhbat":
            generated_commands.add(template)
            continue
            
        for placeholder in placeholders:
            if placeholder in ENTITIES:
                command = command.replace(f"{{{placeholder}}}", str(random.choice(ENTITIES[placeholder])), 1)
        
        # Bir xillikni oldini olish uchun ozgina o'zgartirish
        if random.random() > 0.8:
            command += " iltimos"
        
        generated_commands.add(command.capitalize())
        
    return list(generated_commands)

if __name__ == "__main__":
    # 40,000 o'rniga, tizimni ko'rsatish uchun 500 ta sifatli namuna
    num_to_generate = 500
    commands = generate_commands(num_to_generate)
    
    txt_filename = "buyruqlar.txt"
    zip_filename = "buyruqlar.zip"
    
    # TXT faylga yozish
    with open(txt_filename, "w", encoding="utf-8") as f:
        for cmd in commands:
            f.write(cmd + "\n")
            
    print(f"{len(commands)} ta buyruq '{txt_filename}' fayliga yozildi.")
    
    # ZIP arxivga joylash
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(txt_filename)
        
    print(file=}