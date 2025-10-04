"""
Unit tests for REST API server resources.
"""
import os
import sys

# Add the parent directory to Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from rest_server.resources import TaxCalculationResource, UserResource, CalculationResource


class TestTaxCalculationResource:
    """Test tax calculation resource."""
    
    def test_create_calculation_simple(self):
        """Test creating simple tax calculation.
        
        Tests the TaxCalculationResource.create_calculation method with basic parameters.
        
        Inputs:
            - income: 50000 (annual income)
            - deductions: 5000 (tax deductions)
            - tax_rate: 0.20 (20% tax rate)
        
        Expected outputs:
            - id: 1 (auto-generated ID)
            - type: 'simple' (calculation type)
            - income: 50000 (original income)
            - deductions: 5000 (applied deductions)
            - taxable_income: 45000 (income - deductions)
            - tax_amount: 9000 (taxable_income * tax_rate)
            - net_income: 41000 (income - tax_amount)
            - created_at: timestamp
            - updated_at: timestamp
        """
        resource = TaxCalculationResource()
        calc = resource.create_calculation(income=50000, deductions=5000, tax_rate=0.20)
        
        assert calc['id'] == 1
        assert calc['type'] == 'simple'
        assert calc['income'] == 50000
        assert calc['deductions'] == 5000
        assert calc['taxable_income'] == 45000
        assert calc['tax_amount'] == 9000
        assert calc['net_income'] == 41000
        assert 'created_at' in calc
        assert 'updated_at' in calc
    
    def test_create_calculation_progressive(self):
        """Test creating progressive tax calculation.
        
        Tests the TaxCalculationResource.create_calculation method with progressive tax brackets.
        
        Inputs:
            - income: 100000 (high income to trigger progressive tax brackets)
            - calculation_type: 'progressive' (uses progressive tax system)
        
        Expected outputs:
            - type: 'progressive' (calculation type)
            - income: 100000 (original income)
            - total_tax: > 0 (calculated tax amount using progressive brackets)
            - tax_breakdown: list of tax amounts per bracket
        """
        resource = TaxCalculationResource()
        calc = resource.create_calculation(income=100000, calculation_type='progressive')
        
        assert calc['type'] == 'progressive'
        assert calc['income'] == 100000
        assert calc['total_tax'] > 0
        assert 'tax_breakdown' in calc
        assert len(calc['tax_breakdown']) > 0
    
    def test_get_calculation(self):
        """Test getting tax calculation by ID.
        
        Tests the TaxCalculationResource.get_calculation method for retrieving existing calculations.
        
        Inputs:
            - Creates a calculation first with income=50000
            - Retrieves using the auto-generated ID from creation
        
        Expected outputs:
            - Returns the complete calculation object matching what was created
            - All fields should be identical to the created calculation
        """
        resource = TaxCalculationResource()
        created = resource.create_calculation(income=50000)
        
        retrieved = resource.get_calculation(created['id'])
        assert retrieved == created
    
    def test_get_calculation_not_found(self):
        """Test getting non-existent calculation.
        
        Tests the TaxCalculationResource.get_calculation method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent calculation ID)
        
        Expected outputs:
            - Returns None when calculation doesn't exist
        """
        resource = TaxCalculationResource()
        assert resource.get_calculation(999) is None
    
    def test_get_all_calculations(self):
        """Test getting all calculations.
        
        Tests the TaxCalculationResource.get_all_calculations method for listing all stored calculations.
        
        Inputs:
            - Creates two calculations with different incomes (50000, 60000)
        
        Expected outputs:
            - result['total']: 2 (total number of calculations)
            - result['calculations']: list containing both created calculations
        """
        resource = TaxCalculationResource()
        resource.create_calculation(income=50000)
        resource.create_calculation(income=60000)
        
        result = resource.get_all_calculations()
        assert result['total'] == 2
        assert len(result['calculations']) == 2
    
    def test_get_all_calculations_pagination(self):
        """Test pagination of calculation results.
        
        Tests the TaxCalculationResource.get_all_calculations method with pagination parameters.
        
        Inputs:
            - Creates 5 calculations with incremental incomes
            - limit: 2 (return only 2 results per page)
            - offset: 1 (skip first result, start from second)
        
        Expected outputs:
            - result['total']: 5 (total calculations in system)
            - result['calculations']: list with 2 items (limited by limit parameter)
            - result['has_more']: True (indicates more results available)
        """
        resource = TaxCalculationResource()
        for i in range(5):
            resource.create_calculation(income=50000 + i * 1000)
        
        result = resource.get_all_calculations(limit=2, offset=1)
        assert result['total'] == 5
        assert len(result['calculations']) == 2
        assert result['has_more'] is True
    
    def test_update_calculation(self):
        """Test updating tax calculation.
        
        Tests the TaxCalculationResource.update_calculation method for modifying existing calculations.
        
        Inputs:
            - Creates initial calculation with income=50000, tax_rate=0.20
            - Updates with income=60000, tax_rate=0.25
        
        Expected outputs:
            - Returns updated calculation object (not None)
            - updated['income']: 60000 (new income value)
            - updated['tax_rate']: 0.25 (new tax rate)
            - updated['tax_amount']: 15000 (recalculated: 60000 * 0.25)
        """
        resource = TaxCalculationResource()
        calc = resource.create_calculation(income=50000, tax_rate=0.20)
        calc_id = calc['id']
        
        updated = resource.update_calculation(calc_id, income=60000, tax_rate=0.25)
        assert updated is not None
        assert updated['income'] == 60000
        assert updated['tax_rate'] == 0.25
        assert updated['tax_amount'] == 15000  # 60000 * 0.25
    
    def test_update_calculation_not_found(self):
        """Test updating non-existent calculation.
        
        Tests the TaxCalculationResource.update_calculation method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent calculation ID)
            - income: 50000 (update parameters)
        
        Expected outputs:
            - Returns None when calculation doesn't exist
        """
        resource = TaxCalculationResource()
        assert resource.update_calculation(999, income=50000) is None
    
    def test_delete_calculation(self):
        """Test deleting tax calculation.
        
        Tests the TaxCalculationResource.delete_calculation method for removing existing calculations.
        
        Inputs:
            - Creates a calculation first with income=50000
            - Deletes using the auto-generated ID
        
        Expected outputs:
            - Returns True on successful deletion
            - Subsequent get_calculation call returns None (calculation no longer exists)
        """
        resource = TaxCalculationResource()
        calc = resource.create_calculation(income=50000)
        calc_id = calc['id']
        
        assert resource.delete_calculation(calc_id) is True
        assert resource.get_calculation(calc_id) is None
    
    def test_delete_calculation_not_found(self):
        """Test deleting non-existent calculation.
        
        Tests the TaxCalculationResource.delete_calculation method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent calculation ID)
        
        Expected outputs:
            - Returns False when calculation doesn't exist
        """
        resource = TaxCalculationResource()
        assert resource.delete_calculation(999) is False


class TestUserResource:
    """Test user resource."""
    
    def test_create_user(self):
        """Test creating user.
        
        Tests the UserResource.create_user method for adding new users to the system.
        
        Inputs:
            - name: "John Doe" (user's full name)
            - email: "john@example.com" (unique email address)
            - age: 30 (user's age)
        
        Expected outputs:
            - id: 1 (auto-generated unique ID)
            - name: "John Doe" (stored name)
            - email: "john@example.com" (stored email)
            - age: 30 (stored age)
            - created_at: timestamp (creation time)
            - updated_at: timestamp (last update time)
        """
        resource = UserResource()
        user = resource.create_user("John Doe", "john@example.com", 30)
        
        assert user['id'] == 1
        assert user['name'] == "John Doe"
        assert user['email'] == "john@example.com"
        assert user['age'] == 30
        assert 'created_at' in user
        assert 'updated_at' in user
    
    def test_create_user_duplicate_email(self):
        """Test creating user with duplicate email.
        
        Tests the UserResource.create_user method error handling for duplicate email addresses.
        
        Inputs:
            - First user: name="John Doe", email="john@example.com"
            - Second user: name="Jane Doe", email="john@example.com" (duplicate email)
        
        Expected outputs:
            - Raises ValueError with message containing "already exists"
        """
        resource = UserResource()
        resource.create_user("John Doe", "john@example.com")
        
        with pytest.raises(ValueError, match="already exists"):
            resource.create_user("Jane Doe", "john@example.com")
    
    def test_get_user(self):
        """Test getting user by ID.
        
        Tests the UserResource.get_user method for retrieving existing users.
        
        Inputs:
            - Creates a user first with name="John Doe", email="john@example.com"
            - Retrieves using the auto-generated ID from creation
        
        Expected outputs:
            - Returns the complete user object matching what was created
            - All fields should be identical to the created user
        """
        resource = UserResource()
        created = resource.create_user("John Doe", "john@example.com")
        
        retrieved = resource.get_user(created['id'])
        assert retrieved == created
    
    def test_get_user_not_found(self):
        """Test getting non-existent user.
        
        Tests the UserResource.get_user method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent user ID)
        
        Expected outputs:
            - Returns None when user doesn't exist
        """
        resource = UserResource()
        assert resource.get_user(999) is None
    
    def test_get_all_users(self):
        """Test getting all users.
        
        Tests the UserResource.get_all_users method for listing all stored users.
        
        Inputs:
            - Creates two users with different names and emails
        
        Expected outputs:
            - result['total']: 2 (total number of users)
            - result['users']: list containing both created users
        """
        resource = UserResource()
        resource.create_user("John Doe", "john@example.com")
        resource.create_user("Jane Doe", "jane@example.com")
        
        result = resource.get_all_users()
        assert result['total'] == 2
        assert len(result['users']) == 2
    
    def test_update_user(self):
        """Test updating user.
        
        Tests the UserResource.update_user method for modifying existing users.
        
        Inputs:
            - Creates initial user with name="John Doe", email="john@example.com", age=30
            - Updates with age=31, name="John Smith"
        
        Expected outputs:
            - Returns updated user object (not None)
            - updated['age']: 31 (new age value)
            - updated['name']: "John Smith" (new name)
            - updated['email']: "john@example.com" (unchanged email)
        """
        resource = UserResource()
        user = resource.create_user("John Doe", "john@example.com", 30)
        user_id = user['id']
        
        updated = resource.update_user(user_id, age=31, name="John Smith")
        assert updated is not None
        assert updated['age'] == 31
        assert updated['name'] == "John Smith"
        assert updated['email'] == "john@example.com"
    
    def test_update_user_duplicate_email(self):
        """Test updating user with duplicate email.
        
        Tests the UserResource.update_user method error handling for email conflicts.
        
        Inputs:
            - Creates two users: "John Doe"/"john@example.com" and "Jane Doe"/"jane@example.com"
            - Attempts to update Jane's email to "john@example.com" (duplicate)
        
        Expected outputs:
            - Raises ValueError with message containing "already exists"
        """
        resource = UserResource()
        resource.create_user("John Doe", "john@example.com")
        user2 = resource.create_user("Jane Doe", "jane@example.com")
        
        with pytest.raises(ValueError, match="already exists"):
            resource.update_user(user2['id'], email="john@example.com")
    
    def test_update_user_not_found(self):
        """Test updating non-existent user.
        
        Tests the UserResource.update_user method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent user ID)
            - name: "Test" (update parameters)
        
        Expected outputs:
            - Returns None when user doesn't exist
        """
        resource = UserResource()
        assert resource.update_user(999, name="Test") is None
    
    def test_delete_user(self):
        """Test deleting user.
        
        Tests the UserResource.delete_user method for removing existing users.
        
        Inputs:
            - Creates a user first with name="John Doe", email="john@example.com"
            - Deletes using the auto-generated ID
        
        Expected outputs:
            - Returns True on successful deletion
            - Subsequent get_user call returns None (user no longer exists)
        """
        resource = UserResource()
        user = resource.create_user("John Doe", "john@example.com")
        user_id = user['id']
        
        assert resource.delete_user(user_id) is True
        assert resource.get_user(user_id) is None
    
    def test_delete_user_not_found(self):
        """Test deleting non-existent user.
        
        Tests the UserResource.delete_user method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent user ID)
        
        Expected outputs:
            - Returns False when user doesn't exist
        """
        resource = UserResource()
        assert resource.delete_user(999) is False


class TestCalculationResource:
    """Test calculation resource."""
    
    def test_create_calculation_add(self):
        """Test creating addition calculation.
        
        Tests the CalculationResource.create_calculation method for addition operations.
        
        Inputs:
            - operation: "add" (mathematical operation type)
            - operands: [10, 5] (numbers to add)
        
        Expected outputs:
            - id: 1 (auto-generated unique ID)
            - operation: 'add' (stored operation type)
            - operands: [10, 5] (stored input numbers)
            - result: 15 (calculated result: 10 + 5)
            - created_at: timestamp (creation time)
        """
        resource = CalculationResource()
        calc = resource.create_calculation("add", [10, 5])
        
        assert calc['id'] == 1
        assert calc['operation'] == 'add'
        assert calc['operands'] == [10, 5]
        assert calc['result'] == 15
        assert 'created_at' in calc
    
    def test_create_calculation_subtract(self):
        """Test creating subtraction calculation.
        
        Tests the CalculationResource.create_calculation method for subtraction operations.
        
        Inputs:
            - operation: "subtract" (mathematical operation type)
            - operands: [10, 5, 2] (numbers to subtract sequentially)
        
        Expected outputs:
            - operation: 'subtract' (stored operation type)
            - result: 3 (calculated result: 10 - 5 - 2)
        """
        resource = CalculationResource()
        calc = resource.create_calculation("subtract", [10, 5, 2])
        
        assert calc['operation'] == 'subtract'
        assert calc['result'] == 3  # 10 - 5 - 2
    
    def test_create_calculation_multiply(self):
        """Test creating multiplication calculation.
        
        Tests the CalculationResource.create_calculation method for multiplication operations.
        
        Inputs:
            - operation: "multiply" (mathematical operation type)
            - operands: [3, 4, 5] (numbers to multiply)
        
        Expected outputs:
            - operation: 'multiply' (stored operation type)
            - result: 60 (calculated result: 3 * 4 * 5)
        """
        resource = CalculationResource()
        calc = resource.create_calculation("multiply", [3, 4, 5])
        
        assert calc['operation'] == 'multiply'
        assert calc['result'] == 60  # 3 * 4 * 5
    
    def test_create_calculation_divide(self):
        """Test creating division calculation.
        
        Tests the CalculationResource.create_calculation method for division operations.
        
        Inputs:
            - operation: "divide" (mathematical operation type)
            - operands: [20, 2, 2] (numbers to divide sequentially)
        
        Expected outputs:
            - operation: 'divide' (stored operation type)
            - result: 5 (calculated result: 20 / 2 / 2)
        """
        resource = CalculationResource()
        calc = resource.create_calculation("divide", [20, 2, 2])
        
        assert calc['operation'] == 'divide'
        assert calc['result'] == 5  # 20 / 2 / 2
    
    def test_create_calculation_power(self):
        """Test creating power calculation.
        
        Tests the CalculationResource.create_calculation method for exponentiation operations.
        
        Inputs:
            - operation: "power" (mathematical operation type)
            - operands: [2, 3] (base and exponent)
        
        Expected outputs:
            - operation: 'power' (stored operation type)
            - result: 8 (calculated result: 2^3)
        """
        resource = CalculationResource()
        calc = resource.create_calculation("power", [2, 3])
        
        assert calc['operation'] == 'power'
        assert calc['result'] == 8  # 2^3
    
    def test_create_calculation_invalid_operation(self):
        """Test creating calculation with invalid operation.
        
        Tests the CalculationResource.create_calculation method error handling for unsupported operations.
        
        Inputs:
            - operation: "invalid" (unsupported operation type)
            - operands: [1, 2] (valid operands)
        
        Expected outputs:
            - Raises ValueError with message containing "Unsupported operation"
        """
        resource = CalculationResource()
        with pytest.raises(ValueError, match="Unsupported operation"):
            resource.create_calculation("invalid", [1, 2])
    
    def test_create_calculation_insufficient_operands(self):
        """Test creating calculation with insufficient operands.
        
        Tests the CalculationResource.create_calculation method validation for minimum operand requirements.
        
        Inputs:
            - operation: "add" (valid operation)
            - operands: [5] (only one operand, insufficient for any operation)
        
        Expected outputs:
            - Raises ValueError with message containing "at least two operands"
        """
        resource = CalculationResource()
        with pytest.raises(ValueError, match="At least two operands are required"):
            resource.create_calculation("add", [5])
    
    def test_create_calculation_divide_by_zero(self):
        """Test division by zero error handling.
        
        Tests the CalculationResource.create_calculation method error handling for division by zero.
        
        Inputs:
            - operation: "divide" (division operation)
            - operands: [10, 0] (second operand is zero, causing division by zero)
        
        Expected outputs:
            - Raises ValueError with message containing "not allowed"
        """
        resource = CalculationResource()
        with pytest.raises(ValueError, match="not allowed"):
            resource.create_calculation("divide", [10, 0])
    
    def test_get_calculation(self):
        """Test getting calculation by ID.
        
        Tests the CalculationResource.get_calculation method for retrieving existing calculations.
        
        Inputs:
            - Creates a calculation first with operation="add", operands=[10, 5]
            - Retrieves using the auto-generated ID from creation
        
        Expected outputs:
            - Returns the complete calculation object matching what was created
            - All fields should be identical to the created calculation
        """
        resource = CalculationResource()
        created = resource.create_calculation("add", [10, 5])
        
        retrieved = resource.get_calculation(created['id'])
        assert retrieved == created
    
    def test_get_calculation_not_found(self):
        """Test getting non-existent calculation.
        
        Tests the CalculationResource.get_calculation method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent calculation ID)
        
        Expected outputs:
            - Returns None when calculation doesn't exist
        """
        resource = CalculationResource()
        assert resource.get_calculation(999) is None
    
    def test_get_all_calculations(self):
        """Test getting all calculations.
        
        Tests the CalculationResource.get_all_calculations method for listing all stored calculations.
        
        Inputs:
            - Creates two calculations with different operations and operands
        
        Expected outputs:
            - result['total']: 2 (total number of calculations)
            - result['calculations']: list containing both created calculations
        """
        resource = CalculationResource()
        resource.create_calculation("add", [1, 2])
        resource.create_calculation("multiply", [3, 4])
        
        result = resource.get_all_calculations()
        assert result['total'] == 2
        assert len(result['calculations']) == 2
    
    def test_get_all_calculations_filter(self):
        """Test filtering calculations by operation.
        
        Tests the CalculationResource.get_all_calculations method with operation filtering.
        
        Inputs:
            - Creates three calculations: two "add" operations and one "multiply"
            - operation: "add" (filter parameter to return only addition calculations)
        
        Expected outputs:
            - result['total']: 2 (only calculations with "add" operation)
            - All returned calculations have operation == 'add'
        """
        resource = CalculationResource()
        resource.create_calculation("add", [1, 2])
        resource.create_calculation("multiply", [3, 4])
        resource.create_calculation("add", [5, 6])
        
        result = resource.get_all_calculations(operation="add")
        assert result['total'] == 2
        assert all(calc['operation'] == 'add' for calc in result['calculations'])
    
    def test_delete_calculation(self):
        """Test deleting calculation.
        
        Tests the CalculationResource.delete_calculation method for removing existing calculations.
        
        Inputs:
            - Creates a calculation first with operation="add", operands=[10, 5]
            - Deletes using the auto-generated ID
        
        Expected outputs:
            - Returns True on successful deletion
            - Subsequent get_calculation call returns None (calculation no longer exists)
        """
        resource = CalculationResource()
        calc = resource.create_calculation("add", [10, 5])
        calc_id = calc['id']
        
        assert resource.delete_calculation(calc_id) is True
        assert resource.get_calculation(calc_id) is None
    
    def test_delete_calculation_not_found(self):
        """Test deleting non-existent calculation.
        
        Tests the CalculationResource.delete_calculation method error handling for invalid IDs.
        
        Inputs:
            - id: 999 (non-existent calculation ID)
        
        Expected outputs:
            - Returns False when calculation doesn't exist
        """
        resource = CalculationResource()
        assert resource.delete_calculation(999) is False


if __name__ == '__main__':
    pytest.main([__file__])