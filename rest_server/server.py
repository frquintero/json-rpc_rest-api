"""
REST API Server Implementation
Demonstrates resource-oriented paradigm with HTTP methods and resource endpoints.
"""
from flask import Flask, request, jsonify, Response
from typing import Dict, Any, Optional, Tuple
import traceback
from .resources import TaxCalculationResource, UserResource, CalculationResource


class RESTAPIServer:
    """REST API Server implementation."""
    
    def __init__(self):
        self.app = Flask(__name__)
        
        # Initialize resource managers
        self.tax_calculations = TaxCalculationResource()
        self.users = UserResource()
        self.calculations = CalculationResource()
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register Flask routes for REST endpoints."""
        
        # Root endpoint - API information
        @self.app.route('/', methods=['GET'])
        def api_info():
            """API information endpoint."""
            return jsonify({
                "api": "REST API Server",
                "version": "1.0.0",
                "resources": {
                    "tax-calculations": "/api/tax-calculations",
                    "users": "/api/users", 
                    "calculations": "/api/calculations"
                },
                "health": "/health"
            })
        
        # Health check endpoint
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({"status": "healthy", "server": "REST API"})
        
        # Tax Calculations Resource
        @self.app.route('/api/tax-calculations', methods=['GET', 'POST'])  # type: ignore
        def tax_calculations_collection():
            """Handle tax calculations collection."""
            if request.method == 'GET':
                return self._get_tax_calculations()
            elif request.method == 'POST':
                return self._create_tax_calculation()
        
        @self.app.route('/api/tax-calculations/<int:calc_id>', methods=['GET', 'PUT', 'DELETE'])  # type: ignore
        def tax_calculations_item(calc_id: int):
            """Handle individual tax calculation resource."""
            if request.method == 'GET':
                return self._get_tax_calculation(calc_id)
            elif request.method == 'PUT':
                return self._update_tax_calculation(calc_id)
            elif request.method == 'DELETE':
                return self._delete_tax_calculation(calc_id)
        
        # Users Resource
        @self.app.route('/api/users', methods=['GET', 'POST'])  # type: ignore
        def users_collection():
            """Handle users collection."""
            if request.method == 'GET':
                return self._get_users()
            elif request.method == 'POST':
                return self._create_user()
        
        @self.app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])  # type: ignore
        def users_item(user_id: int):
            """Handle individual user resource."""
            if request.method == 'GET':
                return self._get_user(user_id)
            elif request.method == 'PUT':
                return self._update_user(user_id)
            elif request.method == 'DELETE':
                return self._delete_user(user_id)
        
        # Calculations Resource
        @self.app.route('/api/calculations', methods=['GET', 'POST'])  # type: ignore
        def calculations_collection():
            """Handle calculations collection."""
            if request.method == 'GET':
                return self._get_calculations()
            elif request.method == 'POST':
                return self._create_calculation()
        
        @self.app.route('/api/calculations/<int:calc_id>', methods=['GET', 'DELETE'])  # type: ignore
        def calculations_item(calc_id: int):
            """Handle individual calculation resource."""
            if request.method == 'GET':
                return self._get_calculation(calc_id)
            elif request.method == 'DELETE':
                return self._delete_calculation(calc_id)
        
        # Error handlers
        @self.app.errorhandler(400)
        def bad_request(error):
            return jsonify({"error": "Bad Request", "message": str(error)}), 400
        
        @self.app.errorhandler(404)
        def not_found(error):
            return jsonify({"error": "Not Found", "message": "Resource not found"}), 404
        
        @self.app.errorhandler(405)
        def method_not_allowed(error):
            return jsonify({"error": "Method Not Allowed", "message": str(error)}), 405
        
        @self.app.errorhandler(500)
        def internal_error(error):
            return jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred"}), 500
    
    # Tax Calculations endpoints
    def _get_tax_calculations(self) -> Any:
        """Get all tax calculations."""
        try:
            limit = min(int(request.args.get('limit', 50)), 100)
            offset = int(request.args.get('offset', 0))
            
            result = self.tax_calculations.get_all_calculations(limit=limit, offset=offset)
            return jsonify(result), 200
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _create_tax_calculation(self) -> Any:
        """Create a new tax calculation."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Bad Request", "message": "JSON body required"}), 400
            
            income = data.get('income')
            if income is None:
                return jsonify({"error": "Bad Request", "message": "Income is required"}), 400
            
            deductions = data.get('deductions', 0)
            tax_rate = data.get('tax_rate', 0.20)
            calculation_type = data.get('type', 'simple')
            
            calculation = self.tax_calculations.create_calculation(
                income=income, 
                deductions=deductions,
                tax_rate=tax_rate,
                calculation_type=calculation_type
            )
            
            return jsonify(calculation), 201
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _get_tax_calculation(self, calc_id: int) -> Any:
        """Get a specific tax calculation."""
        try:
            calculation = self.tax_calculations.get_calculation(calc_id)
            if not calculation:
                return jsonify({"error": "Not Found", "message": f"Tax calculation {calc_id} not found"}), 404
            
            return jsonify(calculation), 200
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _update_tax_calculation(self, calc_id: int) -> Any:
        """Update a specific tax calculation."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Bad Request", "message": "JSON body required"}), 400
            
            calculation = self.tax_calculations.update_calculation(calc_id, **data)
            if not calculation:
                return jsonify({"error": "Not Found", "message": f"Tax calculation {calc_id} not found"}), 404
            
            return jsonify(calculation), 200
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _delete_tax_calculation(self, calc_id: int) -> Any:
        """Delete a specific tax calculation."""
        try:
            success = self.tax_calculations.delete_calculation(calc_id)
            if not success:
                return jsonify({"error": "Not Found", "message": f"Tax calculation {calc_id} not found"}), 404
            
            return '', 204
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    # Users endpoints
    def _get_users(self) -> Any:
        """Get all users."""
        try:
            limit = min(int(request.args.get('limit', 50)), 100)
            offset = int(request.args.get('offset', 0))
            
            result = self.users.get_all_users(limit=limit, offset=offset)
            return jsonify(result), 200
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _create_user(self) -> Any:
        """Create a new user."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Bad Request", "message": "JSON body required"}), 400
            
            name = data.get('name')
            email = data.get('email')
            age = data.get('age')
            
            if not name or not email:
                return jsonify({"error": "Bad Request", "message": "Name and email are required"}), 400
            
            user = self.users.create_user(name=name, email=email, age=age)
            return jsonify(user), 201
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _get_user(self, user_id: int) -> Any:
        """Get a specific user."""
        try:
            user = self.users.get_user(user_id)
            if not user:
                return jsonify({"error": "Not Found", "message": f"User {user_id} not found"}), 404
            
            return jsonify(user), 200
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _update_user(self, user_id: int) -> Any:
        """Update a specific user."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Bad Request", "message": "JSON body required"}), 400
            
            user = self.users.update_user(user_id, **data)
            if not user:
                return jsonify({"error": "Not Found", "message": f"User {user_id} not found"}), 404
            
            return jsonify(user), 200
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _delete_user(self, user_id: int) -> Any:
        """Delete a specific user."""
        try:
            success = self.users.delete_user(user_id)
            if not success:
                return jsonify({"error": "Not Found", "message": f"User {user_id} not found"}), 404
            
            return '', 204
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    # Calculations endpoints
    def _get_calculations(self) -> Any:
        """Get all calculations."""
        try:
            operation = request.args.get('operation')
            limit = min(int(request.args.get('limit', 50)), 100)
            offset = int(request.args.get('offset', 0))
            
            result = self.calculations.get_all_calculations(
                operation=operation, limit=limit, offset=offset
            )
            return jsonify(result), 200
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _create_calculation(self) -> Any:
        """Create a new calculation."""
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Bad Request", "message": "JSON body required"}), 400
            
            operation = data.get('operation')
            operands = data.get('operands')
            
            if not operation or not operands:
                return jsonify({"error": "Bad Request", "message": "Operation and operands are required"}), 400
            
            # Extract metadata (any other fields)
            metadata = {k: v for k, v in data.items() if k not in ['operation', 'operands']}
            
            calculation = self.calculations.create_calculation(
                operation=operation, 
                operands=operands,
                **metadata
            )
            
            return jsonify(calculation), 201
            
        except ValueError as e:
            return jsonify({"error": "Bad Request", "message": str(e)}), 400
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _get_calculation(self, calc_id: int) -> Any:
        """Get a specific calculation."""
        try:
            calculation = self.calculations.get_calculation(calc_id)
            if not calculation:
                return jsonify({"error": "Not Found", "message": f"Calculation {calc_id} not found"}), 404
            
            return jsonify(calculation), 200
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def _delete_calculation(self, calc_id: int) -> Any:
        """Delete a specific calculation."""
        try:
            success = self.calculations.delete_calculation(calc_id)
            if not success:
                return jsonify({"error": "Not Found", "message": f"Calculation {calc_id} not found"}), 404
            
            return '', 204
        except Exception as e:
            return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    
    def run(self, host='localhost', port=8002, debug=True):
        """Run the REST API server."""
        print(f"Starting REST API Server on http://{host}:{port}")
        print("Available endpoints:")
        print(f"  GET  http://{host}:{port}/")
        print(f"  GET  http://{host}:{port}/health")
        print(f"  GET  http://{host}:{port}/api/tax-calculations")
        print(f"  POST http://{host}:{port}/api/tax-calculations")
        print(f"  GET  http://{host}:{port}/api/users")
        print(f"  POST http://{host}:{port}/api/users")
        print(f"  GET  http://{host}:{port}/api/calculations")
        print(f"  POST http://{host}:{port}/api/calculations")
        print()
        
        self.app.run(host=host, port=port, debug=debug)


def main():
    """Main entry point for running the REST API server."""
    server = RESTAPIServer()
    server.run()


if __name__ == '__main__':
    main()