import subprocess
import sys
import os
import json
import logging
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import time
app = Flask(__name__)
CORS(app)
import random
from fake_useragent import UserAgent

# Example proxy list (you should replace these with your actual proxies)
PROXIES = [
    '37.1.211.58',
    '178.128.148.69',
    '149.20.253.66'
]

def get_random_proxy():
    return random.choice(PROXIES)

def get_random_user_agent():
    user_agent = UserAgent()
    return user_agent.random

@app.route('/scrape', methods=['POST'])
def scrape():
    logger.info("Scrape route accessed")
    data = request.json
    keywords = data.get('keywords')
    if not keywords:
        logger.error("Keywords parameter is missing")
        return jsonify({"error": "Keywords parameter is missing"}), 400

    scraper_script_path = os.path.abspath('./amazon-scraper/searchresults.py')
    scraper_dir = os.path.dirname(scraper_script_path)
    urls_file_path = os.path.join(scraper_dir, 'search_results_urls.txt')
    search_url = f"https://www.amazon.com/s?k={keywords}"

    # Select random proxy and user-agent
    proxy = get_random_proxy()
    user_agent = get_random_user_agent()
    headers = {'User-Agent': user_agent}

    # Configure proxies for requests
    proxy_dict = {
        "http": proxy,
        "https": proxy
    }

    # Add random delay
    time.sleep(random.uniform(1, 5))

    try:
        response = requests.get(search_url, headers=headers, proxies=proxy_dict)
        response.raise_for_status()  # To handle HTTP errors
        
        # Save the response to a file for the scraper to process
        with open(urls_file_path, 'w') as file:
            file.write(response.text)
        
        # Assume that your scraping script can now read the saved HTML for processing
        # Execute the scraping script as a subprocess if necessary
        return jsonify({"success": "Data fetched and processed successfully."})
    except requests.RequestException as e:
        logger.error("Error during web scraping: %s", str(e))
        return jsonify({"error": "Failed to scrape the website", "details": str(e)}), 500

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
headers = {"Authorization": "Bearer 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"}

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()  # Ensure we catch HTTP errors
    return response.json()

@app.route('/')
def home():
    logger.info("Home route accessed")
    return 'Hello, World'

# @app.route('/scrape', methods=['POST'])
# def scrape():
#     print("Scrape route accessed")
#     data = request.json
#     logger.info("Scrape route accessed with data: %s", data)
#     keywords = data.get('keywords')
#     if not keywords:
#         logger.error("Keywords parameter is missing")
#         return jsonify({"error": "Keywords parameter is missing"}), 400
#     print(f"Keywords: {keywords}")
#     # Define the path to the scraper script and set the directory
#     scraper_script_path = os.path.abspath('./amazon-scraper/searchresults.py')
#     scraper_dir = os.path.dirname(scraper_script_path)
#     urls_file_path = os.path.join(scraper_dir, 'search_results_urls.txt')
#     search_url = f"https://www.amazon.com/s?k={keywords}"

#     try:
#         # Ensure the file is empty before adding the new URL
#         with open(urls_file_path, 'w') as file:
#             file.write(f"{search_url}\n")

#         # Run the scraper script
#         subprocess_result = subprocess.run(
#             [sys.executable, scraper_script_path],
#             cwd=scraper_dir,  # Set the current working directory to the script's directory
#             capture_output=True,
#             text=True
#         )
#         if subprocess_result.returncode != 0:
#             logger.error("Error running subprocess: %s", subprocess_result.stderr)
#             return jsonify({"error": "Error running the scraper script", "details": subprocess_result.stderr}), 500

#         # Assuming the output is written to a JSONL file
#         output_file_path = os.path.join(scraper_dir, 'search_results_output.jsonl')
#         if not os.path.exists(output_file_path):
#             logger.error("Output file not found")
#             return jsonify({"error": "Output file not found"}), 404

#         results = []
#         with open(output_file_path, 'r') as file:
#             for line in file:
#                 results.append(json.loads(line))
#         logger.info("Scrape successful with results: %s", results)
#         print("scraper successful")
#         return jsonify(results)
#     except FileNotFoundError as e:
#         logger.error("File not found: %s", e)
#         return jsonify({"error": "File not found. Ensure the script generates the file correctly."}), 404
#     except json.JSONDecodeError as e:
#         logger.error("JSON decode error: %s", e)
#         return jsonify({"error": "Error decoding JSON from the output file."}), 500
#     except Exception as e:
#         logger.error("Unexpected error: %s", e, exc_info=True)
#         return jsonify({"error": "An unexpected error occurred", "exception": str(e)}), 500

@app.route('/getimage', methods=['POST'])
def get_image():
    data = request.json
    logger.info("GetImage route accessed with data: %s", data)
    product_url = data.get('product_url')
    product_url = f"http://www.amazon.com{product_url}"
    print(f"Product URL: {product_url}")
    if not product_url:
        logger.error("Product URL parameter is missing")
        return jsonify({"error": "Product URL parameter is missing"}), 400

    scraper_script_path = os.path.abspath('./amazon-scraper/amazon.py')
    scraper_dir = os.path.dirname(scraper_script_path)
    urls_file_path = os.path.join(scraper_dir, 'urls.txt')

    try:
        # Clear the urls.txt file and add the new URL
        with open(urls_file_path, 'w') as file:
            file.write(f"{product_url}\n")

        # Run the scraper script
        subprocess_result = subprocess.run(
            [sys.executable, scraper_script_path],
            cwd=scraper_dir,
            capture_output=True,
            text=True
        )
        if subprocess_result.returncode != 0:
            logger.error("Error running subprocess: %s", subprocess_result.stderr)
            return jsonify({"error": "Error running the scraper script", "details": subprocess_result.stderr}), 500

        # Read the output file to get the product details
        output_file_path = os.path.join(scraper_dir, 'output.jsonl')
        if not os.path.exists(output_file_path):
            logger.error("Output file not found")
            return jsonify({"error": "Output file not found"}), 404

        with open(output_file_path, 'r') as file:
            product_data = json.loads(file.readline())  # Assuming the output is stored in the first line
            print(product_data)
        # Parse images and select the first one
        if 'images' in product_data:
            images = json.loads(product_data['images'])
            first_image_url = list(images.keys())[0]
        else:
            logger.error("No images found in the product data")
            return jsonify({"error": "No images found in the product data"}), 500

        # Respond with all the product details including the first image URL
        return jsonify({
            "name": product_data.get("name", "N/A"),
            "price": product_data.get("price", "N/A"),
            "short_description": product_data.get("short_description", "N/A"),
            "image_url": first_image_url,
            "variants": product_data.get("variants", []),
            "product_description": product_data.get("product_description", "N/A"),
            "link_to_all_reviews": product_data.get("link_to_all_reviews", "N/A")
        })
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        return jsonify({"error": "An unexpected error occurred", "exception": str(e)}), 500

@app.route('/query', methods=['POST'])
def query_model():
    data = request.json
    logger.info("Query route accessed with data: %s", data)
    inputs = data.get('inputs')
    if not inputs:
        logger.error("Inputs parameter is missing")
        return jsonify({"error": "Inputs parameter is missing"}), 400

    prompt = """
Return the fundamental product type based on the above product name. """
    inputs = "Q." + inputs + prompt
    try:
        output = query_huggingface({"inputs": inputs})
        logger.info("Model query successful with output: %s", output)
        return jsonify(output)
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP error: %s", e)
        return jsonify({"error": "HTTP error occurred", "details": str(e)}), e.response.status_code
    except Exception as e:
        logger.error("Unexpected error: %s", e, exc_info=True)
        return jsonify({"error": "An unexpected error occurred", "exception": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

