import re

class Plugin:
	active = True

	def __init__(self, controller):
		self.controller = controller

	def fetch_leaderboard(self):
		headers = None
		message = []

		if headers:
		    r = requests.get("https://groklearning.com/competition/challenge-advanced-2013/leaderboard/senior/", headers=headers)
		    soup = BeautifulSoup(r.content)

		    leaders = [{str(soup.select(".neat-table__cell--important")[i]).split("\n")[2].lstrip(): 
		                str(soup.select(".leaderboard-table__points-cell")[i]).split("\n")[1].lstrip()} for i in xrange(3)]

		    for position, person in enumerate(leaders):
		        for details in person   :
		            name = details
		            points = person[details]

		        message.append("{}. {} - {} points.".format(position+1, name, points))
		else:
		    message.append("Leaderboard functionality disabled.")

		return message

	def on_message(self, msg):
		leaderboard_grammar = re.match(r'^--leaderboard', msg)

		if leaderboard_grammar:
			for message in self.fetch_leaderboard():
				self.controller.send_message(message)