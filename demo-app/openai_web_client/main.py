import os
import json
import requests
import datetime
import logging
from flask import Flask, render_template, request, jsonify, make_response, url_for
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__, static_url_path='/static', static_folder='static')

# Configure cache
cache_config = {
    "CACHE_TYPE": "SimpleCache",  # Simple in-memory cache
    "CACHE_DEFAULT_TIMEOUT": 300  # 5 minutes
}
cache = Cache(app, config=cache_config)

# Configure rate limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# Configure Swagger UI
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Hello-GenAI API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

def configure_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    app.logger.setLevel(level)

def resolve_runtime_mode():
    run_mode = os.getenv("RUN_MODE", "local").lower()
    debug = os.getenv("DEBUG", "false").lower() == "true"

    if run_mode not in ("local", "container"):
        raise RuntimeError(f"Invalid RUN_MODE: {run_mode}")

    return run_mode, debug

def maybe_enable_debugger(
    run_mode: str = "local",
    debug: bool | None = None
):
    if run_mode == "container" and debug:
        app.logger.warning("🐛 Container debug mode — waiting for debugger on port 5680")
        import debugpy
        debugpy.listen(("0.0.0.0", 5680))
        debugpy.wait_for_client()

def get_llm_endpoint():
    """Returns the complete LLM API endpoint URL"""
    # Use Docker Model Runner injected variables
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
    return f"{LLM_BASE_URL}/chat/completions"

def get_model_name():
    """Returns the model name to use for API requests"""
    # Use Docker Model Runner injected variables
    return os.getenv("LLM_MODEL_NAME", "")

def validate_environment():
    """Validates required environment variables and provides warnings"""
    # Use Docker Model Runner injected variables
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "")
    
    if not LLM_BASE_URL:
        app.logger.warning("No LLM endpoint configured. Set LLM_BASE_URL.")
    if not LLM_MODEL_NAME:
        app.logger.warning("No LLM model configured. Set LLM_MODEL_NAME.")
    
    return LLM_BASE_URL and LLM_MODEL_NAME

@app.route('/')
def index():
    """Serves the chat web interface"""
    return render_template('index.html')

@app.route('/example')
def example():
    """Serves an example of structured formatting"""
    with open('static/examples/structured_response_example.md', 'r') as file:
        example_text = file.read()
    return jsonify({'response': example_text})

@app.route('/health')
def health_check():
    """Health check endpoint for container orchestration"""
    # Check if LLM API is accessible
    llm_status = "ok"
    try:
        # Simple check if the LLM endpoint is configured
        if not get_llm_endpoint():
            llm_status = "not_configured"
    except Exception as e:
        llm_status = "error"
        app.logger.error(f"Health check error: {e}")
    
    return jsonify({
        "status": "healthy",
        "llm_api": llm_status,
        "timestamp": datetime.datetime.now().isoformat()
    })

def validate_chat_request(data):
    """Validates and sanitizes chat API request data"""
    if not isinstance(data, dict):
        return False, "Invalid request format"
    
    message = data.get('message', '')
    if not message or not isinstance(message, str):
        return False, "Message is required and must be a string"
    
    if len(message) > 4000:  # Reasonable limit
        return False, "Message too long (max 4000 characters)"
    
    return True, message

@app.route('/api/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat_api():
    """Processes chat API requests"""
    data = request.json
    
    # Validate request
    valid, result = validate_chat_request(data)
    if not valid:
        return jsonify({'error': result}), 400
    
    message = result
    
    # Special command for getting model info
    if message == "!modelinfo":
        return jsonify({'model': get_model_name()})
    
    # Call the LLM API
    try:
        response = call_llm_api(message)
        return jsonify({'response': response})
    except Exception as e:
        app.logger.error(f"Error calling LLM API: {e}")
        return jsonify({'error': 'Failed to get response from LLM'}), 500

# @cache.memoize(timeout=300)
def call_llm_api(user_message):
    """Calls the LLM API and returns the response with caching"""
    chat_request = {
        "model": get_model_name(),
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant. Please provide structured responses using markdown formatting. Use headers (# for main points), bullet points (- for lists), bold (**text**) for emphasis, and code blocks (```code```) for code examples. Organize your responses with clear sections and concise explanations."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    
    # Send request to LLM API
    response = requests.post(
        get_llm_endpoint(),
        headers=headers,
        json=chat_request,
        timeout=60
    )
    
    # Check if the status code is not 200 OK
    if response.status_code != 200:
        raise Exception(f"API returned status code {response.status_code}: {response.text}")
    
    # Parse the response
    chat_response = response.json()
    
    # Extract the assistant's message
    if chat_response.get('choices') and len(chat_response['choices']) > 0:
        return chat_response['choices'][0]['message']['content'].strip()
    
    raise Exception("No response choices returned from API")

@app.after_request
def add_security_headers(response):
    """Add security headers to response"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; font-src 'self' https://cdnjs.cloudflare.com"
    return response

@app.after_request
def disable_cache_in_dev(response):
    if os.getenv("RUN_MODE", "local") == "local":
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

if __name__ == '__main__':
    run_mode, debug = resolve_runtime_mode()

    configure_logging(debug)
    maybe_enable_debugger(run_mode, debug)

    port = int(os.getenv("PORT", 8081))

    validate_environment()

    app.logger.info(f"Server starting on 0.0.0.0:{port}")

    app.logger.info(f"LLM endpoint: {get_llm_endpoint()}")
    app.logger.info(f"Model: {get_model_name()}")
    app.logger.info(f"Run mode: {run_mode}")
    app.logger.info(f"Debug: {debug}")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=(run_mode == "local"),
        extra_files=None
    )

