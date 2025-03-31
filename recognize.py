import os
import sys
import json
import pyaudio
import time

from vosk import Model, KaldiRecognizer, SetLogLevel

sys.path.append(os.path.join(os.path.dirname(__file__), 'class'))

import Mikki  # Теперь импорт должен работать
# Перенаправление stderr в devnull
sys.stderr = open(os.devnull, 'w')
# Установите уровень логирования на 0 (отключить)
SetLogLevel(0)
model_path = os.path.join(os.path.dirname(__file__), "model/vosk-model-small-ru-0.22")
# Инициализация модели
modelRU = Model(model_path)
# modelEN = Model(os.path.join(os.path.dirname(__file__) , "model/vosk-model-small-en-us-0.15"))
recognizerRU = KaldiRecognizer(modelRU, 16000)
# recognizerEN = KaldiRecognizer(modelEN, 16000)

# Настройка PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()

print("Слушаю...")
Mikki.voice('weke_up')
initMikkiBool = False
init_time = None
live_time = 20
listen_time = 2
ini_listen = None
previous_textRU = ""
final_text = ""
last_update_time = time.time()  # Время последнего обновления textRU
try:
# Бесконечный цикл для прослушивания микрофона
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        textRU = ""
        # textEN = ""
        if recognizerRU.AcceptWaveform(data) :
            result = recognizerRU.Result()
            textRU = json.loads(result)["text"]
        else:
            partial_result = recognizerRU.PartialResult()
            textRU = json.loads(partial_result)["partial"]
        # if recognizerEN.AcceptWaveform(data) :
        #     result = recognizerEN.Result()
        #     textEN = json.loads(result)["text"]
        # else:
        #     partial_result = recognizerEN.PartialResult()
        #     textEN = json.loads(partial_result)["partial"]

        if  textRU and textRU != previous_textRU:
            previous_textRU = textRU
            # print(textRU)
            final_text = textRU.strip()  # Добавляем новое распознанное слово
            # print("textRU :", textRU)
            # print("final_text :", final_text.strip())
             # Проверяем, прошло ли более 2-3 секунд с последнего обновления textRU
        if time.time() - last_update_time > 2.6:  # 3 секунды
            if final_text.strip() and initMikkiBool:  # Если есть текст для обработки
                print("Запуск команды Mikki с текстом:", final_text)
                init_time = time.time()
                if Mikki.MikkiCommand(final_text):
                    initMikkiBool = False
                final_text = ""  # Очищаем финальный текст после выполнения команды
                last_update_time = time.time()  # Обновляем время последнего обновления
            
        if textRU and not initMikkiBool :
            initMikkiBool = Mikki.MikkiInit(textRU)
            init_time = time.time()
            final_text = ""
            last_update_time = time.time()  # Обновляем время последнего обновления

        if init_time is not None and time.time() - init_time > live_time and initMikkiBool:
            print("Микки уснул...")
            Mikki.voice("sleep")
            final_text = ""
            initMikkiBool = False
            init_time = None
        textRU = ""
        # textEN = ""
except Exception as e:
    print("Произошла ошибка:", e)
# Закрытие потока и PyAudio (в данном случае это не будет достигнуто, но для полноты)



finally:
    stream.stop_stream()
    stream.close()
    p.terminate()