import os
import sys
import subprocess
import webbrowser
import time
import signal
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("strands_web_runner")

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import flask
        import flask_cors
        logger.info("All required dependencies are installed.")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.info("Installing required dependencies...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "../requirements.txt"])
            logger.info("Dependencies installed successfully.")
            return True
        except subprocess.CalledProcessError:
            logger.error("Failed to install dependencies. Please install them manually.")
            return False

def run_server():
    """Run the Flask server."""
    logger.info("Starting Flask server...")
    server_process = subprocess.Popen(
        [sys.executable, "server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    logger.info("Flask server started.")
    return server_process

def open_browser():
    """Open the web application in the default browser."""
    url = "http://localhost:5000"
    logger.info(f"Opening {url} in the default browser...")
    
    # Wait a moment for the server to start
    time.sleep(2)
    
    try:
        webbrowser.open(url)
        logger.info("Browser opened successfully.")
    except Exception as e:
        logger.error(f"Failed to open browser: {e}")
        logger.info(f"Please open {url} manually in your browser.")

def handle_shutdown(server_process):
    """Handle graceful shutdown of the server."""
    logger.info("Shutting down...")
    
    if server_process:
        logger.info("Stopping Flask server...")
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
            logger.info("Flask server stopped.")
        except subprocess.TimeoutExpired:
            logger.warning("Flask server did not terminate gracefully. Forcing shutdown...")
            server_process.kill()
    
    logger.info("Shutdown complete.")

def main():
    """Main entry point for the Strands Web UI runner."""
    print("=" * 60)
    print("Strands Agent Creator - Web UI")
    print("=" * 60)
    
    # Check if we're in the correct directory
    if not os.path.exists("server.py"):
        print("Error: This script must be run from the strands-web-ui directory.")
        print(f"Current directory: {os.getcwd()}")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("Error: Missing dependencies. Please install them and try again.")
        return
    
    # Start the server
    server_process = None
    try:
        server_process = run_server()
        
        # Open the browser
        open_browser()
        
        print("\nStrands Agent Creator is now running!")
        print("Access the web interface at: http://localhost:5000")
        print("\nPress Ctrl+C to stop the server and exit.")
        
        # Keep the script running until interrupted
        while True:
            # Check if the server is still running
            if server_process.poll() is not None:
                stdout, stderr = server_process.communicate()
                print("Server stopped unexpectedly.")
                if stdout:
                    print("Server output:", stdout)
                if stderr:
                    print("Server error:", stderr)
                break
            
            # Sleep to reduce CPU usage
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nReceived interrupt signal. Shutting down...")
    finally:
        handle_shutdown(server_process)
        print("Strands Agent Creator has been stopped.")

if __name__ == "__main__":
    main()
