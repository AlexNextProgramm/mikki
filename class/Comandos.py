# class/Comandos.py
# Пример использования
commandMiki = [ "бай", "стоп", "да", "отдыхай", "умри"]
Name = { "привет микки", "микки", "мики", "веке", "мити", "никки", "ники"}
delete = {"открой", "запусти", "стартуй", "привет", "хай"}
commands = {
    "закрой браузер" : {'command' : "pkill chrome" , "voice" : "close_chrome" },
    "бразузер" : {'command' : "google-chrome" , "voice" : "open_chrome" },
    "гугл" : {'command' : "google-chrome" , "voice" : "open_chrome" },
    "музыка": {'command' : "google-chrome https://music.yandex.ru/ "},
    "найди": { 'command': "google-chrome https://www.google.com/search?q=[найди]" },
    "проект трекер": {'command': "code /project/tracker-widget"},
    "проект си плюс плюс" : {'command': "code \"/home/aleksandr/Рабочий стол/PROJECT/C++\""},
    "проект асситент": { "command": "code \"/home/aleksandr/Рабочий стол/PROJECT/mikki\"" },
    "папка дом": {'command': "nautilus $HOME"},
    "терминал": {'command': 'gnome-terminal'},
    "телеграмм": {'command': "/home/aleksandr/.config/Telegram/Telegram"},
    "папка":{'command': 'DISPLAY=:1 gnome-terminal -- bash -c "/home/aleksandr/Рабочий\ стол/PROJECT/mikki/class/script/find_folder [папка]; exec bash"' },
    "громче":{'command': 'amixer set Master 15%+'},
    "тише":{'command': 'amixer set Master 15%-'},
    "громкость пятьдесят процентов":{'command': 'amixer set Master 50%' },
    "громкость сто процентов": {'command':'amixer set Master 100%'},
    "громкость двадцать процентов": {'command':'amixer set Master 20%'},
    "настройки экранов": { "command": " gnome-control-center display" },
    "настройки": { "command": "gnome-control-center" },
}

