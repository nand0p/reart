from flask import Flask, request
import requests
import random
import json
import os


app = Flask(__name__)

refresh = 300

collections = [
                'picasso',
                'japanese',
                'impressionism',
                'seago',
                'russian',
                'alex_ross',
                'postimpressionism',
                'jackson_hole',
                'modern',
                'contemporary',
                'western',
                'renaissance',
                'tate_gallery',
                'google_gallery',
                'kunsthistorisches',
                'european',
                'gauguin',
                'toulouse-lautrec',
                'utopian',
                'renoir',
                'caillebotte',
                'cezanne',
                'friedrich',
                'draper',
                'film_noir',
                'crivelli',
                'pissarro',
                'schongauer',
                'luini',
                'lebourg',
                'vallejo',
                'mucha',
                'rossetti',
                'blake',
                'chinese',
              ]


@app.route('/')
def home():
  html = get_header('collections')
  html += '<table height=65% width=100%><tr><td width=100>.</td><td height=65%>'
  for endpoint in collections:
      html += '<a href=' + endpoint + '><b><font size=8>' + endpoint + '</font></b></a> : : : '
  html += '</td><td height=65% width=100>.</td></tr></table><center>'
  html += get_footer('collections')
  return html


@app.route('/<collection>')
def each_collection(collection):
  url = get_image(collection)
  html = get_header(collection)
  html += '<center><img src=' + url + ' height=95%><br>' + url.split('/')[-1]
  html += get_footer(collection)
  return html


def get_header(collection):
  return '<html><head><meta http-equiv=refresh content=' + str(refresh) + '>' + \
         '<style type="text/css"> body { overflow: hidden; } </style>' + \
         '<script async src="https://www.googletagmanager.com/gtag/js?id=UA-32710227-4"></script>' + \
         '<script>window.dataLayer = window.dataLayer || [];' + \
         'function gtag(){dataLayer.push(arguments);}' + \
         'gtag("js", new Date()); gtag("config", "UA-32710227-4");</script>' + \
         '<title>reart - ' + collection + '</title></head>' + \
         '<body bgcolor=black><font color=white>'


def get_image(collection):
  with open('../reart_' + collection + '_image_urls.json', 'r') as infile:
    images = json.load(infile)
  return random.choice(images)


def get_footer(collection):
  return '<h1>reart - ' + collection + '</h1>' + \
         '<p><br><p><center>' + request.headers.get('User-Agent') + '<br>SEDME<br>' + get_ip() + \
         '<p><b><font size=5>&copy;2000-2020 </font></b>' + \
         '<a target=_blank href=http://hex7.com><b><font size=5>Hex 7 Internet Solutions</font></b></a>' + \
         '</body></html>'


def get_ip():
  if request.headers.getlist("X-Forwarded-For"):
    return request.headers.getlist("X-Forwarded-For")[0]
  else:
    return request.remote_addr


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5006, debug=True)
