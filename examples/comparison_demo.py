"""
Comparison demonstration script
Shows side-by-side comparison of JSON-RPC vs REST API approaches.
"""
import time
import json
from clients.jsonrpc_client import JSONRPCClient
from clients.rest_client import RESTAPIClient


def demonstrate_tax_calculation():
    """Demonstrate tax calculation in both paradigms."""
    print("=" * 60)
    print("TAX CALCULATION COMPARISON")
    print("=" * 60)
    
    # JSON-RPC Approach
    print("\\n1. JSON-RPC Approach (Action-oriented):")
    print("   - Single endpoint: /jsonrpc")
    print("   - Method call: calculate_tax")
    print("   - Direct function invocation")
    
    jsonrpc_client = JSONRPCClient()
    try:
        start_time = time.time()
        tax_result = jsonrpc_client.calculate_tax(income=75000, deductions=10000, tax_rate=0.25)
        rpc_time = time.time() - start_time
        
        print(f"   Request: {json.dumps({'jsonrpc': '2.0', 'method': 'calculate_tax', 'params': {'income': 75000, 'deductions': 10000, 'tax_rate': 0.25}, 'id': 1}, indent=4)}")
        print(f"   Response: {json.dumps(tax_result, indent=4)}")
        print(".4f")
        
    except Exception as e:
        print(f"   Error: {e}")
        rpc_time = 0
    
    # REST API Approach
    print("\\n2. REST API Approach (Resource-oriented):")
    print("   - Resource endpoint: /api/tax-calculations")
    print("   - HTTP method: POST")
    print("   - Resource creation")
    
    rest_client = RESTAPIClient()
    try:
        start_time = time.time()
        tax_resource = rest_client.create_tax_calculation("income", 75000, 0.25)
        rest_time = time.time() - start_time
        
        print(f"   Request: POST /api/tax-calculations")
        print(f"   Body: {json.dumps({'income': 75000, 'deductions': 10000, 'tax_rate': 0.25}, indent=4)}")
        print(f"   Response: {json.dumps(tax_resource, indent=4)}")
        print(".4f")
        
    except Exception as e:
        print(f"   Error: {e}")
        rest_time = 0
    
    # Performance comparison
    if rpc_time and rest_time:
        print("\\n3. Performance Comparison:")
        print(".4f")
        print(".4f")
        faster = "JSON-RPC" if rpc_time < rest_time else "REST API"
        print(f"   Faster: {faster}")


def demonstrate_user_management():
    """Demonstrate user management in both paradigms."""
    print("\\n" + "=" * 60)
    print("USER MANAGEMENT COMPARISON")
    print("=" * 60)
    
    # JSON-RPC Approach
    print("\\n1. JSON-RPC Approach:")
    jsonrpc_client = JSONRPCClient()
    
    try:
        # Create user
        print("\\n   Creating user:")
        user = jsonrpc_client.create_user("Alice Johnson", "alice@example.com", 28)
        user_id = user['id']
        print(f"   Created: {json.dumps(user, indent=4)}")
        
        # Get user
        print("\\n   Retrieving user:")
        retrieved = jsonrpc_client.get_user_by_id(user_id)
        print(f"   Retrieved: {json.dumps(retrieved, indent=4)}")
        
        # Update user
        print("\\n   Updating user:")
        updated = jsonrpc_client.update_user(user_id, age=29)
        print(f"   Updated: {json.dumps(updated, indent=4)}")
        
        # Delete user
        print("\\n   Deleting user:")
        deleted = jsonrpc_client.delete_user(user_id)
        print(f"   Deleted: {json.dumps(deleted, indent=4)}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    # REST API Approach
    print("\\n2. REST API Approach:")
    rest_client = RESTAPIClient()
    
    try:
        # Create user
        print("\\n   Creating user:")
        user = rest_client.create_user("Bob Smith", "bob@example.com", 35)
        user_id = user['id']
        print(f"   Created: {json.dumps(user, indent=4)}")
        
        # Get user
        print("\\n   Retrieving user:")
        retrieved = rest_client.get_user(user_id)
        print(f"   Retrieved: {json.dumps(retrieved, indent=4)}")
        
        # Update user
        print("\\n   Updating user:")
        updated = rest_client.update_user(user_id, age=36)
        print(f"   Updated: {json.dumps(updated, indent=4)}")
        
        # Delete user
        print("\\n   Deleting user:")
        rest_client.delete_user(user_id)
        print("   Deleted: (204 No Content)")
        
    except Exception as e:
        print(f"   Error: {e}")


def demonstrate_batch_operations():
    """Demonstrate batch operations capabilities."""
    print("\\n" + "=" * 60)
    print("BATCH OPERATIONS COMPARISON")
    print("=" * 60)
    
    # JSON-RPC Batch Operations
    print("\\n1. JSON-RPC Batch Operations:")
    print("   - Native batch support")
    print("   - Single request, multiple method calls")
    
    jsonrpc_client = JSONRPCClient()
    try:
        batch_operations = [
            {"operation": "add", "a": 10, "b": 20},
            {"operation": "multiply", "a": 5, "b": 6},
            {"operation": "divide", "a": 100, "b": 4},
            {"operation": "power", "base": 2, "exponent": 8}
        ]
        
        print(f"   Batch request: {json.dumps(batch_operations, indent=4)}")
        
        start_time = time.time()
        results = jsonrpc_client.batch_calculate(batch_operations)
        batch_time = time.time() - start_time
        
        print(f"   Results: {json.dumps(results, indent=4)}")
        print(".4f")
        
    except Exception as e:
        print(f"   Error: {e}")
        batch_time = 0
    
    # REST API Sequential Operations
    print("\\n2. REST API Sequential Operations:")
    print("   - Multiple individual requests")
    print("   - No native batch support")
    
    rest_client = RESTAPIClient()
    try:
        start_time = time.time()
        
        # Perform operations sequentially
        results = []
        
        # Addition
        add_result = rest_client.add_numbers(10, 20)
        results.append({"operation": "add", "result": add_result["result"]})
        
        # Multiplication
        mult_result = rest_client.multiply_numbers(5, 6)
        results.append({"operation": "multiply", "result": mult_result["result"]})
        
        # Division
        div_result = rest_client.divide_numbers(100, 4)
        results.append({"operation": "divide", "result": div_result["result"]})
        
        # Power
        power_result = rest_client.power_calculation(2, 8)
        results.append({"operation": "power", "result": power_result["result"]})
        
        sequential_time = time.time() - start_time
        
        print(f"   Results: {json.dumps(results, indent=4)}")
        print(".4f")
        
    except Exception as e:
        print(f"   Error: {e}")
        sequential_time = 0
    
    # Comparison
    if batch_time and sequential_time:
        print("\\n3. Efficiency Comparison:")
        print(".4f")
        print(".4f")
        print(".2f")


def demonstrate_error_handling():
    """Demonstrate error handling in both approaches."""
    print("\\n" + "=" * 60)
    print("ERROR HANDLING COMPARISON")
    print("=" * 60)
    
    # JSON-RPC Error Handling
    print("\\n1. JSON-RPC Error Handling:")
    print("   - Standardized error codes")
    print("   - Structured error responses")
    
    jsonrpc_client = JSONRPCClient()
    
    # Invalid method
    try:
        result = jsonrpc_client.call_method("nonexistent_method")
        print(f"   Unexpected success: {result}")
    except Exception as e:
        print(f"   Invalid method error: {e}")
    
    # Invalid parameters
    try:
        result = jsonrpc_client.calculate_tax(income=-1000)
        print(f"   Unexpected success: {result}")
    except Exception as e:
        print(f"   Invalid params error: {e}")
    
    # REST API Error Handling
    print("\\n2. REST API Error Handling:")
    print("   - HTTP status codes")
    print("   - Custom error messages")
    
    rest_client = RESTAPIClient()
    
    # Invalid resource
    try:
        result = rest_client.get_user(99999)
        print(f"   Unexpected success: {result}")
    except Exception as e:
        print(f"   Not found error: {e}")
    
    # Invalid data
    try:
        result = rest_client.create_tax_calculation("income", -5000, 0.25)
        print(f"   Unexpected success: {result}")
    except Exception as e:
        print(f"   Bad request error: {e}")


def demonstrate_caching_simulation():
    """Demonstrate caching behavior differences."""
    print("\\n" + "=" * 60)
    print("CACHING BEHAVIOR SIMULATION")
    print("=" * 60)
    
    print("\\n1. JSON-RPC Caching:")
    print("   - Difficult to cache (single endpoint, POST method)")
    print("   - Each request is unique, no standard caching headers")
    print("   - Application-level caching required")
    
    print("\\n2. REST API Caching:")
    print("   - Easy to cache (multiple endpoints, GET method)")
    print("   - Standard HTTP caching headers")
    print("   - CDN and browser caching friendly")
    
    rest_client = RESTAPIClient()
    
    try:
        # Create a tax calculation
        tax_calc = rest_client.create_tax_calculation("income", 60000, 0.25)
        calc_id = tax_calc['id']
        
        print(f"\\n   Created resource: /api/tax-calculations/{calc_id}")
        
        # Simulate multiple GET requests (cacheable)
        print("\\n   Multiple GET requests (would be cacheable):")
        for i in range(3):
            start_time = time.time()
            result = rest_client.get_tax_calculation(calc_id)
            elapsed = time.time() - start_time
            print(".4f")
            
    except Exception as e:
        print(f"   Error: {e}")


def main():
    """Run all comparison demonstrations."""
    print("JSON-RPC vs REST API Comparison Demo")
    print("=====================================")
    print("This demonstration shows the key differences between")
    print("action-oriented (JSON-RPC) and resource-oriented (REST) paradigms.")
    print()
    
    try:
        demonstrate_tax_calculation()
        demonstrate_user_management()
        demonstrate_batch_operations()
        demonstrate_error_handling()
        demonstrate_caching_simulation()
        
        print("\\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print("JSON-RPC:")
        print("  ✓ Direct method calls")
        print("  ✓ Batch operations")
        print("  ✓ Standardized errors")
        print("  ✓ Single endpoint")
        print("  ✗ Difficult to cache")
        print("  ✗ Less discoverable")
        print()
        print("REST API:")
        print("  ✓ Resource-based")
        print("  ✓ Easy to cache")
        print("  ✓ Self-descriptive")
        print("  ✓ Multiple endpoints")
        print("  ✗ No native batch support")
        print("  ✗ More complex for simple operations")
        
    except Exception as e:
        print(f"\\nDemo failed: {e}")
        print("Make sure both servers are running:")
        print("  JSON-RPC: python -m jsonrpc_server.server")
        print("  REST API: python -m rest_server.server")


if __name__ == '__main__':
    main()