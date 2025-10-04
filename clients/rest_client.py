"""
REST API Client Implementation
Demonstrates how to interact with resource-oriented REST APIs.
"""
import requests
import json
from typing import Any, Dict, List, Optional, Union


class RESTAPIClient:
    """REST API Client implementation."""
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        """
        Initialize REST API client.
        
        Args:
            base_url: Base URL for the REST API server
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None,
                     params: Optional[Dict[str, Any]] = None) -> Union[Dict[str, Any], str]:
        """
        Make HTTP request to REST API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data or empty string for 204 responses
            
        Raises:
            Exception: If the request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=30
            )
            
            # Handle different response codes
            if response.status_code == 204:
                return ""  # No content
            
            response.raise_for_status()
            
            if response.headers.get('content-type', '').startswith('application/json'):
                return response.json()
            else:
                return response.text
                
        except requests.exceptions.HTTPError as e:
            # Try to get error details from response
            try:
                error_data = response.json()
                raise Exception(f"HTTP {response.status_code}: {error_data.get('message', str(e))}")
            except (json.JSONDecodeError, AttributeError):
                raise Exception(f"HTTP {response.status_code}: {str(e)}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
    
    # General API methods
    def get_api_info(self) -> Dict[str, Any]:
        """Get API information."""
        result = self._make_request("GET", "/")
        if isinstance(result, str):
            raise Exception(f"Expected JSON response, got string: {result}")
        return result
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        result = self._make_request("GET", "/health")
        if isinstance(result, str):
            raise Exception(f"Expected JSON response, got string: {result}")
        return result
    
    # Tax Calculations Resource
    def get_tax_calculations(self, operation: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get list of tax calculations with optional filtering.
        
        Args:
            operation: Filter by tax operation type
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Dictionary containing tax calculations list
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if operation:
            params["operation"] = operation
        result = self._make_request("GET", "/api/tax-calculations", params=params)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def create_tax_calculation(self, operation: str, amount: float, rate: float, **kwargs) -> Dict[str, Any]:
        """
        Create a new tax calculation.
        
        Args:
            operation: Tax operation type (income, sales, property)
            amount: Base amount for calculation
            rate: Tax rate as decimal
            **kwargs: Additional tax calculation parameters
            
        Returns:
            Dictionary containing created tax calculation
        """
        data = {"operation": operation, "amount": amount, "rate": rate, **kwargs}
        result = self._make_request("POST", "/api/tax-calculations", data=data)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def get_tax_calculation(self, calc_id: int) -> Dict[str, Any]:
        """
        Get a specific tax calculation.
        
        Args:
            calc_id: Tax calculation ID
            
        Returns:
            Tax calculation resource
        """
        result = self._make_request("GET", f"/api/tax-calculations/{calc_id}")
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def update_tax_calculation(self, calc_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update a tax calculation.
        
        Args:
            calc_id: Tax calculation ID
            **kwargs: Fields to update
            
        Returns:
            Updated tax calculation resource
        """
        result = self._make_request("PUT", f"/api/tax-calculations/{calc_id}", data=kwargs)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def delete_tax_calculation(self, calc_id: int) -> str:
        """
        Delete a tax calculation.
        
        Args:
            calc_id: Tax calculation ID
            
        Returns:
            Empty string (204 No Content)
        """
        result = self._make_request("DELETE", f"/api/tax-calculations/{calc_id}")
        if isinstance(result, str):
            return result
        return ""
    
    # Users Resource
    def get_users(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get list of users with pagination.
        
        Args:
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Dictionary containing users list
        """
        params = {"limit": limit, "offset": offset}
        result = self._make_request("GET", "/api/users", params=params)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")

    def create_user(self, name: str, email: str, age: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            name: User name
            email: User email
            age: User age (optional)
            
        Returns:
            Dictionary containing created user
        """
        data: Dict[str, Any] = {"name": name, "email": email}
        if age is not None:
            data["age"] = age
        result = self._make_request("POST", "/api/users", data=data)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def get_user(self, user_id: int) -> Dict[str, Any]:
        """
        Get a specific user.
        
        Args:
            user_id: User ID
            
        Returns:
            User resource
        """
        result = self._make_request("GET", f"/api/users/{user_id}")
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def update_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update a user.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user resource
        """
        result = self._make_request("PUT", f"/api/users/{user_id}", data=kwargs)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def delete_user(self, user_id: int) -> str:
        """
        Delete a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Empty string (204 No Content)
        """
        result = self._make_request("DELETE", f"/api/users/{user_id}")
        if isinstance(result, str):
            return result
        return ""
    
    # Calculations Resource
    def create_calculation(self, operation: str, operands: List[float], **metadata) -> Dict[str, Any]:
        """
        Create a new calculation.
        
        Args:
            operation: Type of operation (add, subtract, multiply, divide, power)
            operands: List of numbers to operate on
            **metadata: Additional metadata for the calculation
            
        Returns:
            Created calculation resource
        """
        data = {
            "operation": operation,
            "operands": operands,
            **metadata
        }
        result = self._make_request("POST", "/api/calculations", data=data)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def get_calculations(self, operation: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """
        Get all calculations.
        
        Args:
            operation: Filter by operation type (optional)
            limit: Maximum number of results
            offset: Number of results to skip
            
        Returns:
            Dictionary with calculations list and pagination info
        """
        params: Dict[str, Any] = {"limit": limit, "offset": offset}
        if operation:
            params["operation"] = operation
        result = self._make_request("GET", "/api/calculations", params=params)
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")
    
    def get_calculation(self, calc_id: int) -> Dict[str, Any]:
        """
        Get a specific calculation.
        
        Args:
            calc_id: Calculation ID
            
        Returns:
            Calculation resource
        """
        result = self._make_request("GET", f"/api/calculations/{calc_id}")
        if isinstance(result, dict):
            return result
        raise ValueError(f"Expected dict response, got {type(result)}")

    def delete_calculation(self, calc_id: int) -> str:
        """
        Delete a calculation.
        
        Args:
            calc_id: Calculation ID
            
        Returns:
            Empty string (204 No Content)
        """
        result = self._make_request("DELETE", f"/api/calculations/{calc_id}")
        if isinstance(result, str):
            return result
        return ""    # Convenience methods for common mathematical operations
    def add_numbers(self, *numbers, description: Optional[str] = None) -> Dict[str, Any]:
        """Add multiple numbers."""
        metadata = {"description": description} if description else {}
        return self.create_calculation("add", list(numbers), **metadata)
    
    def subtract_numbers(self, *numbers, description: Optional[str] = None) -> Dict[str, Any]:
        """Subtract multiple numbers."""
        metadata = {"description": description} if description else {}
        return self.create_calculation("subtract", list(numbers), **metadata)
    
    def multiply_numbers(self, *numbers, description: Optional[str] = None) -> Dict[str, Any]:
        """Multiply multiple numbers."""
        metadata = {"description": description} if description else {}
        return self.create_calculation("multiply", list(numbers), **metadata)
    
    def divide_numbers(self, *numbers, description: Optional[str] = None) -> Dict[str, Any]:
        """Divide multiple numbers."""
        metadata = {"description": description} if description else {}
        return self.create_calculation("divide", list(numbers), **metadata)
    
    def power_calculation(self, base: float, exponent: float, description: Optional[str] = None) -> Dict[str, Any]:
        """Calculate power."""
        metadata = {"description": description} if description else {}
        return self.create_calculation("power", [base, exponent], **metadata)


def main():
    """Example usage of REST API client."""
    client = RESTAPIClient()
    
    try:
        # Test server connection
        print("Testing REST API Client...")
        print("1. API Info:")
        api_info = client.get_api_info()
        print(f"   API: {api_info}")
        
        print("\\n2. Health Check:")
        health = client.health_check()
        print(f"   Health: {health}")
        
        # Tax calculation
        print("\\n3. Create tax calculation:")
        tax_calc = client.create_tax_calculation("income", 50000, 0.25)  # operation, amount, rate
        print(f"   Tax calculation: {tax_calc}")
        
        # Get the created tax calculation
        print("\\n4. Get tax calculation:")
        retrieved_tax = client.get_tax_calculation(tax_calc['id'])
        print(f"   Retrieved: {retrieved_tax}")
        
        # User operations
        print("\\n5. Create user:")
        user = client.create_user(name="Jane Doe", email="jane@example.com", age=25)
        print(f"   Created user: {user}")
        
        # Update user
        print("\\n6. Update user:")
        updated_user = client.update_user(user['id'], age=26)
        print(f"   Updated user: {updated_user}")
        
        # Mathematical operations
        print("\\n7. Mathematical calculations:")
        
        # Addition
        add_result = client.add_numbers(10, 5, 3, description="Adding three numbers")
        print(f"   Addition: {add_result}")
        
        # Multiplication
        mult_result = client.multiply_numbers(4, 5, description="Simple multiplication")
        print(f"   Multiplication: {mult_result}")
        
        # Get all calculations
        print("\\n8. All calculations:")
        all_calcs = client.get_calculations(limit=10)
        print(f"   Total calculations: {all_calcs['total']}")
        for calc in all_calcs['calculations']:
            print(f"   - {calc['operation']}: {calc['operands']} = {calc['result']}")
        
        # Get all users
        print("\\n9. All users:")
        all_users = client.get_users()
        print(f"   Total users: {all_users['total']}")
        for usr in all_users['users']:
            print(f"   - {usr['name']} ({usr['email']})")
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    main()