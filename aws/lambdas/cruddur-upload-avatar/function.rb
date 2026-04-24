require 'aws-sdk-s3'
require 'json'


def handler(event:, context:)
  puts event
  s3 = Aws::S3::Resource.new
  bucket_name = ENV["UPLOADS_BUCKET_NAME"]
  object_key = 'jean.jpg'

  obj = s3.bucket(bucket_name).object(object_key)
  url = obj.presigned_url(:put, expires_in: 3600)
  body = {url: url}.to_json
  {
    headers: {
      'Access-Control-Allow-Headers': '*, Authorization',
      'Access-Control-Allow-Origin': 'http://127.0.0.1:3000',
      'Access-Control-Allow-Methods': 'OPTIONS,GET,POST'
    }, 
    statusCode: 200,
    body: body
  }
end

puts handler(event:{}, context:{})