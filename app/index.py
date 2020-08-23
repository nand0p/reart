from flask import Flask, request
import requests
import random
import json
import os


app = Flask(__name__)

collections = [
                'picasso',
                'japanese',
                'impressionism',
                'postimpressionism',
                'modern',
                'contemporary',
                'western',
                'renaissance',
                'tate_gallery',
                'google_gallery',
              ]


@app.route('/')
def home():
  html = get_header('all')
  for endpoint in collections:
    html += '<a href=' + endpoint + '><h1>' + endpoint + '</h1></a><p>'
  return html


@app.route('/<collection>')
def each_collection(collection):
  url = get_image(collection)
  html = get_header(collection)
  html += '<img src=' + url + ' height=95%><br>' + url.split('/')[-1]
  html += get_footer(collection)
  return html


def get_header(collection):
  return '<html><head><meta http-equiv=refresh content=60>' + \
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
  app.run(host='0.0.0.0', port=5000, debug=True)
