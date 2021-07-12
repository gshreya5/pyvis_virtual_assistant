import wolframalpha
import wikipedia
import PySimpleGUI as sg                  
import pyttsx3
import speech_recognition as sr

# Define the window's contents
sg.theme('dark grey 9')
layout = [[sg.Text("Hello human! I am PyVis, your very own Python Virtual Assistant. How can I help you today?")],
          [sg.Input(key='-INPUT-')],
          [sg.Text(size=(40,1), key='-OUTPUT-')],
          [sg.Button('Search'), sg.Button('Mic'), sg.Button('Quit')]]

# Create the window
window = sg.Window('PyVis', layout)


# Display and interact with the Window using an Event Loop
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    engine = pyttsx3.init()  
    engine.setProperty("rate", 200) 
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say("Hello human! I am PyVis, your very own Python Virtual Assistant.") 
    engine.runAndWait()   
    
    if event == sg.WINDOW_CLOSED or event == 'Quit':
        break


    if event == 'Mic':
        r = sr.Recognizer()
        with sr.Microphone() as source:
            engine.say("How can I help you today?")
            engine.runAndWait()
            audio = r.listen(source)
        try:
            print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
            engine.say("Looking up wolfram and wikipedia for results to query " + r.recognize_google(audio))
            engine.runAndWait()
            values['-INPUT-'] =  r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            engine.say("Sorry could not understand you")
            engine.runAndWait()
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            engine.say("Looks like we have a connectivity issue")
            engine.runAndWait()

    try:
        answer_wiki = wikipedia.summary(values['-INPUT-'],sentences=1)
        engine.say("Wikipedia Results are "+ answer_wiki)
        engine.runAndWait()   
        
        app_id = "76EXJP-RWX9G4QG9Q"
        client = wolframalpha.Client(app_id)
        res = client.query(values['-INPUT-'])
        answer_wolf = next(res.results).text # print primary results
        engine.say("Wolfram Results are "+ answer_wolf+ "\nHope that helps! Bye now." )
        engine.runAndWait()
    except wikipedia.exceptions.PageError:
        app_id = "76EXJP-RWX9G4QG9Q"
        client = wolframalpha.Client(app_id)
        res = client.query(values['-INPUT-'])
        answer_wolf = next(res.results).text # print primary results
        engine.say("Wolfram Results are "+ answer_wolf + "\nHope that helps! Bye now.")
        engine.runAndWait()
    except Exception :
        engine.say("Sorry I can't help with this.")
        engine.runAndWait()    


    #sg.PopupNonBlocking("Wolfram Results:\n "+ answer_wolf +"\nWikipedia Results:\n "+ answer_wiki + "\nHope that helps! Bye now.")

# Finish up by removing from the screen
window.close()
