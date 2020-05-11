from flask import Flask, request
import logging
import json

app = Flask(__name__)

# Устанавливаем уровень логирования
logging.basicConfig(level=logging.INFO)

sessionStorage = {}
sessionDate = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json!r}')

    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи
    # библиотеки json преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info(f'Response:  {response!r}')

    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    print()

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        # Запишем подсказки, которые мы ему покажем в первый раз
        sessionDate[user_id] = {
            'new_trening': None,
            'ex_count': None,
            'time_of_ex': None,
            'rounds': None,
            'right': None
        }
        sessionStorage[user_id] = {
            'suggests': [
                "ДА!",
                "Нет",
                "Конечно!",
            ]
        }
        # Заполняем текст ответа
        res['response']['text'] = 'Привет! Сделаем новую тренировку?'
        res['response']['tts'] = 'Прив+ет! Сд+елаем н+овую тренир+овку?'
        # Получим подсказки
        res['response']['buttons'] = get_suggests(user_id)
        return

    # Сюда дойдем только, если пользователь не новый,
    # и разговор с Алисой уже был начат
    # Обрабатываем ответ пользователя.
    # В req['request']['original_utterance'] лежит весь текст,
    # что нам прислал пользователь
    # Если он написал 'ладно', 'куплю', 'покупаю', 'хорошо',
    # то мы считаем, что пользователь согласился.
    # Подумайте, всё ли в этом фрагменте написано "красиво"?
    '''if req['session']['message_id'] == 2 and req['request']['original_utterance'].lower() in ['1', '2', '3', '4', '5',
                                                                                              '6', '7', '8', '9',
                                                                                              '10', '11', '12',
                                                                                              '13', '14', '15', '16',
                                                                                              '17', '18', '19', '20',
                                                                                              '21', '22',
                                                                                              '23', '24', '25', '26',
                                                                                              '27', '28', '29', '30',
                                                                                              '31', '32',
                                                                                              '33', '34', '35', '36',
                                                                                              '37', '38', '39', '40',
                                                                                              '41', '42',
                                                                                              '43', '44', '45', '46',
                                                                                              '47', '48', '49', '50',
                                                                                              '51']:
        res['response']['text'] = 'Приветули'
        return'''

    if req['request']['original_utterance'].lower() in [
        'ладно',
        'да!',
        'да',
        'конечно',
        'конечно!',
        'окей',
        'хорошо'
    ]:
        # Пользователь согласился, прощаемся.

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

        # res['response']['end_session'] = True
        return

    elif req['request']['original_utterance'].lower() in ['нет', 'не хочу', 'неа', 'нет конечно', 'не хочу']:
        res['response']['text'] = 'Жду вас на следующей тренировке:)'
        res['response']['tts'] = 'Жд+у в+ас н+а сл+едующей тренир+овочке'
        res['response']['end_session'] = True
        return
    elif req['request']['original_utterance'].lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12',
                                                          '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
                                                          '23', '24', '25', '26', '27', '28', '29', '30', '31', '32',
                                                          '33', '34', '35', '36', '37', '38', '39', '40', '41', '42',
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
        return
    if req['request']['original_utterance'].lower() in ['0.5 минуты', '10 секунд', '15 секунд', '20 секунд',
                                                        '30 секунд', '25 секунд', '35 секунд', '40 секунд', '45 секунд',
                                                        '50 секунд', '55 секунд', '60 секунд', '1 минута', 'пол минуты',
                                                        'полторы минуты', '2 минуты', '3 минуты', '4 минуты', '5 минут',
                                                        '6 минут', '7 минут', '8 минут', '9 минут', '10 минут',
                                                        '11 минут', '12 минут', '13 минут', '14 минут', '15 минут',
                                                        '16 минут']:
        res['response']['text'] = 'Сколько будет кругов(сетов, повторов)?'
        res['response']['tts'] = 'Ск+олько б+удет круг+ов?'
        sessionStorage[user_id] = {
            'suggests': [
                '1 круг',
                "2 круга",
                "3 круга",
                "4 круга",
                '5 круга',
            ]
        }

        time = req['request']['original_utterance'].lower()
        res['response']['buttons'] = get_suggests(user_id)
        return
    elif req['request']['original_utterance'].lower() in ['1 круг', '2 круга', '3 круга', '4 круга', '5 кругов',
                                                          '6 кругов', '7 кругов', '8 кругов', '9 кругов',
                                                          '10 кругов', '11 кругов', '12 кругов']:
        res['response']['text'] = 'Отлично, получается {} упражнений с длительностью {} и всего {} цикла, верно?'
        res['response'][
            'tts'] = 'Отл+ично sil <[500]> получ+ается упр+ажнений с дл+ительностью и всег+о ц+икла sil <[500]> верно?'
    else:
        res['response']['text'] = 'Не расслышала, повтори пожалуйста'
        res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'

    # Если нет, то убеждаем его купить слона!
    '''res['response']['text'] = \
        f"Все говорят '{req['request']['original_utterance']}', а ты купи слона!"
    res['response']['buttons'] = get_suggests(user_id)'''


def about_exercize(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        # Запишем подсказки, которые мы ему покажем в первый раз

        sessionStorage[user_id] = {
            'suggests': [
                "3",
                "5",
                "7",
            ]
        }
        # Заполняем текст ответа
        res['response']['text'] = 'Сколько будет упражнений?'
        # Получим подсказки
        # res['response']['buttons'] = get_suggests(user_id)
        return


# Функция возвращает две подсказки для ответа.
def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:]
    ]

    return suggests


if __name__ == '__main__':
    app.run()
