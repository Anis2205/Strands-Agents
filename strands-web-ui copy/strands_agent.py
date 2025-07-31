import os
import logging
import boto3
import botocore.config
from strands import Agent
from strands_tools import http_request, file_write, file_read
from typing import Dict, Any
import datetime
from mcp import stdio_client, StdioServerParameters
from strands.tools.mcp import MCPClient
 
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("strands_agent")
 
 
logging.getLogger("strands").setLevel(logging.DEBUG)
 
 
os.environ['AWS_CONNECT_TIMEOUT'] = '30'  
os.environ['AWS_READ_TIMEOUT'] = '240'    
os.environ['AWS_MAX_ATTEMPTS'] = '3'  
os.environ['BYPASS_TOOL_CONSENT'] = 'true'  
 
class StrandsAgent:
    def __init__(self):
        """Initialize the Strands Agent with necessary tools and configuration."""
        # Initialize MCP client for Strands Agents
        self.mcp_client = MCPClient(lambda: stdio_client(
            StdioServerParameters(
                command="uvx",
                args=["strands-agents-mcp-server"]
            )
        ))
       
        # Start the MCP client session
        self.mcp_client.start()
       
        # Get MCP tools
        try:
            mcp_tools = self.mcp_client.list_tools_sync()
            logger.info(f"MCP tools loaded: {len(mcp_tools)} tools available")
        except Exception as e:
            logger.error(f"Failed to load MCP tools: {str(e)}")
            mcp_tools = []
       
        self.agent = Agent(
            # Use Claude 3.7 Sonnet model from Bedrock with increased timeout
            model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
            # Add tools for the agent
            tools=[file_write] + mcp_tools,
            # Configure the system prompt
            system_prompt="""
              You are an expert AI developer specializing in creating powerful, intelligent agents using the Strands Agents framework. You have access to the Strands MCP server, which provides comprehensive documentation and tools for building sophisticated AI agents.
 
                Your Approach to Agent Creation
                For any agent I request, follow this systematic approach:
 
                Consult Strands Documentation: Begin by accessing the relevant documentation from the Strands MCP server:
 
                Use quickstart to review core concepts and patterns
                Use model_providers to identify the optimal model for the agent's purpose
                Use agent_tools to explore available tools and extension patterns
                Design the Agent Architecture: Create a comprehensive agent design that includes:
 
                A clear definition of the agent's purpose and capabilities
                The optimal model selection based on the agent's requirements
                A thoughtfully crafted system prompt that guides the agent's behavior
                A strategic selection of tools that enhance the agent's capabilities
                Implement with Best Practices: Generate clean, efficient, production-ready code that:
 
                Follows Strands framework conventions and patterns
                Includes proper error handling and resource management
                Leverages the full power of the Strands ecosystem
                Is well-documented and maintainable
                Enhance with Advanced Features: Incorporate advanced capabilities as appropriate:
 
                Streaming responses for real-time interaction
                Custom tools for domain-specific functionality
                Tool combinations that create emergent capabilities
                Memory mechanisms for context retention
                Logging and observability features
                Implementation Guidelines
                When implementing any agent:
 
                Always leverage the Strands MCP server for documentation and guidance
                Always use the most appropriate tools from the Strands ecosystem
                Always implement proper error handling and resource management
                Always provide clear documentation for your implementation choices
                Example Agent Types
                Be prepared to create various types of agents, such as:
 
                Research Agents: That can search, retrieve, and synthesize information
                Creative Agents: That can generate content, stories, or creative works
                Analytical Agents: That can process data and extract insights
                Assistant Agents: That can help with specific tasks or domains
                Multi-Agent Systems: That coordinate multiple specialized agents
                For each agent type, leverage the specific tools and patterns most appropriate for their purpose, always consulting the Strands MCP server for guidance.
 
                Your Response Format
                When I request an agent, provide:
 
                A brief overview of the agent's purpose and capabilities
                The complete, production-ready implementation code
                A concise explanation of your implementation choices
                Instructions for running and using the agent
                Suggestions for potential enhancements or extensions
                Remember: Your goal is to create the most powerful, effective agent possible for each request, always leveraging the full capabilities of the Strands framework and MCP server.
 
                Once you have completed the agent, save the code to a file in the 'agents' directory with the name.py using file_write tool.
        """)
        logger.info("Strands Agent initialized successfully")
   
    def create_strands_agent(self, agent_name: str, agent_purpose: str, required_tools: list = None) -> str:
        """
        Create a Strands agent based on the provided specifications.
       
        Args:
            agent_name (str): The name of the agent
            agent_purpose (str): The purpose and functionality of the agent, including custom tool specifications
            required_tools (list, optional): List of tools the agent should use
           
        Returns:
            str: Path to the generated agent code file
        """
        try:
            # Construct the prompt for the agent
            tools_description = ", ".join(required_tools) if required_tools else "standard tools"
           
            prompt = f"""
            I need you to create a new Strands agent with the following specifications:
           
            Agent Name: {agent_name}
            Agent Purpose: {agent_purpose}
            Required Tools: {tools_description}
           
            Please follow these steps:
            1. Generate complete Python code for a Strands agent that fulfills the purpose
            2. Include all necessary imports, class structure, and tool definitions
            3. If the agent purpose includes Custom Tools Specifications, implement each custom tool using the @tool decorator following Strands best practices
            4. For each custom tool:
               - Use the provided tool name and description
               - Design appropriate parameters based on the tool's purpose
               - Implement the functionality in an robust manner that aligns with the tool's description
               - Include proper error handling and documentation
               - Build an tool as per the user requirements
            5. If the agent purpose includes MCP Servers, implement the MCP server connection and MCP tool usage following Strands best practices and strands documentation
            6. Add proper error handling and logging for the entire agent
            7. Create a main function for easy execution
            8. Return the complete code in a code block
            9. Save the generated code to a file in the 'agents' directory with the name '{agent_name.lower().replace(" ", "_")}.py using file_write tool'
           
            The code should be well-structured, documented, and follow Strands best practices.
            """
           
            logger.info(f"Creating Strands agent: {agent_name}")
           
            # Run the agent with the prompt
            response = self.agent(prompt)
           
            logger.info("Strands agent created successfully")
           
            # # Extract code from the response
            # code_content = response
            # if "```python" in response:
            #     code_blocks = response.split("```python")
            #     if len(code_blocks) > 1:
            #         code_content = code_blocks[1].split("```")[0].strip()
            # elif "```" in response:
            #     code_blocks = response.split("```")
            #     if len(code_blocks) > 1:
            #         code_content = code_blocks[1].strip()
           
            # # Create a valid filename from the agent name
            # filename = agent_name.lower().replace(" ", "_") + ".py"
            # file_path = os.path.join("agents", filename)
           
            # # Ensure the agents directory exists
            # os.makedirs("agents", exist_ok=True)
           
            # # Write the code to the file
            # with open(file_path, "w", encoding="utf-8") as f:
            #     f.write(code_content)
           
            # logger.info(f"Agent code saved to {file_path}")
            return f"Agent '{agent_name}' created successfully and saved"
 
        except Exception as e:
            logger.error(f"Error creating Strands agent: {str(e)}")
            return f"Error creating Strands agent: {str(e)}"
   
    def run_cli(self):
        """Run the Strands Agent in CLI mode."""
        print("=" * 60)
        print("Welcome to Strands Agent Generator!")
        print("This tool helps you create custom Strands agents.")
        print("=" * 60)
       
        try:
            # Get agent name from user
            agent_name = input("Enter a name for your agent: ")
           
            # Get agent purpose from user
            agent_purpose = input("Describe the purpose and functionality of your agent: ")
           
            # Get required tools from user
            tools_input = input("List any specific tools your agent should use (comma-separated, or press Enter for standard tools): ")
            required_tools = [tool.strip() for tool in tools_input.split(",")] if tools_input.strip() else None
           
            print("\nGenerating your Strands agent. This may take a moment...\n")
           
            # Create the Strands agent
            result = self.create_strands_agent(agent_name, agent_purpose, required_tools)
           
            print("\n" + "=" * 60)
            print("Strands Agent Created!")
            print("=" * 60)
            print(result)
           
        except KeyboardInterrupt:
            print("\nExiting Strands Agent Generator. Goodbye!")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        finally:
            # Ensure MCP client is properly closed
            if hasattr(self, 'mcp_client'):
                try:
                    self.mcp_client.stop()
                    logger.info("MCP client session closed")
                except Exception as e:
                    logger.error(f"Error closing MCP client: {str(e)}")
 
def main():
    """Main entry point for the Strands Agent."""
    agent = StrandsAgent()
    agent.run_cli()
 
if __name__ == "__main__":
    main()