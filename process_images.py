import argparse
import boto3
import json
import sys
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument('--collection')
parser.add_argument('--format', action='store_true')
parser.add_argument('--dry-run', action='store_true')
parser.add_argument('--generate-all-json', action='store_true')
args = parser.parse_args()

bucket = 'reart'
client = boto3.client('s3')
image_urls_dir = 'images/'


def generate_all_json():
  print('generate reart_all.json')
  json_all = []
  json_files = os.listdir(image_urls_dir)
  for json_file in json_files:
    print(json_file)
    with open(image_urls_dir + json_file, 'r') as infile:
      json_all.extend(json.load(infile))
  with open('reart_all.json', 'w') as outfile:
    json.dump(json_all, outfile)


def format_imagefile(filename, image_path):
    newname = filename.replace(' ', '_').lower()
    newname = re.sub('[^a-z0-9_.-]+', '', newname)
    print('rename: ' + filename + ' -> ' + newname)
    if not args.dry_run:
      os.rename(os.path.join(image_path, filename),
                os.path.join(image_path, newname))
    return newname


def upload_imagefile(filename, image_path):
  object = args.collection + '/' + filename
  print('upload: s3://' + bucket + '/' + object)
  if not args.dry_run:
    response = client.upload_file(os.path.join(image_path, filename),
                                  bucket,
                                  object)
    response = client.put_object_acl(
      ACL='public-read',
      Bucket=bucket,
      Key=object,
    )


def write_urls_file(image_urls):
  image_urls_file = bucket + '_' + args.collection + '.json'
  if args.dry_run:
    print('dryrun')
    print(image_urls)
  else:
    print('write image urls file: ' + image_urls_dir + image_urls_file)
    with open(image_urls_dir + image_urls_file, 'w') as outfile:
      json.dump(image_urls, outfile)


def main():
  image_urls = []
  if args.collection:
    image_path = '../art/' + args.collection
    image_files = os.listdir(image_path)

    for filename in image_files:
      if args.format:
        filename = format_imagefile(filename, image_path)
      upload_imagefile(filename, image_path)
      image_urls.extend('https://{}.s3.us-east-1.amazonaws.com/{}/{}'.format(bucket, args.collection, filename))
    write_urls_file(image_urls)

  elif args.generate_all_json:
    generate_all_json()

  else:
    print('no action')


if __name__ == "__main__":
    main()
