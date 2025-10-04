"""
JSON-RPC Server Implementation
Demonstrates action-oriented paradigm with method-based operations.
"""
from flask import Flask, request, jsonify
import json
import traceback
from typing import Any, Dict, Optional, Union
from .methods import TaxService, UserService, CalculationService, SystemService


class JSONRPCError:
    """JSON-RPC error codes as per specification."""
    PARSE_ERROR = -32700
    INVALID_REQUEST = -32600
    METHOD_NOT_FOUND = -32601
    INVALID_PARAMS = -32602
    INTERNAL_ERROR = -32603


class JSONRPCServer:
    """JSON-RPC 2.0 Server implementation."""
    
    def __init__(self):
        self.app = Flask(__name__)
        
        # Initialize service instances
        self.tax_service = TaxService()
        self.user_service = UserService()
        self.calculation_service = CalculationService()
        self.system_service = SystemService()
        
        # Register routes
        self._register_routes()
    
    def _register_routes(self):
        """Register Flask routes."""
        
        @self.app.route('/jsonrpc', methods=['POST'])
        def handle_jsonrpc():
            """Handle JSON-RPC requests."""
            return self._handle_request()
        
        @self.app.route('/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({"status": "healthy", "server": "JSON-RPC"})
        
        @self.app.route('/', methods=['GET'])
        def info():
            """Server information endpoint."""
            return jsonify({
                "server": "JSON-RPC Server",
                "version": "1.0.0",
                "endpoint": "/jsonrpc",
                "methods": [
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
            })
    
    def _handle_request(self):
        """Handle incoming JSON-RPC request."""
        try:
            # Parse JSON request
            try:
                data = request.get_json()
                if data is None:
                    return self._create_error_response(
                        None, JSONRPCError.PARSE_ERROR, "Parse error"
                    )
            except Exception:
                return self._create_error_response(
                    None, JSONRPCError.PARSE_ERROR, "Parse error"
                )
            
            # Handle batch requests
            if isinstance(data, list):
                responses = []
                for item in data:
                    response = self._process_single_request(item)
                    if response is not None:  # Notifications return None
                        responses.append(response)
                return jsonify(responses) if responses else ('', 204)
            else:
                # Handle single request
                response = self._process_single_request(data)
                return jsonify(response) if response is not None else ('', 204)
                
        except Exception as e:
            return self._create_error_response(
                None, JSONRPCError.INTERNAL_ERROR, f"Internal error: {str(e)}"
            )
    
    def _process_single_request(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process a single JSON-RPC request."""
        # Validate JSON-RPC structure
        if not isinstance(data, dict):
            return self._create_error_response(
                None, JSONRPCError.INVALID_REQUEST, "Invalid Request"
            )
        
        jsonrpc = data.get('jsonrpc')
        method = data.get('method')
        params = data.get('params', [])
        request_id = data.get('id')
        
        # Check for notification (no id)
        is_notification = 'id' not in data
        
        # Validate jsonrpc version
        if jsonrpc != '2.0':
            if not is_notification:
                return self._create_error_response(
                    request_id, JSONRPCError.INVALID_REQUEST, "Invalid Request"
                )
            return None
        
        # Validate method
        if not method or not isinstance(method, str):
            if not is_notification:
                return self._create_error_response(
                    request_id, JSONRPCError.INVALID_REQUEST, "Invalid Request"
                )
            return None
        
        # Call method
        try:
            result = self._call_method(method, params)
            
            # Don't respond to notifications
            if is_notification:
                return None
            
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }
            
        except Exception as e:
            if not is_notification:
                error_code = JSONRPCError.METHOD_NOT_FOUND if "not found" in str(e).lower() else JSONRPCError.INTERNAL_ERROR
                return self._create_error_response(request_id, error_code, str(e))
            return None
    
    def _call_method(self, method: str, params: Union[list, dict]) -> Any:
        """Call the specified method with parameters."""
        
        # Method mapping
        method_map = {
            # Tax service methods
            'calculate_tax': self.tax_service.calculate_tax,
            'calculate_progressive_tax': self.tax_service.calculate_progressive_tax,
            
            # User service methods
            'create_user': self.user_service.create_user,
            'get_user_by_id': self.user_service.get_user_by_id,
            'update_user': self.user_service.update_user,
            'delete_user': self.user_service.delete_user,
            'list_users': self.user_service.list_users,
            
            # Calculation service methods
            'add': self.calculation_service.add,
            'subtract': self.calculation_service.subtract,
            'multiply': self.calculation_service.multiply,
            'divide': self.calculation_service.divide,
            'power': self.calculation_service.power,
            'batch_calculate': self.calculation_service.batch_calculate,
            
            # System service methods
            'get_server_info': self.system_service.get_server_info,
            'ping': self.system_service.ping
        }
        
        if method not in method_map:
            raise Exception(f"Method '{method}' not found")
        
        func = method_map[method]
        
        try:
            # Handle different parameter formats
            if isinstance(params, dict):
                # Named parameters
                return func(**params)
            elif isinstance(params, list):
                # Positional parameters
                return func(*params)
            else:
                # No parameters
                return func()
                
        except TypeError as e:
            raise Exception(f"Invalid parameters for method '{method}': {str(e)}")
        except ValueError as e:
            raise Exception(f"Invalid parameter values for method '{method}': {str(e)}")
    
    def _create_error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Create JSON-RPC error response."""
        return {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": request_id
        }
    
    def run(self, host='localhost', port=8001, debug=True):
        """Run the JSON-RPC server."""
        print(f"Starting JSON-RPC Server on http://{host}:{port}")
        print(f"JSON-RPC endpoint: http://{host}:{port}/jsonrpc")
        print("Available methods:")
        for method in self.system_service.get_server_info()['supported_methods']:
            print(f"  - {method}")
        print()
        
        self.app.run(host=host, port=port, debug=debug)


def main():
    """Main entry point for running the JSON-RPC server."""
    server = JSONRPCServer()
    server.run()


if __name__ == '__main__':
    main()