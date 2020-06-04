from enum import Enum
import xml.etree.ElementTree as ET
import os

BASE_URL_TRAINING = "./Dataset/reddit-traning/"
BASE_URL_TEST = "./Dataset/reddit-test/"

#Enum class that represents dataset format(training formal)
class DatasetTraining(Enum):
	POSITIVE = BASE_URL_TRAINING + "positive_examples_anonymous/"
	NEGATIVE = BASE_URL_TRAINING + "negative_examples_anonymous/"

class DatasetTest(Enum):
	POSITIVE = BASE_URL_TEST + "positive_examples_anonymous/"
	NEGATIVE = BASE_URL_TEST + "negative_examples_anonymous/"

#Custom exception if the dataset isn't providedss
class NoDatasetDefinedException(Exception):
	pass

#class that represents a single Reddit post
class Post:
	def __init__(self,id,date,title,info,content):
		self.id = id
		self.date = date
		self.title = title
		self.info = info
		self.content = content

	def __str__(self):
		post = ""

		post += Post.addLine("Id",self.id)
		post += Post.addLine("Date",self.date)
		post += Post.addLine("Title",self.title)
		post += Post.addLine("Content",self.content)

		return post

	@staticmethod
	def addLine(header,body):
		return Post.bold(header) + "\n" + body + "\n\n"

	#text bolding for clearer output
	@staticmethod
	def bold(text):
		return '\033[1m' + text + '\033[0m'

#Parser class 
class Parser:
	def __init__(self,datasets = []):
		self.datasets = datasets
		self.data = []

	def parse(self):
		if len(self.datasets) == 0:
			raise NoDatasetDefinedException

		data = {}

		for dataset in self.datasets:
			files = [file for file in os.listdir(dataset.value) if file.endswith(".xml")]

			dataset_posts = []
			for file in files:
				path = dataset.value+file
				tree = ET.parse(path.strip())

				id = ""
				for child in tree.getroot():
					id = child.text
					break
				
				for child in tree.getroot():

					title = ""
					text = ""
					date = ""
					info = ""
					for item in child:
						if(item.tag == "TITLE"):
							title = item.text.strip()
						elif(item.tag == "TEXT"):
							text = item.text.strip()
						elif(item.tag == "DATE"):
							date = item.text.strip()
						elif(item.tag == "INFO"):
							info = item.text.strip()
						else:
							raise NoDatasetDefinedException
					post = Post(id,date,title,info,text)
					dataset_posts.append(post)
			data[dataset] = dataset_posts
		return data

def main():
	parser = Parser([DatasetTraining.POSITIVE,DatasetTraining.NEGATIVE,DatasetTest.POSITIVE,DatasetTest.NEGATIVE])
	parser.parse()

main()