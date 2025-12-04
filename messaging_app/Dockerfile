# استخدم Python 3.10
FROM python:3.10

# حدّد مجلد العمل
WORKDIR /app

# انسخ requirements وثبّتهم
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# انسخ باقي الكود
COPY . .

# عرف البورت اللي Django هيشتغل عليه
EXPOSE 8000

# شغّل السيرفر على 0.0.0.0:8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]