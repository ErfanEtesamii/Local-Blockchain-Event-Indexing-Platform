# استفاده از نسخه سبک پایتون
FROM python:3.11-slim

# تعیین مسیر کاری داخل کانتینر
WORKDIR /app

# نصب کتابخانه flask
RUN pip install flask

# کپی کردن فایل برنامه به داخل کانتینر
COPY main.py .

# باز کردن پورت 8080 برای دسترسی خارجی
EXPOSE 8080

# دستور اجرای برنامه
CMD ["python", "main.py"]