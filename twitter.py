import dao


tweetsDAO = dao.DAO("tweets")
tweetsDAO.dbConnTest()


def persistFromPickle(fileName):
	pass
