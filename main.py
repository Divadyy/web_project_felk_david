import os

from flask import Flask, render_template, redirect, request, abort, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from forms.reviews import ReviewsForm
from forms.user import RegisterForm, LoginForm
from data.reviews import Reviews
from data.users import User
from data import db_session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'a4siuhd7asd7123jas851ks91aksj18kmmz912mx217'


@app.route('/')
@app.route('/index')
@app.route('/catalog')
def catalog():
    return render_template('catalog.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


def main():
    db_session.global_init("db/reviews.db")
    port = os.environ.get('PORT', 8080)
    app.run(port=port, host='0.0.0.0')


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template("login.html", message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect("/")


@app.route('/reviews',  methods=['GET', 'POST'])
@login_required
def add_reviews():
    form = ReviewsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        reviews = Reviews()
        reviews.title = form.title.data
        reviews.content = form.content.data
        reviews.product = session.get('url')
        current_user.reviews.append(reviews)

        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('reviews.html', title='Добавление новости',
                           form=form)


@app.route('/reviews/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_reviews(id):
    form = ReviewsForm()

    if request.method == "GET":
        db_sess = db_session.create_session()
        reviews = db_sess.query(Reviews).filter(Reviews.id == id,
                                          Reviews.user == current_user
                                          ).first()
        if reviews:
            form.title.data = reviews.title
            form.content.data = reviews.content
        else:
            abort(404)

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        reviews = db_sess.query(Reviews).filter(Reviews.id == id,
                                          Reviews.user == current_user
                                          ).first()
        if reviews:
            reviews.title = form.title.data
            reviews.content = form.content.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('reviews.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/reviews_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def reviews_delete(id):
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.id == id,
                                      Reviews.user == current_user
                                      ).first()
    if reviews:
        db_sess.delete(reviews)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/I5-13600KF_BOX')
def i5_13600kf_box():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/i5.jpg',
                           naming='I5-13600KF',
                           price='27 999',
                           description='Процессор I5 от intel 13 поколения. Идеально подойдёт для геймеров.',
                           proportions='4.37 x 3.71 x 0.49 см',
                           weight='0.036 кг',
                           year='2022',
                           feature_1='Сокет',
                           to_feature_1='LGA 1700',
                           feature_2='Количество производительных ядер',
                           to_feature_2='6',
                           feature_3='Количество энергоэффективных ядер',
                           to_feature_3='8',
                           feature_4='Базовая частота процессора',
                           to_feature_4='3.5 ГГц',
                           feature_5='Максимальная частота в турбо режиме',
                           to_feature_5='5.1 ГГц',
                           feature_6='Тип памяти',
                           to_feature_6='DDR4, DDR5',
                           feature_7='Частота оперативной памяти',
                           to_feature_7='DDR4-3200, DDR5-5600',
                           feature_8='Тепловыделение (TDP)',
                           to_feature_8='181 Вт',
                           feature_9='Видеоядро',
                           to_feature_9='Отсутствует')


@app.route('/I7-13700KF_BOX')
def i7_13700kf_box():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/i7.jpg',
                           naming='I7-13700KF',
                           price='43 799',
                           description='Процессор I7 от intel 13 поколения. Подойдёт для требовательных геймеров.',
                           proportions='4.37 x 3.71 x 0.49 см',
                           weight='0.036 кг',
                           year='2022',
                           feature_1='Сокет',
                           to_feature_1='LGA 1700',
                           feature_2='Количество производительных ядер',
                           to_feature_2='8',
                           feature_3='Количество энергоэффективных ядер',
                           to_feature_3='8',
                           feature_4='Базовая частота процессора',
                           to_feature_4='3.4 ГГц',
                           feature_5='Максимальная частота в турбо режиме',
                           to_feature_5='5.4 ГГц',
                           feature_6='Тип памяти',
                           to_feature_6='DDR4, DDR5',
                           feature_7='Частота оперативной памяти',
                           to_feature_7='DDR4-3200, DDR5-5600',
                           feature_8='Тепловыделение (TDP)',
                           to_feature_8='253 Вт',
                           feature_9='Видеоядро',
                           to_feature_9='Отсутствует')


@app.route('/I9-13900KF_BOX')
def i9_13900kf_box():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/i9.jpg',
                           naming='I9-13900KF',
                           price='56 999',
                           description='Процессор I9 от intel 13 поколения. Подойдёт для энтузиастов, которым действительно важна мощность.',
                           proportions='4.37 x 3.71 x 0.49 см',
                           weight='0.036 кг',
                           year='2022',
                           feature_1='Сокет',
                           to_feature_1='LGA 1700',
                           feature_2='Количество производительных ядер',
                           to_feature_2='8',
                           feature_3='Количество энергоэффективных ядер',
                           to_feature_3='16',
                           feature_4='Базовая частота процессора',
                           to_feature_4='3 ГГц',
                           feature_5='Максимальная частота в турбо режиме',
                           to_feature_5='5.8 ГГц',
                           feature_6='Тип памяти',
                           to_feature_6='DDR4, DDR5',
                           feature_7='Частота оперативной памяти',
                           to_feature_7='DDR4-3200, DDR5-5600',
                           feature_8='Тепловыделение (TDP)',
                           to_feature_8='253 Вт',
                           feature_9='Видеоядро',
                           to_feature_9='Отсутствует')


@app.route('/ASUS_PRIME_B760M-K_D4')
def asus_prime_b760m_k_d4():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/b760.jpg',
                           naming='ASUS PRIME B760M-K D4',
                           price='8 999',
                           description='Материнская плата от ASUS на чипсете B760 для процессоров intel под сокет LGA 1700. Подойдёт для нетребовательных геймеров.',
                           proportions='Micro-ATX, 211x244 мм',
                           weight='0.95 кг',
                           year='2023',
                           feature_1='Сокет',
                           to_feature_1='LGA 1700',
                           feature_2='Чипсет Intel',
                           to_feature_2='B760',
                           feature_3='Тип поддерживаемой памяти',
                           to_feature_3='DDR4',
                           feature_4='Количество фаз питания',
                           to_feature_4='8',
                           feature_5='Разъемы для корпусных вентиляторов (4 pin)',
                           to_feature_5='1',
                           feature_6='Разъемы для корпусных вентиляторов (3 pin)',
                           to_feature_6='0',
                           feature_7='Разъемы 5V-D-G (3 pin) для ARGB подсветки',
                           to_feature_7='2',
                           feature_8='Разъемы 12V-G-R-B (4 pin) для RGB подсветки',
                           to_feature_8='1',
                           feature_9='Количество разъемов M.2',
                           to_feature_9='2')


@app.route('/ASUS_TUF_GAMING_B760M-BTF_WIFI_D4')
def asus_tuf_gaming_b760m_btf_wifi_d4():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/b760_tuf.jpg',
                           naming='ASUS TUF GAMING B760M-BTF WIFI D4 ',
                           price='22 999',
                           description='Материнская плата от ASUS на чипсете B760 для процессоров intel под сокет LGA 1700. Идеально подойдёт для геймеров.',
                           proportions='Micro-ATX, 244x244 мм',
                           weight='1.07 кг',
                           year='2023',
                           feature_1='Сокет',
                           to_feature_1='LGA 1700',
                           feature_2='Чипсет Intel',
                           to_feature_2='B760',
                           feature_3='Тип поддерживаемой памяти',
                           to_feature_3='DDR4',
                           feature_4='Количество фаз питания',
                           to_feature_4='12+1+1',
                           feature_5='Разъемы для корпусных вентиляторов (4 pin)',
                           to_feature_5='3',
                           feature_6='Разъемы для помпы СЖО (4 pin)',
                           to_feature_6='1',
                           feature_7='Разъемы 5V-D-G (3 pin) для ARGB подсветки',
                           to_feature_7='3',
                           feature_8='Разъемы 12V-G-R-B (4 pin) для RGB подсветки',
                           to_feature_8='1',
                           feature_9='Количество разъемов M.2',
                           to_feature_9='3')


@app.route('/ASUS_ROG_MAXIMUS_Z790_APEX_ENCORE')
def asus_rog_maximus_z790_apex_encore():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/z790.png',
                           naming='ASUS ROG MAXIMUS Z790 APEX ENCORE',
                           price='73 499',
                           description='Материнская плата от ASUS на чипсете Z790 для процессоров intel под сокет LGA 1700. Подойдёт для энтузиастов, которым действительно нужна мощность.',
                           proportions='Standart-ATX, 244x305 мм',
                           weight='3.75 кг',
                           year='2023',
                           feature_1='Сокет',
                           to_feature_1='LGA 1700',
                           feature_2='Чипсет Intel',
                           to_feature_2='Z790',
                           feature_3='Тип поддерживаемой памяти',
                           to_feature_3='DDR5',
                           feature_4='Количество фаз питания',
                           to_feature_4='24+0+2',
                           feature_5='Разъемы для корпусных вентиляторов (4 pin)',
                           to_feature_5='5',
                           feature_6='Разъемы для помпы СЖО (4 pin)',
                           to_feature_6='2',
                           feature_7='Разъемы 5V-D-G (3 pin) для ARGB подсветки',
                           to_feature_7='3',
                           feature_8='Разъемы 12V-G-R-B (4 pin) для RGB подсветки',
                           to_feature_8='1',
                           feature_9='Количество разъемов M.2',
                           to_feature_9='3')


@app.route('/ASUS_GeForce_RTX_4070_Ti_TUF_Gaming_OC_Edition')
def asus_geforce_rtx_4070_ti_tuf_gaming_oc_edition():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/4070ti.jpg',
                           naming='ASUS GeForce RTX 4070 Ti TUF Gaming OC Edition',
                           price='97 999',
                           description='Видеокарта RTX 4070 Ti от nVidia. Идеально подойдёт для геймеров.',
                           proportions='305x138x65 мм',
                           weight='2.15 кг',
                           year='2023',
                           feature_1='Техпроцесс',
                           to_feature_1='5 нм',
                           feature_2='Штатная частота работы видеочипа',
                           to_feature_2='2310 МГц',
                           feature_3='Турбочастота',
                           to_feature_3='2760 МГц',
                           feature_4='Количество универсальных процессоров (ALU)',
                           to_feature_4='7680',
                           feature_5='Число текстурных блоков',
                           to_feature_5='240',
                           feature_6='Число блоков растеризации',
                           to_feature_6='80',
                           feature_7='Аппаратное ускорение трассировки лучей (RT-ядра)',
                           to_feature_7='60',
                           feature_8='Тензорные ядра',
                           to_feature_8='240',
                           feature_9='Объем видеопамяти',
                           to_feature_9='12 ГБ')


@app.route('/ASUS_GeForce_RTX_4090_ROG_Strix_OC_Edition')
def asus_geforce_rtx_4090_rog_strix_oc_edition():
    url = request.url
    session['url'] = url
    db_sess = db_session.create_session()
    reviews = db_sess.query(Reviews).filter(Reviews.product == url)
    return render_template('product.html',
                           reviews=reviews,
                           src='static/images/4090.jpg',
                           naming='ASUS GeForce RTX 4090 ROG STRIX OC Edition',
                           price='329 999',
                           description='Видеокарта RTX 4090 от nVidia. Подойдёт для требовательных геймеров и энтузиастов.',
                           proportions='358x149x70.1 мм',
                           weight='2.5 кг',
                           year='2023',
                           feature_1='Техпроцесс',
                           to_feature_1='5 нм',
                           feature_2='Штатная частота работы видеочипа',
                           to_feature_2='2210 МГц',
                           feature_3='Турбочастота',
                           to_feature_3='2640 МГц',
                           feature_4='Количество универсальных процессоров (ALU)',
                           to_feature_4='16384',
                           feature_5='Число текстурных блоков',
                           to_feature_5='512',
                           feature_6='Число блоков растеризации',
                           to_feature_6='176',
                           feature_7='Аппаратное ускорение трассировки лучей (RT-ядра)',
                           to_feature_7='128',
                           feature_8='Тензорные ядра',
                           to_feature_8='512',
                           feature_9='Объем видеопамяти',
                           to_feature_9='24 ГБ')


if __name__ == '__main__':
    main()
