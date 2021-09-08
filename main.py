import speech_recognition as sr
import pyttsx3
import datetime
import sys
import webbrowser


r = sr.Recognizer()
engine = pyttsx3.init()


class Assistant:
    def __init__(self, name, todos):
        self.name = name
        self.todos = todos


    def greet(self):
        return f'Hello, I am a {self.name}ized voice assistant. How can I assist you today?'


    def speak(self, speech):
        engine.say(speech)
        engine.runAndWait()


    def listen(self):
        with sr.Microphone() as source:
            audio = r.listen(source)
            command = ''
            try:
                command = r.recognize_google(audio)
            except sr.UnknownValueError:
                self.speak("Sorry, can you please repeat that?")
            except sr.RequestError:
                self.speak(
                    "My apologies, my speech service is down. Please try again later.")
                sys.exit()
            return command


    def cant_do(self):
        self.speak("Sorry, I do not have that ability yet. Please try again later.")


    # Respond to the command given by the user
    def respond(self, command):
        # if the name of the instance is in the command
        if self.name.lower() in command:
            self.speak("Yes")

        if "what is the time" in command:
            now = datetime.datetime.now()
            hours = now.strftime("%H")
            if hours > str(12):
                hours = int(hours) - 12
            elif hours == '00':
                hours = int(hours) + 12
            self.speak(now.strftime(f"{str(hours)}:%M %p"))

        if "goodbye" in command:
            self.speak("Goodbye, have a nice day.")
            sys.exit()

        if "search" in command:
            self.speak('What would you like to search for?')
            print("ask for something to search for...")
            query = self.listen()
            webbrowser.open("https://google.com/search?query="+query)

        if "add a to-do" in command:
            self.speak("What to-do would you like to add?")
            print("Say a to-do that you would like to add...")
            todo = self.listen()
            self.todos.append(todo)
            self.speak("Your to-do has successfully been added.")
            print("Your to-dos ->", self.todos)

        if "remove a to-do" in command:
            self.speak("What to-do would you like to remove?")
            print("Say a to-do that you would like to remove", self.todos)
            todo = self.listen()
            if todo not in self.todos:
                self.speak("That to-do does not exist. If you meant to say a different to-do, please ask to remove a to-do again.")
                todo = self.listen()
            if todo in self.todos:
                self.todos.remove(todo)
                self.speak("Your to-do has been successfully removed.")
                print("Your to-dos ->", self.todos)

        if "show me my to-do list" in command:
            self.speak("Here are your to-dos.")
            print("Your to-dos ->", self.todos)

        if "what day is it" in command:
            self.speak(f'Today is {datetime.datetime.today().strftime("%A")}, {datetime.date.today().strftime("%B %d, %Y")}')

        else:
            self.cant_do()


# Create assistant
assistant = Assistant("Computer", [])

# Get the assistant's greeting
greeting = assistant.greet()

# Use the speak() method and pass in the greeting to greet the user
assistant.speak(greeting)

while True:
    # This command variable contains what command was said to the assistant and prints it.
    command = assistant.listen()
    print(command)
    assistant.respond(command)
