from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import socket

host = socket.gethostname()

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    print('server run')
    return 'Hello World!'


@app.route('/api')
def api():
    data = [{'message': 'Request successful'}]

    with open('backend/data.json', 'w') as file:
        json.dump(data, file)

    print("server is active")

    return data


@app.route('/getAffairs', methods=['GET'])
def get_user_affairs():
    user_id = request.args.get('userId')

    with open('backend/user_affairs.json', 'r', encoding='utf-8') as file:
        user_affairs = json.load(file)

    if user_id not in user_affairs:
        user_affairs[user_id] = {'affairs':{}}

    print(user_affairs[user_id])
    date = request.args.get('date')
    # print('Обращение в affairs' + user_affairs[user_id]['affairs'])
    if date not in user_affairs[user_id]['affairs']:
        user_affairs[user_id]['affairs'][date] = []

    with open('backend/user_affairs.json', 'w', encoding='utf-8') as file:
        json.dump(user_affairs, file, ensure_ascii=False, indent=4)

    return jsonify(user_affairs[user_id])  # Отправляем ответ клиенту в формате JSON.


@app.route('/addAffair', methods=['POST'])
def add_affair():
    new_affair = request.get_json()  # Получаем данные из тела запроса
    user_id = request.args.get('userId')

    date = request.args.get('date')
    with open('backend/user_affairs.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    if date in data[user_id]['affairs']:
        data[user_id]['affairs'][date].append(new_affair)  # Добавляем новый элемент в список affairs
    else:
        data[user_id]['affairs'] = {date:[new_affair]}
        print(data[user_id]['affairs'])
    with open('backend/user_affairs.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # Сохраняем обновленные данные в файл JSON

    return jsonify({'message': 'New affair added successfully'})  # Отправляем ответ клиенту


@app.route('/removeAffair', methods=['POST'])
def remove_affair():
    user_id = request.args.get('userId')
    id_affair = (request.get_json())["id"]  # Получаем данные из тела запроса
    print(id_affair)
    with open('backend/user_affairs.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        user_affairs = data.get(str(user_id), {}).get('affairs', {})
        for date, affairs in user_affairs.items():
            for affair in affairs:
                if affair["id"] == id_affair:
                    affairs.remove(affair)

    with open('backend/user_affairs.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # Сохраняем обновленные данные в файл JSON

    return jsonify({'message': 'Affair removed successfully'})  # Отправляем ответ клиенту

    
if __name__ == '__main__':
    app.run( host=host, debug='True', ssl_context=('cert.pem', 'key.pem'))
