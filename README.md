# 🤖 NexusAI Telegram Bot

بوت تلقرام يعمل بالذكاء الاصطناعي عبر Groq API (مجاني وسريع).

---

## 📁 الملفات
```
bot.py            — الكود الرئيسي
requirements.txt  — المكتبات المطلوبة
README.md         — هذا الملف
```

---

## ⚙️ طريقة التشغيل

### 1. ضع المتغيرات البيئية
سواء على جهازك أو على منصة الاستضافة:
```
TELEGRAM_TOKEN = توكن البوت من BotFather
GROQ_API_KEY   = مفتاح API من console.groq.com
```

### 2. تثبيت المكتبات
```bash
pip install -r requirements.txt
```

### 3. تشغيل البوت
```bash
python bot.py
```

---

## ☁️ استضافة مجانية على Render

1. ارفع الملفات على GitHub
2. اذهب إلى [render.com](https://render.com) وأنشئ **Web Service** جديد
3. اختر الريبو، وفي الإعدادات:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
4. أضف المتغيرات البيئية في قسم **Environment**:
   - `TELEGRAM_TOKEN`
   - `GROQ_API_KEY`
5. اضغط **Deploy** ✅

---

## 🎯 أوامر البوت
| الأمر | الوظيفة |
|-------|---------|
| `/start` | تشغيل البوت والترحيب |
| `/help` | عرض المساعدة |
| `/clear` | مسح سجل المحادثة |

---

## 🧠 النموذج المستخدم
`llama-3.3-70b-versatile` من Groq — مجاني ويدعم العربية والإنجليزية.
