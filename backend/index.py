from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import socket
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json
import calendar

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
    
    if date not in user_affairs[user_id]['affairs']:
        user_affairs[user_id]['affairs'][date] = []

    with open('backend/user_affairs.json', 'w', encoding='utf-8') as file:
        json.dump(user_affairs, file, ensure_ascii=False, indent=4)

    return jsonify(user_affairs[user_id])  # Отправляем ответ клиенту в формате JSON.


@app.route('/getCategoryStats', methods=['GET'])
def get_category_stats():
    user_id = request.args.get('userId')
    date_range = request.args.get('dateRange')

    with open('backend/user_affairs.json', 'r', encoding='utf-8') as file:
        user_affairs = json.load(file)

    if user_id not in user_affairs:
        return jsonify({"error": "User not found"})

    if date_range not in ['day', 'week', 'month', 'year']:
        return jsonify({"error": "Invalid date range"})

    date_today = datetime.now()
    start_date = None

    if date_range == 'day':
        start_date = date_today - timedelta(days=1)
        range_duration = 86400
    elif date_range == 'week':
        start_date = date_today - timedelta(days=date_today.weekday())
        range_duration = 7 * 86400
    elif date_range == 'month':
        start_date = date_today.replace(day=1)
        days_in_month = calendar.monthrange(date_today.year, date_today.month)[1]
        # Вычисляем range_duration
        range_duration = days_in_month * 86400
    elif date_range == 'year':
        start_date = date_today.replace(month=1, day=1)
        year = date_today.year
        print(year)
        days_in_year = calendar.isleap(year) and 366 or 365
        # Вычисляем range_duration
        range_duration = days_in_year * 86400

    total_category_time = {}

    for date, affairs in user_affairs[user_id]['affairs'].items():
        affair_date = datetime.strptime(date, '%d-%m-%Y')
        if affair_date >= start_date and affair_date <= date_today:
            for affair in affairs:
                category_name = affair['category'][0]
                category_color = affair['category'][1]
                duration = [int(i) for i in affair['duration'].split()]
                duration_seconds = duration[0]*3600 + duration[1]*60 + duration[2]

                if category_name in total_category_time:
                    total_category_time[category_name]['duration'] += duration_seconds
                else:
                    total_category_time[category_name] = {'duration': duration_seconds, 'color': category_color}

    print(total_category_time)
    total_category_time['  Другое'] = {'duration': range_duration - sum([value['duration'] for value in total_category_time.values()]), 'color': '#DBDBDB'}

    return jsonify(total_category_time)


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
