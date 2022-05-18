import os

#from cs50 import SQL
import sqlite3 # замість cs50
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from my_helpers import apology, login_required

app = Flask(__name__)
app.secret_key = "super secret key"

if __name__ == '__main__':
    app.debug = True
    app.run()

## Так було на CS50 (З їх костилями щодо SQL)
#Configure CS50 Library to use SQLite database
#dbb = sqlite3.connect("sqlite:///club.db")
## А так на реальному сервері - https://www.pythonanywhere.com/
dbb = sqlite3.connect('D:\\VS_Code\\project_Club\\venv\\datbase\\club.db', check_same_thread=False)
db = dbb.cursor()

""" Прогноз на матч та історія прогнозів (зараз це index) """
@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # якщо звичайни користувач
    if session.get("user_id") is not None:
        
        # коли приходять дані для прогноза
        if request.method == "POST":

            # отримуємо дані прогноз на матч - (Господарі та Гості)
            inp_prognoz_home = request.form.get("home")
            inp_prognoz_visitors = request.form.get("visitor")
            inp_razom = request.form.get("razom")
            inp_prognoz_type = request.form.get("gridRadios")

            # чекаємо базу для додаткової інфи
            check_matches = db.execute ("SELECT match_id, round, mtch_round FROM m3 WHERE razom =:razom", dict(razom = inp_razom))
            check_matches = check_matches.fetchone()

            # витягуємо id матчу та номер тура
            match_id = check_matches[0]
            tur_nomer = check_matches[1]
            match_round = check_matches[2]

            # ДЛЯ НЕДОПУЩЕННЯ ОДНОЧАСНО ДВОХ ТИПІВ СТАВОК
            # якщо в юзеря є прогнози, то чекаємо їх тип (ординар чи експреси - Choo-choo), і блочим інший
            # тільки унікальні значення витягуємо
            prognoz_type = db.execute("SELECT DISTINCT prognoz_type FROM p3 WHERE user_id = :user_id AND tur = :tur",\
                                    dict(user_id=session["user_id"], tur=tur_nomer))
            prognoz_type = prognoz_type.fetchone()

            # перевіряємо базу на наявність двох типві прогнозів (про всяк випадок), і якщо є кидаємо помилку
            if prognoz_type is not None:
                n_prognoz_type = len(prognoz_type)

                if n_prognoz_type > 1:
                    return apology("no ordinar and express", 600)

                # достаємо тип прогнозу з бази
                if len(prognoz_type) == 1:
                    type_v_bazi = prognoz_type[0]

                    # блок на експреси - Choo-choo )))
                    if type_v_bazi == 'Ординар' and inp_prognoz_type == 'exp':
                        return apology("Ordinar only...", 400)

                    # блок на ординари
                    elif type_v_bazi == 'Експрес' and inp_prognoz_type == 'ord':
                        return apology("Expres only...", 400)

            # чекаємо актуальний час на момент зміни рпогноза (без мілісекунд)
            date_and_time_now = datetime.now()
            date_and_time_now = date_and_time_now.replace(microsecond=0)

            # коригуємо часовий пояс (додаємо +2 години)
            timestamp = datetime.timestamp(date_and_time_now)
            timestamp = timestamp + 7200                        ###60 сек * 60 хв * 2 години
            date_and_time_now = datetime.fromtimestamp(timestamp)

            # якщо прогноз - Сhoo-Choo (експрес)
            if inp_prognoz_type == 'exp':
                # пишемо прогноз в базу (експрес)
                add_prognoz = db.execute ("INSERT INTO p3 (oper_id, match_id, user_id, teams, home, guest, tur, status, time, mtch_round, prognoz_type)\
                                        VALUES (NULL, :match_id, :user_id, :teams, :home, :guest, :tur, 'new', :time, :mtch_round, :prognoz_type)",\
                                        dict(match_id=match_id, user_id=session["user_id"], teams=inp_razom, home=inp_prognoz_home,\
                                        guest=inp_prognoz_visitors, tur=tur_nomer, time=date_and_time_now, mtch_round=match_round, prognoz_type='Експрес'))
                dbb.commit()

                ### ЗМІНИТИ ТИП ДАНИХ в SQL.p3.time ПІСЛЯ ТУРНІРА
                # коригуємо часовий пояс для прогноза
                #time_correction = db.execute(SELECT time FROM p3 WHERE match_id = :match_id, user_id = :user_id)

            # якщо прогноз - ординар, тобто звичайний
            if inp_prognoz_type == 'ord':
                # пишемо прогноз в базу
                add_prognoz = db.execute ("INSERT INTO p3 (oper_id, match_id, user_id, teams, home, guest, tur, status, time, mtch_round, prognoz_type)\
                                        VALUES (NULL, :match_id, :user_id, :teams, :home, :guest, :tur, 'new', :time, :mtch_round, :prognoz_type)",\
                                        dict(match_id=match_id, user_id=session["user_id"], teams=inp_razom, home=inp_prognoz_home,\
                                        guest=inp_prognoz_visitors, tur=tur_nomer, time=date_and_time_now, mtch_round=match_round, prognoz_type='Ординар'))
                dbb.commit()

                ### ЗМІНИТИ ТИП ДАНИХ в SQL.p3.time ПІСЛЯ ТУРНІРА
                # коригуємо часовий пояс для прогноза
                #time_correction = db.execute("UPDATE p3 SET time = :time WHERE match_id = :match_id AND user_id = :user_id",\
                #                            dict(time=date_and_time_now, match_id=match_id, user_id=session["user_id"]))
                #dbb.commit()

                #time_correction = db.execute("SELECT time FROM p3 WHERE match_id = :match_id AND user_id = :user_id",\
                #                              dict(match_id=match_id, user_id=session["user_id"]))
                #time_correction = time_correction.fetchone()
                #print("time_correction =", time_correction)
                #print(type(time_correction))

            # перевіряємо прогнози від юзверя (для виведення)
            prognoz_check = db.execute("SELECT * FROM p3 WHERE user_id =:user_id ORDER BY tur DESC, match_id ASC",\
                                        dict(user_id = session["user_id"]))
            prognoz_check = prognoz_check.fetchall()

            # отримаємо доступні матчі для прогноза
            dostupni_matchi = db.execute("SELECT * FROM m3 WHERE availability =:yes ORDER BY mtch_round ASC", dict(yes = 'yes'))
            dostupni_matchi = dostupni_matchi.fetchall()

            # ДЛЯ актуального списка матчів на прогноз
            # якщо в юзверя були прогнози, то створюємо оновлений список доступних матчів для прогноза
            if len(prognoz_check) != 0:

                # допоміжні змінні
                n_dostupni = len(dostupni_matchi)
                n_prognoz = len(prognoz_check)
                new_dostupni_matchi = dostupni_matchi.copy() # копія списка доступних матчів для видалення з нього прогнозів

                # беремо і перевіряємо кожем доступний матч із зробленим прогнозом (поматчево)
                for i in range (n_dostupni):
                    razom = dostupni_matchi[i][5]

                    for y in range (n_prognoz):
                        teams = prognoz_check[y][3]

                        # якщо є співпадіння (доступний матч і прогноз) то починаєм цикл на видалення
                        if razom == teams:
                            # визначаєм величину допоміжного списка - кожен раз заново (бо є видалення)
                            new_len = len(new_dostupni_matchi)

                            # для кожного елемента в доп списку шукаємо елемент на видалення
                            for k in range(new_len):
                                if new_dostupni_matchi[k][5] == teams:
                                    del new_dostupni_matchi[k]
                                    break

                # треба очистить список доступних матчів
                dostupni_matchi.clear()
                # вставляємо матчі що залишилася доступні для прогноза
                dostupni_matchi = new_dostupni_matchi.copy()

            # вивід сторінки з доступними матчами для прогноза та зробленими прогнозами від юзверя
            return render_template("index.html", rows=prognoz_check, match_rows=dostupni_matchi)

        # Перша відкриття сторінки, і якщо пререйшли просто по ссилі
        else:

            # перевіряємо прогнози від юзверя (для виведення)
            prognoz_check = db.execute("SELECT * FROM p3 WHERE user_id =:user_id ORDER BY tur DESC, match_id ASC",\
                                        dict(user_id = session["user_id"]))
            prognoz_check = prognoz_check.fetchall()

            # отримаємо доступні матчі для прогноза
            dostupni_matchi_start = db.execute("SELECT * FROM m3 WHERE availability =:yes ORDER BY mtch_round ASC", dict(yes = 'yes'))
            dostupni_matchi_start = dostupni_matchi_start.fetchall()

            # розміри баз
            n_dostupni = len(dostupni_matchi_start)
            n_prognoz = len(prognoz_check)

            # якщо в юзверя були прогнози, то створюємо оновлений список доступних матчів для прогноза
            if len(prognoz_check) != 0:

                # допоміжні змінні
                n_dostupni = len(dostupni_matchi_start)
                n_prognoz = len(prognoz_check)
                new_dostupni_matchi = dostupni_matchi_start.copy() # копія списка доступних матчів для видалення з нього прогнозів
                # беремо і перевіряємо кожем доступний матч із зробленим прогнозом (поматчево)
                for i in range (n_dostupni):
                    razom = dostupni_matchi_start[i][5]

                    for y in range (n_prognoz):
                        teams = prognoz_check[y][3]

                        # якщо є співпадіння (доступний матч і прогноз) то починаєм цикл на видалення
                        if razom == teams:
                            # визначаєм величину допоміжного списка - кожен раз заново (бо є видалення)
                            new_len = len(new_dostupni_matchi)

                            # для кожного елемента в доп списку шукаємо елемент на видалення
                            for k in range(new_len):
                                if new_dostupni_matchi[k][5] == teams:
                                    del new_dostupni_matchi[k]
                                    break

                # треба очистить список доступних матчів
                dostupni_matchi_start.clear()
                # вставляємо матчі що залишилася доступні для прогноза
                dostupni_matchi_start = new_dostupni_matchi.copy()

            # рендерим сторінку
            return render_template("index.html", rows=prognoz_check, match_rows=dostupni_matchi_start)
    
    # якщо зайшов адмін
    if session.get("admin_name") is not None:
        return redirect("fintable")

""" ГОТОВО - реєстрація нового користувача """
@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id - про всяк випадок
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # якщо пусте поле - ім'я користувача
        inp_username = request.form.get("username")
        if len(inp_username) < 1:
            return apology("Use correct username, min 1 symbol (A-z, 0-9)", 400)

        # якщо пусте перше поле - пароль користувача
        inp_password = request.form.get("password")
        if len(str(inp_password)) < 1:
            return apology("Use not empty pass", 400)

        # якщо друге поле пароль користувача є пустим чи не збігаєтсья з першим
        confirm_password = request.form.get("confirmation")
        if len(confirm_password) < 1 or confirm_password != inp_password:
            return apology("Use correct confirmation", 400)

        # умова по мінімальній кількості символів в паролі
#        if len(str(inp_password)) < 5:
#            return apology("Use correct pass, min 5 symbols (A-z, 0-9)", 400)

        # умова по мінімальній кількості цифр в паролі
#        counter = 0
#        x = len(str(inp_password))
#        for i in range(x):
#            if inp_password[i].isdigit() == True:
#                counter += 1

#        if counter < 3:
#            return apology("Use min 3 number in pass", 400)

        # для адмінки
        if request.form.get("admin") == 'yes':
            # шукаємо в базі введений логін
            db_check_admin_name = db.execute("SELECT * FROM adminka WHERE admin_name =:username", dict(username=inp_username))
            db_check_admin_name = db.fetchone()

            # якщо є то виводимо помилку
            if db_check_admin_name:
                return apology("Sorry this Username was occupied before", 400)

            # якщо логіна немає, то нарешті реєструємо нового користувача
            if not db_check_admin_name:

                # генеруємо хеш пароля
                new_hash = generate_password_hash(inp_password)

                # додаємо адмінчика в базу користувачів
                add_admin_db = db.execute("INSERT INTO adminka (admin_name,admin_pass_hash) VALUES (:name, :thash)", dict(name=inp_username, thash=new_hash))

                # і еренаправляємо на сторінку входу
                return render_template("login.html")

        else:
            # шукаємо в базі введений логін
            db_check_username = db.execute("SELECT * FROM users WHERE user_name =:username", dict(username=inp_username))
            db_check_username = db.fetchone()

            # якщо є то виводимо помилку
            if db_check_username is not None:
                return apology("Sorry this Username was occupied before", 400)

            # якщо логіна немає, то нарешті реєструємо нового користувача
            if db_check_username == None:

                # генеруємо хеш пароля
                new_hash = generate_password_hash(inp_password)

                # додаємо юзверя в базу користувачів
                add_user_db = db.execute("INSERT INTO users (user_name, hash) VALUES (:name, :thash)", dict(name=inp_username, thash=new_hash))

                # готовимо дані для запису в підсумкову табличку
                user_id_check = db.execute("SELECT user_id FROM users WHERE user_name =:username", dict(username=inp_username))
                dbb.commit()
                user_id_check = user_id_check.fetchone()

                # витягуємо user_id для запису в підсумкову табличку (fintab)
                user_id_check2 = user_id_check[0]

                # записуємо всі дані про користувача в підсумкову табличку (fintab)
                add_user_ft = db.execute("INSERT INTO fintab (user_id, user_name, total_points, total_matchi_prognoz, vgad_rah,\
                                          vgad_resultat, aver_bal_za_match, potential_points, vgad_expresy, nevgad_expres, guru_turu)\
                                          VALUES (:usid, :name, 0, 0, 0, 0, 0, 0, 0, 0, 0)", dict(usid=user_id_check2, name=inp_username,))

                # і перенаправляємо на сторінку входу
                return render_template("login.html")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


""" ГОТОВО - вхід користувача """
@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # перевірка якщо входить АДМІН
        if request.form.get("username") == "admin111":

            # Query database for username
            admin_rows = db.execute("SELECT * FROM adminka WHERE admin_name = :username", dict(username=request.form.get("username")))
            admin_rows = admin_rows.fetchone()

            # no admin in database
            if admin_rows is None:
                return apology("no user, please register", 403)

            # Ensure username exists and password is correct
            if check_password_hash(admin_rows[2], request.form.get("password")) == False:
                return apology("invalid username and/or password", 403)

            # Remember which user has logged in
            session["admin_name"] = admin_rows[0]

            # Redirect user to home page
            return redirect("fintable")

        # перевірка якщо це звичайні юзери
        else:

            # Query database for username
            user_rows = db.execute("SELECT * FROM users WHERE user_name = :username", dict(username=request.form.get("username")))
            user_rows = user_rows.fetchone()

            # no user in database
            if user_rows is None:
                return apology("no user, please register", 403)

            # Ensure username exists and password is correct
            if check_password_hash(user_rows[2], request.form.get("password")) == False:
                return apology("invalid username and/or password", 403)

            # Remember which user has logged in
            session["user_id"] = user_rows[0]

            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


""" ГОТОВО - вихід користувача (кінець сесії) """
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


""" (fintable) - підсумкова табличка (з прибамбасами для адміна) """
@app.route("/fintable")
@login_required
def fintable():

    # витягуємо та сортуємо дані для підсумкової таблички
    fintable = db.execute("SELECT * FROM fintab ORDER BY total_points DESC, vgad_rah DESC, aver_bal_za_match DESC")
    fintable = fintable.fetchall()

    # визначаємо в писуємо місце учасника в табличку для вивода
    n_fintable = len(fintable)
    user_counter = 0
    for i in range (n_fintable):
        user_counter +=1
        temp_list = list(fintable[i])
        temp_list[9] = user_counter
        fintable[i] = tuple(temp_list)
        #fintable[i].insert(9, user_counter) # вже не актуальний шматок кода

    # командний залік
    team_zalik = db.execute("SELECT * FROM teams ORDER BY team_points DESC")
    team_zalik = team_zalik.fetchall()

    # визначаємо в писуємо місце учасника в табличку для вивода
    n_team_zalik = len(team_zalik)
    team_counter = 0
    for y in range (n_team_zalik):
        team_counter +=1
        temp_team_zalik_list = list(team_zalik[y])
        temp_team_zalik_list[3] = team_counter
        team_zalik[y] = tuple(temp_team_zalik_list)
        #team_zalik[y].update({"place": team_counter}) # вже не актуальний шматок кода

    # доповнення для адміна
    if session.get("admin_name") is not None:

        # визначаємо кількість турів для виводу на сторінку
        tur_for_open = db.execute("SELECT DISTINCT round FROM m3")
        tur_for_open = tur_for_open.fetchall()

        # робим список юзерів для гуру тура
        guru_users_list = db.execute("SELECT user_name FROM users ORDER BY user_name ASC")
        guru_users_list = guru_users_list.fetchall()

        # доп інфа для адмінки, для візуалки по відкритому туру
        tury = db.execute("SELECT DISTINCT round, availability FROM m3")
        tury = tury.fetchall()

        # рендерим сторінку
        return render_template("fintable.html", rows=fintable, rows2=tur_for_open, rows3=guru_users_list, rows4=tury, rows5=team_zalik)

    # тільки для юзера
    elif session.get("user_id") is not None:

        # доп інфа для адмінки (візуалка по відкритому туру)
        tury = db.execute("SELECT DISTINCT round, availability FROM m3")
        tury = tury.fetchall()

        # виводим табличку
        return render_template("fintable.html", rows=fintable, rows4=tury, rows5=team_zalik)


""" Зміна вже зробленого прогноза """
@app.route("/changeprognoz", methods=["GET", "POST"])
@login_required
def changeprognoz():

    if request.method == "POST":

        # отримуємо нові дані (прогноз на матч - Господарі та Гості)
        inp_change_prognoz_home = request.form.get("home")
        inp_change_prognoz_visitors = request.form.get("visitor")
        inp_razom = request.form.get("razom")
        inp_delete = request.form.get("delete")
        inp_del_all = request.form.get("del_all")

        # перевіряємо чи не видаляє юзер ВСІ матч взагалі
        if inp_del_all  == 'yes':

            # чекаємо який тур зараз активний
            tur_check = db.execute ("SELECT DISTINCT round FROM m3 WHERE availability = :availability",\
                                     dict(availability='yes'))
            tur_check = tur_check.fetchone()

            # і витягуємо саму цифру
            tur_num_only = tur_check[0]

            # а тепер, видаляємо ВСІ записи по цьому туру з бази прогнозів
            all_prognoz_del = db.execute ("DELETE FROM p3 WHERE user_id = :user_id AND tur = :tur",\
                                           dict(user_id=session["user_id"], tur=tur_num_only))
            dbb.commit()

            # повертаємо на сторінку прогнозів (для прогноза з нуля)
            return redirect("/")

        # чекаємо id матчу, та витягуємо тільки його з бібліотеки
        check_match_id = db.execute ("SELECT match_id FROM m3 WHERE razom =:razom", dict(razom = inp_razom))
        check_match_id = check_match_id.fetchone()

        match_id_only = check_match_id[0]

        # перевіряємо чи видаляє юзер матч взагалі
        if inp_delete == 'yes':

            # видаляємо запис з бази прогнозів
            prognoz_del = db.execute("DELETE FROM p3 WHERE user_id = :user_id AND match_id = :match_id",\
                                      dict(user_id=session["user_id"], match_id=match_id_only))
            dbb.commit()


        # якщо не видаляє, то оновлюємо дані в нашій базі
        else:

            # чекаємо актуальний час на момент зміни рпогноза (без мілісекунд)
            date_and_time_now = datetime.now()
            date_and_time_now = date_and_time_now.replace(microsecond=0)

            # коригуємо часовий пояс (додаємо +2 години)
            timestamp = datetime.timestamp(date_and_time_now)
            timestamp = timestamp + 7200                        ###60 сек * 60 хв * 2 години
            date_and_time_now = datetime.fromtimestamp(timestamp)

            # оновлюємо прогноз в базі
            update_prognoz = db.execute ("UPDATE p3 SET home = :home, guest = :guest, time = :time WHERE user_id = :user_id AND teams = :teams",\
                                          dict(user_id=session["user_id"], home=inp_change_prognoz_home, guest=inp_change_prognoz_visitors,\
                                          teams=inp_razom, time=date_and_time_now))
            dbb.commit()

        ## Готуємо до виводу список доступних матчів для прогноза ##
        # перевіряємо прогнози від юзверя (для виведення)
        prognoz_check_start = db.execute("SELECT * FROM p3 WHERE user_id =:user_id ORDER BY tur DESC, match_id ASC",\
                                          dict(user_id = session["user_id"]))
        prognoz_check_start = prognoz_check_start.fetchall()

        # отримаємо доступні матчі для прогноза
        dostupni_matchi_start = db.execute("SELECT * FROM m3 WHERE availability =:yes ORDER BY mtch_round ASC", dict(yes = 'yes'))
        dostupni_matchi_start = dostupni_matchi_start.fetchall()

        # розміри баз
        n_dostupni = len(dostupni_matchi_start)
        n_prognoz = len(prognoz_check_start)

        # якщо в юзверя були прогнози, то створюємо оновлений список доступних матчів для прогноза
        if len(prognoz_check_start) != 0:

            # допоміжні змінні
            n_dostupni = len(dostupni_matchi_start)
            n_prognoz = len(prognoz_check_start)
            new_dostupni_matchi = dostupni_matchi_start.copy() # копія списка доступних матчів для видалення з нього прогнозів

            # беремо і перевіряємо кожем доступний матч із зробленим прогнозом (поматчево)
            for i in range (n_dostupni):
                razom = dostupni_matchi_start[i][5]

                for y in range (n_prognoz):
                    teams = prognoz_check_start[y][3]

                    # якщо є співпадіння (доступний матч і прогноз) то починаєм цикл на видалення
                    if razom == teams:
                        # визначаєм величину допоміжного списка - кожен раз заново (бо є видалення)
                        new_len = len(new_dostupni_matchi)

                        # для кожного елемента в доп списку шукаємо елемент на видалення
                        for k in range(new_len):
                            if new_dostupni_matchi[k][5] == teams:
                                del new_dostupni_matchi[k]
                                break

            # треба очистить список доступних матчів
            dostupni_matchi_start.clear()
            # вставляємо матчі що залишилася доступні для прогноза
            dostupni_matchi_start = new_dostupni_matchi.copy()

        # рендерим сторінку
        return render_template("index.html", rows=prognoz_check_start, match_rows=dostupni_matchi_start)

    # якщо пререйшли просто по ссилі
    else:
        # витягуємо вже зроблені прогнози від юзверя (для виведення)
        prognoz_check = db.execute("SELECT * FROM p3 WHERE user_id =:user_id AND status =:new ORDER BY match_id ASC",\
                                    dict(user_id = session["user_id"], new = 'new'))
        prognoz_check = prognoz_check.fetchall()

        # рендерим сторінку з витягнутими даними про матчі
        return render_template("changeprognoz.html", prog_rows=prognoz_check)


""" Прогноза на матч від інших членів клубу"""
@app.route("/prognozy_inshyh", methods=["GET", "POST"])
@login_required
def prognozy_inshyh():

    # витягуємо прогнози інших гравців
    prognozy_inshyh = db.execute("SELECT p3.user_id, users.user_name, p3.teams, p3.home, p3.guest, p3.time, p3.mtch_round, p3.tur,\
                                  p3.prognoz_type, p3.bal FROM p3 LEFT JOIN users ON p3.user_id=users.user_id ORDER BY tur DESC,\
                                  user_name ASC, mtch_round ASC")
    prognozy_inshyh = prognozy_inshyh.fetchall()

    # Щоб не дублювати показ прогнозів від залогіненого юзера
    # для звичайного користувача
    if session.get("user_id") is not None:

        # створюємо пустий список для словників з "prognozy_inshyh"
        temp_prognozy_inshyh = []

        # допоміжний список
        n_prognozy_inshyh = len(prognozy_inshyh)

        # перебираємо по одному всі записи
        for i in range (n_prognozy_inshyh):

            # витягуємо user_id
            user_id = prognozy_inshyh[i][0]

            # якщо user_id з прогнозу прогнозів не співпадає за user_id залогіненого юзера
            if user_id != session["user_id"]:
                # то додаємо його для показу на сторінці
                temp_prognozy_inshyh.append(prognozy_inshyh[i])

        # очищаємо список прогнозів
        prognozy_inshyh.clear()

        # оновлюємо список матчів що залишилася доступні для прогноза
        prognozy_inshyh = temp_prognozy_inshyh.copy()

    # і рендерим сторінку
    return render_template("prognozy_inshyh.html", rows=prognozy_inshyh)


""" Обраховуємо бали корустувачів (як зіграли ставки) """
@app.route("/rozrahunky", methods=["GET", "POST"])
@login_required
def rozrahunky():

    if request.method == "POST":

        ## ОСНОВНІ ТАБЛИЦІ ##
        # загружаєм юзверів
        load_user = db.execute("SELECT * FROM users")
        load_user = load_user.fetchall()

        # загружаєм результати матчів
        load_results = db.execute("SELECT * FROM m3 WHERE availability = :availability", dict(availability = 'yes'))
        load_results = load_results.fetchall()

        # кількість записиів в таблиці результатів
        n_results = len(load_results)
        # БЛОК для інформування адміна що невистачає: рахунків матчів чи прогнозів від юзерів
        # лічильник внесених адміном результатів в турі
        results_counter = 0

        # рахуємо чи вніс адмін рахунки по всих матчах в турі
        for i in range (n_results):
            if load_results[i][9] is not None: #.get("home_rez")
                results_counter += 1

        # якщо внесених результатів менше ніж самих матчів в турі, то виводимо помилку
        if results_counter < n_results:
            return apology("vnesty rahunky")

        # загружаєм прогнози, і якщо їх немає, то виводимо помилку
        load_prognoz = db.execute("SELECT * FROM p3 WHERE status = :status", dict(status = 'new'))
        load_prognoz = load_prognoz.fetchall()

        if not load_prognoz:
            return apology("nema prognoziv")

        # загружаєм підсумкову таблицю
        load_faintab = db.execute("SELECT * FROM fintab")
        load_faintab = load_faintab.fetchall()

        # визначаємо кількість юзверів
        n_user = len(load_user)

        # кількість записиів в таблиці прогнозів
        n_prognoz = len(load_prognoz)

        # кількість записиів в підсумковій таблиці
        #n_fintab = len(load_faintab)

        ## ДОДАТКОВІ змінні для експресів ##
        # створюємо пустий список (по кількості юзерів) для словників (де буде доп інфа для обрахунку експресів)
        # (user_id, кількість експресів в прогнозі від юзера, та реальна кількість матчів в експресі які зайшли)
        expres_support_list = []

        # додаємо в список шаблони на кожного юзера
        for i in range(n_user):

            # витягуємо user_id
            user_id = load_user[i][0] #.get("user_id")
            # чекаємо кількість матчів в самому експресі (в цьому турі) від юзера
            expresiv_v_prog = db.execute("SELECT COUNT (prognoz_type) FROM p3 WHERE user_id = :user_id AND status = :status AND prognoz_type = :prognoz_type",\
                                          dict(user_id=user_id, status='new', prognoz_type='Експрес'))
            expresiv_v_prog = expresiv_v_prog.fetchone()

            # створюємо словник даних які додамо в список
            user_data = {"user_id": user_id, "expres_prog": expresiv_v_prog[0], "exp_counter": 0} #expresiv_v_prog[0].get("COUNT (prognoz_type)")
            # додаємо в список наші дані (словник)
            expres_support_list.append(user_data)

        ## ПІДГОТОВКА ЗАКІНЧЕНА, і починаємо процес підрахунки балів ##
        # витягуємо результат і-ого матчу
        for i in range(n_results):
            # витягуємо ID матча

            result_home = load_results[i][9] #.get("home_rez")
            result_guest = load_results[i][10] #.get("visitor_rez")

            # визначаємо хто переміг в матчі
            # виграли господарі
            if result_home > result_guest:
                resultat = 10
            # виграли гості
            elif result_home < result_guest:
                resultat = 20
            # нічия
            elif result_home == result_guest:
                resultat = 30

            # поматчево звіряємо результат з прогнозом
            for j in range(n_prognoz):

                # звіряємо матч ID
                if load_results[i][0] == load_prognoz[j][1]: #if load_results[i].get("match_id") == load_prognoz[j].get("match_id"):

                    load_match_id = load_prognoz[j][1] #.get("match_id")
                    # витягуємо результат j-ого матчу
                    prognoz_home = load_prognoz[j][4] #.get("home")
                    prognoz_guest = load_prognoz[j][5] #.get("guest")

                    # тепер визначаємо на кого був прозног (10 виграли господарі, 20 - гості, 30 - нічия)
                    if prognoz_home > prognoz_guest:
                        prognoz = 10
                    elif prognoz_home < prognoz_guest:
                        prognoz = 20
                    elif prognoz_home == prognoz_guest:
                        prognoz = 30

                    # визначємо результат для кожного юзверя
                    for k in range(n_user):


                        # звіряємо user ID хто робив прогноз з базою юзерів
                        if load_prognoz[j][2] == load_user[k][0]: #if load_prognoz[j].get("user_id") == load_user[k].get("user_id"):

                            user_id_update = load_user[k][0] #.get("user_id")

                            # ця ЛОГІКА для ЕКСПРЕСІВ (Choo-Choo), бали запишемо потім
                            if load_prognoz[j][11] == 'Експрес': #.get("prognoz_type")
                                # порівнюємо прогноз на матч з результатом
                                if prognoz == resultat:
                                    # витягуємо дані з доп таблички
                                    load_exp_counter = expres_support_list[k].get("exp_counter") #

                                    # апдейтим дані з таблички
                                    new_exp_counter = load_exp_counter + 1
                                    # записуємо проапдейчені дані в табличку
                                    expres_support_list[k]["exp_counter"] = new_exp_counter

                            # ця ЛОГІКА для ОРДІНАРІВ
                            if load_prognoz[j][11] == 'Ординар': #.get("prognoz_type")
                                # порівнюємо прогноз на матч з результатом
                                # і якщо повністю вгадав то отримує 2 бали
                                if result_home == prognoz_home and result_guest == prognoz_guest:
                                    bal_za_match = 2
                                # якщо ні, то чекаємо чи вгадано результат матчу загалом
                                elif prognoz == resultat:
                                    bal_za_match = 1
                                # або ж не вгадано)
                                else:
                                    bal_za_match = 0

                                # сам результат
                                bal_for_update_acount = bal_za_match + load_prognoz[j][9] #.get("bal")

                                # апдейтим результат для кожного юзверя в акаунт
                                bal_update_acount = db.execute("UPDATE p3 SET bal = :bal WHERE user_id = :id AND match_id = :match_id",\
                                                                dict(bal = bal_for_update_acount, id = user_id_update, match_id = load_match_id))
                                dbb.commit()

                                # витягуємо бали (старі) юзера
                                check_user_fintab = db.execute("SELECT total_points FROM fintab WHERE user_id = :user_id",\
                                                                dict(user_id = user_id_update))
                                check_user_fintab = check_user_fintab.fetchone()

                                # додаємо нові (тільки що зароблені) бали до старих
                                bal_for_update_fintab = bal_za_match + check_user_fintab[0] #.get("total_points")
                                # апдейтим результат для кожного юзверя в підсумковій табличці
                                bal_update_fintab = db.execute("UPDATE fintab SET total_points = :bal WHERE user_id = :id",\
                                                                dict(bal = bal_for_update_fintab, id = user_id_update))
                                dbb.commit()

        ## блок по перевірці кількості матчів в експресі, скільки їх по факту зіграло (з доп таблички expres_support_list)
        # перебор по кожному юзеру, і заодно пишемо зароблені бали за експреси (якщо є)
        for m in range (n_user):

            # звіряємо кількість матчів в прогнозованому експресі з фактичними ісходами
            # якщо є БІНГО, то пишемо бали у ВСІ наші таблички
            if expres_support_list[m].get("expres_prog") == expres_support_list[m].get("exp_counter") and expres_support_list[m].get("expres_prog") > 0:

                # визначаємо в кого зайшов експрес
                user_id_for_update = expres_support_list[m].get("user_id")

                # визначаємо кількість балів як зароблені за експрес
                bal_for_update_fintab = expres_support_list[m].get("exp_counter") * 2

                # апдейтим результат для кожного юзверя в підсумковій табличці
                bal_update_fintab = db.execute("UPDATE fintab SET total_points = :new_bal WHERE user_id = :user_id",\
                                                dict(new_bal = bal_for_update_fintab, user_id = user_id_for_update))
                dbb.commit()

                # апдейтим результат для кожного юзверя в акаунт
                bal_update_acount = db.execute("UPDATE p3 SET bal = :new_bal WHERE user_id = :user_id AND status = :status",\
                                                dict(new_bal = 2, user_id = user_id_for_update, status = 'new'))
                dbb.commit()

        # інфа для підсумкової таблички для кожного юзверя
        for d in range (n_user):
            # грузим юзер ID
            user_id = load_user[d][0] #.get("user_id")

            # кільсть матчів де був прогноз
            check_all_matches_z_prognozom = db.execute("SELECT COUNT (teams) FROM p3 WHERE user_id = :user_id", dict(user_id = user_id))
            check_all_matches_z_prognozom = check_all_matches_z_prognozom.fetchone()
            # потенційні бали
            pot_points = check_all_matches_z_prognozom[0] * 2 #check_all_matches_z_prognozom[0].get("COUNT (teams)")

            # кількість вгаданих точних рахунків
            vgad_rah = db.execute("SELECT COUNT (bal) FROM p3 WHERE user_id = :user_id AND bal = 2 AND prognoz_type = :prognoz_type",\
                                   dict(user_id = user_id, prognoz_type='Ординар'))
            vgad_rah = vgad_rah.fetchone()

            # кількість просто вгаданих результатів матчу
            vgad_resultat = db.execute("SELECT COUNT (bal) FROM p3 WHERE user_id = :user_id AND bal = 1",\
                                        dict(user_id = user_id))
            vgad_resultat = vgad_resultat.fetchone()

            # кількість ЕКСПРЕСІВ які зайшли
            vgad_expres = db.execute("SELECT vgad_expresy FROM fintab WHERE user_id = :user_id",\
                                      dict(user_id = user_id))
            vgad_expres = vgad_expres.fetchone()
            vgad_expres = vgad_expres[0] #.get("vgad_expresy")

            # кількість ЕКСПРЕСІВ які НЕ зайшли
            ne_vgad_expres = db.execute("SELECT nevgad_expres FROM fintab WHERE user_id = :user_id",\
                                         dict(user_id = user_id))
            ne_vgad_expres = ne_vgad_expres.fetchone()
            ne_vgad_expres = ne_vgad_expres[0] #.get("nevgad_expres")

            # операції з туром
            tur = db.execute("SELECT DISTINCT tur FROM p3 WHERE status = :status", dict(status='new'))
            tur = tur.fetchone()

            prognoz_type = db.execute("SELECT DISTINCT prognoz_type FROM p3 WHERE user_id = :user_id AND prognoz_type = :prognoz_type AND tur = :tur",\
                                       dict(user_id = user_id, prognoz_type='Експрес', tur=tur[0])) #tur=tur[0].get("tur")
            prognoz_type = prognoz_type.fetchall()

            if len(prognoz_type) > 0:

                # рахуємо наші нові числа
                if expres_support_list[d].get("expres_prog") == expres_support_list[d].get("exp_counter") and prognoz_type[0][0] == 'Експрес': #prognoz_type[0].get("prognoz_type")
                    vgad_expres += 1

                    bal_za_expresy = db.execute("SELECT COUNT (prognoz_type) FROM p3 WHERE user_id = :user_id AND prognoz_type = :prognoz_type\
                                                 AND tur = :tur", dict(user_id = user_id, prognoz_type='Експрес', tur=tur[0])) #tur=tur[0].get("tur")
                    bal_za_expresy= bal_za_expresy.fetchone()

                    # беремо старі бали з підсумкової таблички
                    old_total_points = load_faintab[d][2] #.get("total_points")
                    # додаємо до старих бали за зіграний експрес
                    total_points = old_total_points + (bal_za_expresy[0] * 2) #.get("COUNT (prognoz_type)")

                    # додаємо бали за експрес у підсумкову табличку
                    bal_fintab_update = db.execute("UPDATE fintab SET total_points = :total_points WHERE user_id = :user_id",\
                                                    dict(total_points=total_points, user_id = user_id))
                    dbb.commit()

                    # додаємо бали за експрес у табличку до прогнозованих юзером матчів
                    bal_p3_update = db.execute("UPDATE p3 SET bal = 2 WHERE user_id = :user_id AND prognoz_type = :prognoz_type",\
                                                dict(user_id = user_id, prognoz_type='Експрес'))
                    dbb.commit()

                elif expres_support_list[d].get("expres_prog") != expres_support_list[d].get("exp_counter") and prognoz_type[0][0] == 'Експрес': #prognoz_type[0].get("prognoz_type")
                    ne_vgad_expres += 1

            # середній бал за матч
            new_load_faintab = db.execute("SELECT * FROM fintab WHERE user_id = :user_id", dict(user_id = user_id))
            new_load_faintab = new_load_faintab.fetchall()

            # якщо немає взагалі жодного прогноза на матч
            if check_all_matches_z_prognozom[0] == 0: #check_all_matches_z_prognozom[0].get("COUNT (teams)")
                ser_bal_za_match = 0
            else:
                # ser_bal_za_match = new_load_faintab[0].get("total_points") / check_all_matches_z_prognozom[0].get("COUNT (teams)")
                ser_bal_za_match = new_load_faintab[0][2] / check_all_matches_z_prognozom[0]

            # АПДЕЙТ показників у підсумковій табличці
            update_fintab = db.execute("UPDATE fintab SET total_matchi_prognoz = :matchi_prognoz, vgad_rah = :vgad_rah,\
                                        vgad_resultat = :vgad_resultat, aver_bal_za_match = :ser_bal_za_match, potential_points = :potential_points,\
                                        vgad_expresy = :vgad_expresy, nevgad_expres = :nevgad_expres WHERE user_id = :user_id",\
                                        dict(matchi_prognoz = check_all_matches_z_prognozom[0], vgad_rah = vgad_rah[0], vgad_resultat = vgad_resultat[0],\
                                        ser_bal_za_match = "%.2f" % (ser_bal_za_match), potential_points = pot_points, vgad_expresy=vgad_expres,\
                                        nevgad_expres=ne_vgad_expres, user_id = user_id))
            dbb.commit()
                                        # check_all_matches_z_prognozom[0].get("COUNT (teams)"), vgad_rah[0].get("COUNT (bal)"), vgad_resultat[0].get("COUNT (bal)")

        # АПДЕЙТ показників у табличці з командами
        # витягуємо команди
        check_team = db.execute("SELECT DISTINCT team_name FROM teams")
        check_team = check_team.fetchall()

        # визначаємо їх кількість
        n_check_team = len(check_team)

        # і для кожної закидаємо бали в табличку
        for i in range (n_check_team):

            team_name = check_team[i] #.get("team_name")

            team_points = db.execute("SELECT SUM(total_points) FROM fintab WHERE team = :team", dict(team=team_name[0]))
            team_points = team_points.fetchone()

            # якщо в командах немає гравців, виводим помилку
            if team_points[0] is None:
                return apology("Komandy bez gravtsiv", 400)

            else:
                update_teams_points = db.execute("UPDATE teams SET team_points = :team_points WHERE team_name = :team_name",\
                                                  dict(team_points=team_points[0], team_name=team_name[0])) #team_points[0].get("SUM(total_points)")
                dbb.commit()

        # і перекидаємо на домашню сторінку адміна
        return redirect("fintable")


""" (fintable) Зброс даних у підсумковій табличці, та балів у табличці з прогнозами """
@app.route("/zbros", methods=["GET", "POST"])
@login_required
def zbros():

    if request.method == "POST":

        # скидаємо дані по фін табличці
        zbros_fintab = db.execute("UPDATE fintab SET total_points = 0, total_matchi_prognoz = 0, vgad_rah = 0,\
                                   vgad_resultat = 0, aver_bal_za_match = 0, potential_points = 0, vgad_expresy = 0,\
                                   nevgad_expres = 0, guru_turu = 0") #, team = NULL
        dbb.commit()

        # скидаємо бали в прогнозах
        zbros_p3 = db.execute("UPDATE p3 SET bal = 0")
        dbb.commit()

        # скидаємо бали в командному заліку
        zbros_team_zalik = db.execute("UPDATE teams SET team_points = 0")
        dbb.commit()

        # і перекидаємо на домашню сторінку
        return redirect("fintable")


""" (fintable) Вкл/Викл адміном нового тура для прогноза """
@app.route("/vidkryty_tur", methods=["GET", "POST"])
@login_required
def vidkryty_tur():

    if request.method == "POST":

        # допоміжні величини
        inp_tur_open = request.form.get("tur_nomer")

        # про всяк випадок чекаємо чи не пусто
        if not inp_tur_open:
            return apology("Choose symbol from row", 400)

        load_all_matches = db.execute("SELECT * FROM m3")
        load_all_matches = load_all_matches.fetchall()

        n_load_all_matches = len(load_all_matches)

        # витягуємо номер тура що закриваємо, для його подальшої заміни в табличі прогнозів
        load_old_tur = db.execute("SELECT DISTINCT round FROM m3 WHERE availability = :availability",\
                                   dict(availability='yes'))
        load_old_tur = load_old_tur.fetchone()

        # перебираємо кожен матч
        for i in range (n_load_all_matches):

            # витягуємо номер раунда
            check_round = load_all_matches[i][1] #.get("round")
            # позначаємо тури як вже зіграні
            if check_round < int(inp_tur_open):
                open_tur = db.execute("UPDATE m3 SET availability = 'buv' WHERE round = :round",\
                                       dict(round = check_round))
                dbb.commit()

            # відкриваємо тур
            elif check_round == int(inp_tur_open):
                open_tur = db.execute("UPDATE m3 SET availability = 'yes' WHERE round = :round",\
                                       dict(round = check_round))
                dbb.commit()

            else:
                # залишаємо закритим на мабутнє
                close_tur = db.execute("UPDATE m3 SET availability = 'no' WHERE round = :round",\
                                        dict(round = check_round))
                dbb.commit()

        # ТРЕБА ДОПИЛЯТИ, ПОМИЛКА ПРИ ЗАПУСКУ ПЕРШОГО ТУРА
        print(f"load_old_tur", load_old_tur)


        # міняємо статус прогноза в табличці (тобто робимо їх старими)
        close_tur_prognoz = db.execute("UPDATE p3 SET status = 'old' WHERE tur = :tur", dict(tur = load_old_tur[0])) #load_old_tur[0].get("round")
        dbb.commit()

        ## частина кода яка треба при ТЕСТУВАННІ, якщо заново відкриваємо Першший тур
        check_status = db.execute("SELECT status FROM p3 WHERE status = 'old' AND tur = :tur", dict(tur = int(inp_tur_open)))
        check_status = check_status.fetchall()

        if len(check_status) > 0:
            change_status = db.execute("UPDATE p3 SET status = 'new' WHERE tur = :tur", dict(tur = load_old_tur[0])) #load_old_tur[0].get("round")
            dbb.commit()

        close_tur2 = db.execute("UPDATE p3 SET status = 'old'")
        dbb.commit()
        open_tur2 = db.execute("UPDATE p3 SET status = 'new' WHERE tur = :tur", dict(tur = int(inp_tur_open)))
        dbb.commit()

        # визначаємо кількість турів для виводу на сторінку
        tur_for_open = db.execute("SELECT DISTINCT round FROM m3")
        tur_for_open = tur_for_open.fetchall()

        # рендерим сторінку
        return redirect("fintable")
        #return render_template("vidkryty_tur.html", rows=tur_for_open)


""" (fintable) Призначаємо когось на "посаду" Гуру туру """
@app.route("/guru", methods=["GET", "POST"])
@login_required
def guru():

    if request.method == "POST":

        # отримуємо юзера якого зробили гуру
        inp_guru = request.form.get("guru")
        # витягуємо з бази інфу про минулі звання "Гуру"
        guru_check = db.execute("SELECT guru_turu FROM fintab WHERE user_name = :user_name",\
                                 dict(user_name = inp_guru))
        guru_check = guru_check.fetchone()

        # апдейтим значення
        new_guru_turu = guru_check[0] + 1 # .get("guru_turu")
        # і записуємо нове значення назад в базу
        guru_update = db.execute("UPDATE fintab SET guru_turu = :guru_turu WHERE user_name = :user_name",\
                                  dict(guru_turu = new_guru_turu, user_name = inp_guru))
        dbb.commit()

        # і редірект назад на сторінку підсумкової таблички
        return redirect("fintable")


""" Адмін додає новий матч в турнір """
@app.route("/newmatch", methods=["GET", "POST"])
@login_required
def newmatch():

    if request.method == "POST":

        # отримуємо дані про матч - (Господарі, Гості, та номер тура)
        inp_home = request.form.get("home")
        inp_visitors = request.form.get("visitor")
        inp_tur = request.form.get("tur_number")
        inp_match_tur = request.form.get("matchintur")
        inp_match_date = request.form.get("match_date")
        inp_match_time = request.form.get("match_time")

        #допоміжні дані
        defis = '-'
        pre_razom = inp_home + " {} " + inp_visitors
        razom = pre_razom.format(defis)

        # пишемо отримані дані в базу
        add_match = db.execute ("INSERT INTO m3 (match_id, round, mtch_round, home, visitor, razom, match_date,\
                                 match_time, availability) VALUES (NULL, :round, :mtch_round, :home, :visitor,\
                                 :razom, :match_date, :match_time, 'no')", dict(round=inp_tur, mtch_round=inp_match_tur,\
                                 home=inp_home, visitor=inp_visitors, match_date=inp_match_date, match_time=inp_match_time,\
                                 razom=razom))
        dbb.commit()

        # список матчів
        check_match = db.execute ("SELECT * FROM m3 ORDER BY round DESC, mtch_round DESC")
        check_match = check_match.fetchall()
        # рендерим сторінку
        return render_template("newmatch.html", rows=check_match)

    else:
        # список матчів
        check_match = db.execute ("SELECT * FROM m3 ORDER BY round DESC, mtch_round DESC")
        check_match = check_match.fetchall()
        # рендерим сторінку
        return render_template("newmatch.html", rows=check_match)


""" Адмін вносить зміни в існуючий матч турніра"""
@app.route("/changematch", methods=["GET", "POST"])
@login_required
def changematch():

    if request.method == "POST":

        # отримуємо нові дані (прогноз на матч - Господарі та Гості)
        inp_change_match = request.form.get("razom")
        inp_change_home_rez = request.form.get("home_rez")
        inp_change_visitor_rez = request.form.get("visitor_rez")
        inp_change_tur = request.form.get("tur")
        inp_change_tur_match = request.form.get("tur_match")
        inp_delete = request.form.get("delete2")

        if not inp_change_home_rez:
            inp_change_home_rez = None
        if not inp_change_visitor_rez:
            inp_change_visitor_rez = None

        # чекаємо id матчу, та витягуємо тільки його з бібліотеки
        check_match_id = db.execute ("SELECT match_id FROM m3 WHERE razom =:razom", dict(razom = inp_change_match))
        check_match_id = check_match_id.fetchone()
        match_id_only = check_match_id[0] # .get("match_id")

        # перевіряємо чи видаляє адмін матч взагалі
        if inp_delete == 'yes':

            # видаляємо запис з бази прогнозів
            prognoz_del = db.execute("DELETE FROM m3 WHERE match_id = :match_id", dict(match_id=match_id_only))
            dbb.commit()

        # якщо не видаляє, то оновлюємо дані в нашій базі
        else:
            # оновлюємо прогноз в базі
            update_prognoz = db.execute ("UPDATE m3 SET round = :round, mtch_round = :mtch_round, home_rez = :home_rez,\
                                        visitor_rez = :visitor_rez WHERE razom = :razom", dict(round=inp_change_tur,\
                                        mtch_round=inp_change_tur_match, home_rez=inp_change_home_rez,\
                                        visitor_rez=inp_change_visitor_rez, razom=inp_change_match))
            dbb.commit()

        # список матчів які може змінити адмін
        change_match = db.execute ("SELECT * FROM m3 ORDER BY round DESC, mtch_round DESC")
        change_match = change_match.fetchall()
        # рендерим сторінку
        return render_template("changematch.html", rows=change_match)

    else:
        # список матчів які може змінити адмін
        change_match = db.execute ("SELECT * FROM m3 ORDER BY round DESC, mtch_round DESC")
        change_match = change_match.fetchall()
        # рендерим сторінку
        return render_template("changematch.html", rows=change_match)


""" Адмін вписує результат матчу """
@app.route("/rahunok", methods=["GET", "POST"])
@login_required
def rahunok():

    if request.method == "POST":

        # отримуємо дані про матч - (Господарі, Гості, та номер тура)
        inp_razom = request.form.get("razom")
        inp_home_result = request.form.get("home")
        inp_visitors_result = request.form.get("visitor")

        # чекаємо id матчу, та витягуємо тільки його з бібліотеки
        check_match_id = db.execute ("SELECT match_id FROM m3 WHERE razom =:razom", dict(razom = inp_razom))
        check_match_id = check_match_id.fetchone()

        match_id_only = check_match_id[0] #.get("match_id")

        # вписуємо рахунок матчу в базу
        add_match = db.execute ("UPDATE m3 SET home_rez = :home_rez, visitor_rez = :visitor_rez WHERE match_id = :match_id",\
                                 dict(home_rez=int(inp_home_result), visitor_rez=int(inp_visitors_result), match_id=match_id_only))
        dbb.commit()

        # загружаєм список матчів
        load_matches = db.execute("SELECT * FROM m3 WHERE availability = :availability AND home_rez IS NULL",\
                                   dict(availability = 'yes'))
        load_matches = load_matches.fetchall()

        # рендерим сторінку
        return render_template("rahunok.html", rows=load_matches)

    else:
        # загружаєм список матчів
        load_matches = db.execute("SELECT * FROM m3 WHERE availability = :availability AND home_rez IS NULL",\
                                   dict(availability = 'yes'))
        load_matches = load_matches.fetchall()

        # рендерим сторінку
        return render_template("rahunok.html", rows=load_matches)


""" БЛОК операці з КОМАНДАМИ """
""" (для командного заліку) Додаємо нову команду """
@app.route("/add_team", methods=["GET", "POST"])
@login_required
def add_team():

    if request.method == "POST":
        # отримуємо назву команди
        inp_team_name = request.form.get("team_name")

        # додаємо команду в базу
        add_match = db.execute("INSERT INTO teams (team_id, team_name) VALUES (NULL, :team_name)",\
                                dict(team_name=inp_team_name))
        dbb.commit()

        # готуємо список команд які є
        team_list = db.execute("SELECT * FROM teams")
        team_list = team_list.fetchall()

        # рендерим сторінку
        return render_template("add_team.html", rows=team_list)

    else:
        # готуємо список команд які є
        team_list = db.execute("SELECT * FROM teams")
        team_list = team_list.fetchall()

        # рендерим сторінку
        return render_template("add_team.html", rows=team_list)


""" (для командного заліку) Міняємо назву команди, чи видаляємо команду з бази взагалі """
@app.route("/changeteamname", methods=["GET", "POST"])
@login_required
def changeteamname():

    if request.method == "POST":

        # отримуємо нову назву для "старої" команди
        inp_team_name = request.form.get("team_name")
        inp_new_team_name = request.form.get("new_team_name")

        # для видалення
        inp_del_team = request.form.get("del_team")
        # якщо є маркер на видалення
        if inp_del_team == 'yes':
            # то видаляємо зі списка команд
            del_team = db.execute("DELETE FROM teams WHERE team_name = :team_name",\
                                   dict(team_name=inp_team_name))
            dbb.commit()

        # оновлюємо назву команди
        update_team_name = db.execute("UPDATE teams SET team_name = :new_team_name WHERE team_name = :team_name",\
                                       dict(new_team_name=inp_new_team_name, team_name=inp_team_name))
        dbb.commit()

        # готуємо список команд які є
        team_list = db.execute("SELECT * FROM teams")
        team_list = team_list.fetchall()

        # рендерим сторінку
        return render_template("changeteamname.html", rows=team_list)

    else:
        # готуємо список команд які є
        team_list = db.execute("SELECT * FROM teams")
        team_list = team_list.fetchall()

        # рендерим сторінку
        return render_template("changeteamname.html", rows=team_list)


""" (для командного заліку) Додаємо гравців в команду """
@app.route("/add_players_to_team", methods=["GET", "POST"])
@login_required
def add_players_to_team():

    if request.method == "POST":
        # назву команди
        inp_team_name = request.form.get("team_name")
        # учасник клуба
        inp_user_name = request.form.get("user_name")

        # вписуємо учасника клуба в команду
        add_user_to_team = db.execute("UPDATE fintab SET team = :team_name WHERE user_name = :user_name",\
                                       dict(team_name=inp_team_name, user_name=inp_user_name))
        dbb.commit()

        # готуємо списки команд та юзерів які є (для включення)
        team_list = db.execute("SELECT * FROM teams")
        team_list = team_list.fetchall()
        user_list = db.execute("SELECT * FROM fintab WHERE team IS NULL")
        user_list = user_list.fetchall()

        # дані чисто для візуалізації, хто в якій команді зараз вже є
        check_list = db.execute("SELECT user_name, team FROM fintab WHERE team NOT NULL ORDER BY team DESC")
        check_list = check_list.fetchall()
        # рендерим сторінку
        return render_template("add_players_to_team.html", rows=team_list, rows2=user_list, rows3=check_list)

    else:
        # готуємо списки команд та юзерів які є (для включення)
        team_list = db.execute("SELECT * FROM teams")
        team_list = team_list.fetchall()
        user_list = db.execute("SELECT * FROM fintab WHERE team IS NULL")
        user_list = user_list.fetchall()

        # дані чисто для візуалізації, хто в якій команді зараз вже є
        check_list = db.execute("SELECT user_name, team FROM fintab WHERE team NOT NULL ORDER BY team DESC")
        check_list = check_list.fetchall()

        # рендерим сторінку
        return render_template("add_players_to_team.html", rows=team_list, rows2=user_list, rows3=check_list)


""" (для командного заліку) Видаляємо гравця з команди """
@app.route("/del_player_from_team", methods=["GET", "POST"])
@login_required
def del_player_from_team():

    if request.method == "POST":
        # отримуємо ім'я користувача, якого треба видалити з командного заліка
        inp_user_name = request.form.get("gridRadios")

        # і видаляємо його
        del_user = db.execute("UPDATE fintab SET team = NULL WHERE user_name = :user_name",\
                               dict(user_name=inp_user_name))
        dbb.commit()

        # команди та їх учасники
        check_list = db.execute("SELECT user_name, team FROM fintab WHERE team NOT NULL ORDER BY team DESC")
        check_list = check_list.fetchall()

        # рендерим сторінку
        return render_template("del_player_from_team.html", rows=check_list)

    else:
        # команди та їх учасники
        check_list = db.execute("SELECT user_name, team FROM fintab WHERE team NOT NULL ORDER BY team DESC")
        check_list = check_list.fetchall()

        # рендерим сторінку
        return render_template("del_player_from_team.html", rows=check_list)


""" Команди та їх склад """
@app.route("/teams_and_members", methods=["GET", "POST"])
@login_required
def teams_and_members():

    # команди та їх учасники
    teams_and_members = db.execute("SELECT user_name, total_points, team FROM fintab WHERE team NOT NULL ORDER BY team DESC")
    teams_and_members = teams_and_members.fetchall()

    # рендерим сторінку
    return render_template("teams_and_members.html", rows=teams_and_members)

""" TECT """
@app.route("/test", methods=["GET", "POST"])
@login_required
def test():

    # рендерим сторінку
    return render_template("test.html")

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
