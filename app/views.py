from flask import render_template, request
from app import app, lyricsearch
from config import URI_SEARCH, URI_GET


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/google')
def google():
    return render_template('google.html', title='Google Search')


@app.route('/lyrics', methods=['GET', 'POST'])
def lyrics():
    if request.method == "POST":
        terms = request.form.get('search_terms')
        results = lyricsearch.search(URI_SEARCH, terms)
        id, song, artist, lyrics, year, rank, snippet = lyricsearch.format_results(results, terms)
        return render_template('lyrics.html', title='Lyric Search', thumbnail_info=zip(song, artist, snippet, id))
    return render_template('lyrics.html', title='Lyric Search')


@app.route('/lyrics/<id>')
def selected_lyric(id):
    result = lyricsearch.get_lyric_result(id, URI_GET)
    song, artist, lyrics, year, rank = lyricsearch.format_lyric_result(result)
    print(song)
    return render_template('selected_lyric.html', title=song+' '+artist, artist=artist, song=song, rank=rank, year=year, lyrics=lyrics)