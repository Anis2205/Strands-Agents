import os
import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("simple_web_server")

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory('.', path)

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """API endpoint to get all agents."""
    try:
        # Return mock data for testing
        mock_agents = [
            {
                'name': 'Sample Agent',
                'description': 'A sample agent for demonstration',
                'tools': ['http_request', 'file_read'],
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
        ]
        return jsonify({
            'success': True,
            'agents': mock_agents
        })
    except Exception as e:
        logger.error(f"Error retrieving agents: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error retrieving agents: {str(e)}"
        }), 500

@app.route('/api/create-agent', methods=['POST'])
def create_agent():
    """API endpoint to create a Strands agent."""
    try:
        # Get data from request
        data = request.json
        logger.info(f"Received request to create agent: {data['name']}")
        
        # Extract agent details
        agent_name = data['name']
        agent_description = data['description']
        standard_tools = data.get('standardTools', [])
        custom_tools = data.get('customTools', [])
        
        # Combine all tools
        all_tools = standard_tools.copy()
        
        # Process custom tools
        for tool in custom_tools:
            all_tools.append(tool['name'])
        
        # Create mock agent code
        agent_code = f'''"""
{agent_name} - Generated Strands Agent

Description: {agent_description}
Tools: {", ".join(all_tools)}
Generated: {datetime.now().isoformat()}
"""

import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("{agent_name.lower().replace(" ", "_")}")

class {agent_name.replace(" ", "")}Agent:
    def __init__(self):
        """Initialize the {agent_name} agent."""
        self.name = "{agent_name}"
        self.description = "{agent_description}"
        self.tools = {all_tools}
        logger.info(f"{{self.name}} agent initialized")
    
    def run(self, query: str) -> Dict[str, Any]:
        """Run the agent with a query."""
        logger.info(f"Processing query: {{query}}")
        
        # Mock implementation
        result = f"{{self.name}} processed: {{query}}"
        
        return {{
            "success": True,
            "result": result,
            "agent": self.name,
            "tools_used": self.tools
        }}

def main():
    """Main entry point."""
    agent = {agent_name.replace(" ", "")}Agent()
    
    while True:
        try:
            query = input("Enter your query (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            
            result = agent.run(query)
            print(f"Result: {{result}}")
            
        except KeyboardInterrupt:
            print("\\nExiting...")
            break

if __name__ == "__main__":
    main()
'''
        
        # Ensure the agents directory exists
        os.makedirs('agents', exist_ok=True)
        
        # Create a valid filename from the agent name
        filename = agent_name.lower().replace(" ", "_") + ".py"
        file_path = os.path.join("agents", filename)
        
        # Write the code to the file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(agent_code)
        
        logger.info(f"Agent created successfully: {agent_name}")
        
        # Return success response
        return jsonify({
            'success': True,
            'message': f"Agent '{agent_name}' created successfully",
            'agent': {
                'name': agent_name,
                'description': agent_description,
                'tools': all_tools,
                'file_path': file_path
            }
        })
        
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error creating agent: {str(e)}"
        }), 500

if __name__ == '__main__':
    # Ensure the agents directory exists
    os.makedirs('agents', exist_ok=True)
    
    print("=" * 60)
    print("Simple Strands Agent Creator - Web UI")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)