from flask import Flask, request
import logging
import json
import random  # import all things we need

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)  # logging

sessionStorage = {}
sessionDate = {}  # create dicts
best_phrases = ['Ты молодец', 'Ты сможешь! Осталось чуть-чуть', 'Давай!', 'Держись!', 'Ничто не достигается без усилий',
                'Я верю в тебя', 'Я знаю, ты сможешь преодолеть себя', 'Каждое усилие еще один шаг к победе',
                'Делай сколько можешь, завтра сможешь ещё больше', 'Победи себя и ты победитель']

warm_up = ['1540737/5c0d70d149bd986d48a6']


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
    if req['request']['original_utterance'].lower() in ['хватит']:
        res['response']['text'] = 'Жду тебя на следующей тренировочке'
        res['response']['end_session'] = True

    if req['request']['original_utterance'].lower() in ['помощь', 'помоги', "что ты умеешь?", "что ты умеешь",
                                                        "что ты можешь?", "что ты можешь"]:
        res['response']['text'] = 'Я буду следить за твоим временем на тренировках. Надо будет просто указать' \
                      ' количество упражнений, время выполнения каждого и количество подходов. Если ты' \
                      ' захочешь выйти просто скажи "хватит". Начнем?'

    if req['session']['new']:  # if dialog with person is new
        res['response'][
            'text'] = 'Привет! Я буду следить за твоим временем на тренировках. Надо будет просто указать' \
                      ' количество упражнений, время выполнения каждого и количество подходов. Если ты' \
                      ' захочешь выйти просто скажи "хватит". Начнем?:)'
        res['response']['tts'] = 'Привет! Я буду след+ить за твоим вр+еменем на тренир+овках. Надо будет' \
                                 'пр+осто указать количество упражнений, время выполнения каждого и ' \
                                 'количество подходов. Если ты захочешь выйти sil <[300]> просто ' \
                                 'скажи хватит. sil <[500]> Начнем?'  # message for user
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
            'хорошо',
            "начинаем",
            "начнем",
            "начнём",
            "поехали",
            "погнали",
            "гоу"
        ]:

            sessionStorage[user_id] = {
                'suggests': [
                    '1',
                    '2',
                    "3",
                    '4',
                    "5",
                    '6',
                    "7",
                    '8',
                    '9',
                    '10'
                ]
            }
            res['response']['text'] = 'Сколько будет упражнений?'
            res['response']['tts'] = 'Ск+олько б+удет упражн+ений?'
            res['response']['buttons'] = get_suggests(user_id)
            sessionDate[user_id]['new_training'] = req['request']['original_utterance'].lower()
            return

        else:
            res['response']['text'] = 'Не расслышала, повтори пожалуйста'
            res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуста'
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
                    "30 секунд",
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
                                                            '10', '11', '12']:
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
                'text'] = 'Если готов прямо сейчас начать тренировку, скажи "готов"'
            sessionDate[user_id]['right'] = True
            sessionDate[user_id]['training_started'] = False
            sessionDate[user_id]['exercizes'] = 0
            sessionDate[user_id]['round_counter'] = 0
            sessionStorage[user_id] = {
                'suggests': [
                    'готов'
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
            return
        if req['request']['original_utterance'].lower() in ['нет', 'не хочу', 'неа', 'нет конечно', 'не хочу']:
            res['response']['text'] = "Хорошо, начинаем заново, сделаем новую тренировку?"
            sessionDate[user_id] = {  # date for code
                'new_training': None,
                'ex_count': None,
                'time_of_ex': None,
                'rounds': None,
                'right': None,
                'training_started': False
            }
            return

        # У нас уже есть имя, и теперь мы ожидаем ответ на предложение начать.
        # В sessionDate[user_id]['training_started'] хранится True или False в зависимости от того,
        # начал пользователь игру или нет.
    if sessionDate[user_id]['training_started'] == False:
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

            # если есть не сделанные упражнения, то продолжаем тренировку
            morning_exercises(res, req)  # СДЕЛАЙ ФУНКЦИЮ ПОД ЗАРЯДКУ
            sessionStorage[user_id] = {
                'suggests': [
                    'готов'
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
            return

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
            res['response']['text'] = 'Не расслышала, повтори пожалуйста 249'  # that's okey
            res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'
            sessionStorage[user_id] = {
                'suggests': [
                    'да',
                    "нет"
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)
            return

    else:
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
            if (sessionDate[user_id]['round_counter'] + 1 == sessionDate[user_id]['rounds']) and (
                    sessionDate[user_id]['exercizes'] + 1 == sessionDate[user_id]['ex_count']):
                last_ex(res, req)
                sessionDate[user_id]['training_started'] = False
                return
            if sessionDate[user_id]['round_counter'] == sessionDate[user_id]['rounds']:
                res['response'][
                    'text'] = 'Ееееей! Тренировка окончена! Мы это сделали! Ты супер! Продолжай так же каждый день'
                res['end_session'] = True
                sessionDate[user_id]['training_started'] = False
                return
            if sessionDate[user_id]['exercizes'] + 1 == sessionDate[user_id]['ex_count']:
                ## если все упражнения сделаны, то заканчиваем сессию
                last_ex_of_round(res, req)
                sessionDate[user_id]['round_counter'] += 1
                sessionDate[user_id]['exercizes'] = 0
                sessionStorage[user_id] = {
                    'suggests': [
                        'готов'
                    ]
                }
                res['response']['buttons'] = get_suggests(user_id)
                return
            else:
                # если есть не сделанные упражнения, то продолжаем тренировку
                sessionDate[user_id]['training_started'] = True
                training_exercize(res, req)
                sessionStorage[user_id] = {
                    'suggests': [
                        'готов'
                    ]
                }
                res['response']['buttons'] = get_suggests(user_id)
                return

        if req['request']['original_utterance'].lower() in ['нет', 'не хочу', 'неа', 'нет конечно',
                                                            'не хочу']:
            res['response']['text'] = "Хорошо, начинаем заново, сделаем новую тренировку?"
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
            res['response']['text'] = 'Не расслышала, повтори пожалуйста 249'  # that's okey
            res['response']['tts'] = 'Не рассл+ышала sil <[350]> повтор+и пож+алуйста'
            sessionStorage[user_id] = {
                'suggests': [
                    'да',
                    "нет"
                ]
            }
            res['response']['buttons'] = get_suggests(user_id)


def last_ex_of_round(res, req):
    user_id = req['session']['user_id']
    res['response']['text'] = 'упражнениеее ты закончил один круг отдохни секунд 20 как бушь готов смолви готов'
    sessionStorage[user_id] = {
        'suggests': [
            'готов'
        ]
    }
    res['response']['buttons'] = get_suggests(user_id)


def last_ex(res, req):
    user_id = req['session']['user_id']
    res['response']['text'] = 'Осталось последнее упражнение, давай! погнали бла бла ' \
                              'ееееей  ты молодец тренировка завершена продолжай в том же духе каждый день'
    res['response']['tts'] = '<speaker audio="alice-sounds-game-win-1.opus">'


def morning_exercises(res, req):  # okey
    user_id = req['session']['user_id']
    res['response']['text'] = 'Перед тренировкой разомнитесь'
    res['response']['card'] = {}
    res['response']['card']['type'] = 'BigImage'
    res['response']['card']['title'] = 'Рекомендую размяться. Как будешь готов, скажи "готов"'
    res['response']['card']['image_id'] = warm_up[0]
    sessionDate[user_id]['training_started'] = True
    sessionStorage[user_id] = {
        'suggests': [
            'готов'
        ]
    }
    res['response']['buttons'] = get_suggests(user_id)


def training_exercize(res, req):
    user_id = req['session']['user_id']
    sessionDate[user_id]['exercizes'] += 1
    exez = sessionDate[user_id]['exercizes']
    sessionDate[user_id]['training_started'] = True
    res['response']['text'] = '3 2 1 0 нач'
    res['response']['tts'] = 'три sil <[1000]> два sil <[1000]> один sil <[1000]> Время пошло '
    sessionStorage[user_id] = {
        'suggests': [
            'готов'
        ]
    }
    res['response']['buttons'] = get_suggests(user_id)
    return


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

'''
расставить паузы поддерживающие фразы добавить
текст прописать
звук прописать
звук подключить
'''
