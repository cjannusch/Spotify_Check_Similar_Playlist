import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from SpotifyApiKeys import CLIENT_ID,CLIENT_SECRET
import sys

sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

def createSpotifyAPIConnection():
    auth_manager = SpotifyClientCredentials(CLIENT_ID,CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    return sp

def lookAtUsersPublicPlayLists(sp,SpotifyUserToSearchFor = "claytonjannusch",TOPRINT = True):
    dictOfAlbums = {}
    count = 0
    
    playlists = sp.user_playlists(SpotifyUserToSearchFor)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            #print("Playlist = " + str(playlist['name']) + "\n")
            #newFile.write("Playlist = " + str(playlist['name']) + "\n")
            dictOfAlbums[str(playlist['name'])] = []
            
            result = sp.user_playlist_tracks(SpotifyUserToSearchFor,playlist['id'])

            if result['items'] == None:
                break

            for song in result['items']:
                if song == None:
                    continue
                    #print("total songs" + str(count) + "\n")
                    #newFile.write("total songs" + str(count) + "\n")
                    #newFile.close()
                count +=1
                #print('\t' + str(song['track']['name']) + "\n")
                #newFile.write('\t' + str(song['track']['name']) + "\n")
                stringToAppend = ""
                try:
                    stringToAppend = stringToAppend + str(song['track']['name'])
                except:
                    continue

                #in case there are multiple listed artists for the track
                for artist in song['track']['artists']:
                    stringToAppend = stringToAppend + ' - ' + artist['name']
                dictOfAlbums[str(playlist['name'])].append(stringToAppend)
    
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            print("total songs",count)
            playlists = None
    if not TOPRINT:
        return dictOfAlbums
    for album in dictOfAlbums:
        print(album + "\n")
        print(dictOfAlbums[album])
        print("____________________________________")
    #print(dictOfAlbums)
    return dictOfAlbums

def compareUsersMatching(sp,user1 = "claytonjannusch", user2 = "abbeybeem"):
    print("1")
    playlists1 = lookAtUsersPublicPlayLists(sp,user1,False)
    print("2")
    playlists2 = lookAtUsersPublicPlayLists(sp,user2,False)
    print("3")

    songs1 = set(map(tuple, list(playlists1.values())))
    songs2 = set(map(tuple, list(playlists2.values())))
    #print(type(songs1),songs1)

    matches = songs1.union(songs2)
    numberOfMatches = len(matches)

    if len(songs1) > len(songs2):
        percent = numberOfMatches / len(songs2)
    else:
        percent = numberOfMatches / len(songs1)

    print("You have", numberOfMatches, "matches and a", str(percent) + "%", "a match")

    print(list(matches)[0])

def Main():

    sp = createSpotifyAPIConnection()
    compareUsersMatching(sp)
    #lookAtUsersPublicPlayLists(sp,"gkldawson1234")



Main()