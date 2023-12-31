
__version__ = "1.0"

from kivymd.app import MDApp
from kivymd.uix.navigationdrawer import MDNavigationLayout, MDNavigationDrawer
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, ObjectProperty, NumericProperty
from kivy.lang.builder import Builder
from kivy.core.text import LabelBase

import random

class Test(MDBoxLayout):
	question : str = StringProperty("")
	ans1 : str = StringProperty("")
	ans2 : str = StringProperty("")
	ans3 : str = StringProperty("")
	ans4 : str = StringProperty("")
	realAnswer : str = StringProperty("")
	selectedAnswer : str = StringProperty("")
	
	selections : str = ListProperty([False, False , False , False])
	
	score : int = NumericProperty(0)
	
	def selectAnswer(self , pos : int ):
		for i in range(len(self.selections)):
			self.selections[i] = False
		
		self.selections[pos] = True
		
		if pos == 0:
			self.selectedAnswer = self.ans1
		elif pos == 1:
			self.selectedAnswer = self.ans2
		elif pos == 2:
			self.selectedAnswer = self.ans3
		else:
			self.selectedAnswer = self.ans4
	
	def reset(self):
		self.selectedAnswer = ""
		self.realAnswer = ""
		self.score = 0
		
		for i in range(4):
			self.selections[i] = False
	
	
	def checking(self):
		if self.realAnswer == self.selectedAnswer:
			self.score = 1
		


class Reviewer(Screen):
	verText : str = StringProperty("")
	holder : BoxLayout = ObjectProperty(None)
	
	corrected_view : BoxLayout = ObjectProperty()
	
	ratingText : str = StringProperty( "0%")
	correctText : str = StringProperty("Correct : 0")
	
	def on_pre_enter(self , *args):
		self.verText = "S U B M I T"
		questions = random.sample(self.parent.sheet.copy(), 5)
		
		for i , child in enumerate(self.holder.children):
			child.question = questions[i][0]
			child.ans1 = questions[i][1][0]
			child.ans2 = questions[i][1][1]
			child.ans3 = questions[i][1][2]
			child.ans4 = questions[i][1][3]
			child.realAnswer = questions[i][2]
	
	def on_pre_leave(self , *args):
		for child in self.corrected_view.children:
				child.md_bg_color = "red"
				self.ratingText = "0%"
	
	def submit(self):
		if self.verText ==  "R E T U R N":
			for child in self.holder.children:
				child.reset()
			self.correctText = "Correct : 0"
			self.parent.current = "home"
			return
		
		score = 0
		ratings = 0
		
		for n , child in enumerate(self.holder.children):
			child.checking()
			score += child.score
			if child.score :
				ratings += 20
				self.corrected_view.children[n].md_bg_color = "green"
		
		self.correctText = f"Correct : {score}"
		self.ratingText = f"{ratings}%"
		
		self.verText = "R E T U R N"

class HomePage(Screen):
	pass

class DeveloperScreen(Screen):
	pass

class AboutScreen(Screen):
	pass
	

class MainWindow(ScreenManager):
	
	sheet = [ 
		[ "What is the main language of Android Studio?" , ("Java", "C++", "Kotlin", "Python"), "Java" ],
		[ "Which one is not the programming languge?", ("Notepad", "C++", "Java", "Python"), "Notepad"],
		[ "What company own android?", ("Google", "Apple", "Nokia", "Samsung"), "Google"],
		[ "Is android studio good for app development?", ("Yes", "No", "Maybe", "IDK"), "Yes"],
		["Can we use Android Studio Online?", ("Yes", "No", "IDK", "Maybe"), "Yes"]
	]
	
	def on_kv_post(self , *args):
		self.add_widget(HomePage(name = "home"))
		self.add_widget(Reviewer(name="test"))
		self.add_widget(DeveloperScreen(name="dev"))
		self.add_widget(AboutScreen(name="about"))
		


class NavigationWindowHolder(MDNavigationLayout):
		pass
		

class QuizApp(MDApp):
	
	def build(self):
		return Builder.load_file("design.kv")


if __name__ == "__main__":
	LabelBase.register(name="title_font", fn_regular="Pangram-Bold.otf")
	LabelBase.register(name="reg_font", fn_regular="Pangram-Regular.otf")
	QuizApp().run()
