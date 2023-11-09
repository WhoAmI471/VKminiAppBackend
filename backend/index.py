from flask import Flask, request, jsonify
import json


app = Flask(__name__)

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

@app.route('/addAffair', methods=['POST'])
def add_affair():

    print(request)
    new_affair = request.get_json()  # Получаем данные из тела запроса
    

    with open('affairs.json', 'w') as file:
        json.dump(new_affair, file)

    return jsonify({'message': 'New affair added successfully'})  # Отправляем ответ клиенту

if __name__ == '__main__':
    app.run(debug='True', ssl_context='adhoc')
