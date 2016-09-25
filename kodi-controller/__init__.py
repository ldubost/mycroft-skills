
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from netifaces import interfaces, ifaddresses, AF_INET
import os.path
import httplib2
import json
import socket

__author__ = 'k3yb0ardn1nja'

headers = {"Content-type": "application/json"}
configFile = 'mycroft/configuration/kodi-config.json'

searchBy = {
    'name': 'title',
    'category': 'genre',
    'recent': 'dateadded'
}

LOGGER = getLogger(__name__)
    
def make_request(conn, method, json_params):
	config = auto_discover()
	if config == -1:
	    return -1
	try:
	    LOGGER.debug("KODI REQUEST START")
            if config.has_key('USER'):
 	        conn.add_credentials(config['USER'], config['PASSWORD'])

	    url = 'http://' + config['HOST'] + ':' + str(config['PORT']) + '/jsonrpc?' + method
	    LOGGER.debug("URL: " + url)
	    res, c = conn.request(url, 'POST', json.dumps(json_params), headers)

	    if hasattr(res, 'status'):
		status = res['status']
	    else:
		return -1

	    if status == '200':
		if 'c' in locals():
		    result = json_loads_byteified(c)
		    if result.has_key('error'):
			# TODO: better handle errors returned from kodi
			return -1
		    elif 'result' in locals():
			return result
	    return -1
	    # TODO: better handle errors caught from request attempt
	except socket.error, err:
	    return -1
	except httplib2.ServerNotFoundError:
	    return -1

def get_player_id(conn):
	method = 'Player.GetActivePlayers'
	json_params = {
	   'jsonrpc':'2.0',
	   'method':method,
	   'id':1
	}
	result = make_request(conn, method, json_params)

	if result == -1:
	    return -1
	elif result['result'] != [] and result['result'][0].has_key('playerid'):
	    return result['result'][0]['playerid']
	else:
	    return 0

def auto_discover():
	# TODO: use async requests
	conn = httplib2.Http(timeout=.1)
	method = 'XBMC.GetInfoLabels'
	json_params = {
	    'jsonrpc':'2.0',
	    'method':method,
	    'id':1,
	    'params': [['Network.IPAddress','System.FriendlyName']]
	}

	if os.path.isfile(configFile):
            LOGGER.debug("KodiControler read config file " + configFile)
	    with open(configFile) as data_file:
		config = json_load_byteified(data_file)

	if ('config' in locals() and
	    config.has_key('HOST') and
	    config.has_key('PORT')):
            print(config)
	    try:
                if config.has_key('USER'):
                    print("Kodi adding credentials: " + config['USER'])
 	            conn.add_credentials(config['USER'], config['PASSWORD'])

                url = 'http://' + config['HOST'] + ':' + str(config['PORT']) + '/jsonrpc?' + method
                print("Trying Kodi url: " + url)
		res, c = conn.request(url, 'POST', json.dumps(json_params), headers)
		if ('res' in locals() and
		    res.has_key('status') and
		    res['status'] == '200'):
		    print('Using config in ' + configFile)
		    return config
		else:
		    print('Status is ' + res['status'])
		    print("Reconfiguring")
	    except:
		print("Reconfiguring with exception")

	for ifaceName in interfaces():
	    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
	    if ifaceName != "lo":
		for xxx in range(1, 255):
		    try:
			ipPrefix = addresses[0][:addresses[0].rfind('.') + 1]

			res, c = conn.request('http://' + ipPrefix + str(xxx) + ':8080/jsonrpc?' + method, 'POST', json.dumps(json_params), headers)

			if hasattr(res, 'status'):
			    status = res['status']
			else:
			    print("Response received, but no status.")
			    return -1

			if status == '200':
			    if 'c' in locals():
				result = json_loads_byteified(c)
				if result.has_key('error'):
				    print("Error received from Kodi")
				    return -1
				elif 'result' in locals():
				    print("Kodi found at 10.10.1." + str(xxx))
				    if 'config' in globals():
					config['NAME'] = result['result']['System.FriendlyName']
					config['HOST'] = result['result']['Network.IPAddress']
					config['PORT'] = 8080
				    else:
					f = open(configFile, 'w+')
					config = {
					    'NAME': result['result']['System.FriendlyName'],
					    'HOST': result['result']['Network.IPAddress'],
					    'PORT': 8080
					}
					f.writelines([
					    '{',
					    '\n\t"NAME":"' + result['result']['System.FriendlyName'] + '",',
					    '\n\t"HOST":"' + result['result']['Network.IPAddress'] + '",',
					    '\n\t"PORT":' + '8080',
					    '\n}'
					])
			    return config
			print("Response received, but there was an issue. Status: " + status)
			return -1
		    except socket.error, err:
			pass
		    except:
			pass
	return -1

def json_load_byteified(file_handle):
	return _byteify(
	    json.load(file_handle, object_hook=_byteify),
	    ignore_dicts=True
	)

def json_loads_byteified(json_text):
	return _byteify(
	    json.loads(json_text, object_hook=_byteify),
	    ignore_dicts=True
	)

def _byteify(data, ignore_dicts = False):
	# if this is a unicode string, return its string representation
	if isinstance(data, unicode):
	    return data.encode('utf-8')
	# if this is a list of values, return list of byteified values
	if isinstance(data, list):
	    return [ _byteify(item, ignore_dicts=True) for item in data ]
	# if this is a dictionary, return dictionary of byteified keys and values
	# but only if we haven't already byteified it
	if isinstance(data, dict) and not ignore_dicts:
	    return {
		_byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
		for key, value in data.iteritems()
	    }
	# if it's anything else, return it in its original form
	return data

def PlayPause(conn):
	playerid = get_player_id(conn)

	if playerid > 0:
	    method = 'Player.PlayPause'
	    json_params = {
		'jsonrpc':'2.0',
		'method':method,
		'id':1,
		'params': {
		    'playerid':playerid
		}
	    }
	    res = make_request(conn, method, json_params)

	elif playerid == 0:
	    print 'There is no player'

	else:
	    print 'An error occurred'

def Stop(conn):
	playerid = get_player_id(conn)

	if playerid > 0:
	    method = 'Player.Stop'
	    json_params = {
		'jsonrpc':'2.0',
		'method':method,
		'id':1,
		'params': {
		    'playerid':playerid
		}
	    }
	    res = make_request(conn, method, json_params)

	elif playerid == 0:
	    print 'There is no player'

	else:
	    print 'An error occurred'

def GetPlayerItem(conn):
	playerid = get_player_id(conn)

	if playerid > 0:
	    method = 'Player.GetItem'
	    json_params = {
		'jsonrpc':'2.0',
		'method':method,
		'id':1,
		'params': {
		    'playerid':playerid
		}
	    }
    	    res = make_request(conn, method, json_params)
	    if (res.has_key('result') and
	       res['result'].has_key('item') and
	       res['result']['item'].has_key('label')):
		print(res['result']['item']['label'])
	    else:
		print 'An error occurred'

	elif playerid == 0:
	    print 'There is no player'

	else:
	    print 'An error occurred'

def GetMoviesBySearch(conn, getBy, searchTerm, start=0):
	if searchBy.has_key(getBy.lower()):
	    method = 'VideoLibrary.GetMovies'
	    json_params = {
		'jsonrpc':'2.0',
		'method':method,
		'id':15,
		'params': {
		    'properties': [],
		    'limits': {
			'start': start,
			'end': start + 3
		    },
		    'sort': {
			'order': 'ascending',
			'method': 'title',
			'ignorearticle': True
		    },
		    'filter': {
			'field': searchBy[getBy.lower()],
			'operator': 'contains',
			'value': searchTerm
		    }
		}
	    }
	else:
	    return {
		'error': 'Unable to search by ' + getBy + '.'
	    }
	res = make_request(conn, method, json_params)
	if (res.has_key('result') and
	    res['result'].has_key('movies') and
	    len(res['result']['movies']) > 0):
	    movies = res['result']['movies']
	    for i in range(0,len(movies)):
		return movies
	else:
	    print 'An error occurred'



class KodiSkill(MycroftSkill):
    def __init__(self):
        super(KodiSkill, self).__init__(name="KodiSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        playpause_intent = IntentBuilder("PlayPause").require("PlayPauseKeyword").build()
        self.register_intent(playpause_intent, self.handle_playpause_intent)

        stop_intent = IntentBuilder("Stop").require("StopKeyword").build()
        self.register_intent(stop_intent, self.handle_stop_intent)

        pick_movie_intent = IntentBuilder("PickMovie").require("PickMovieKeyword").build()
        self.register_intent(pick_movie_intent, self.handle_pick_movie_intent)

    def handle_playpause_intent(self, message):
        conn = httplib2.Http()

        playerid = get_player_id(conn)
        if playerid > 0:
            method = "Player.PlayPause"
            json_params = {
                "jsonrpc":"2.0",
                "method":method,
                "id":1,
                "params": {
                    "playerid":playerid
                }
            }
            res = make_request(conn, method, json_params)

        elif playerid == 0:
            self.speak("There is no open video")

        else:
            self.speak("An error occurred")

        pass

    def handle_stop_intent(self, message):
        #self.speak("Play Videos.")
        conn = httplib2.Http()

        playerid = get_player_id(conn)
        if playerid > 0:
            method = "Player.Stop"
            json_params = {
                "jsonrpc":"2.0",
                "method":method,
                "id":1,
                "params": {
                    "playerid":playerid
                }
            }
            res = make_request(conn, method, json_params)

        elif playerid == 0:
            self.speak("There is no open video")

        else:
            self.speak("An error occurred")

        pass

    def handle_pick_movie_intent(self, message):
        #self.speak("Play Videos.")
        conn = httplib2.Http()

        searchTerm = 'ring'

        res = GetMoviesBySearch(conn, 'name', searchTerm)
        if (type(res) is dict and
            res.has_key('error')):
            print(res['error'])
        else:
            speech = 'I found ' + str(len(res)) + ' movies matching your search for ' + searchTerm + '... '
            for i in range(0,3):
                speech += res[i]['label'] + ' , , '
            speech += 'Were you looking for one of these?'
            self.speak(speech)

def create_skill():
    return KodiSkill()


