from termcolor import colored
import speech_recognition
import pyttsx3
import traceback
import json
import os


def settings_golos():
    # настройки языка голосовго ассистента

    goloses = ttsEngine.getProperty("voices")

    if AT.speech_language == "en":
        AT.recognition_language = "en-US"
        ttsEngine.setProperty("voice", goloses[1].id)
    else:
        AT.recognition_language = "ru-RU"
        ttsEngine.setProperty("voice", goloses[0].id)


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

def language(*args: tuple):
    # смена языка ассистента

    if AT.speech_language == "ru":
        AT.speech_language = "en"
        vospr_AT_golos(interpretator.get("Язык изменён на английский"))
    else:
        AT.speech_language = "ru"
        vospr_AT_golos(interpretator.get("Language switched to russian"))
    settings_golos()

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