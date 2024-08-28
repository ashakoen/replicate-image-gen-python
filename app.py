import json
import os
import sys
from loguru import logger
import replicate
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Loguru
logger.remove()
logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
logger.add("replicate.log", rotation="10 MB", format="{time} {level} {message}", level="INFO")

app = Flask(__name__)
CORS(app)

# Load defaults from environment variables
DEFAULT_MODEL = os.getenv("MODEL", "dev")
DEFAULT_NUM_OUTPUTS = int(os.getenv("NUM_OUTPUTS", 1))
DEFAULT_GUIDANCE_SCALE = float(os.getenv("GUIDANCE_SCALE", 3.5))
DEFAULT_NUM_INFERENCE_STEPS = int(os.getenv("NUM_INFERENCE_STEPS", 28))
DEFAULT_OUTPUT_FORMAT = os.getenv("OUTPUT_FORMAT", "png")
DEFAULT_OUTPUT_QUALITY = int(os.getenv("OUTPUT_QUALITY", 100))
DEFAULT_DISABLE_SAFETY_CHECKER = os.getenv("DISABLE_SAFETY_CHECKER", "false").lower() == "true"
DEFAULT_LORA_SCALE = float(os.getenv("LORA_SCALE", 1))
DEFAULT_ASPECT_RATIO = os.getenv("ASPECT_RATIO", "9:16")
DEFAULT_LORA = os.getenv("LORA", "ashakoen/akv-1-flux2:c13e23ce8ac6f56a7f7c5a91cf1a6bb351d1ad5c99a916966f0218c914acd1f0")

REPLICATE_API_KEY = os.getenv("REPLICATE_API_KEY")
HEADER_API_KEY = os.getenv("X_API_KEY")


class ImageGenerator:
    def __init__(self, api_key):
        self.api_key = api_key  # Store the API key in the instance
        logger.info(f"ImageGenerator initialized with default model: {DEFAULT_MODEL}")

    def generate_images(self, prompt):
        try:
            logger.debug(f"Received prompt: {prompt}")
            logger.debug(f"Setting replicate API key: {self.api_key[:5]}...")

            # Set the replicate API key in the environment
            os.environ["REPLICATE_API_TOKEN"] = self.api_key

            # Build parameters dictionary with defaults from .env
            replicate_params = {
                "prompt": prompt,
                "model": DEFAULT_MODEL,
                "num_outputs": DEFAULT_NUM_OUTPUTS,
                "guidance_scale": DEFAULT_GUIDANCE_SCALE,
                "num_inference_steps": DEFAULT_NUM_INFERENCE_STEPS,
                "output_format": DEFAULT_OUTPUT_FORMAT,
                "output_quality": DEFAULT_OUTPUT_QUALITY,
                "disable_safety_checker": DEFAULT_DISABLE_SAFETY_CHECKER,
                "aspect_ratio": DEFAULT_ASPECT_RATIO,
                "lora_scale": DEFAULT_LORA_SCALE,
            }

            # Log the API call
            logger.info(f"Using model: {DEFAULT_LORA}")
            logger.info(f"API call parameters: {json.dumps(replicate_params, indent=2)}")

            # Make the API call
            output = replicate.run(DEFAULT_LORA, input=replicate_params)

            # Log the API response
            logger.info(f"API Response: {json.dumps(output, indent=2)}")

            logger.success(f"Images generated successfully.")
            return output

        except Exception as e:
            error_message = f"Error generating images: {str(e)}"
            logger.exception(error_message)
            raise ImageGenerationError(error_message)
        finally:
            # Clear the replicate API key from the environment
            if "REPLICATE_API_TOKEN" in os.environ:
                del os.environ["REPLICATE_API_TOKEN"]
                logger.debug("Replicate API key cleared from environment")


class ImageGenerationError(Exception):
    pass


def validate_api_key(request):
    """Validate the request based on the x-api-key."""
    incoming_api_key = request.headers.get('x-api-key')
    if not incoming_api_key or incoming_api_key != HEADER_API_KEY:
        return False
    return True


@app.route('/generate-images', methods=['POST'])
def generate_images_route():
    # Authenticate the request based on `x-api-key`
    if not validate_api_key(request):
        logger.warning("Unauthorized access attempt.")
        return jsonify({'error': 'Unauthorized access'}), 401

    try:
        data = request.json  # Expecting JSON body with the "prompt"
        prompt = data.get('prompt')

        if not prompt:
            raise ValueError("Prompt is required")

        logger.info(f"Received generation request with prompt: {prompt}")

        # Create a new ImageGenerator instance with the API key
        image_generator = ImageGenerator(REPLICATE_API_KEY)
        
        output = image_generator.generate_images(prompt)
        return jsonify({'imageUrls': output})

    except Exception as e:
        error_message = f"Error during image generation: {str(e)}"
        logger.error(error_message)
        return jsonify({'error': error_message}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # Port 8080 is more commonly available in cloud environments
