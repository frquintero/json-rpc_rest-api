"""
AI Agent Example: Demonstrating JSON-RPC usage in AI agent contexts
This example shows how an AI agent might use JSON-RPC to interact with tools and services.
"""
import json
from clients.jsonrpc_client import JSONRPCClient


class SimpleAIAgent:
    """A simple AI agent that uses JSON-RPC to interact with tools."""

    def __init__(self):
        self.client = JSONRPCClient()
        self.available_tools = {}
        self.conversation_history = []

    def discover_tools(self):
        """Discover available tools from the JSON-RPC server."""
        print("🤖 Agent: Discovering available tools...")
        try:
            server_info = self.client.get_server_info()
            self.available_tools = {
                method: f"Tool: {method}"
                for method in server_info.get('supported_methods', [])
            }
            print(f"✅ Discovered {len(self.available_tools)} tools:")
            for tool in self.available_tools.keys():
                print(f"   - {tool}")
            return True
        except Exception as e:
            print(f"❌ Failed to discover tools: {e}")
            return False

    def analyze_request(self, user_request):
        """Analyze user request and determine which tools to use."""
        print(f"\\n🤖 Agent: Analyzing request: '{user_request}'")

        # Simple keyword-based tool selection (in real AI, this would use LLM)
        if "tax" in user_request.lower() or "income" in user_request.lower():
            return ["calculate_tax"]
        elif "user" in user_request.lower() or "create" in user_request.lower():
            return ["create_user", "list_users"]
        elif "calculate" in user_request.lower() or "math" in user_request.lower():
            return ["add", "subtract", "multiply", "divide"]
        elif "batch" in user_request.lower():
            return ["batch_calculate"]
        else:
            return ["ping", "get_server_info"]

    def execute_tool_call(self, tool_name, params=None):
        """Execute a tool call using JSON-RPC."""
        print(f"🔧 Agent: Calling tool '{tool_name}' with params: {params}")

        try:
            if params:
                result = self.client.call_method(tool_name, params)
            else:
                result = self.client.call_method(tool_name)

            print(f"✅ Tool result: {json.dumps(result, indent=2)}")
            return result

        except Exception as e:
            print(f"❌ Tool call failed: {e}")
            return None

    def perform_batch_operations(self, operations):
        """Perform multiple operations in a batch."""
        print(f"🔧 Agent: Executing batch operations: {operations}")

        try:
            results = self.client.batch_calculate(operations)
            print(f"✅ Batch results: {json.dumps(results, indent=2)}")
            return results
        except Exception as e:
            print(f"❌ Batch operation failed: {e}")
            return None

    def process_user_request(self, user_request):
        """Process a user request using available tools."""
        print(f"\\n👤 User: {user_request}")

        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": user_request})

        # Analyze and select tools
        tools_to_use = self.analyze_request(user_request)

        results = []
        for tool in tools_to_use:
            if tool == "batch_calculate":
                # Special handling for batch operations
                batch_ops = [
                    {"operation": "add", "a": 10, "b": 20},
                    {"operation": "multiply", "a": 5, "b": 6},
                    {"operation": "divide", "a": 100, "b": 4}
                ]
                result = self.perform_batch_operations(batch_ops)
            elif tool == "calculate_tax":
                result = self.execute_tool_call(tool, {
                    "income": 75000,
                    "deductions": 10000,
                    "tax_rate": 0.22
                })
            elif tool == "create_user":
                result = self.execute_tool_call(tool, {
                    "name": "AI Assistant",
                    "email": "assistant@ai.com",
                    "age": 1
                })
            elif tool == "add":
                result = self.execute_tool_call(tool, {"a": 42, "b": 58})
            else:
                result = self.execute_tool_call(tool)

            if result is not None:
                results.append(result)

        # Generate response (in real AI, this would use LLM)
        response = self.generate_response(user_request, results)
        print(f"🤖 Agent: {response}")

        self.conversation_history.append({"role": "assistant", "content": response})
        return response

    def generate_response(self, user_request, tool_results):
        """Generate a response based on tool results."""
        if not tool_results:
            return "I wasn't able to complete your request. Let me try a different approach."

        # Simple response generation based on results
        if "tax" in user_request.lower():
            tax_result = tool_results[0]
            return f"Based on your income of ${tax_result['income']:,} with deductions of ${tax_result['deductions']:,}, your tax would be ${tax_result['tax_amount']:,.2f} (effective rate: {tax_result['tax_rate']:.1%})."

        elif "calculate" in user_request.lower() and len(tool_results) > 1:
            return f"I performed {len(tool_results)} calculations for you. The results show various mathematical operations completed successfully."

        elif "user" in user_request.lower():
            return f"I successfully created a user account. The user ID is {tool_results[0]['id']}."

        else:
            return f"I completed {len(tool_results)} operations for you. All tools executed successfully!"


def demonstrate_ai_agent():
    """Demonstrate AI agent using JSON-RPC tools."""
    print("🧠 AI Agent JSON-RPC Demonstration")
    print("=" * 50)

    agent = SimpleAIAgent()

    # Step 1: Tool discovery
    if not agent.discover_tools():
        print("❌ Cannot proceed without tools")
        return

    # Step 2: Process various user requests
    requests = [
        "Can you calculate my taxes for $75,000 income with $10,000 deductions?",
        "Create a user account for me",
        "Perform some mathematical calculations",
        "Show me how batch operations work"
    ]

    for request in requests:
        agent.process_user_request(request)
        print("-" * 50)

    print("\\n🎯 Key AI Agent Benefits of JSON-RPC:")
    print("• Tool Discovery: Agents can dynamically learn available functions")
    print("• Structured Calling: Consistent parameter passing and error handling")
    print("• Batch Operations: Multiple tool calls in single request")
    print("• State Management: Can maintain context across tool calls")
    print("• Error Recovery: Standardized error responses help agents adapt")


def demonstrate_mcp_style_interaction():
    """Demonstrate Model Context Protocol style interaction."""
    print("\\n🔗 Model Context Protocol (MCP) Style Interaction")
    print("=" * 55)

    client = JSONRPCClient()

    print("1. Initialize connection and discover capabilities")
    try:
        server_info = client.get_server_info()
        print(f"   Server: {server_info.get('server_type', 'Unknown')}")
        print(f"   Version: {server_info.get('version', 'Unknown')}")
        print(f"   Available tools: {len(server_info.get('supported_methods', []))}")

        print("\\n2. Tool execution workflow")
        # Simulate an AI model's tool calling workflow
        tools_called = [
            ("ping", None, "Health check"),
            ("calculate_tax", {"income": 60000, "deductions": 8000}, "Tax calculation"),
            ("create_user", {"name": "MCP Client", "email": "mcp@client.com"}, "User creation"),
            ("add", {"a": 123, "b": 456}, "Mathematical operation")
        ]

        for method, params, description in tools_called:
            print(f"   Calling: {method} - {description}")
            result = client.call_method(method, params)
            print(f"   Result: {result}")

        print("\\n3. Batch tool execution")
        batch_operations = [
            {"operation": "add", "a": 10, "b": 15},
            {"operation": "multiply", "a": 8, "b": 7},
            {"operation": "subtract", "a": 100, "b": 25}
        ]
        print(f"   Batch operations: {batch_operations}")
        batch_results = client.batch_calculate(batch_operations)
        print(f"   Batch results: {batch_results}")

    except Exception as e:
        print(f"❌ MCP demonstration failed: {e}")


def main():
    """Run AI agent demonstrations."""
    try:
        demonstrate_ai_agent()
        demonstrate_mcp_style_interaction()

        print("\\n🚀 JSON-RPC in AI Agent Systems:")
        print("• Enables function calling capabilities in LLMs")
        print("• Provides structured tool interfaces")
        print("• Supports complex multi-step workflows")
        print("• Facilitates agent-to-agent communication")
        print("• Powers frameworks like MCP, LangChain, and AutoGen")

    except Exception as e:
        print(f"\\n❌ Demonstration failed: {e}")
        print("Make sure the JSON-RPC server is running:")
        print("  python -m jsonrpc_server.server")


if __name__ == '__main__':
    main()