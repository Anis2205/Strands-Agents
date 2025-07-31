# Strands Agent Creator - Web UI

A web-based interface for creating and managing Strands agents with custom tools and capabilities using AWS Bedrock and advanced AI technologies.

## Quick Start

### Option 1: HTML Version (Simple)
```bash
cd "strands-web-ui copy"
python server.py
```
Open: `http://localhost:5000`

### Option 2: React Version (Recommended)

**Terminal 1 - Backend:**
```bash
cd "strands-web-ui copy"
python server.py
```

**Terminal 2 - Frontend:**
```bash
cd strands-react-ui
npm install
npm start
```
Open: `http://localhost:3000`

## Technologies Used

### Frontend Options
- **Option 1 - HTML/JS**: HTML5, CSS3, JavaScript (ES6+)
- **Option 2 - React**: React 18, Axios, Modern Component Architecture

### Backend
- **Server**: Python Flask with Flask-CORS
- **Database**: MongoDB (Cloud Atlas)
- **AI/ML**: AWS Bedrock (Claude 3.7 Sonnet)
- **Framework**: Strands Agents Framework
- **Tools**: MCP (Model Context Protocol) Server
- **Dependencies**: PyMongo, Boto3, Strands Tools

## Features

- Create new Strands agents with a user-friendly web interface
- Specify agent name, description, and purpose
- Select from standard tools or create custom tools
- Automatically generate agent code with proper structure and documentation
- View success confirmation with agent details
- Store agent configurations in MongoDB
- Real-time agent creation using AWS Bedrock AI models

## Prerequisites

### System Requirements
- Python 3.8 or higher
- pip (Python package manager)
- Node.js (for MCP server dependencies)
- Internet connection for cloud services

### AWS Requirements
- **AWS Account** with active subscription
- **AWS Bedrock Access** with Claude 3.7 Sonnet model enabled
- **AWS CLI** configured with appropriate credentials
- **IAM Permissions** for Bedrock model access

### Cloud Services
- **MongoDB Atlas** account and cluster setup
- Valid MongoDB connection string

### Framework Dependencies
- Strands framework and dependencies
- MCP (Model Context Protocol) server
- Strands-agents-mcp-server

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd strands-web-ui
```

### 2. Set Up AWS Bedrock Access

**Configure AWS CLI:**
```bash
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key
# Enter your default region (e.g., us-east-1)
# Enter output format (json)
```

**Enable Claude 3.7 Sonnet in AWS Bedrock:**
1. Go to AWS Bedrock Console
2. Navigate to "Model access"
3. Request access to "Claude 3.7 Sonnet" model
4. Wait for approval (may take a few minutes to hours)

**Verify Bedrock Access:**
```bash
aws bedrock list-foundation-models --region us-east-1
```

### 3. Set Up MongoDB

1. Create a MongoDB Atlas account at https://www.mongodb.com/atlas
2. Create a new cluster
3. Get your connection string
4. Update the connection string in `server.py`

### 4. Install Dependencies

**Install Python dependencies:**
```bash
pip install -r "strands-web-ui copy/requirements.txt"
```

**Install MCP server:**
```bash
npm install -g uvx
uvx strands-agents-mcp-server
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:
```bash
AWS_REGION=us-east-1
AWS_CONNECT_TIMEOUT=30
AWS_READ_TIMEOUT=240
AWS_MAX_ATTEMPTS=3
BYPASS_TOOL_CONSENT=true
MONGO_CONNECTION_STRING=your_mongodb_connection_string
```

## Usage

### Running the Application

#### Option 1: HTML/JavaScript Version
1. Navigate to the `strands-web-ui copy` directory
2. Run the Flask server:
```bash
python server.py
```
3. Open browser: `http://localhost:5000`

#### Option 2: React Version (Recommended)
1. **Start Backend Server:**
```bash
cd "strands-web-ui copy"
python server.py
```

2. **Start React App:**
```bash
cd strands-react-ui
npm install
npm start
```

3. **Access Application:**
- React UI: `http://localhost:3000`
- Backend API: `http://localhost:5000`

**Benefits of React Version:**
- Modern component architecture
- Better performance and user experience
- Hot reloading for development
- Production-ready builds

### Creating a New Agent

1. Click the "Create New Agent" button
2. Fill in the agent details:
   - Name: A descriptive name for your agent
   - Description: What the agent does and its purpose
3. Select tools:
   - Check the standard tools you want to include
   - Add custom tools with name and description
4. Click "Create Agent" to generate the agent
5. View the success confirmation with agent details

### Custom Tools

When creating custom tools, you need to provide:
- Tool Name: A descriptive name for the tool
- Tool Description: What the tool does and how it works

The system will automatically:
- Generate the tool code using the Strands `@tool` decorator
- Add the tool to the agent's class
- Implement basic functionality that you can customize later

## Project Structure

### HTML/JS Version (`strands-web-ui copy/`)
- `index.html`: Main web interface
- `css/styles.css`: Styling for the web interface
- `js/script.js`: Client-side JavaScript
- `server.py`: Flask server for API requests
- `simple_server.py`: Simplified server for testing

### React Version (`strands-react-ui/`)
- `src/App.js`: Main React application
- `src/components/`: React components
- `src/styles/App.css`: Styling
- `public/index.html`: HTML template
- `package.json`: Dependencies and scripts

## Customizing Generated Agents

Generated agents are saved in the `agents` directory. You can customize them by:

1. Opening the generated Python file
2. Modifying the code as needed
3. Implementing custom tool functionality
4. Running the agent directly:

```bash
python agents/your_agent_name.py
```

## Troubleshooting

### Common Issues

**Server won't start:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if MongoDB connection string is valid
- Verify AWS credentials are configured: `aws sts get-caller-identity`

**AWS Bedrock Access Denied:**
- Ensure Claude 3.7 Sonnet model access is approved in AWS Bedrock Console
- Check IAM permissions for Bedrock service
- Verify AWS region is correct (us-east-1 recommended)

**MCP Server Issues:**
- Install uvx: `npm install -g uvx`
- Install MCP server: `uvx strands-agents-mcp-server`
- Check if Node.js is installed and updated

**MongoDB Connection Issues:**
- Verify MongoDB Atlas cluster is running
- Check connection string format
- Ensure IP address is whitelisted in MongoDB Atlas

**Browser Issues:**
- If browser doesn't open automatically, navigate to `http://localhost:5000`
- Clear browser cache and cookies
- Try a different browser

**Port Already in Use:**
```bash
# Kill process using port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F
```

### Error Logs
Check console output for detailed error messages. Common error patterns:
- `ImportError`: Missing Python dependencies
- `ConnectionError`: AWS or MongoDB connectivity issues
- `PermissionError`: AWS IAM or file system permissions
- `ModuleNotFoundError`: Missing Strands framework components

### Getting Help
- Check AWS Bedrock documentation for model access
- Review MongoDB Atlas connection guides
- Consult Strands framework documentation
- Verify all environment variables are set correctly