"""
Business logic methods for JSON-RPC server.
These methods demonstrate action-oriented paradigm where each method performs a specific operation.
"""
from datetime import datetime
from typing import Dict, List, Any, Union, Optional
import uuid


class TaxService:
    """Tax calculation service with various methods."""
    
    def calculate_tax(self, income: float, deductions: float = 0, tax_rate: float = 0.20) -> Dict[str, Any]:
        """
        Calculate tax based on income and deductions.
        
        Args:
            income: Annual income
            deductions: Tax deductions
            tax_rate: Tax rate (default 20%)
            
        Returns:
            Dict containing tax calculation results
        """
        if income < 0 or deductions < 0:
            raise ValueError("Income and deductions must be non-negative")
        
        taxable_income = max(0, income - deductions)
        tax_amount = taxable_income * tax_rate
        
        return {
            "income": income,
            "deductions": deductions,
            "taxable_income": taxable_income,
            "tax_rate": tax_rate,
            "tax_amount": tax_amount,
            "net_income": income - tax_amount,
            "calculation_id": str(uuid.uuid4()),
            "calculated_at": datetime.now().isoformat()
        }
    
    def calculate_progressive_tax(self, income: float) -> Dict[str, Any]:
        """
        Calculate tax using progressive tax brackets.
        
        Args:
            income: Annual income
            
        Returns:
            Dict containing progressive tax calculation
        """
        brackets = [
            (10000, 0.10),
            (40000, 0.12),
            (85000, 0.22),
            (float('inf'), 0.24)
        ]
        
        total_tax = 0
        previous_bracket = 0
        tax_breakdown = []
        
        for bracket_limit, rate in brackets:
            if income <= previous_bracket:
                break
                
            taxable_in_bracket = min(income, bracket_limit) - previous_bracket
            tax_in_bracket = taxable_in_bracket * rate
            total_tax += tax_in_bracket
            
            tax_breakdown.append({
                "bracket": f"${previous_bracket:,.0f} - ${min(income, bracket_limit):,.0f}",
                "rate": f"{rate:.0%}",
                "taxable_income": taxable_in_bracket,
                "tax": tax_in_bracket
            })
            
            previous_bracket = bracket_limit
            if income <= bracket_limit:
                break
        
        return {
            "income": income,
            "total_tax": total_tax,
            "effective_rate": total_tax / income if income > 0 else 0,
            "net_income": income - total_tax,
            "tax_breakdown": tax_breakdown,
            "calculation_id": str(uuid.uuid4()),
            "calculated_at": datetime.now().isoformat()
        }


class UserService:
    """User management service."""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create_user(self, name: str, email: str, age: Optional[int] = None) -> Dict[str, Any]:
        """
        Create a new user.
        
        Args:
            name: User's name
            email: User's email
            age: User's age (optional)
            
        Returns:
            Dict containing user information
        """
        if not name or not email:
            raise ValueError("Name and email are required")
        
        # Check for duplicate email
        for user in self.users.values():
            if user['email'] == email:
                raise ValueError(f"User with email {email} already exists")
        
        user_id = self.next_id
        self.next_id += 1
        
        user = {
            "id": user_id,
            "name": name,
            "email": email,
            "age": age,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        self.users[user_id] = user
        return user
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict containing user information
        """
        if user_id not in self.users:
            raise ValueError(f"User with ID {user_id} not found")
        
        return self.users[user_id]
    
    def update_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """
        Update user information.
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Dict containing updated user information
        """
        if user_id not in self.users:
            raise ValueError(f"User with ID {user_id} not found")
        
        user = self.users[user_id]
        for key, value in kwargs.items():
            if key in ['name', 'email', 'age']:
                user[key] = value
        
        user['updated_at'] = datetime.now().isoformat()
        return user
    
    def delete_user(self, user_id: int) -> Dict[str, str]:
        """
        Delete user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict containing deletion confirmation
        """
        if user_id not in self.users:
            raise ValueError(f"User with ID {user_id} not found")
        
        del self.users[user_id]
        return {"message": f"User {user_id} deleted successfully"}
    
    def list_users(self) -> List[Dict[str, Any]]:
        """
        List all users.
        
        Returns:
            List of user dictionaries
        """
        return list(self.users.values())


class CalculationService:
    """Mathematical calculation service."""
    
    def add(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Add two numbers."""
        result = a + b
        return {
            "operation": "addition",
            "operands": [a, b],
            "result": result,
            "calculation_id": str(uuid.uuid4()),
            "calculated_at": datetime.now().isoformat()
        }
    
    def subtract(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Subtract two numbers."""
        result = a - b
        return {
            "operation": "subtraction",
            "operands": [a, b],
            "result": result,
            "calculation_id": str(uuid.uuid4()),
            "calculated_at": datetime.now().isoformat()
        }
    
    def multiply(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Multiply two numbers."""
        result = a * b
        return {
            "operation": "multiplication",
            "operands": [a, b],
            "result": result,
            "calculation_id": str(uuid.uuid4()),
            "calculated_at": datetime.now().isoformat()
        }
    
    def divide(self, a: Union[int, float], b: Union[int, float]) -> Dict[str, Any]:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Division by zero is not allowed")
        
        result = a / b
        return {
            "operation": "division",
            "operands": [a, b],
            "result": result,
            "calculation_id": str(uuid.uuid4()),
            "calculated_at": datetime.now().isoformat()
        }
    
    def power(self, base: Union[int, float], exponent: Union[int, float]) -> Dict[str, Any]:
        """Calculate power of a number."""
        result = base ** exponent
        return {
            "operation": "power",
            "operands": [base, exponent],
            "result": result,
            "calculation_id": str(uuid.uuid4()),
            "calculated_at": datetime.now().isoformat()
        }
    
    def batch_calculate(self, operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Perform batch calculations.
        
        Args:
            operations: List of operation dictionaries with 'operation', 'a', and 'b' keys
            
        Returns:
            List of calculation results
        """
        results = []
        
        for op in operations:
            try:
                operation = op.get('operation')
                a = op.get('a')
                b = op.get('b')
                
                # Validate parameters
                if a is None or b is None:
                    results.append({
                        "error": "Missing operands 'a' or 'b'",
                        "operation": operation,
                        "operands": [a, b]
                    })
                    continue
                
                if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                    results.append({
                        "error": "Operands must be numbers",
                        "operation": operation,
                        "operands": [a, b]
                    })
                    continue
                
                if operation == 'add':
                    result = self.add(a, b)
                elif operation == 'subtract':
                    result = self.subtract(a, b)
                elif operation == 'multiply':
                    result = self.multiply(a, b)
                elif operation == 'divide':
                    result = self.divide(a, b)
                elif operation == 'power':
                    result = self.power(a, b)
                else:
                    result = {
                        "error": f"Unknown operation: {operation}",
                        "operation": operation,
                        "operands": [a, b]
                    }
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    "error": str(e),
                    "operation": op.get('operation'),
                    "operands": [op.get('a'), op.get('b')]
                })
        
        return results


class SystemService:
    """System utility methods."""
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information."""
        return {
            "server_type": "JSON-RPC",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "status": "running",
            "supported_methods": [
                "calculate_tax",
                "calculate_progressive_tax", 
                "create_user",
                "get_user_by_id",
                "update_user",
                "delete_user",
                "list_users",
                "add",
                "subtract",
                "multiply",
                "divide",
                "power",
                "batch_calculate",
                "get_server_info",
                "ping"
            ]
        }
    
    def ping(self) -> Dict[str, str]:
        """Simple ping method for health checks."""
        return {
            "message": "pong",
            "timestamp": datetime.now().isoformat()
        }