# необходимые библиотеки

from googlesearch import search
from termcolor import colored
import speech_recognition
import pyttsx3
import wikipediaapi
import random
import webbrowser
import traceback
import json
import os


class Trans:
    # мультиязычный ассистент

    with open("translations.json", "r", encoding="UTF-8") as f:
        trans = json.load(f)

    def get(self, stroklist: str):
        # получение перевода строки по тексту

        if stroklist in self.trans:
            return self.trans[stroklist][AT.speech_language]
        else:
            # перевод
            print(colored("{}".format(stroklist), "red"))
            return stroklist


def settings_golos():
    # настройки языка голосовго ассистента

    goloses = ttsEngine.getProperty("voices")

    if AT.speech_language == "en":
        AT.recognition_language = "en-US"
        ttsEngine.setProperty("voice", goloses[1].id)
    else:
        AT.recognition_language = "ru-RU"
        ttsEngine.setProperty("voice", goloses[0].id)


def record_audio(*args: tuple):
    # распознавание и запись речи

    with micro:
        reco_d = ""

        # улучшение сбора звука с микрофона

        recognizer.adjust_for_ambient_noise(micro, duration=2)

        try:
            print("Говорите...")
            audio = recognizer.listen(micro, 5, 5)

            f17 = False  # обычный флаг

            with open("microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            f17 = True

        # онлайн распознавание google

        if f17 is False:
            try:
                print("Обработка голоса...")
                reco_d = recognizer.recognize_google(audio, language=AT.recognition_language).lower()

            except speech_recognition.UnknownValueError:
                if AT.speech_language == "en":
                    vospr_AT_golos("What did you say again?")
                else:
                    vospr_AT_golos("Пожалуйста, повторите")


            # исключение проблем с интернетом

            except speech_recognition.RequestError:
                if AT.speech_language == "en":
                    vospr_AT_golos("Please, check your internet connection...")
                else:
                    vospr_AT_golos("Пожалуйста, проверьте своё интернет соединение")

            return reco_d


def vospr_AT_golos(stroklist_to_speech):
    # воспроизведение голоса

    ttsEngine.say(str(stroklist_to_speech))
    ttsEngine.runAndWait()


def hello(*args: tuple):
    # приветствие

    greetings = [
        interpretator.get("Hello, {}! How can I help you today?").format(person.name),
        interpretator.get("Good day to you {}! How can I help you today?").format(person.name)
    ]
    vospr_AT_golos(greetings[random.randint(0, len(greetings) - 1)])


def goodbye(*args: tuple):
    # речь о завершении работы

    farewells = [
        interpretator.get("Goodbye, {}! Have a nice day!").format(person.name),
        interpretator.get("See you soon, {}!").format(person.name)
    ]
    vospr_AT_golos(farewells[random.randint(0, len(farewells) - 1)])
    ttsEngine.stop()
    quit()


def google_search(*args: tuple):
    # запросы поиска в интернете

    if not args[0]: return
    search_term = " ".join(args[0])

    # ссылка
    url = "https://google.com/search?q=" + search_term
    webbrowser.get().open(url)

    # ссылка на результат
    search_results = []
    try:
        for _ in search(search_term, tld="com", lang=AT.speech_language, num=1, start=0, stop=1, pause=1.0, ):
            search_results.append(_)
            webbrowser.get().open(_)

    except TypeError:
        vospr_AT_golos(interpretator.get("Here is what I found for {} on google").format(search_term))
        return

    # исключения

    except:
        vospr_AT_golos(interpretator.get("Seems like we have a trouble. See logs for more information"))
        traceback.print_exc()
        return

    print(search_results)
    vospr_AT_golos(interpretator.get("Here is what I found for {} on google").format(search_term))


def youtube(*args: tuple):
    # поиск видео на ютуб

    if not args[0]: return
    search_term = " ".join(args[0])
    url = "https://www.youtube.com/results?search_query=" + search_term
    webbrowser.get().open(url)
    vospr_AT_golos(interpretator.get("Here is what I found for {} on youtube").format(search_term))


def open_google(*args: tuple):
    # открыть google

    url = "https://google.com/"
    webbrowser.get().open(url)


def open_yandex(*args: tuple):
    # открыть yandex

    url = "https://yandex.ru/"
    webbrowser.get().open(url)


def wikipedia(*args: tuple):
    # поиск в википедии
    if not args[0]: return

    search_term = " ".join(args[0])

    wiki = wikipediaapi.Wikipedia(AT.speech_language)

    # поиск по самому запросу

    wiki_page = wiki.page(search_term)
    try:
        if wiki_page.exists():
            vospr_AT_golos(interpretator.get("Here is what I found for {} on Wikipedia").format(search_term))
            webbrowser.get().open(wiki_page.fullurl)

            # чтение
            # ассистентом

            vospr_AT_golos(wiki_page.summary.split(".")[:2])
        else:
            # открытие ссылки в браузере по результатам (отсутствие в вики)

            vospr_AT_golos(interpretator.get(
                "Can't find {} on Wikipedia. But here is what I found on google").format(search_term))
            url = "https://google.com/search?q=" + search_term
            webbrowser.get().open(url)

    # исключения

    except:
        vospr_AT_golos(interpretator.get("Seems like we have a trouble. See logs for more information"))
        traceback.print_exc()
        return


def language(*args: tuple):
    # смена языка ассистента

    if AT.speech_language == "ru":
        AT.speech_language = "en"
        vospr_AT_golos(interpretator.get("Язык изменён на английский"))
    else:
        AT.speech_language = "ru"
        vospr_AT_golos(interpretator.get("Language switched to russian"))
    settings_golos()


def find_people(*args: tuple):
    # пробить информацию о человеке в соц. сетях

    if not args[0]: return

    facebook_search = "-".join(args[0])
    google_search = " ".join(args[0])
    vk_search = "_".join(args[0])

    # открытие ссылок

    vk = "https://vk.com/people/" + vk_search
    webbrowser.get().open(vk)

    facebook = "https://www.facebook.com/public/" + facebook_search
    webbrowser.get().open(facebook)

    vospr_AT_golos(interpretator.get("Here is what I found for {} on social nets").format(google_search))


def random_to(*args: tuple):
    # программа - рандомайзер, подбрасывает монетку :)

    fcount, h, t = 3, 0, 0

    for fl in range(fcount):
        if random.randint(0, 1) == 0:
            h += 1

    t = fcount - h
    w = "Tails" if t > h else "Heads"
    vospr_AT_golos(interpretator.get(w) + " " + interpretator.get("won"))


def execute_command_with_name(c_name: str, *args: list):
    # команды

    for key in commands.keys():
        if c_name in key:
            commands[key](*args)
        else:
            pass


# словарь команд

commands = {
    ("hello", "hi", "morning", "привет"): hello,
    ("bye", "goodbye", "quit", "exit", "stop", "пока", "выход", "стоп"): goodbye,
    ("search", "find", "найди", "поиск"): google_search,
    ("гугл", "google"): open_google,
    ("яндекс", "yandex"): open_yandex,
    ("video", "youtube", "watch", "видео", "смотреть"): youtube,
    ("wikipedia", "definition", "about", "определение", "википедия"): wikipedia,
    ("language", "язык"): language,
    ("person", "run", "пробей", "контакт"): find_people,
    ("toss", "coin", "монета", "подбрось"): random_to,
}


class Lichnost:
    # информация о пользователе

    name = ""
    native_language = ""
    target_language = ""


class GolosAT:
    # настройки голосового ассистента

    name = "Алиса"
    speech_language = "ru"
    recognition_language = "en"
    

if __name__ == "__main__":

    # инициализация инструментов распознавания и ввода речи
    recognizer = speech_recognition.Recognizer()
    micro = speech_recognition.Microphone()

    # инициализация инструмента синтеза речи
    ttsEngine = pyttsx3.init()

    # настройка данных голосового помощника
    AT = GolosAT()
    AT.name = "Alice"
    AT.speech_language = "ru"
    AT.recognition_language = "en"

    # установка голоса по умолчанию
    settings_golos()

    interpretator = Trans()

    # настройка данных пользователя
    person = Lichnost()
    person.name = ""
    person.home_city = ""
    person.native_language = "ru"
    person.target_language = "en"

    while True:
        # старт записи речи

        golos_input = record_audio()
        if golos_input is not None:
            os.remove("microphone-results.wav")
            print(colored(golos_input, "blue"))

            # разделение команд

            golos_input = golos_input.split(" ")
            c = golos_input[0]
            c_settings = [str(input_part) for input_part in golos_input[1:len(golos_input)]]
            execute_command_with_name(c, c_settings)