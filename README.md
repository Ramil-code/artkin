# Artkin: The Art of Pumpkin Carving / AWS - Serverless /

## Introduction
Artkin is a fun and educational web service for generating colorful pumpkin carving templates. Users can input a description of what they want to carve on a pumpkin, and the service generates a detailed silhouette template. Artkin aims to make Halloween preparation easier and more creative for everyone.

![artkin](https://github.com/user-attachments/assets/ad2883a9-7d13-4c19-be5f-cfffcd0651dd)

---

## Features
- **Input Description**: Users can type in words or phrases describing the desired carving design.
- **Image Generation**: Uses DALL-E 3 to create colorful, printable silhouette templates suitable for pumpkin carving.
- **Template Management**: Automatically manages up to 12 images in S3, ensuring only the most recent images are available.
- **Static Web Page**: Displays generated templates as a gallery with 100x100 pixel previews.
- **View Previous Creations**: Users can see templates created by others or earlier by themselves in the gallery.

![artkin-2](https://github.com/user-attachments/assets/5ee125dc-c231-4feb-a06c-6ba80653ceb0)


---

## Installation
Follow these steps to set up the project:

1. **Set Up AWS Resources**:
   - Create an S3 bucket and folder for image storage
   - Enable Static Website Hosting on the S3 bucket. The index.html example attached to project docs.
   - Set up an AWS Lambda function [(code attached)](https://github.com/Ramil-code/artkin/blob/main/lambda.py) that is triggered by an API Gateway GET request
   - Parameter Store: Store your OpenAI API key in AWS Systems Manager Parameter Store
   - Attach poilcies for S3, Parameter Store, Lambda. Configure API Gateway Permissions.

2. **How to Obtain and Add OpenAI API Key**
   - Go to OpenAI and create an account if you don't have one yet.
   - Navigate to the API Keys section. Click Create new secret key and copy the generated key (it will only be shown once)

---

## Architecture

### Core Components:
1. **Static Website**:
   - Hosted on Amazon S3.
   - Includes a simple HTML form for user input.
   - Displays a gallery of generated images.

2. **AWS Lambda Function**:
   - Handles user requests to generate images via the DALL-E 3 API.
   - Stores generated images in an S3 bucket.
   - Maintains the naming convention and image rotation logic (1 to 12).

3. **API Gateway**:
   - Provides an endpoint for the HTML form to invoke the Lambda function.

4. **Amazon S3**:
   - Stores generated images.
   - Publicly accessible for the static website and gallery.

5. **OpenAI DALL-E 3**:
   - Generates colorful carving templates based on user input.

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

