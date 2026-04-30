require 'aws-sdk-s3'
require 'json'
require 'jwt'

def handler(event:, context:)
  s3 = Aws::S3::Resource.new
  bucket_name = ENV["UPLOADS_BUCKET_NAME"]
  
  # Define CORS headers once
  cors_headers = {
    'Access-Control-Allow-Headers' => '*, Authorization',
    'Access-Control-Allow-Origin' => 'http://127.0.0.1:3000',
    'Access-Control-Allow-Methods' => 'OPTIONS,GET,POST'
  }

  if event["routeKey"] == "OPTIONS /{proxy+}"
    return { headers: cors_headers, statusCode: 200 }
  end

  # 1. Safe Header Extraction
  auth_header = event.dig("headers", "authorization") || event.dig("headers", "Authorization")
  return { statusCode: 401, body: "Missing Authorization" } unless auth_header

  token = auth_header.split(" ").last
  decoded_token = JWT.decode(token, nil, false)
  image_name = decoded_token[0]["username"]
  
  # 2. Robust JSON Parsing
  event_body = event["body"]
  json_obj = event_body.is_a?(String) ? JSON.parse(event_body) : event_body
  json_obj = JSON.parse(json_obj) if json_obj.is_a?(String) # Handle double-encoding

  extension = json_obj["extension"]
  return { statusCode: 400, body: "Missing extension" } unless extension

  # 3. Presigned URL Generation
  object_key = "#{image_name}.#{extension}"
  obj = s3.bucket(bucket_name).object(object_key)
  url = obj.presigned_url(:put, expires_in: 3600)

  {
    headers: cors_headers,
    statusCode: 200,
    body: { url: url }.to_json
  }
end