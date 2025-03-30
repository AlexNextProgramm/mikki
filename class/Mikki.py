# class/Mikki.py
import subprocess
import os
import re
import sys
import Comandos
commands = Comandos.commands
commandMiki = Comandos.commandMiki
Name = Comandos.Name
deleteName = Comandos.delete
def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_closest_command(command_list, input_command):
    closest_command = None
    min_distance = float('inf')

    for command in command_list:
        distance = levenshtein_distance(command, input_command)
        if distance < min_distance:
            min_distance = distance
            closest_command = command

    return closest_command, min_distance



def voice(command):
    current_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", f"{command}.wav")
    try:
        # Execute the command using subprocess
        subprocess.Popen("aplay \""+current_script_path+"\"", shell=True)
        # subprocess.run(["aplay", current_script_path], check=True)
    except Exception as e:
            print("Ошибка при выполнении команды:", e)

def MikkiInit(textRU):
    INIT = False
    closest_command, distance = find_closest_command(Name, textRU)
    if (distance <= 1):
        print("Инициализация Микки")
        INIT = True
        if (MikkiCommand(textRU)):
             INIT = False
        else :
            voice("activate")
    return INIT

deafCommand = ""
search = "" 
def MikkiCommand(textRU):
    textRU = wordDelete(textRU)
    if textRU == '':
        return False
    global deafCommand
    global search
    cmdM, disM = find_closest_command(commandMiki, textRU)

    if(disM != 0):
        cmdM = ""
    searchC = searthCMD(textRU)
    if (searchC is not None):
        return searchC


    closest_command, distance = find_closest_command(commands.keys(), textRU)  # Убедитесь, что 'commands' доступен
    print(closest_command, " ", distance)
    if (cmdM == "да" and deafCommand ):
        closest_command = deafCommand.strip()
        deafCommand = ""
        distance = 0
    if (cmdM == "умри"):
        voice("ded")
        sys.exit(0)
        # distance = 0

    if ( cmdM == "стоп" or cmdM == "отдыхай" or cmdM == "бай" or cmdM == "отдыхать" ):
        print("Деинциализация Микки")
        voice("start_command")
        return True

    if distance <= 1:
        print("Запускаю команду:", closest_command)
        deafCommand = ""
        voice("start_command")
        try:
            # Execute the command using subprocess
            subprocess.Popen(commands.get(closest_command).get('command'), shell=True)
        except Exception as e:
            print("Ошибка при выполнении команды:", e)
        return True
    elif (distance < 5):
        deafCommand = closest_command
        print("Не расслышал: ", closest_command, "distance",  distance)
        notify(" Вы иммелли ввиду " + closest_command + "?"  )
        voice("deactivate")
        return False  # Возвращаем False, если команда не распознана

def wordDelete(text):
    global deleteName
    global Name
    for NameText in Name:
        text = text.replace(NameText, "").strip()
    for NameText in deleteName:
         text = text.replace(NameText, "").strip()
    return text

def searthCMD(textRU):
    global search
    if "найди" in textRU or search != "" :
        search += textRU
        google = commands.get("найди").get('command')
        if textRU.strip() == "найди" :
            search = " "
            return False
        search = search.replace('найди', "").strip()
        search = search.replace(' ', '+').strip()
        if search.strip()  == "":
            return False
        google = google.replace('[найди]', search)
        
        print("Запускаю команду: Найди")
        voice("start_command")

        try:
            # Execute the command using subprocess
            subprocess.Popen(google, shell=True)
            search = ""
        except Exception as e:
            print("Ошибка при выполнении команды:", e)
        return True
    if "папка" in textRU or search != "" :
        search += textRU
        folder = commands.get("папка").get('command')
        search = search.replace('папка', "").strip()
        if search.strip()  == "":
            return False
        folder = folder.replace('[папка]', search)
        print("Запускаю команду: Папка")
        voice("start_command")

        try:
            # Execute the command using subprocess
            subprocess.Popen(folder, shell=True)
            search = ""
        except Exception as e:
            print("Ошибка при выполнении команды:", e)
        return True

def notify(text, header = "Микки"):
    subprocess.Popen("notify-send \"" + header +"\" \"" + text + "\""  , shell=True)
