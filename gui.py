import mysql
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
import runpy
import mysql.connector

import enviroment


# Simple gui with kivy

class SayHello(App):

    def build(self):

        self.initList = []

        self.window = GridLayout()
        self.window.cols = 1
        self.window.size = (1600, 1600)
        self.window.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        self.greeter = Label(text="Reddit stock scraper", font_size=24, color='#FFA500')
        self.window.add_widget(self.greeter)

        self.user = TextInput(text="Stock subreddits to scrape (separate by " " )", padding_y=(20, 20),
                              size_hint=(1, 0.5))
        self.window.add_widget(self.user)

        self.submit = Button(text="Scrape", size_hint=(1, 0.5), bold=True, background_color='#FFA500')
        self.submit.bind(on_press=self.loading)
        self.submit.bind(on_release=self.submit_button)
        self.window.add_widget(self.submit)

        self.viewBox = TextInput(text="", padding_y=(20, 20), size_hint=(1, 1), multiline=False, auto_indent=True)
        self.window.add_widget(self.viewBox)

        self.clear = Button(text="Clear")
        self.clear.bind(on_press=self.clearViewBox)
        self.window.add_widget(self.clear)

        self.window.spacing = 20

        return self.window

    # def updateTextBox(self):

    def submit_button(self, instance):
        open("subreddits.txt", "w")
        with open("subreddits.txt", "a") as f:
            f.write(self.user.text)
            self.user.text = ""

        runpy.run_path(path_name='crawl.py')
        self.greeter.text = "Reddit stock scraper"
        self.getTables(instance)

    def loading(self, instance):
        self.greeter.text = "Loading"

    def getTables(self, instance):
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=enviroment.password,
            database=enviroment.database
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM <enviroment.database><enviroment.table>")
        myresult = mycursor.fetchall()
        for x in myresult:
            self.initList.append(str(x[1]))
            self.initList.append(x[0])

        for i in range(len(self.initList)):
            self.viewBox.text += self.initList[i] + "\n"

    def clearViewBox(self, instance):
        self.viewBox.text = ""


if __name__ == "__main__":
    SayHello().run()
