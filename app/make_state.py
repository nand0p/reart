import boto3
import json
import sys

bucket = 'reart'
prefix = sys.argv[1]
image_urls = []
image_urls_file = bucket + '_' + prefix + '_urls.json'

client = boto3.client('s3')

response = client.list_objects_v2(
  Bucket = bucket,
  Prefix = prefix
)

for item in response['Contents']:
    image_urls.append('https://' + bucket + '.s3.us-east-1.amazonaws.com/' + item['Key'])


print('write image urls file: ' + image_urls_file)

with open(image_urls_file, 'w') as outfile:
    json.dump(image_urls, outfile)
