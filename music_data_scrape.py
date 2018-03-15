import urllib.request
import re
import time
import csv
import io

#returns list of all alphabetical web links from url
def alphabet_spyder(url):
    web_page = urllib.request.urlopen(url)
    contents = web_page.read().decode(errors="replace")
    web_page.close()
    alphabet = re.findall('(?<=<a class="btn btn-menu" href="//).+?(?=">)',contents,re.DOTALL)
    formatted_links = ["https://"+str(letter) for letter in alphabet]
    return formatted_links

#returns list of artist links for a specified letter from alphabet_spyder
def artist_crawl(url):
    web_page = urllib.request.urlopen(url)
    contents = web_page.read().decode(errors="replace")
    web_page.close()
    artist_content = re.findall('(?<=<div class="col-sm-6 text-center artist-col">).+?(?=<!-- container main-page -->)',contents,re.DOTALL)[0]
    artists = re.findall('(?<=<a href=").+?(?=".)',artist_content,re.DOTALL)
    artist_links = ["https://www.azlyrics.com/"+str(artist) for artist in artists]
    return artist_links

#returns list of artist names and ads to table with
def artist_name_crawl(url):
    web_page = urllib.request.urlopen(url)
    contents = web_page.read().decode(errors="replace")
    web_page.close()
    artist_contents = re.findall('(?<=<!-- main -->).+(?=</div>)',contents,re.DOTALL)[0]
    artists = re.findall('(?<=html">).+?(?=</a>)',artist_contents,re.DOTALL)
    return artists

#return list of song names and ads to table with id
def song_name_crawl(contents):
    song_names = re.findall('(?<=target="_blank">).+?(?=</a>)',contents,re.DOTALL)
    return(song_names)
    
#uppercase split module
def split_uppercase(value):
    return re.sub(r'([A-Z])', r' \1', value)

#returns list of song links for a specified artist from artist_crawl
def song_crawl(contents):
    links = re.findall('(?<=href=").+?(?=")',contents,re.DOTALL)
    stripped_links = [link.replace("#","").replace("..","www.azlyrics.com").replace("www","https://www").replace("\n","") for link in links]
    return(stripped_links)

#returns list of lyrics for a specified song from song_crawl
def read_lyrics(url):
    web_page = urllib.request.urlopen(url)
    contents = web_page.read().decode(errors="replace")
    web_page.close()
    lyrics = re.findall('(?<=<!-- Usage of azlyrics.com content by any third-party lyrics provider is prohibited by our licensing agreement. Sorry about that. -->).+?(?=</div>)',contents,re.DOTALL)[0]
    stripped_lyrics = lyrics.replace("<br>"," ").replace(':',"").replace("</i>","").replace("<i>","").replace('[Chorus]',"").replace(',',"").replace('.',"").replace('\r\n',"").replace("\n","").replace('!',"").replace('?',"")
    stripped_lyrics =  re.sub("[\(\[].*?[\)\]]", "", stripped_lyrics)
##    stripped_lyrics = split_uppercase(stripped_lyrics)
    lyric_list = stripped_lyrics.split(" ")
    return lyric_list

#returns list of album years
def album_year_crawl(contents):
    album_year = re.findall('(?<=</b> ).+?(?=</div>)',contents,re.DOTALL)
    return album_year


#returns list of albums and mixtapes for a specified artist from artist_crawl
def album_crawl(contents):
    album_names = re.findall('(?<=album: <b>").+?(?="</b>)',contents,re.DOTALL)
    mixtape_names = re.findall('(?<=<mixtape: <b>").+?(?="</b>)',contents,re.DOTALL)
    compilation_names = re.findall('(?<=compilation: <b>").+?(?="</b>)',contents,re.DOTALL)
    ep_names = re.findall('(?<=EP: <b>").+?(?="</b>)',contents,re.DOTALL)
    soundtrack_names = re.findall('(?<=soundtrack: <b>").+?(?="</b>)',contents,re.DOTALL)
    other_songs = re.findall('(?<=songs: <b>").+?(?="</b>)',contents,re.DOTALL)
    discography = album_names + mixtape_names + compilation_names + ep_names + other_songs
    return discography

#album_crawl 2.0
#returns dictionary with album as key and list of lyrics as value
def album_id_crawl(url):
    web_page = urllib.request.urlopen(url)
    contents = web_page.read().decode(errors="replace")
    web_page.close()
#section off content into sets of albums/mixtapes/others
    contents = re.findall('(?<=<!-- start of song list -->).+?(?=<script type="text/javascript">)',contents,re.DOTALL)[0]
#loop through list of album contents and create dictionary with album as key and list of songs as value
    album_contents = re.findall('(?<=<div class="album">).+?(?=<div class)',contents,re.DOTALL)
##    mixtape_contents = re.findall('(?<=<div class="album">).+?(?=<div class)',contents,re.DOTALL)
    other_songs = re.findall('(?<=<div class="album">other).+',contents,re.DOTALL)
    discography = album_contents + other_songs
    return discography

#Main
##print(read_lyrics("https://www.azlyrics.com/lyrics/a1/bethefirsttobelieve.html"))
##print(lyric_crawl("https://www.azlyrics.com/w/west.html"))
##for link in lyric_crawl("https://www.azlyrics.com/w/west.html"):
##    if link:
##        time.sleep(5)
##        print(read_lyrics(link))
##print(album_crawl("https://www.azlyrics.com/e/earlsweatshirt.html"))
##for item in album_id_crawl("https://www.azlyrics.com/a/aaliyah.html"):
##    time.sleep(1)
##    print(item)
##print(artist_crawl("https://www.azlyrics.com/a.html"))
##print(alphabet_spyder("https://www.azlyrics.com/"))




##
####creating table of all artists:
##csv_file = open('artists.csv','w')
##writer = csv.writer(csv_file, dialect='excel',delimiter = ",")
##with csv_file:
##    artist_id = 0
##    for letter in alphabet_spyder("https://www.azlyrics.com/"):
##        time.sleep(.5)
##        for artist in artist_name_crawl(letter):
##            time.sleep(.002)
##            artist_id += 1
##            try:
##                writer.writerow([artist_id,artist.lower()])
##                print(artist_id,artist.lower())
##            except:
##                writer.writerow([artist_id,"unknown"])
##                print(artist_id,"unknown")   


#creating table of all albums:
csv_file = open('albums.csv','w')
writer = csv.writer(csv_file, dialect='excel',delimiter = ",")
with csv_file:
    for letter in alphabet_spyder("https://www.azlyrics.com/"):
        artist_id = 0
        for artist in artist_crawl(letter):
            artist_id += 1
            time.sleep(1)
            album_id = 0
            for album in album_id_crawl(artist):
                time.sleep(1)
                album_id += 1
                album_name = album_crawl(album)
                album_year = album_year_crawl(album)
                if album_year:
                    if album_name:
                        writer.writerow([artist_id,album_id,album_name[0].lower(),album_year[0]])
                        print(artist_id,album_id,album_name,album_year[0])
                else:
                    if album_name:
                        writer.writerow([artist_id,album_id,album_name[0].lower()])
                        print(artist_id,album_id,album_name)
                    else:
                        writer.writerow([artist_id,album_id,"other songs"])
                        print(artist_id,album_id,"other songs")
                    

##creating table of all songs:
##csv_file = open('songs.csv','w')
##writer = csv.writer(csv_file, dialect='excel',delimiter = ",")
##with csv_file:
##    for letter in alphabet_spyder("https://www.azlyrics.com/"):
##        artist_id = 0
##        time.sleep(2)
##        for artist in artist_crawl(letter):
##            artist_id += 1
##            time.sleep(2)
##            album_id = 0
##            for album in album_id_crawl(artist):
##                album_id += 1
##                song_id = 0
##                for song in song_name_crawl(album):
##                    time.sleep(.7)
##                    song_id += 1
##                    writer.writerow([artist_id,album_id,song_id,song])
##                    print(artist_id,album_id,song_id,song)
    
#creating table of all lyrics
##csv_file = open('lyrics.csv','w')
##writer = csv.writer(csv_file, dialect='excel',delimiter = ",")
##with csv_file:
##    for letter in alphabet_spyder("https://www.azlyrics.com/"):
##        artist_id = 0
##        time.sleep(2)
##        for artist in artist_crawl(letter):
##            artist_id += 1
##            time.sleep(3)
##            album_id = 0
##            print(artist)
##            for album in album_id_crawl(artist):
##                album_id +=1
##                time.sleep(5)
##                song_id = 0 
##                for song in song_crawl(album):
##                    song_id +=1
##                    if song:
##                        lyrics = read_lyrics(song)
##                        count = 0
##                        for lyric in lyrics:
##                            if lyric:
##                                time.sleep(.5)
##                                count += 1
##                                writer.writerow([artist_id,album_id,song_id,count,lyric.lower()])
##                                print(artist_id,album_id,song_id,count,lyric)
####
#####creating a table of all 
####
####
####
####
##
##











