#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import spotipy
sp = spotipy.Spotify()


QUERY_MAX_LIMIT = 50 #this is actaully the max limit


def memoize(f):
    memo = {}
    def helper(x):
    	r = ' '.join(x).lower()
        if r not in memo:            
            memo[r] = f(x)
        return memo[r]
    return helper


def find_song_with_name(phrase):
	"""
	This looksup if a song exists with the following phrase. Now
	what should count as a match? An intersesting question, but 
	this implementation uses case insensitive direc match, this means 
	that if the keywoard "hey," will count as one word and match exactly
	it also greedily evaluates to the first match.
	"""
	if len(phrase) == 0:
		return None 
	query_results = sp.search(q=phrase, limit=QUERY_MAX_LIMIT, type='track')
	for result in query_results['tracks']['items']:
		if result['name'].lower().strip() == phrase.lower().strip(): 
			return result
	return None

@memoize
def make_playlist_min(keywords):
	"""
	make_playlist_min(input_string keywords) -> list of songs
	This function returns a list of songs whose names concatenate to the 
	keywords argument. If a song contaning a word in the input string does not 
	exist, the function will ignore that word and continues to create the 
	playlist creating a break at the unfound word using None. The function 
	creates the shortest playlist that exists and reduces some of the overhead 
	using memoization
	""" 
	if len(keywords) == 0:
		return []
	if len(keywords) == 1:
		song = find_song_with_name(keywords[0]) 
		if song == None: 
			return []
		else: 
			return [song]
	rolling_word = ""
	song = None
	min_playlist = []
	for (i, word) in enumerate(keywords):
		rolling_word += " " + word
		song = find_song_with_name(rolling_word)
		if song != None:
			# Check the shortest arangement for rest of playlist
			current_list = [song] + make_playlist_min(keywords[i + 1:])
			if not min_playlist or len(current_list) <= len(min_playlist):
				min_playlist = current_list
	if not min_playlist:
		#this means there is not match from this word or any phrase containing 
		#this word first, gives none to alert failure 
		return [None] + make_playlist_min(keywords[1:])
	else:
		return min_playlist



while True:
	keywords = raw_input("ENTER A POEM: ")
	keywords = str(keywords).split(' ')
	print "loading..."
	for i, x in enumerate(filter(None,make_playlist_min(keywords))):
		print str(i + 1) + '(' , x['name'], '(' + x['uri'] + ')'