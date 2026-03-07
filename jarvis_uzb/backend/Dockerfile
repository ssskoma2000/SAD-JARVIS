# 1-bosqich: Asosiy Python muhitini o'rnatish
FROM python:3.10-slim

# Ishchi papkani o'rnatish
WORKDIR /app

# requirements.txt faylini nusxalash va kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Butun backend ilovasini nusxalash
COPY ./app /app/app

# Ilova ishga tushadigan port
EXPOSE 8000

# Ilovani ishga tushirish buyrug'i
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]