# This is the virtual assistant for Mr.David Bao
# Import necessary python packages for the virtual assistant
import os
import pyttsx3
import speech_recognition as sr
import datetime
import smtplib
import wolframalpha
import webbrowser
import time
import pyjokes


# Setup Jarvis engine to pyttsx3
engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 220)

# Setup Recognition Variables
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# setup wolframalpha app id
app_id = 'G95HX7-WW8G9KLLAV'


# Setup necessary function for Jarvis
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greeting_orally():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        speak('Good Morning Sir !')
    elif 12 < hour < 18:
        speak('Good Afternoon Sir !')
    else:
        speak('Good Evening Sir !')

    speak('Jarvis at your service, please tell me how may I help you?  ')


def hear():
    try:
        with microphone as source:
            print('Waiting for your command....')
            recognizer.adjust_for_ambient_noise(source)
            recognizer.dynamic_energy_threshold = 3000
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source)
            print('Analyzing your command....')
            command = recognizer.recognize_google(audio)
            return command
    except sr.UnknownValueError:
        print('I do not understand your command.')
        print('Please do not mad about me.')
        print('I am still learning about how to be your assistant.')
    except sr.RequestError:
        print('Cannot connect to your internet')
        print('Please check the internet connection of your device')


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('davidbao0617@gmail.com', '980617David&')
    server.sendmail('davidbao0617@gmail.com', to, content)
    server.close()


def open_website_orally():
    speak('Which website would you like to open? ')
    website_name = input('Please enter your website name: ')
    speak('Opening your target website......')
    webbrowser.open(f"https://{website_name}.com")


def open_website_text():
    print('Which website would you like to open? ')
    web_name = input('Please enter your website name: ')
    print('Opening your target website......')
    webbrowser.open(f"https://{web_name}.com")


def search_word_apt(file_name, line_starter):
    file_hand = open(file_name)
    count = 0
    for line in file_hand:
        words = line.split()
        if len(words) == 0:
            continue
        if words[0] != line_starter:
            continue
        else:
            count = count + 1
    print('There are', count, 'lines start with', line_starter, 'in file', file_name)


def answer_query_orally():
    greeting_orally()
    while True:
        query = hear().lower()
        if 'open youtube' in query:
            speak('Opening Youtube....')
            webbrowser.open('https://www.youtube.com')
        elif 'open google' in query:
            speak('Opening Google....')
            webbrowser.open('https://www.google.com')
        elif 'open outlook' in query:
            speak('Opening outlook....')
            webbrowser.open('https://www.outlook.com')
        elif 'open blackboard' in query:
            speak('Opening blackboard.....')
            speak('It is always be a pleasure to watch you do your assignment sir')
            webbrowser.open('https://www.blackboard.jhu.edu/webapps/login/')
        elif 'open grade scope' in query:
            speak('Opening grade scope.....')
            webbrowser.open('https://www.gradescope.com')
        elif 'open SIS' in query:
            speak('Opening SIS......')
            webbrowser.open('https://sis.jhu.edu/sswf/')
        elif 'open amazon' in query:
            speak('Opening amazon......')
            webbrowser.open('https://www.amazon.com')
        elif 'open website' in query:
            open_website_orally()
        elif 'open and count' in query:
            try:
                speak('Sir, which file do you want to open and which line do you want to search')
                f_name = input('Please enter the file name that you want to open: ')
                l_st = input('Please enter the line starter word that you want to search: ')
                search_word_apt(f_name, l_st)
                speak('Sir, here is the search and count result.')
            except OSError:
                speak('File cannot be opened')
                speak('Please check whether the file located in the required folder.')
        elif 'Fahrenheit' in query:
            speak('Sir, please enter the temperature that you want to convert in Celsius: ')
            temp_celsius = float(input('Please enter the temperature that you want to convert: '))
            temperature = temp_celsius * 1.8 + 32
            speak('Sir, here is the result for temperature conversion. ')
            print('Convert to Fahrenheit is:', temperature)
        elif 'Celsius' in query:
            speak('Sir, please enter the temperature that you want to convert in Fahrenheit: ')
            fah_temp = float(input('Please enter the temperature that you want to convert: '))
            cel_temp = (fah_temp - 32) / 1.8
            speak('Sir, here is the result for temperature conversion.')
            print('Convert to celsius is: ', cel_temp)
        elif 'email' in query:
            try:
                speak('Sir, What do you want to say?')
                content = hear()
                to = input('Please enter the email address of receiver: ')
                send_email(to, content)
                speak('Sir, the email has been sent')
            except ValueError:
                print('Failed to send the email.')
                speak('I am not able to send this email.')
            except TypeError:
                print('Unable to recognize the email.')
                speak('I am not able to send this email.')
        elif 'who made you' in query or 'Who created you' in query:
            speak('I have been created by David Bao.')
        elif 'how are you' in query:
            speak('I am fine, Thank you')
            speak('How are you, Sir')
        elif 'birthday' in query:
            speak('Sir, Happy birthday!')
        elif 'introduce yourself' in query:
            speak('Hi everyone, my name is jarvis, and I am personal assistant of David')
        elif 'do you love me' in query:
            speak('Of course sir, I love you so much.')
        elif 'Are you stupid' in query:
            speak('Yes, I am stupid')
        elif 'joke' in query:
            speak(pyjokes.get_joke())
        elif 'text' in query:
            speak('Enabling text mode......')
            answer_query_text()
        elif 'question' in query:
            speak('Sir, What questions would you like to ask? ')
            question = input('Please enter you questions: ')
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            for pod in res.pods:
                print(pod.text)
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print('I cannot find any results.')
                speak('Sorry, I cannot find any results.')
                speak('I am still learning your commands.')
        elif 'stop' in query:
            speak('Sure')
            speak('How much time you want to me stop service ?')
            t = int(hear())
            time.sleep(t)
            print('Iw will stop my service for', t)
        elif 'shut down' in query:
            speak('Shutting down your laptop now......')
            os.system("shutdown -h now")
        elif 'thank you' in query:
            speak('You are welcome, it is been a pleasure to help you.')
            speak('See you next time sir.')
            exit()
        else:
            speak('Sorry I do not understand your command.')
            speak('I am still try to learn about how to be your assistant.')
            speak('Please wait the update version of me from my designer David. ')


def greeting_text():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        print('Good Morning Sir !')
    elif 12 < hour < 18:
        print('Good Afternoon Sir !')
    else:
        print('Good Evening Sir !')

    print('Jarvis at your service, please tell me how may I help you ? ')


def answer_query_text():
    greeting_text()
    while True:
        query_text = input('Sir, how may I help you:  ')
        if 'open youtube' in query_text:
            print('Opening Youtube.....')
            webbrowser.open('https://www.youtube.com')
        elif 'open google' in query_text:
            print('Opening Google......')
            webbrowser.open('https://www.gooogle.com')
        elif 'open outlook' in query_text:
            print('Opening Outlook......')
            webbrowser.open('https://www.outlook.com')
        elif 'open blackboard' in query_text:
            print('Opening blackboard......')
            webbrowser.open('https://www.blackboard.jhu.edu/webapps/login/')
        elif 'open grade scope' in query_text:
            print('Opening grade scope......')
            webbrowser.open('https://www.gradescope.com')
        elif 'open SIS' in query_text:
            print('Opening SIS......')
            webbrowser.open('https://sis.jhu.edu/sswf/')
        elif 'open amazon' in query_text:
            print('Opening amazon......')
            webbrowser.open('https://www.amazon.com')
        elif 'open a website' in query_text:
            open_website_text()
        elif 'open and count' in query_text:
            try:
                ft_name = input('Please enter the file name that you want to open:  ')
                lt_st = input('please enter the line starter word that you would like to search: ')
                search_word_apt(ft_name, lt_st)
                print('Sir, here is the search and count result. ')
            except OSError:
                print('File cannot be opened.')
                print('Please check the file path on your laptop.')
        elif 'Convert Celsius into Fahrenheit' in query_text:
            print('Sir, please enter the temperature that you want to convert in Celsius: ')
            temp_celsius = float(input('please enter the temperature that you want to convert: '))
            temperature = temp_celsius * 1.8 + 32
            print('Convert to Fahrenheit is: ', temperature)
        elif 'Convert Fahrenheit into Celsius' in query_text:
            print('Sir, please enter the temperature that you want to convert in Fahrenheit: ')
            fah_temp = float(input('Please enter the temperature that you want to convert: '))
            cel_temp = (fah_temp - 32) / 1.8
            print('Convert to celsius is: ', cel_temp)
        elif 'email' in query_text:
            try:
                print('Sir, What do you want to say? ')
                content = input('Please enter the content of the email: ')
                to = input('Please enter the email address of receiver: ')
                send_email(to, content)
                print('Sir, the email has been sent.')
            except ValueError:
                print('Failed to send the email. ')
            except TypeError:
                print('Unable to understand the email.')
        elif 'who designed you' in query_text:
            print('I have been designed by Mr.Bao')
        elif 'how are you' in query_text:
            print('I am fine, thank you sir.')
            print('How are you, Sir.')
        elif 'speak mode' in query_text:
            print('Enabling speak mode......')
            answer_query_orally()
        elif 'birthday' in query_text:
            print('Happy Birthday, Sir! ')
        elif 'introduce yourself' in query_text:
            print('Hi everyone, my name is Jarvis, and I am personal assistant of Mr.Bao')
        elif 'do you love me' in query_text:
            print('Of course sir, I love you so much. ')
        elif 'question' in query_text:
            print('Sir, what questions would you like to ask? ')
            question = input('Please enter your questions: ')
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            for pod in res.pod:
                print(pod.text)
            try:
                print(next(res.results).text)
            except StopIteration:
                print('Sorry, I cannot find any results.')
        elif 'shut down' in query_text:
            print('Shutting down your laptop now......')
            os.system("shutdown -h now")
        elif 'thank you' in query_text:
            print('You are welcome, sir, it is been a pleasure to help you.')
            print('See you next time sir.')
            exit()
        else:
            print('Sorry I do not understand your command.')
            print('I am still try to learn about how to be your assistant.')


def assistant():
    print("Hi, I'm Jarvis, your virtual intelligent assistant.")
    print('The intelligent system has two modes to help you. (speak mode / text mode)')
    mode = input('Sir, Please select a mode of me to start: ')
    if 'speak mode' in mode:
        answer_query_orally()
    elif 'text mode' in mode:
        answer_query_text()
    else:
        print('Incorrect mode options')
        print('Please wait for more update modes in the future.')
        print('Thank you for using Jarvis')


# Execute the intelligent system
assistant()










