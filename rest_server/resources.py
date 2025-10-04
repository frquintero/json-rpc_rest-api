"""
Resource models and business logic for REST API server.
Demonstrates resource-oriented paradigm with CRUD operations on data entities.
"""
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid


class TaxCalculationResource:
    """Tax calculation resource for REST API."""
    
    def __init__(self):
        self.calculations = {}
        self.next_id = 1
    
    def create_calculation(self, income: float, deductions: float = 0, 
                         tax_rate: float = 0.20, calculation_type: str = "simple") -> Dict[str, Any]:
        """Create a new tax calculation resource."""
        if income < 0 or deductions < 0:
            raise ValueError("Income and deductions must be non-negative")
        
        calc_id = self.next_id
        self.next_id += 1
        
        if calculation_type == "progressive":
            # Progressive tax calculation
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
            
            calculation = {
                "id": calc_id,
                "type": "progressive",
                "income": income,
                "deductions": deductions,
                "total_tax": total_tax,
                "effective_rate": total_tax / income if income > 0 else 0,
                "net_income": income - total_tax,
                "tax_breakdown": tax_breakdown,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        else:
            # Simple tax calculation
            taxable_income = max(0, income - deductions)
            tax_amount = taxable_income * tax_rate
            
            calculation = {
                "id": calc_id,
                "type": "simple",
                "income": income,
                "deductions": deductions,
                "taxable_income": taxable_income,
                "tax_rate": tax_rate,
                "tax_amount": tax_amount,
                "net_income": income - tax_amount,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        
        self.calculations[calc_id] = calculation
        return calculation
    
    def get_calculation(self, calc_id: int) -> Optional[Dict[str, Any]]:
        """Get a tax calculation by ID."""
        return self.calculations.get(calc_id)
    
    def get_all_calculations(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get all tax calculations with pagination."""
        calculations = list(self.calculations.values())
        total = len(calculations)
        
        # Apply pagination
        start = offset
        end = offset + limit
        paginated = calculations[start:end]
        
        return {
            "calculations": paginated,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": end < total
        }
    
    def update_calculation(self, calc_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a tax calculation."""
        if calc_id not in self.calculations:
            return None
        
        calculation = self.calculations[calc_id]
        
        # Update allowed fields
        updatable_fields = ['income', 'deductions', 'tax_rate']
        updated = False
        
        for field in updatable_fields:
            if field in kwargs:
                calculation[field] = kwargs[field]
                updated = True
        
        if updated:
            # Recalculate if financial data changed
            if calculation['type'] == 'simple':
                taxable_income = max(0, calculation['income'] - calculation['deductions'])
                calculation['taxable_income'] = taxable_income
                calculation['tax_amount'] = taxable_income * calculation['tax_rate']
                calculation['net_income'] = calculation['income'] - calculation['tax_amount']
            
            calculation['updated_at'] = datetime.now().isoformat()
        
        return calculation
    
    def delete_calculation(self, calc_id: int) -> bool:
        """Delete a tax calculation."""
        if calc_id in self.calculations:
            del self.calculations[calc_id]
            return True
        return False


class UserResource:
    """User resource for REST API."""
    
    def __init__(self):
        self.users = {}
        self.next_id = 1
    
    def create_user(self, name: str, email: str, age: Optional[int] = None) -> Dict[str, Any]:
        """Create a new user resource."""
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
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get a user by ID."""
        return self.users.get(user_id)
    
    def get_all_users(self, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get all users with pagination."""
        users = list(self.users.values())
        total = len(users)
        
        # Apply pagination
        start = offset
        end = offset + limit
        paginated = users[start:end]
        
        return {
            "users": paginated,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": end < total
        }
    
    def update_user(self, user_id: int, **kwargs) -> Optional[Dict[str, Any]]:
        """Update a user resource."""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        
        # Check for email uniqueness if updating email
        if 'email' in kwargs:
            new_email = kwargs['email']
            for uid, u in self.users.items():
                if uid != user_id and u['email'] == new_email:
                    raise ValueError(f"User with email {new_email} already exists")
        
        # Update allowed fields
        updatable_fields = ['name', 'email', 'age']
        updated = False
        
        for field in updatable_fields:
            if field in kwargs:
                user[field] = kwargs[field]
                updated = True
        
        if updated:
            user['updated_at'] = datetime.now().isoformat()
        
        return user
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user resource."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


class CalculationResource:
    """Mathematical calculation resource for REST API."""
    
    def __init__(self):
        self.calculations = {}
        self.next_id = 1
    
    def create_calculation(self, operation: str, operands: List[float], **kwargs) -> Dict[str, Any]:
        """Create a new calculation resource."""
        if operation not in ['add', 'subtract', 'multiply', 'divide', 'power']:
            raise ValueError(f"Unsupported operation: {operation}")
        
        if len(operands) < 2:
            raise ValueError("At least two operands are required")
        
        calc_id = self.next_id
        self.next_id += 1
        
        # Perform calculation
        try:
            if operation == 'add':
                result = sum(operands)
            elif operation == 'subtract':
                result = operands[0]
                for op in operands[1:]:
                    result -= op
            elif operation == 'multiply':
                result = 1
                for op in operands:
                    result *= op
            elif operation == 'divide':
                result = operands[0]
                for op in operands[1:]:
                    if op == 0:
                        raise ValueError("Division by zero is not allowed")
                    result /= op
            elif operation == 'power':
                if len(operands) != 2:
                    raise ValueError("Power operation requires exactly two operands")
                result = operands[0] ** operands[1]
            
        except Exception as e:
            raise ValueError(f"Calculation error: {str(e)}")
        
        calculation = {
            "id": calc_id,
            "operation": operation,
            "operands": operands,
            "result": result,
            "metadata": kwargs,
            "created_at": datetime.now().isoformat()
        }
        
        self.calculations[calc_id] = calculation
        return calculation
    
    def get_calculation(self, calc_id: int) -> Optional[Dict[str, Any]]:
        """Get a calculation by ID."""
        return self.calculations.get(calc_id)
    
    def get_all_calculations(self, operation: Optional[str] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Get all calculations with optional filtering and pagination."""
        calculations = list(self.calculations.values())
        
        # Filter by operation if specified
        if operation:
            calculations = [c for c in calculations if c['operation'] == operation]
        
        total = len(calculations)
        
        # Apply pagination
        start = offset
        end = offset + limit
        paginated = calculations[start:end]
        
        return {
            "calculations": paginated,
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": end < total,
            "filter": {"operation": operation} if operation else None
        }
    
    def delete_calculation(self, calc_id: int) -> bool:
        """Delete a calculation resource."""
        if calc_id in self.calculations:
            del self.calculations[calc_id]
            return True
        return False