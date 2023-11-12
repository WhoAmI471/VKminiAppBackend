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

    with open('backend/user_affairs.json', 'r', encoding='utf-8') as file:
        user_affairs = json.load(file)
    print(user_affairs)
    return jsonify(user_affairs)  # Отправляем ответ клиенту в формате JSON


@app.route('/addAffair', methods=['POST'])

def add_affair():
    new_affair = request.get_json()  # Получаем данные из тела запроса

    with open('backend/user_affairs.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        data['users'][0]['affairs'].append(new_affair)  # Добавляем новый элемент в список affairs

    with open('backend/user_affairs.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # Сохраняем обновленные данные в файл JSON

    return jsonify({'message': 'New affair added successfully'})  # Отправляем ответ клиенту


@app.route('/removeAffair', methods=['POST'])

def remove_affair():
    id_affair = (request.get_json())["id"]  # Получаем данные из тела запроса
    print(id_affair)
    count = 0
    with open('backend/user_affairs.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        affairs = data['users'][0]['affairs']  # удаляем новый элемент из списока affairs
        for affair in affairs:
            if affair["id"] == id_affair:
                affairs.pop(count)
            count += 1

    with open('backend/user_affairs.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)  # Сохраняем обновленные данные в файл JSON

    return jsonify({'message': 'New affair added successfully'})  # Отправляем ответ клиенту


    
if __name__ == '__main__':
    app.run( host=host, debug='True', ssl_context=('cert.pem', 'key.pem'))
