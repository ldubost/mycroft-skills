# Copyright 2016 Ludovic Dubost
#
# This file is a skill for the MyCroft.AI. More information in the README file
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import json, requests, urllib
from pprint import pprint
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'ldubost'
__name__ = 'RATPTimeTable'

baseurl = "http://api-ratp.pierre-grimaud.fr/v2/"
linetype = "bus"
line = "72"
station = "Lamballe-Ankara"
destination = "Hotel de Ville"

introText = "next bus is"

logger = getLogger(__name__)

class RATPTimeTableSkill(MycroftSkill):

    def __init__(self):
        super(RATPTimeTableSkill, self).__init__(name="RATPTimeTableSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        ratptimetable_intent = IntentBuilder("RATPTimeTableIntent").\
            require("RATPTimeTableKeyword").build()
        self.register_intent(ratptimetable_intent, self.handle_ratptimetable_intent)

    def handle_ratptimetable_intent(self, message):
        url = baseurl + linetype + "/" + line + "/stations/" + urllib.quote(station) + "/?destination=" + urllib.quote(destination)
        logger.debug("URL: " + url)
        resp = requests.get(url=url)
	data = json.loads(resp.text)
	str = introText

	for dest in data["response"]["schedules"]: 
          str+= " " + dest["message"].replace("mn", "minutes").replace("A l'approche", "coming")
  	  str+= " " + dest["destination"]

        self.speak(str)

    def stop(self):
        pass


def create_skill():
    return RATPTimeTableSkill()
