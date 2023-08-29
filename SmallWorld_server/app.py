from flask import Flask ,request,redirect,render_template,url_for
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user,current_user
from flask_cors import CORS
import json
import os
from sw import sw2,sw1
from name2id import right_name


with open('./users_info.json','r',encoding='utf-8') as f:
    users_info = json.load(f)

with open('./handled_cards.json','r',encoding='utf-8') as f:
    cards = json.load(f)

class User(UserMixin):
    pass

app = Flask(__name__)
app.secret_key = 'dstxqljp'
CORS(app)

login_manager = LoginManager()
login_manager.login_view = '_login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    if id not in users_info:
        return

    user = User()
    user.id = id
    return user

@login_manager.request_loader
def request_loader(request):
    id = request.form.get('id')
    if id not in users_info:
        return

    user = User()
    user.id = id
    return user




@app.route('/')
def _index():
    return render_template('index.html')


@app.route('/card')
def _card():
    cost = request.args.get('cost')
    target = request.args.get('target')
    deck = request.args.get('deck')

    if deck:
        username = current_user._get_current_object().id
        deckPath = './data/deck/{}/{}'.format(username,deck)
        ret = sw2(deckPath,cost)
    else:
        ret = sw1(cost,target)
    return json.dumps(ret , ensure_ascii=False)


@app.route('/RightName/<name>')
def _name(name):
    return right_name(name)

@app.route('/RightName/<name>/<deck>')
def __name(name,deck):
    username = current_user._get_current_object().id
    with open('./data/deck/{}/{}'.format(username,deck),'r',encoding='utf-8') as f:
        deck = f.readlines()
        start=deck.index('#main\n')+1
        end=deck.index('#extra\n')
        main_deck=[]
        for i in range(start,end):
            temp_card=deck[i].strip()
            if temp_card not in main_deck:
                if temp_card in cards.keys():
                    main_deck.append(temp_card)
    return right_name(name,main_deck)


with open('./name2id.json','r',encoding='utf-8') as f:
    NameId = json.load(f)

@app.route('/cardInfo/<name>')
def _cardinfo(name):
    id = NameId[name]
    return redirect('https://ygocdb.com/card/{}'.format(id))


@app.route('/smallWorld1')
def _sw1():
    return render_template('smallWorld1.html')

@app.route('/smallWorld2')
@login_required
def _sw2():
    return render_template('smallWorld2.html')

@app.route('/smallWorld2/login',methods=['GET', 'POST'])
def _login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_info.keys() and users_info[username] == password:
            user = User()
            user.id = username
            login_user(user)
            return redirect('/smallWorld2')
        else:
            return "登录失败，请检查您的用户名和密码"
    return render_template('login.html')

@app.route('/smallWorld2/register',methods=['GET', 'POST'])
def _register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_info.keys():
            return '该用户名已被注册'
        users_info[username] = password
        with open('./users_info.json','w',encoding='utf-8') as f:
            json.dump(users_info,f,ensure_ascii=False)
        os.makedirs('./data/deck/{}'.format(username))
        return redirect(url_for('_login'))
    return render_template('register.html')


@app.route('/smallWorld2/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('_login'))


@app.route('/smallWorld2/username')
@login_required
def _username():
    return current_user._get_current_object().id

@app.route('/smallWorld2/userData')
@login_required
def _data():
    decks = os.listdir('./data/deck/{}'.format(current_user._get_current_object().id))
    return json.dumps(decks,ensure_ascii=False)


@app.route('/smallWorld2/deckInput', methods=['GET', 'POST','PUT'])
@login_required
def _deckInput():
    message = ''
    if request.method == 'POST':
        username = current_user._get_current_object().id
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                os.makedirs('./data/deck/{}'.format(username), exist_ok=True)
                file_path = os.path.join('./data/deck/{}'.format(username), file.filename)
                file.save(file_path)
                message = '文件上传成功'
                return render_template('smallWorld2.html')

        text = request.form.get('text')
        filename = request.form.get('filename')
        if text and filename:
            txt_file_path = os.path.join('./data/deck/{}'.format(username), filename + '.txt')
            with open(txt_file_path, 'w') as f:
                f.write(text)
            message = '文本保存成功'
            return render_template('smallWorld2.html')

    return render_template('deckInput.html', message=message)


@app.route('/favicon.ico')
def get_fav():
    return app.send_static_file('img/favicon.ico')


if __name__ == '__main__':
    app.run()