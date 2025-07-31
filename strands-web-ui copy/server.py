import os
import json
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sys
from pymongo import MongoClient
from datetime import datetime

# Add the parent directory to the path so we can import the strands_agent module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from strands_agent import StrandsAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("strands_web_server")

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)  # Enable CORS for all routes

# Initialize MongoDB client
mongo_client = MongoClient('MongoDBURI')
db = mongo_client['digital_clean_core']
agents_collection = db['ktern_agentic_layer']

# Initialize Strands Agent
strands_agent = StrandsAgent()

@app.route('/')
def index():
    """Serve the main HTML page."""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files."""
    return send_from_directory('.', path)

def save_agent_to_mongodb(agent_data):
    """Save agent details to MongoDB."""
    try:
        # Prepare document for MongoDB
        agent_document = {
            'name': agent_data['name'],
            'description': agent_data['description'],
            'tools': agent_data['tools'],
            'status': 'active',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # Insert into MongoDB
        result = agents_collection.insert_one(agent_document)
        logger.info(f"Agent saved to MongoDB with ID: {result.inserted_id}")
        return str(result.inserted_id)
    except Exception as e:
        logger.error(f"Error saving agent to MongoDB: {str(e)}")
        raise

@app.route('/api/agents', methods=['GET'])
def get_agents():
    """API endpoint to get all agents."""
    try:
        # Retrieve all agents from MongoDB
        agents = list(agents_collection.find({}, {'_id': 0}))
        return jsonify({
            'success': True,
            'agents': agents
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
        custom_tool_code = []
        for tool in custom_tools:
            all_tools.append(tool['name'])
            # Generate code for custom tools
            tool_code = generate_custom_tool_code(tool['name'], tool['description'])
            custom_tool_code.append(tool_code)
        
        # Create the agent
        result = strands_agent.create_strands_agent(agent_name, agent_description, all_tools)
        
        # If custom tools were provided, update the agent file to include them
        if custom_tool_code:
            update_agent_with_custom_tools(agent_name, custom_tool_code)
        
        # Save agent to MongoDB
        agent_data = {
            'name': agent_name,
            'description': agent_description,
            'tools': all_tools
        }
        mongo_id = save_agent_to_mongodb(agent_data)
        
        logger.info(f"Agent created successfully: {agent_name}")
        
        # Return success response
        return jsonify({
            'success': True,
            'message': f"Agent '{agent_name}' created successfully",
            'agent': {
                'name': agent_name,
                'description': agent_description,
                'tools': all_tools,
                'mongo_id': mongo_id
            }
        })
        
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        return jsonify({
            'success': False,
            'message': f"Error creating agent: {str(e)}"
        }), 500

def generate_custom_tool_code(tool_name, tool_description):
    """Generate code for a custom tool using the @tool decorator."""
    # Convert tool name to snake_case for function name
    function_name = tool_name.lower().replace(' ', '_')
    
    # Generate the tool code
    tool_code = f"""
    @tool
    def {function_name}(self, query: str) -> Dict[str, Any]:
        \"\"\"
        {tool_description}
        
        Args:
            query (str): The input query for the tool
            
        Returns:
            Dict[str, Any]: A dictionary containing the result of the operation
        \"\"\"
        try:
            # Implement the tool functionality here
            result = f"Processed query: {{query}}"
            
            return {{
                "success": True,
                "result": result,
                "message": f"Successfully executed {tool_name}"
            }}
        except Exception as e:
            return {{
                "success": False,
                "error": str(e),
                "message": f"Failed to execute {tool_name}: {{str(e)}}"
            }}
    """
    
    return tool_code

def update_agent_with_custom_tools(agent_name, custom_tool_code):
    """Update the generated agent file to include custom tools."""
    # Convert agent name to snake_case for filename
    filename = agent_name.lower().replace(' ', '_') + '.py'
    file_path = os.path.join('agents', filename)
    
    try:
        # Read the existing file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Find the class definition
        class_def_index = content.find('class ')
        if class_def_index == -1:
            logger.error(f"Could not find class definition in {file_path}")
            return
        
        # Find a good place to insert the custom tools (after the class definition)
        # Look for the first method definition after the class
        method_index = content.find('def ', class_def_index)
        if method_index == -1:
            logger.error(f"Could not find method definition in {file_path}")
            return
        
        # Insert the custom tools before the first method
        new_content = content[:method_index] + '\n'.join(custom_tool_code) + '\n\n' + content[method_index:]
        
        # Write the updated content back to the file
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        logger.info(f"Updated {file_path} with custom tools")
        
    except Exception as e:
        logger.error(f"Error updating agent file with custom tools: {str(e)}")

if __name__ == '__main__':
    # Ensure the agents directory exists
    os.makedirs('agents', exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
