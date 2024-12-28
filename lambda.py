import requests
import json
import logging
import boto3

# Setting up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initializing AWS clients
s3 = boto3.client('s3')
ssm = boto3.client('ssm')
bucket_name = 'ENTER_S3_bucket_name'
folder_name = 'ENTER_S3_photos_folder_name'

def get_api_key(parameter_name):
    """Retrieve API key from SSM Parameter Store."""
    response = ssm.get_parameter(Name=parameter_name, WithDecryption=True)
    return response['Parameter']['Value']

def create_prompt(user_input):
    """Generate the prompt for DALL-E based on user input."""
    return f"Create a colorful stencil silhouette of one {user_input} on a white background. The cutout areas should be designed in such a way that they stay connected to the surrounding material, ensuring stability when cut. The design should be suitable for printing and cutting out on paper. Additionally, the image should be inverted to enhance contrast."

def shift_images_in_s3():
    """Shift existing images in S3 (delete the oldest, shift others by one)."""
    # Delete the oldest image (12)
    s3.delete_object(Bucket=bucket_name, Key=f"{folder_name}12.png")

    # Shift filenames from 1 to 11
    for i in range(12, 1, -1):
        s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': f"{folder_name}{i-1}.png"}, Key=f"{folder_name}{i}.png")
        s3.delete_object(Bucket=bucket_name, Key=f"{folder_name}{i-1}.png")

def save_image_to_s3(image_data):
    """Save the generated image to S3."""
    image_key = f"{folder_name}1.png"
    s3.put_object(Bucket=bucket_name, Key=image_key, Body=image_data)
    return image_key

def lambda_handler(event, context):
    logger.info(f"Received event: {event}")

    # Get the user input from the event query parameters
    query_params = event.get('queryStringParameters', {})
    user_input = query_params.get('input', 'default_value')

    # Generate the prompt for DALL-E
    prompt = create_prompt(user_input)

    # Retrieve the API key from Parameter Store
    api_key = get_api_key('REPLACE_WITH_YOUR_PARAMETER_NAME')

    # DALL-E API request details
    dall_e_url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    try:
        # Sending the request to DALL-E
        response = requests.post(dall_e_url, headers=headers, data=json.dumps(data))
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")

        if response.status_code == 200:
            # Extract the image URL from the response
            image_url = response.json()['data'][0]['url']

            # Download the image data
            image_data = requests.get(image_url).content

            # Shift images in S3
            shift_images_in_s3()

            # Save the new image as the first one
            image_key = save_image_to_s3(image_data)

            # Return the URL of the newly saved image
            return {
                'statusCode': 200,
                'body': json.dumps({'image_url': f'https://{bucket_name}.s3.amazonaws.com/{image_key}'})
            }
        else:
            return {
                'statusCode': response.status_code,
                'body': json.dumps({'error': response.json().get('error', 'Failed to generate image')})
            }
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'})
        }
