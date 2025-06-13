from telegram import (
    Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters, ConversationHandler
)

import json

BOT_TOKEN = "7801563155:AAGi7B0AnccT3LSY5rUjPK04ZsPTauO3Weg"

# Bosqichlar
LANG, NAME, SURNAME, PHONE, REGION, SPECIALTY, DOCTOR = range(7)

# Doctor JSON ma'lumotlari (namuna)
doctors_data = {
    "Toshkent": {
        "Kardiolog": {
            "Dr. Azizbek": 123456789,
            "Dr. Malika": 987654321
        },
        "Nevropatolog": {
            "Dr. Shavkat": 111222333
        }
    },
    "Andijon": {
        "Urolog": {
            "Dr. Jamshid": 333222111
        }
    }
}

users = {}

languages = {
    "uz": {
        "start": "Salom! DoctorFinderBotga xush kelibsiz!",
        "ask_name": "Ismingizni kiriting:",
        "ask_surname": "Familiyangizni kiriting:",
        "ask_phone": "Telefon raqamingizni yuboring:",
        "choose_region": "Viloyatingizni tanlang:",
        "choose_specialty": "Doktor turini tanlang:",
        "choose_doctor": "Doktorni tanlang:",
        "sent": "Ma'lumotlaringiz doktorga yuborildi. Tez orada siz bilan bog‘lanishadi."
    },
    "ru": {
        "start": "Здравствуйте! Добро пожаловать в DoctorFinderBot!",
        "ask_name": "Введите ваше имя:",
        "ask_surname": "Введите вашу фамилию:",
        "ask_phone": "Отправьте ваш номер телефона:",
        "choose_region": "Выберите ваш регион:",
        "choose_specialty": "Выберите тип врача:",
        "choose_doctor": "Выберите врача:",
        "sent": "Ваши данные были отправлены врачу. Скоро он свяжется с вами."
    },
    "en": {
        "start": "Hello! Welcome to DoctorFinderBot!",
        "ask_name": "Please enter your first name:",
        "ask_surname": "Please enter your last name:",
        "ask_phone": "Send your phone number:",
        "choose_region": "Select your region:",
        "choose_specialty": "Select a doctor type:",
        "choose_doctor": "Select a doctor:",
        "sent": "Your information has been sent to the doctor. They will contact you soon."
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz")],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")]
    ]
    await update.message.reply_text("Tilni tanlang / Select language / Выберите язык:", reply_markup=InlineKeyboardMarkup(keyboard))
    return LANG

async def lang_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lang_code = update.callback_query.data.split("_")[1]
    context.user_data["lang"] = lang_code
    users[update.effective_user.id] = {"lang": lang_code}
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(languages[lang_code]["ask_name"])
    return NAME

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id]["name"] = update.message.text
    await update.message.reply_text(languages[context.user_data["lang"]]["ask_surname"])
    return SURNAME

async def surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id]["surname"] = update.message.text
    button = KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)
    markup = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(languages[context.user_data["lang"]]["ask_phone"], reply_markup=markup)
    return PHONE

async def phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.contact.phone_number if update.message.contact else update.message.text
    users[update.effective_user.id]["phone"] = phone_number

    # Viloyatlar tugmalari
    regions = list(doctors_data.keys())
    keyboard = [[InlineKeyboardButton(region, callback_data=f"region_{region}")] for region in regions]
    await update.message.reply_text(languages[context.user_data["lang"]]["choose_region"], reply_markup=InlineKeyboardMarkup(keyboard))
    return REGION
