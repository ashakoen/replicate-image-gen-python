# Flask Image Generator

Flask Image Generator is a Python application that leverages the Replicate API to generate images based on text prompts. This tool is particularly useful for developers and AI enthusiasts who want to quickly prototype image generation features without needing to build models from scratch.

## Features

- Generates images from text prompts using pre-configured models.
- Wide customization with environment variables for model parameters.
- Secure API access with header-based authentication (`x-api-key`).
- Designed for deployment on Google Cloud Run with Docker support.
- Environment variable management via `.env` files for easy configuration.

## Installation

### Clone the Repository
First, clone the repository to your local machine:

git clone https://github.com/[YOUR_USERNAME]/[YOUR_REPO_NAME].git
cd [YOUR_REPO_NAME]

### Python Environment
Ensure you have Python 3.10 or later installed on your system.

### Install Dependencies
Either install with pip (assuming a virtual environment is set up):

pip install -r requirements.txt
 
Or if using Docker, you don't need to manually install dependencies; the Dockerfile will handle it.

## Usage

### Running the Docker Container

Build the Docker image:

docker build -t flask-image-generator .

Run the Docker container with the `.env` file:

docker run -p 8080:8080 --env-file .env flask-image-generator

### Interacting with the API

After starting the container, you can interact with the API. The service provides an endpoint to generate images based on the user-provided text prompt.

#### Endpoint: `/generate-images`

- **Method:** POST
- **Headers:**
  - `Content-Type: application/json`
  - `x-api-key: <your_header_api_key_here>`
- **Body:** JSON object containing the field:
  - `prompt`: A string representing the text input for generating images.

Example usage with `curl`:

curl -X POST http://localhost:8080/generate-images \
-H "x-api-key: your_header_api_key_here" \
-H "Content-Type: application/json" \
-d '{"prompt": "A realistic, natural photo of a woman gently applying moisturizer in front of a bathroom mirror. The soft light highlights her serene expression as she takes a moment for self-care. Attention to detail in her facial expression and the soothing setting. Shot with a Fuji X-T1 in the style of Sarah Lucas."}'

### Docker Compose

You can use Docker Compose as well for managing the container:

docker-compose up --build

## Configuration

The application uses a `.env` file to configure the parameters used by the Replicate API. See below for the complete list of configurable environment variables:

- REPLICATE_API_KEY: Your API key for Replicate.
- MODEL: The model to use (e.g., "dev").
- NUM_OUTPUTS: The number of output images (default: 1).
- GUIDANCE_SCALE: The guidance scale for the generation process.
- NUM_INFERENCE_STEPS: The number of inference steps.
- OUTPUT_FORMAT: The format for the output image (e.g., "png").
- OUTPUT_QUALITY: The quality of the output image (e.g., 100).
- DISABLE_SAFETY_CHECKER: Disables the safety checker (boolean: true/false).
- LORA_SCALE: Scale for LoRA fine-tuning (default: 1).
- ASPECT_RATIO: Aspect ratio of output image (e.g., "9:16").
- LORA: The LoRA model to apply during image generation.
- X_API_KEY: The key required for accessing the API.

### Google Cloud Run Integration

This repository can be easily integrated with Google Cloud Run for continuous deployment:

1. **Link Your GitHub Repository:** Use the Google Cloud Console to set up a continuous integration pipeline with your GitHub repository.

2. **Environment Variables:** Ensure the required environment variables are set either in the Google Cloud Run console or by using Google Cloud's Secret Manager for secure storage.

3. **GitHub Deployment:**
   - Push your changes to GitHub.
   - Google Cloud Run will automatically build and deploy your service.

## The Story Behind Flask Image Generator

The Flask Image Generator was developed to simplify the process of generating high-quality images based on detailed text prompts. With the rise of AI models capable of creating images from textual descriptions, this project aimed to provide a simple, yet powerful, platform for testing and integrating such features into various applications.

By using the Replicate API, the project reduces the complexity of model management and leverages pre-trained models for quick deployment and testing. It’s designed to be easily customizable and ready to be integrated into cloud environments, making it ideal for prototyping and production use alike.

## File Structure

- app.py: The main Flask application for processing image generation requests.
- requirements.txt: Python dependencies.
- Dockerfile: Instructions for building the Docker image.
- docker-compose.yml: Simplifies local container management.
- .env: Environment variable configurations (not included in repository).
- .dockerignore: Excludes unnecessary files from the Docker context.
- README.md: This file, providing information about the project.

## Dependencies

This project uses several Python libraries detailed in the `requirements.txt` file:

- Flask: Micro web framework for routing and handling API requests.
- Flask-CORS: Handles cross-origin requests.
- Loguru: Logging library for structured logs.
- Replicate: Python client for integrating with the Replicate API.
- python-dotenv: Loads environment variables from a `.env` file.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request with any improvements or bug fixes.

## Contact

For any questions or suggestions, open a Github issue.
