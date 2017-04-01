import requests
import urllib.request
import json
import elastic_init


def search(uri, term):
    query = json.dumps({
        "query": {
            "multi_match":{
                "fields": ["Song", "Artist", "Lyrics"],
                "query": term,
                "type": "cross_fields"
            }},
        "size":20
    })
    response = requests.post(uri, query)
    results = response.json()
    return results


def format_results(results, terms):
    data = [doc for doc in results['hits']['hits']]
    song = []
    id = []
    artist = []
    lyrics = []
    year = []
    rank = []
    snippet = []

    for doc in data:
        song.append(doc['_source']['Song'])
        id.append(doc['_id'])
        artist.append(doc['_source']['Artist'])
        lyrics.append(doc['_source']['Lyrics'])
        snippet.append(get_snippet(doc['_source']['Lyrics'], terms))
        year.append(doc['_source']['Year'])
        rank.append(doc['_source']['Rank'])

    return id, song, artist, lyrics, year, rank, snippet


def get_snippet(lyrics, terms):
    snippet = ""
    term_list = terms.split(' ')
    for term in term_list:
        if term in lyrics:
            before_term, term, after_term = lyrics.partition(term)
            if len(before_term) < 90:
                snippet = snippet + before_term
            else:
                before_term = before_term[len(before_term)-90:]
                while before_term[0] != ' ':
                    before_term = before_term[1:]
                before_term = before_term[1:]
                snippet = snippet + before_term
            snippet = snippet + ' ' + term + ' '
            if len(after_term) < 90:
                snippet = snippet + after_term
            else:
                count = 90
                while after_term[count] != ' ':
                    count += 1
                after_term = after_term[0:count]
                snippet = snippet + after_term
            break
    if not snippet:
        count = 180
        while lyrics[count] != ' ':
            count += 1
        snippet = lyrics[0:count]

    return snippet


def format_snippet(before, after):
    snippet = ""
    for word in before:
        snippet = snippet + word + " "
    for word in after:
        snippet = snippet + word + " "
    return snippet


def get_lyric_result(id, uri):
    print(uri+'lyrics/'+id)
    response = requests.get(uri+'lyrics/'+id)
    results = response.json()
    return results


def format_lyric_result(result):
    data1 = result['_source']
    song = data1['Song']
    artist = data1['Artist']
    lyrics = data1['Lyrics']
    year = data1['Year']
    rank = data1['Rank']
    return song, artist, lyrics, year, rank

