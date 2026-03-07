import shlex

def sanitize_shell_input(text: str) -> str:
    """
    Matnni qobiq (shell) uchun xavfsiz holatga keltiradi.
    Bu buyruq in'ektsiyasining oldini olishga yordam beradi.
    Faqatgina bitta argumentni tozalash uchun mo'ljallangan.
    """
    # Matnni qobiq uchun xavfsiz formatga keltiradi, masalan, ' a b "c" ' -> ''\' a b "c" '\''
    return shlex.quote(text)

def is_safe_path(path: str) -> bool:
    """
    Yo'l (path) xavfsizligini tekshiradi. Hozircha oddiy tekshiruv.
    Masalan, `../` kabi yuqori katalogga chiqishni cheklash.
    """
    # Hozircha bu funksiya murakkablashtirilmagan, ammo kelajakda
    # fayl tizimiga oid buyruqlar uchun kengaytirilishi mumkin.
    if ".." in path:
        return False
    return True

# Test uchun
if __name__ == "__main__":
    dangerous_input = "my_file; rm -rf /"
    sanitized = sanitize_shell_input(dangerous_input)
    
    print(f"Original : {dangerous_input}")
    print(f"Tozalangan: {sanitized}")
    # Natija: 'my_file; rm -rf /' -> "'my_file; rm -rf /'"
    # Bu butun satrni bitta argument sifatida qabul qiladi va `rm` buyrug'i ishlamaydi.

    print("\nPath tekshiruvi:")
    print(f"'/etc/passwd' xavfsizmi? -> {is_safe_path('/etc/passwd')}")
    print(f"'../../secret.txt' xavfsizmi? -> {is_safe_path('../../secret.txt')}")
