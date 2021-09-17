import speech_recognition as sr
import pyttsx3
import datetime
import sys
import webbrowser
import time
import os


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
            print(command)
            return command

    def cant_do(self):
        self.speak("Sorry, I do not have that ability yet.")

    # Respond to the command given by the user
    def respond(self, command):
        # if the name of the instance is in the command
        if self.name.lower() in command:
            self.speak("Yes")

        elif "what is the time" in command:
            now = datetime.datetime.now()
            hours = now.strftime("%H")
            if hours > str(12):
                hours = int(hours) - 12
            elif hours == '00':
                hours = int(hours) + 12
            self.speak(now.strftime(f"{str(hours)}:%M %p"))

        elif "goodbye" in command:
            self.speak("Goodbye, have a nice day.")
            sys.exit()

        elif "search" in command:
            self.speak('What would you like to search for?')
            print("ask for something to search for...")
            print("Listening...")
            query = self.listen()
            webbrowser.open("https://google.com/search?query="+query)

        elif "add a to-do" in command:
            self.speak("What to-do would you like to add?")
            print("Say a to-do that you would like to add...")
            print("Listening...")
            todo = self.listen()
            self.todos.append(todo)
            self.speak("Your to-do has successfully been added.")
            print("Your to-dos ->", self.todos)

        elif "remove a to-do" in command:
            self.speak("What to-do would you like to remove?")
            print("Say a to-do that you would like to remove", self.todos)
            print("Listening...")
            todo = self.listen()
            if todo not in self.todos:
                self.speak(
                    "That to-do does not exist. If you meant to say a different to-do, please ask to remove a to-do again.")
                print("Listening...")
                todo = self.listen()
            if todo in self.todos:
                self.todos.remove(todo)
                self.speak("Your to-do has been successfully removed.")
                print("Your to-dos ->", self.todos)

        elif "show me my to-do list" in command:
            self.speak("Here are your to-dos.")
            print("Your to-dos ->", self.todos)

        elif "what day is it" in command:
            self.speak(
                f'Today is {datetime.datetime.today().strftime("%A")}, {datetime.date.today().strftime("%B %d, %Y")}')

        elif "create a file" in command:
            self.speak("What would you like the filename to be?")
            print("Say the file name...")
            filename = self.listen()
            # Create a file if that file does not exist.
            new_file = open(f'{filename}.txt', 'x')
            self.speak(
                "Your file has been successfully created. Would you like to edit this file?")
            print("Listening...")
            usr_response = self.listen()

            if 'yes' in usr_response:
                self.speak("What would you like to write in this file?")
                file = open(f"{filename}.txt", 'a')
                print("Start listing the contents of this file...")
                file_content = self.listen()
                file.write(file_content)
                file.close()
                self.speak("Your content has successfully been added.")
                print("Saved!")

            if 'no' in usr_response:
                self.speak("Okay.")
                print("No changes will be added to this file.")

        elif "edit a file" in command:
            self.speak("What file would you like to edit?")
            print("Please say the file name that you would like to edit...")
            filename = self.listen()

            if os.path.exists(f"{filename}.txt"):
                self.speak("What would you like to add to this file?")
                print("List what you would like to add to this file.")
                action = self.listen()
                if action == 'add':
                    self.speak("What would you like to add to this file?")
                    file = open(f"{filename}.txt", 'a')
                    print("Say something you would like to add to this file.")
                    add = self.listen()
                    file.write("\n"+add)
                    file.close()
                    self.speak("Your content has been successfully added.")
                    print("Saved!")
                else:
                    self.speak("That action does not exist.")
            else:
                self.speak("That file does not exist.")

        elif "delete a file" in command:
            self.speak("What file would you like to delete?")
            print("Please say the file that you would like to delete...")
            filename = self.listen()
            if os.path.exists(f'{filename}.txt'):
                os.remove(f'{filename}.txt')
                self.speak("Your file has been removed.")
            else:
                self.speak("Sorry, that file does not exist.")

        else:
            self.cant_do()


# Create assistant
assistant = Assistant("Computer", [])

# Get the assistant's greeting
greeting = assistant.greet()

# Use the speak() method and pass in the greeting to greet the user
assistant.speak(greeting)

print("Listening...")
while True:
    # This command variable contains what command was said to the assistant and prints it.
    command = assistant.listen()
    assistant.respond(command)
