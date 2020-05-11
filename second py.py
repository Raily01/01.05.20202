from flask import Flask, request
import logging
import json
import random  # import all things we need

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)  # logging

sessionStorage = {}
sessionDate = {}  # create dicts


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)  # main function
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']  # initializate user id
    if req['session']['new']:  # if dialog with person is new
        res['response']['text'] = 'Привет! Сделаем новую тренировку?'
        res['response']['tts'] = 'Прив+ет! Сд+елаем н+овую тренир+овку?'  # message for user
        sessionDate[user_id] = {  # date for code
            'new_training': None,
            'ex_count': None,
            'time_of_ex': None,
            'rounds': None,
            'right': None,
            'training_started': False
        }
        sessionStorage[user_id] = {  # dict for buttons
            'suggests': [
                "ДА!",
                "Нет",
                "Конечно!",
            ]
        }
        sessionDate[user_id]['exercizes'] = []
        res['response']['buttons'] = get_suggests(user_id)  # get button's json in correct form
        return

    if sessionDate[user_id]['new_training'] is None:
        if req['request']['original_utterance'].lower() in ['нет', 'не хочу', 'неа', 'нет конечно', 'не хочу']:
            res['response']['text'] = 'Жду вас на следующей тренировке:)'
            res['response']['tts'] = 'Жд+у в+ас н+а сл+едующей тренир+овочке'
            res['response']['end_session'] = True
            sessionDate[user_id]['new_training'] = req['request']['original_utterance'].lower()
            return
        if req['request']['original_utterance'].lower() in [
            'ладно',
            'да!',
            'да',
            'конечно',
            'конечно!',
            'окей',
            'хорошо'
        ]:

            sessionStorage[user_id] = {
                'suggests': [
                    "3",
                    "5",
                    "7",
                ]
            }
            res['response']['text'] = 'Сколько будет упражнений?'
            res['response']['tts'] = 'Ск+олько б+удет упражн+ений?'
            res['response']['buttons'] = get_suggests(user_id)
            sessionDate[user_id]['new_training'] = req['request']['original_utterance'].lower()
            return

        else:
            res['response']['text'] = 'Не расслышала, повтори пожалуйста'
            res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'
            return
    if sessionDate[user_id]['ex_count'] is None:
        if req['request']['original_utterance'].lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11',
                                                            '12',
                                                            '13', '14', '15', '16', '17', '18', '19', '20', '21',
                                                            '22',
                                                            '23', '24', '25', '26', '27', '28', '29', '30', '31',
                                                            '32',
                                                            '33', '34', '35', '36', '37', '38', '39', '40', '41',
                                                            '42',
                                                            '43', '44', '45', '46', '47', '48', '49', '50', '51']:
            res['response']['text'] = 'С какой продолжительностью будет идти каждое упражнение?'
            res['response']['tts'] = 'С как+ой пр+одол ж+ительностью б+удет ид+ти к+аждое упражн+ение?'
            sessionStorage[user_id] = {
                'suggests': [
                    "0.5 минуты",
                    "1 минута",
                    "2 минуты",
                    "3 минуты",
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
            ex_count = get_number(req)
            sessionDate[user_id]['ex_count'] = ex_count
            return
        else:
            res['response']['text'] = 'Не расслышала, повтори пожалуйста'
            res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'
            return
    if sessionDate[user_id]['time_of_ex'] == None:
        if req['request']['original_utterance'].lower() in ['0.5 минуты', '10 секунд', '15 секунд', '20 секунд',
                                                            '30 секунд', '25 секунд', '35 секунд', '40 секунд',
                                                            '45 секунд',
                                                            '50 секунд', '55 секунд', '60 секунд', '1 минута',
                                                            'пол минуты',
                                                            'полторы минуты', '2 минуты', '3 минуты', '4 минуты',
                                                            '5 минут',
                                                            '6 минут', '7 минут', '8 минут', '9 минут', '10 минут',
                                                            '11 минут', '12 минут', '13 минут', '14 минут', '15 минут',
                                                            '16 минут']:
            res['response']['text'] = 'Сколько будет кругов(сетов, повторов)?'
            res['response']['tts'] = 'Ск+олько б+удет круг+ов?'
            sessionStorage[user_id] = {
                'suggests': [
                    '1',
                    "2",
                    "3",
                    "4",
                    '5',
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)

            time_of_ex = get_number(req)
            sessionDate[user_id]['time_of_ex'] = time_of_ex
            print(time_of_ex)
            return
        else:
            res['response']['text'] = 'Не расслышала, повтори пожалуйста'
            res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'
            return
    if sessionDate[user_id]['rounds'] == None:
        if req['request']['original_utterance'].lower() in ['1', '2', '3', '4', '5',
                                                            '6', '7', '8', '9',
                                                            '10 кругов', '11 кругов', '12 кругов']:
            rounds = get_number(req)
            sessionDate[user_id]['rounds'] = rounds
            text = 'Отлично, получается {} упражнений с длительностью {} минуты и всего {} цикла, верно?'.format(
                sessionDate[user_id]['ex_count'], sessionDate[user_id]['time_of_ex'], sessionDate[user_id]['rounds'])
            res['response']['text'] = text
            res['response'][
                'tts'] = 'Отл+ично sil <[500]> получ+ается упр+ажнений с дл+ительностью и всег+о ц+икла sil <[500]> верно?'
            sessionStorage[user_id] = {
                'suggests': [
                    'да',
                    "нет"
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
            return
        else:
            res['response']['text'] = 'Не расслышала, повтори пожалуйста'
            res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'
            return
    if sessionDate[user_id]['right'] == None:
        if req['request']['original_utterance'].lower() in [
            'ладно',
            'да!',
            'да',
            'конечно',
            'конечно!',
            'окей',
            'хорошо',
            "верно"
        ]:
            res['response'][
                'text'] = 'чето тип надо начать. тип ты готов?'  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            sessionDate[user_id]['right'] = True
            sessionDate[user_id]['exercizes'] = []
            sessionDate[user_id]['training_started'] = False
            return
        if req['request']['original_utterance'].lower() in ['нет', 'не хочу', 'неа', 'нет конечно', 'не хочу']:
            res['response']['text'] = "все равно будем так заниматься"
            return










    else:
        # У нас уже есть имя, и теперь мы ожидаем ответ на предложение начать.
        # В sessionDate[user_id]['training_started'] хранится True или False в зависимости от того,
        # начал пользователь игру или нет.
        if not sessionDate[user_id]['training_started']:
            # игра не начата, значит мы ожидаем ответ на предложение сыграть.
            if req['request']['original_utterance'].lower() in [
                'ладно',
                'да!',
                'да',
                'конечно',
                'конечно!',
                'окей',
                'хорошо',
                "верно",
                "готов"
            ]:
                # если пользователь согласен, то проверяем не сделал ли он все упражнения уже
                # По схеме можно увидеть, что здесь окажутся и пользователи, которые уже сделали всё
                if len(sessionDate[user_id]['exercizes']) == 4:
                    # если все упражнения сделаны, то заканчиваем сессию
                    res['response']['text'] = 'Молодец! Ты выполнил все упражнения и тд. жду тя на след трене чмок'
                    res['end_session'] = True
                else:
                    # если есть не сделанные упражнения, то продолжаем тренировку
                    sessionDate[user_id]['training_started'] = True
                    # номер попытки, чтобы показывать фото по порядку
                    sessionDate[user_id]['attempt'] = 1
                    # функция, которая выбирает город для игры и показывает фото
                    training_exercize(res, req)
            if req['request']['original_utterance'].lower() in ['нет', 'не хочу', 'неа', 'нет конечно',
                                                                'не хочу']:
                res['response']['text'] = "бе, начинаем заново, сделаем новую тренировку?"
                sessionDate[user_id] = {  # date for code
                    'new_training': None,
                    'ex_count': None,
                    'time_of_ex': None,
                    'rounds': None,
                    'right': None,
                    'training_started': False
                }
                return
            else:
                res['response']['text'] = 'Не расслышала, повтори пожалуйста'  # that's okey
                res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'
                sessionStorage[user_id] = {
                    'suggests': [
                        'да',
                        "нет"
                    ]
                }
                res['response']['buttons'] = get_suggests(user_id)

        else:
            training_exercize(res, req)


def training_exercize(res, req):
    user_id = req['session']['user_id']
    attempt = sessionStorage[user_id]['attempt']
    if attempt == 1:
        # если попытка первая, то случайным образом выбираем город для гадания
        city = random.choice(list(cities))
        # выбираем его до тех пор пока не выбираем город, которого нет в sessionStorage[user_id]['guessed_cities']
        while city in sessionStorage[user_id]['guessed_cities']:
            city = random.choice(list(cities))
        # записываем город в информацию о пользователе
        sessionStorage[user_id]['city'] = city
        # добавляем в ответ картинку
        res['response']['card'] = {}
        res['response']['card']['type'] = 'BigImage'
        res['response']['card']['title'] = 'Что это за город?'
        res['response']['card']['image_id'] = cities[city][attempt - 1]
        res['response']['text'] = 'Тогда сыграем!'
    else:
        # сюда попадаем, если попытка отгадать не первая
        city = sessionStorage[user_id]['city']
        # проверяем есть ли правильный ответ в сообщение
        if get_city(req) == city:
            # если да, то добавляем город к sessionStorage[user_id]['guessed_cities'] и
            # отправляем пользователя на второй круг. Обратите внимание на этот шаг на схеме.
            res['response']['text'] = 'Когда будешь готов скажи "готов"'
            sessionStorage[user_id]['guessed_cities'].append(city)
            sessionStorage[user_id]['game_started'] = False
            return
        else:
            # если нет
            if attempt == 3:
                # если попытка третья, то значит, что все картинки мы показали.
                # В этом случае говорим ответ пользователю,
                # добавляем город к sessionStorage[user_id]['guessed_cities'] и отправляем его на второй круг.
                # Обратите внимание на этот шаг на схеме.
                res['response']['text'] = f'Вы пытались. Это {city.title()}. Сыграем ещё?'
                sessionStorage[user_id]['game_started'] = False
                sessionStorage[user_id]['guessed_cities'].append(city)
                return
            else:
                # иначе показываем следующую картинку
                res['response']['card'] = {}
                res['response']['card']['type'] = 'BigImage'
                res['response']['card']['title'] = 'Неправильно. Вот тебе дополнительное фото'
                res['response']['card']['image_id'] = cities[city][attempt - 1]
                res['response']['text'] = 'А вот и не угадал!'
    # увеличиваем номер попытки доля следующего шага
    sessionDate[user_id]['attempt'] += 1


def get_number(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.NUMBER':
            return entity['value']


def get_minute(req):
    for entity in req['request']['nlu']['entities']:
        if entity['type'] == 'YANDEX.DATETIME':
            print(entity['value'])
            return entity['value'].get('minute', None)


def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:]
    ]

    return suggests


if __name__ == '__main__':
    app.run()
