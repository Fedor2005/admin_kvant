import telebot
import phonenumbers
import time
import petrovna


def check_date(date):
    date = date.replace(' ', '')
    try:
        x = time.strptime(date, '%d.%m.%Y')
        return date
    except ValueError:
        return False


def check_phone_number(number):
    if number[0] == '8':
        number = number.replace('8', '+7', 1)
    if len(number) == 10:
        number = '+7' + number
    number_parse = phonenumbers.parse(number)
    if phonenumbers.is_valid_number(number_parse):
        return number
    else:
        return False


def check_snils(snils):
    snils = snils.replace('-', '')
    snils = snils.replace(' ', '')
    if petrovna.validate_snils(snils):
        return snils
    else:
        return False


from settings import TOKEN

bot = telebot.TeleBot(TOKEN)

A = ['Записаться']
keyboard1 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard1.row(A[0])

A = ['М', 'Ж']
keyboard6 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard6.row(A[0], A[1])

A = ['Да', 'Нет']
keyboard2 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard2.row(A[0], A[1])

A = ['1 смена', '2 смена']
keyboard3 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard3.row(A[0], A[1])

A = ['IT', 'ГЕО', 'Промышленный дизайн', 'VR/AR-реальность', 'Хайтек', 'Промробоквант']
keyboard4 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard4.row(A[0], A[1], A[2], A[3], A[4], A[5])

A = ['Базовый', 'Продвинутый', 'Углублённый', 'Углублённый 2.0']
keyboard5 = telebot.types.ReplyKeyboardMarkup(False, False)
keyboard5.row(A[0], A[1], A[2], A[3])


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Доброго времени суток! Если Вы хотите оставить заявку на обучение в кванториуме нажмите на кнопку записаться!',
                     reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def reg(message):
    if message.text == "Записаться":
        msg = bot.send_message(message.chat.id, 'Укажите ФИО ребёнка, который желает обучаться в кванториуме')
        bot.register_next_step_handler(msg, FIO)


def FIO(message):
    x = message.text
    x.strip()
    y = x.split()
    a = x.replace(" ", "")
    if a.isalpha() and len(y) == 3:
        main_list = [x]
        msg = bot.send_message(message.chat.id, text="Укажите пол ребенка М или Ж",
                               reply_markup=keyboard6)
        bot.register_next_step_handler(msg, sex, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, FIO)


def sex(message, main_list):
    x = message.text
    x.strip()
    if x == 'М' or x == 'Ж':
        main_list.append(x)
        msg = bot.send_message(message.chat.id, text="Укажите дату рождения ребёнка в формате чч.мм.гггг")
        bot.register_next_step_handler(msg, dr, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, sex, main_list)


def dr(message, main_list):
    message.text.strip()
    date = check_date(message.text)
    if date:
        main_list.append(date)
        msg = bot.send_message(message.chat.id,
                               text="Укажите номер телефона ребёнка в формате +7xxxxxxxxxx(вместо х цифры)")
        bot.register_next_step_handler(msg, tel_reb, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные! Попробуйте ещё раз")
        bot.register_next_step_handler(msg, dr, main_list)


def tel_reb(message, main_list):
    x = message.text
    x.strip()
    number = check_phone_number(x)
    if number:
        main_list.append(number)
        msg = bot.send_message(message.chat.id, text="Укажите, в какой школе учится ребёнок")
        bot.register_next_step_handler(msg, fschool, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, tel_reb, main_list)


def fschool(message, main_list):
    schools = ["1", "2", "3", "4", "5", "6", "7", "9", "10", "11", "12", "14", "15", "16", "17", "20", "21", "22", "26",
               "28", "29", "32", "36", "40"]
    school = message.text
    school.strip()
    if school in schools:
        main_list.append(school)
        msg = bot.send_message(message.chat.id, text="Укажите номер класса, в котором учится ребёнок")
        bot.register_next_step_handler(msg, school_class, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, fschool, main_list)


def school_class(message, main_list):
    classes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    class_ = message.text
    class_.strip()
    if class_ in classes:
        main_list.append(class_)
        msg = bot.send_message(message.chat.id, text="Укажите номер сертификата ПФДО")
        bot.register_next_step_handler(msg, PFDO, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, school_class, main_list)


def PFDO(message, main_list):
    pfdo = message.text
    pfdo.strip()
    if len(pfdo) == 10 and pfdo.isdigit():
        main_list.append(pfdo)
        msg = bot.send_message(message.chat.id, text="Укажите, с какой смены обучается ребенок в школе.",
                               reply_markup=keyboard3)
        bot.register_next_step_handler(msg, smena, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, PFDO, main_list)


def smena(message, main_list):
    x = message.text
    x.strip()
    if x:
        if x == '1 смена':
            x = '1'
        elif x == '2 смена':
            x = '2'
        else:
            msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз.",
                                   reply_markup=keyboard3)
            bot.register_next_step_handler(msg, smena, main_list)
        main_list.append(x)
        msg = bot.send_message(message.chat.id, text="Укажите адрес проживания")
        bot.register_next_step_handler(msg, adress, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз.")
        bot.register_next_step_handler(msg, smena, main_list)


def adress(message, main_list):
    adress = message.text
    main_list.append(adress)
    msg = bot.send_message(message.chat.id, text="Укажите номер снилса ребёнка")
    bot.register_next_step_handler(msg, snils, main_list)


def snils(message, main_list):
    x = message.text
    x.strip()
    snils = check_snils(x)
    if snils:
        main_list.append(snils)
        msg = bot.send_message(message.chat.id, text="У вашего ребёнка есть паспорт?", reply_markup=keyboard2)
        bot.register_next_step_handler(msg, passport_roj, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, snils, main_list)


def passport_roj(message, main_list):
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, text="Введите серию и номер паспорта ребёнка через пробел")
        bot.register_next_step_handler(msg, series_number, main_list)

    elif message.text == "Нет":
        msg = bot.send_message(message.chat.id, text="Введите номер свидетельсвта о рождении ребёнка")
        bot.register_next_step_handler(msg, birth_certificate, main_list)

    else:
        msg = bot.send_message(message.chat.id,
                               text='Некорректно введённые данные. Попробуйте ещё раз. Воспользуйтесь кнопками или напишите "Да" или "Нет"',
                               reply_markup=keyboard2)
        bot.register_next_step_handler(msg, passport_roj, main_list)


def series_number(message, main_list):
    n = message.text
    n.strip()
    a = n.replace(" ", "")
    s = a
    s.split()
    if a.isdigit() and len(s) == 10:
        main_list.append(s)
        msg = bot.send_message(message.chat.id, text="Введите дату выдачи паспорта в формате чч.мм.гггг")
        bot.register_next_step_handler(msg, date_of_issue, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, series_number, main_list)


def date_of_issue(message, main_list):
    message.text.strip()
    date = check_date(message.text)
    if date:
        main_list.append(date)
        msg = bot.send_message(message.chat.id, text="Введите кем был ввыдан паспорт")
        bot.register_next_step_handler(msg, issued, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, date_of_issue, main_list)


def issued(message, main_list):
    x = message.text
    x.strip()
    a = x.replace(" ", "")
    if a.isalpha():
        main_list.append(x)
        msg = bot.send_message(message.chat.id, text="Выберите направление, которое будет изучать ребёнок",
                               reply_markup=keyboard4)
        bot.register_next_step_handler(msg, kvant, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, issued, main_list)


def birth_certificate(message, main_list):
    n = message.text
    n.strip()
    s = n
    s.split()
    a = n.replace(" ", "")
    if a.isdigit() and len(s) == 6:
        main_list.append(a)
        msg = bot.send_message(message.chat.id,
                               text="Выберите направление, которое будет изучать ребёнок на панели кнопок. Если они у Вас не отображаются, нажмите на квадратик, который неаходится слева от скрепки.",
                               reply_markup=keyboard4)
        bot.register_next_step_handler(msg, kvant, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, birth_certificate, main_list)


def kvant(message, main_list):
    msg = bot.send_message(message.chat.id,
                           text="Выберите уровень, на котором будет обучаться ребёнок на панели кнопок. Если они у Вас не отображаются, нажмите на квадратик, который неаходится слева от скрепки.",
                           reply_markup=keyboard5)
    faculty = message.text
    main_list.append(faculty)
    bot.register_next_step_handler(msg, level, main_list)


def level(message, main_list):
    msg = bot.send_message(message.chat.id, text="Введите ФИО представителя")
    main_list.append(message.text)
    bot.register_next_step_handler(msg, FIO_rod1, main_list)


def FIO_rod1(message, main_list):
    x = message.text
    x.strip()
    y = x.split()
    a = x.replace(" ", "")
    if a.isalpha() and len(y) == 3:
        main_list.append(x)
        msg = bot.send_message(message.chat.id, text="Укажите дату рождения представителя в формате чч.мм.гггг")
        bot.register_next_step_handler(msg, dr_rod1, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, FIO_rod1, main_list)


def dr_rod1(message, main_list):
    a = message.text.strip()
    a = check_date(a)
    if a:
        main_list.append(a)
        msg = bot.send_message(message.chat.id, text="Введите номер телефона представителя")
        bot.register_next_step_handler(msg, tel_rod1, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные! Попробуйте ещё раз")
        bot.register_next_step_handler(msg, dr_rod1, main_list)


def tel_rod1(message, main_list):
    x = message.text
    x.strip()
    x = check_phone_number(x)
    if x:
        main_list.append(x)
        msg = bot.send_message(message.chat.id, text="Укажите серию и номер паспорта представителя")
        bot.register_next_step_handler(msg, series_number_rod, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, tel_rod1, main_list)


def series_number_rod(message, main_list):
    n = message.text.strip()
    a = n.replace(" ", "")
    s = a
    s.split()
    if a.isdigit() and len(s) == 10:
        main_list.append(s)
        msg = bot.send_message(message.chat.id, text="Введите дату выдачи паспорта в формате чч.мм.гггг")
        bot.register_next_step_handler(msg, date_of_issue_rod, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, series_number_rod, main_list)


def date_of_issue_rod(message, main_list):
    date = message.text.strip()
    date = check_date(date)
    if date:
        main_list.append(date)
        msg = bot.send_message(message.chat.id, text="Введите кем был ввыдан паспорт")
        bot.register_next_step_handler(msg, issued_rod, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, date_of_issue_rod, main_list)


def issued_rod(message, main_list):
    x = message.text
    x.strip()
    a = x.replace(" ", "")
    if a.isalpha():
        main_list.append(x)
        msg = bot.send_message(message.chat.id, text="Есть 2 представитель?", reply_markup=keyboard2)
        bot.register_next_step_handler(msg, pred, main_list)

    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, issued_rod, main_list)


def pred(message, main_list):
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, text="Укажите ФИО второго представителя")
        bot.register_next_step_handler(msg, FIO_rod2, main_list)
    else:
        bot.send_message(message.chat.id, text="Обрабатываем Ваш запрос...")


def FIO_rod2(message, main_list):
    x = message.text
    x.strip()
    y = x.split()
    a = x.replace(" ", "")
    if a.isalpha() and len(y) == 3:
        main_list.append(x)
        msg = bot.send_message(message.chat.id, text="Введите номер телефона представителя")
        bot.register_next_step_handler(msg, tel_rod2, main_list)
    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, FIO_rod2, main_list)


def tel_rod2(message, main_list):
    x = message.text
    x.strip()
    x = check_phone_number(x)
    if x:
        main_list.append(x)
        bot.send_message(message.chat.id, text="Обрабатываем Ваш запрос...")
        print(main_list)
        import sqlite3
        conn = sqlite3.connect('kvant.db')
        c = conn.cursor()
        lst = ["'" + x.replace(' ', '_').replace('.', '-') + "'" for x in main_list]
        c.execute('INSERT or IGNORE into people VALUES (' + f"{', '.join(lst)}" + ')')
        conn.commit()
        conn.close()


    else:
        msg = bot.send_message(message.chat.id, text="Некорректно введённые данные. Попробуйте ещё раз")
        bot.register_next_step_handler(msg, tel_rod2, main_list)


bot.polling()
