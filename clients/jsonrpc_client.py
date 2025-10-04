"""
JSON-RPC Client Implementation
Demonstrates how to interact with action-oriented JSON-RPC services.
"""
import requests
import json
from typing import Any, Dict, List, Optional, Union


class JSONRPCClient:
    """JSON-RPC 2.0 Client implementation."""
    
    def __init__(self, server_url: str = "http://localhost:8001/jsonrpc"):
        """
        Initialize JSON-RPC client.
        
        Args:
            server_url: URL of the JSON-RPC server endpoint
        """
        self.server_url = server_url
        self.request_id = 1
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _get_next_id(self) -> int:
        """Get next request ID."""
        current_id = self.request_id
        self.request_id += 1
        return current_id
    
    def call_method(self, method: str, params: Union[Dict[str, Any], List[Any], None] = None) -> Any:
        """
        Call a JSON-RPC method.
        
        Args:
            method: Method name to call
            params: Method parameters (dict for named params, list for positional)
            
        Returns:
            Method result
            
        Raises:
            Exception: If the call fails or returns an error
        """
        request_data = {
            "jsonrpc": "2.0",
            "method": method,
            "id": self._get_next_id()
        }
        
        if params is not None:
            request_data["params"] = params
        
        try:
            response = self.session.post(
                self.server_url,
                data=json.dumps(request_data),
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            if "error" in result:
                error = result["error"]
                raise Exception(f"JSON-RPC Error {error['code']}: {error['message']}")
            
            return result.get("result")
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
    
    def notify(self, method: str, params: Union[Dict[str, Any], List[Any], None] = None) -> None:
        """
        Send a notification (no response expected).
        
        Args:
            method: Method name to call
            params: Method parameters
        """
        request_data: Dict[str, Any] = {
            "jsonrpc": "2.0",
            "method": method
        }
        
        if params is not None:
            request_data["params"] = params
        
        try:
            response = self.session.post(
                self.server_url,
                data=json.dumps(request_data),
                timeout=30
            )
            response.raise_for_status()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Notification failed: {str(e)}")
    
    def batch_call(self, calls: List[Dict[str, Any]]) -> List[Any]:
        """
        Perform batch JSON-RPC calls.
        
        Args:
            calls: List of call dictionaries with 'method' and optional 'params'
            
        Returns:
            List of results in the same order as calls
        """
        batch_request = []
        
        for call in calls:
            request_data = {
                "jsonrpc": "2.0",
                "method": call["method"],
                "id": self._get_next_id()
            }
            
            if "params" in call:
                request_data["params"] = call["params"]
            
            batch_request.append(request_data)
        
        try:
            response = self.session.post(
                self.server_url,
                data=json.dumps(batch_request),
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            
            # Process results and handle errors
            processed_results = []
            for result in results:
                if "error" in result:
                    error = result["error"]
                    processed_results.append({
                        "error": f"JSON-RPC Error {error['code']}: {error['message']}"
                    })
                else:
                    processed_results.append(result.get("result"))
            
            return processed_results
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Batch request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Invalid JSON response: {str(e)}")
    
    # Convenience methods for specific operations
    
    def ping(self) -> Dict[str, str]:
        """Ping the server."""
        return self.call_method("ping")
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        return self.call_method("get_server_info")
    
    # Tax calculation methods
    def calculate_tax(self, income: float, deductions: float = 0, tax_rate: float = 0.20) -> Dict[str, Any]:
        """Calculate simple tax."""
        return self.call_method("calculate_tax", {
            "income": income,
            "deductions": deductions,
            "tax_rate": tax_rate
        })
    
    def calculate_progressive_tax(self, income: float) -> Dict[str, Any]:
        """Calculate progressive tax."""
        return self.call_method("calculate_progressive_tax", {"income": income})
    
    # User management methods
    def create_user(self, name: str, email: str, age: Optional[int] = None) -> Dict[str, Any]:
        """Create a new user."""
        params: Dict[str, Any] = {"name": name, "email": email}
        if age is not None:
            params["age"] = age
        return self.call_method("create_user", params)
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Get user by ID."""
        return self.call_method("get_user_by_id", {"user_id": user_id})
    
    def update_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """Update user."""
        params = {"user_id": user_id, **kwargs}
        return self.call_method("update_user", params)
    
    def delete_user(self, user_id: int) -> Dict[str, str]:
        """Delete user."""
        return self.call_method("delete_user", {"user_id": user_id})
    
    def list_users(self) -> List[Dict[str, Any]]:
        """List all users."""
        return self.call_method("list_users")
    
    # Mathematical operations
    def add(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Add two numbers."""
        return self.call_method("add", {"a": a, "b": b})
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Subtract two numbers."""
        return self.call_method("subtract", {"a": a, "b": b})
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Multiply two numbers."""
        return self.call_method("multiply", {"a": a, "b": b})
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Divide two numbers."""
        return self.call_method("divide", {"a": a, "b": b})
    
    def power(self, base: Union[int, float], exponent: Union[int, float]) -> Dict[str, Any]:
        """Calculate power."""
        return self.call_method("power", {"base": base, "exponent": exponent})
    
    def batch_calculate(self, operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Perform batch calculations."""
        return self.call_method("batch_calculate", {"operations": operations})


def main():
    """Example usage of JSON-RPC client."""
    client = JSONRPCClient()
    
    try:
        # Test server connection
        print("Testing JSON-RPC Client...")
        print("1. Ping server:")
        ping_result = client.ping()
        print(f"   Response: {ping_result}")
        
        # Tax calculation
        print("\\n2. Calculate tax:")
        tax_result = client.calculate_tax(income=50000, deductions=5000)
        print(f"   Tax calculation: {tax_result}")
        
        # User operations
        print("\\n3. Create user:")
        user_result = client.create_user(name="John Doe", email="john@example.com", age=30)
        print(f"   Created user: {user_result}")
        
        # Mathematical operations
        print("\\n4. Mathematical operations:")
        math_result = client.add(10, 5)
        print(f"   10 + 5 = {math_result}")
        
        # Batch operations
        print("\\n5. Batch calculations:")
        batch_ops = [
            {"operation": "add", "a": 10, "b": 5},
            {"operation": "multiply", "a": 3, "b": 4},
            {"operation": "divide", "a": 20, "b": 4}
        ]
        batch_result = client.batch_calculate(batch_ops)
        print(f"   Batch results: {batch_result}")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()