import dao
import pickle as pkl
import os


tweetsDAO = dao.DAO("tweets")
tweetsDAO.dbConnTest()


def persistFromPickle():
	Months = ["October", "November", "December", "January", "February", "March"]
	DataFolderPath = "metoo_data/"
	tweets = []
	for month in Months:
		for file in os.listdir(DataFolderPath + month):
			if file.endswith(".pkl"):
				tweets.extend(pkl.load(open(DataFolderPath + month + "/" + file, "rb")))

	tweetsDAO.batchCreate(tweets)


persistFromPickle()
