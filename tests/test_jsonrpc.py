"""
Interactive JSON-RPC Method Explorer and Unit Tests.

This module provides both unit tests and an interactive demonstration of all available
JSON-RPC methods. Run with --interactive flag to explore methods interactively.
"""
import os
import sys

# Add the parent directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import json
from jsonrpc_server.methods import TaxService, UserService, CalculationService, SystemService


# Available methods with their descriptions and parameters
AVAILABLE_METHODS = {
    "1": {
        "name": "calculate_tax",
        "description": "Calculate simple tax based on income and deductions",
        "service": "TaxService",
        "parameters": {
            "income": {"type": "float", "description": "Annual income", "required": True, "default": 50000},
            "deductions": {"type": "float", "description": "Tax deductions", "required": False, "default": 0},
            "tax_rate": {"type": "float", "description": "Tax rate (0.0-1.0)", "required": False, "default": 0.20}
        }
    },
    "2": {
        "name": "calculate_progressive_tax",
        "description": "Calculate progressive tax with tax brackets",
        "service": "TaxService",
        "parameters": {
            "income": {"type": "float", "description": "Annual income", "required": True, "default": 100000}
        }
    },
    "3": {
        "name": "create_user",
        "description": "Create a new user",
        "service": "UserService",
        "parameters": {
            "name": {"type": "str", "description": "User's full name", "required": True, "default": "John Doe"},
            "email": {"type": "str", "description": "User's email address", "required": True, "default": "john@example.com"},
            "age": {"type": "int", "description": "User's age", "required": False, "default": 30}
        }
    },
    "4": {
        "name": "get_user_by_id",
        "description": "Get user information by ID",
        "service": "UserService",
        "parameters": {
            "user_id": {"type": "int", "description": "User ID to retrieve", "required": True, "default": 1}
        }
    },
    "5": {
        "name": "update_user",
        "description": "Update user information",
        "service": "UserService",
        "parameters": {
            "user_id": {"type": "int", "description": "User ID to update", "required": True, "default": 1},
            "name": {"type": "str", "description": "New name (optional)", "required": False, "default": None},
            "email": {"type": "str", "description": "New email (optional)", "required": False, "default": None},
            "age": {"type": "int", "description": "New age (optional)", "required": False, "default": None}
        }
    },
    "6": {
        "name": "delete_user",
        "description": "Delete a user by ID",
        "service": "UserService",
        "parameters": {
            "user_id": {"type": "int", "description": "User ID to delete", "required": True, "default": 1}
        }
    },
    "7": {
        "name": "add",
        "description": "Add two numbers",
        "service": "CalculationService",
        "parameters": {
            "a": {"type": "float", "description": "First number", "required": True, "default": 10},
            "b": {"type": "float", "description": "Second number", "required": True, "default": 5}
        }
    },
    "8": {
        "name": "subtract",
        "description": "Subtract two numbers",
        "service": "CalculationService",
        "parameters": {
            "a": {"type": "float", "description": "First number", "required": True, "default": 10},
            "b": {"type": "float", "description": "Second number", "required": True, "default": 5}
        }
    },
    "9": {
        "name": "multiply",
        "description": "Multiply two numbers",
        "service": "CalculationService",
        "parameters": {
            "a": {"type": "float", "description": "First number", "required": True, "default": 10},
            "b": {"type": "float", "description": "Second number", "required": True, "default": 5}
        }
    },
    "10": {
        "name": "divide",
        "description": "Divide two numbers",
        "service": "CalculationService",
        "parameters": {
            "a": {"type": "float", "description": "Dividend", "required": True, "default": 10},
            "b": {"type": "float", "description": "Divisor", "required": True, "default": 2}
        }
    },
    "11": {
        "name": "power",
        "description": "Calculate power (a^b)",
        "service": "CalculationService",
        "parameters": {
            "a": {"type": "float", "description": "Base number", "required": True, "default": 2},
            "b": {"type": "float", "description": "Exponent", "required": True, "default": 3}
        }
    },
    "12": {
        "name": "batch_calculate",
        "description": "Perform multiple calculations at once",
        "service": "CalculationService",
        "parameters": {
            "operations": {"type": "list", "description": "List of operations", "required": True, "default": '[{"operation": "add", "a": 1, "b": 2}, {"operation": "multiply", "a": 3, "b": 4}]'}
        }
    },
    "13": {
        "name": "get_server_info",
        "description": "Get server information and available methods",
        "service": "SystemService",
        "parameters": {}
    },
    "14": {
        "name": "ping",
        "description": "Test server connectivity",
        "service": "SystemService",
        "parameters": {}
    }
}


def interactive_explorer():
    """Interactive JSON-RPC method explorer."""
    print("🚀 JSON-RPC Method Explorer")
    print("=" * 50)
    print("Explore all available JSON-RPC methods interactively!\n")

    # Initialize services
    services = {
        "TaxService": TaxService(),
        "UserService": UserService(),
        "CalculationService": CalculationService(),
        "SystemService": SystemService()
    }

    request_id = 1

    while True:
        print("\n📋 Available Methods:")
        print("-" * 30)
        for key, method_info in AVAILABLE_METHODS.items():
            print(f"{key}. {method_info['name']} - {method_info['description']}")

        print("\n0. Quit")
        print("-" * 30)

        try:
            choice = input("\nChoose a method (0-14): ").strip()

            if choice == "0":
                print("👋 Goodbye! Thanks for exploring JSON-RPC methods!")
                break

            if choice not in AVAILABLE_METHODS:
                print("❌ Invalid choice. Please select 0-14.")
                continue

            method_info = AVAILABLE_METHODS[choice]
            method_name = method_info["name"]
            service_name = method_info["service"]
            parameters = method_info["parameters"]

            print(f"\n🎯 Method: {method_name}")
            print(f"📖 Description: {method_info['description']}")
            print(f"🏢 Service: {service_name}")

            # Get parameters from user
            params = {}
            if parameters:
                print("\n📝 Required Parameters:")
                for param_name, param_info in parameters.items():
                    required = param_info["required"]
                    param_type = param_info["type"]
                    description = param_info["description"]
                    default = param_info["default"]

                    if required:
                        print(f"  • {param_name} ({param_type}): {description}")
                    else:
                        print(f"  • {param_name} ({param_type}, optional): {description} [default: {default}]")

                print("\n💡 Enter parameter values (press Enter for defaults):")

                for param_name, param_info in parameters.items():
                    required = param_info["required"]
                    param_type = param_info["type"]
                    default = param_info["default"]

                    while True:
                        try:
                            user_input = input(f"  {param_name} ({param_type}): ").strip()

                            if not user_input:
                                if required:
                                    print(f"    ⚠️  {param_name} is required. Using default: {default}")
                                    value = default
                                else:
                                    value = default
                            else:
                                if param_type == "int":
                                    value = int(user_input)
                                elif param_type == "float":
                                    value = float(user_input)
                                elif param_type == "str":
                                    value = user_input
                                elif param_type == "list":
                                    value = json.loads(user_input)
                                else:
                                    value = user_input

                            params[param_name] = value
                            break

                        except (ValueError, json.JSONDecodeError) as e:
                            print(f"    ❌ Invalid input: {e}. Please try again.")
            else:
                print("  ℹ️  No parameters required for this method.")

            # Execute the method
            print(f"\n⚡ Executing {method_name}...")
            service = services[service_name]

            try:
                if hasattr(service, method_name):
                    method = getattr(service, method_name)
                    result = method(**params)
                else:
                    raise AttributeError(f"Method {method_name} not found in {service_name}")

                # Create JSON-RPC response
                jsonrpc_response = {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request_id
                }

                print("\n📤 JSON-RPC Response:")
                print("-" * 30)
                print(json.dumps(jsonrpc_response, indent=2, default=str))

                request_id += 1

            except Exception as e:
                # Create JSON-RPC error response
                jsonrpc_error = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32603,
                        "message": str(e),
                        "data": {"method": method_name, "params": params}
                    },
                    "id": request_id
                }

                print("\n❌ JSON-RPC Error Response:")
                print("-" * 30)
                print(json.dumps(jsonrpc_error, indent=2, default=str))

                request_id += 1

            # Ask to continue
            while True:
                continue_choice = input("\n🔄 Run another method? (y/n): ").strip().lower()
                if continue_choice in ['y', 'yes']:
                    break
                elif continue_choice in ['n', 'no']:
                    print("👋 Goodbye! Thanks for exploring JSON-RPC methods!")
                    return
                else:
                    print("❌ Please enter 'y' or 'n'.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for exploring JSON-RPC methods!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            continue


# Unit Tests (unchanged)
class TestTaxService:
    """Test tax calculation methods."""
    
    def test_calculate_tax_simple(self):
        """Test simple tax calculation."""
        service = TaxService()
        result = service.calculate_tax(income=50000, deductions=5000, tax_rate=0.20)
        
        assert result['income'] == 50000
        assert result['deductions'] == 5000
        assert result['taxable_income'] == 45000
        assert result['tax_rate'] == 0.20
        assert result['tax_amount'] == 9000
        assert result['net_income'] == 41000
        assert 'calculation_id' in result
        assert 'calculated_at' in result
    
    def test_calculate_tax_no_deductions(self):
        """Test tax calculation with no deductions."""
        service = TaxService()
        result = service.calculate_tax(income=50000, tax_rate=0.25)
        
        assert result['taxable_income'] == 50000
        assert result['tax_amount'] == 12500
        assert result['net_income'] == 37500
    
    def test_calculate_tax_negative_income(self):
        """Test tax calculation with negative income."""
        service = TaxService()
        with pytest.raises(ValueError, match="must be non-negative"):
            service.calculate_tax(income=-1000)
    
    def test_calculate_progressive_tax(self):
        """Test progressive tax calculation."""
        service = TaxService()
        result = service.calculate_progressive_tax(income=100000)
        
        assert result['income'] == 100000
        assert result['total_tax'] > 0
        assert result['effective_rate'] > 0
        assert result['net_income'] == result['income'] - result['total_tax']
        assert 'tax_breakdown' in result
        assert len(result['tax_breakdown']) > 0


class TestUserService:
    """Test user management methods."""
    
    def test_create_user(self):
        """Test user creation."""
        service = UserService()
        user = service.create_user("John Doe", "john@example.com", 30)
        
        assert user['id'] == 1
        assert user['name'] == "John Doe"
        assert user['email'] == "john@example.com"
        assert user['age'] == 30
        assert 'created_at' in user
        assert 'updated_at' in user
    
    def test_create_user_duplicate_email(self):
        """Test creating user with duplicate email."""
        service = UserService()
        service.create_user("John Doe", "john@example.com")
        
        with pytest.raises(ValueError, match="already exists"):
            service.create_user("Jane Doe", "john@example.com")
    
    def test_get_user_by_id(self):
        """Test getting user by ID."""
        service = UserService()
        created_user = service.create_user("John Doe", "john@example.com")
        user_id = created_user['id']
        
        retrieved_user = service.get_user_by_id(user_id)
        assert retrieved_user == created_user
    
    def test_get_user_not_found(self):
        """Test getting non-existent user."""
        service = UserService()
        with pytest.raises(ValueError, match="not found"):
            service.get_user_by_id(999)
    
    def test_update_user(self):
        """Test user update."""
        service = UserService()
        user = service.create_user("John Doe", "john@example.com", 30)
        user_id = user['id']
        
        updated_user = service.update_user(user_id, age=31, name="John Smith")
        assert updated_user['age'] == 31
        assert updated_user['name'] == "John Smith"
        assert updated_user['email'] == "john@example.com"
        assert 'updated_at' in updated_user
    
    def test_delete_user(self):
        """Test user deletion."""
        service = UserService()
        user = service.create_user("John Doe", "john@example.com")
        user_id = user['id']
        
        result = service.delete_user(user_id)
        assert result == {"message": f"User {user_id} deleted successfully"}
        
        # Verify user is gone
        with pytest.raises(ValueError, match="not found"):
            service.get_user_by_id(user_id)


class TestCalculationService:
    """Test mathematical calculation methods."""
    
    def test_add(self):
        """Test addition."""
        service = CalculationService()
        result = service.add(10, 5)
        
        assert result['operation'] == 'addition'
        assert result['operands'] == [10, 5]
        assert result['result'] == 15
        assert 'calculation_id' in result
        assert 'calculated_at' in result
    
    def test_subtract(self):
        """Test subtraction."""
        service = CalculationService()
        result = service.subtract(10, 5)
        
        assert result['operation'] == 'subtraction'
        assert result['result'] == 5
    
    def test_multiply(self):
        """Test multiplication."""
        service = CalculationService()
        result = service.multiply(10, 5)
        
        assert result['operation'] == 'multiplication'
        assert result['result'] == 50
    
    def test_divide(self):
        """Test division."""
        service = CalculationService()
        result = service.divide(10, 2)
        
        assert result['operation'] == 'division'
        assert result['result'] == 5
    
    def test_divide_by_zero(self):
        """Test division by zero."""
        service = CalculationService()
        with pytest.raises(ValueError, match="not allowed"):
            service.divide(10, 0)
    
    def test_power(self):
        """Test power calculation."""
        service = CalculationService()
        result = service.power(2, 3)
        
        assert result['operation'] == 'power'
        assert result['result'] == 8
    
    def test_batch_calculate(self):
        """Test batch calculations."""
        service = CalculationService()
        operations = [
            {"operation": "add", "a": 1, "b": 2},
            {"operation": "multiply", "a": 3, "b": 4},
            {"operation": "divide", "a": 10, "b": 2}
        ]
        
        results = service.batch_calculate(operations)
        
        assert len(results) == 3
        assert results[0]['result'] == 3  # 1 + 2
        assert results[1]['result'] == 12  # 3 * 4
        assert results[2]['result'] == 5   # 10 / 2
    
    def test_batch_calculate_with_error(self):
        """Test batch calculations with error."""
        service = CalculationService()
        operations = [
            {"operation": "add", "a": 1, "b": 2},
            {"operation": "divide", "a": 10, "b": 0},  # This will error
            {"operation": "multiply", "a": 3, "b": 4}
        ]
        
        results = service.batch_calculate(operations)
        
        assert len(results) == 3
        assert results[0]['result'] == 3
        assert 'error' in results[1]
        assert results[2]['result'] == 12


class TestSystemService:
    """Test system utility methods."""
    
    def test_get_server_info(self):
        """Test server info retrieval."""
        service = SystemService()
        info = service.get_server_info()
        
        assert info['server_type'] == 'JSON-RPC'
        assert 'version' in info
        assert 'status' in info
        assert 'supported_methods' in info
        assert 'ping' in info['supported_methods']
        assert 'calculate_tax' in info['supported_methods']
    
    def test_ping(self):
        """Test ping method."""
        service = SystemService()
        result = service.ping()
        
        assert result['message'] == 'pong'
        assert 'timestamp' in result


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        # Run interactive explorer
        interactive_explorer()
    else:
        # Run unit tests
        pytest.main([__file__])