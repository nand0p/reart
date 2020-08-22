import boto3
import json
import sys
import re
import os


bucket = 'reart'
client = boto3.client('s3')
prefix = sys.argv[1]
path = '../art/' + prefix
image_urls = []
image_urls_file = bucket + '_' + prefix + '_image_urls.json'

filenames = os.listdir(path)

for filename in filenames:
  newname = filename.replace(' ', '_').lower()
  newname = re.sub('[^a-z0-9._]+', '', newname)
  print('rename: ' + filename + ' -> ' + newname)
  os.rename(os.path.join(path, filename), os.path.join(path, newname))

  object = prefix + '/' + newname
  print('upload: s3://' + bucket + '/' + object)
  response = client.upload_file(os.path.join(path, newname), bucket, object)
  response = client.put_object_acl(
    ACL='public-read',
    Bucket=bucket,
    Key=object,
  )

  image_urls.append('https://' + bucket + '.s3.us-east-1.amazonaws.com/' + object)


print('write image urls file: ' + image_urls_file)

with open(image_urls_file, 'w') as outfile:
    json.dump(image_urls, outfile)

