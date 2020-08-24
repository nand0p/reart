import argparse
import boto3
import json
import sys
import re
import os

parser = argparse.ArgumentParser()
parser.add_argument('--collection', required=True)
parser.add_argument('--format', action='store_true')
parser.add_argument('--dry-run', action='store_true')
args = parser.parse_args()

bucket = 'reart'
client = boto3.client('s3')
path = '../art/' + args.collection
image_urls = []
image_urls_file = bucket + '_' + args.collection + '_image_urls.json'
filenames = os.listdir(path)


for filename in filenames:
  if args.format:
    newname = filename.replace(' ', '_').lower()
    newname = re.sub('[^a-z0-9_.-]+', '', newname)
    print('rename: ' + filename + ' -> ' + newname)
    if not args.dry_run:
      os.rename(os.path.join(path, filename), os.path.join(path, newname))
    filename = newname

  object = args.collection + '/' + filename
  print('upload: s3://' + bucket + '/' + object)
  if not args.dry_run:
    response = client.upload_file(os.path.join(path, filename), bucket, object)
    response = client.put_object_acl(
      ACL='public-read',
      Bucket=bucket,
      Key=object,
    )
  image_urls.append('https://' + bucket + '.s3.us-east-1.amazonaws.com/' + object)

if args.dry_run:
  print('dryrun')
  print(image_urls)

else:
  print('write image urls file: ' + image_urls_file)
  with open(image_urls_file, 'w') as outfile:
    json.dump(image_urls, outfile)
