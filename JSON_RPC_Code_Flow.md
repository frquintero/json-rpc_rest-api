# JSON-RPC Request Code Flow: A Step-by-Step Guide

## 🎯 Learning Objective
By the end of this guide, you'll understand how a JSON-RPC request flows through the entire system, from the initial HTTP request to the final response. JSON-RPC uses an **action-oriented** approach where everything goes through a single endpoint.

## 📋 Prerequisites
- Basic understanding of HTTP requests
- Familiarity with JSON data format
- Knowledge of client-server architecture

## 🏗️ System Architecture Overview

```
Client Browser/Terminal → HTTP POST → Flask Server → JSON-RPC Handler → Method Dispatcher → Business Logic → Response
```

## 📚 Phase 1: Server Startup and Initialization

### Step 1: Starting the Server Process
When you run `python run.py servers`, this happens:

```python
# In run.py - run_servers() function
jsonrpc_process = subprocess.Popen([
    sys.executable, "-m", "jsonrpc_server.server"
], cwd=os.getcwd())
```

**What this does:**
- Creates a separate process running the JSON-RPC server
- The server module (`jsonrpc_server/server.py`) gets executed
- This starts a Flask web server on port 8001

### Step 2: Server Initialization
The `main()` function in `jsonrpc_server/server.py` runs:

```python
def main():
    server = JSONRPCServer()  # Create server instance
    server.run()              # Start Flask app
```

### Step 3: JSONRPCServer Constructor
```python
def __init__(self):
    self.app = Flask(__name__)
    
    # Initialize business logic services
    self.tax_service = TaxService()
    self.user_service = UserService()
    self.calculation_service = CalculationService()
    self.system_service = SystemService()
    
    # Set up URL routes
    self._register_routes()
```

**Key Point:** The server creates instances of all the business logic classes that contain the actual methods clients can call.

### Step 4: Route Registration
```python
def _register_routes(self):
    @self.app.route('/jsonrpc', methods=['POST'])
    def handle_jsonrpc():
        return self._handle_request()
```

**Important:** JSON-RPC uses only **ONE endpoint** (`/jsonrpc`) for ALL operations, unlike REST API which uses multiple endpoints.

## 🌐 Phase 2: Handling an Incoming Request

### Step 5: Client Makes HTTP Request
A client sends an HTTP POST request to the single JSON-RPC endpoint:

```bash
curl -X POST http://localhost:8001/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "calculate_tax",
    "params": {"income": 50000, "deductions": 5000},
    "id": 1
  }'
```

### Step 6: Flask Routes to Handler
Flask receives the HTTP request and calls the registered route handler:

```python
@self.app.route('/jsonrpc', methods=['POST'])
def handle_jsonrpc():
    return self._handle_request()  # This method processes the request
```

### Step 7: Parse HTTP Request Body
```python
def _handle_request(self):
    try:
        # Parse JSON from HTTP request body
        data = request.get_json()
        
        # data now contains:
        # {
        #   "jsonrpc": "2.0",
        #   "method": "calculate_tax", 
        #   "params": {"income": 50000, "deductions": 5000},
        #   "id": 1
        # }
```

**Key Point:** The HTTP body contains the entire JSON-RPC request envelope.

## 🔍 Phase 3: JSON-RPC Protocol Processing

### Step 8: Process Single Request
```python
def _process_single_request(self, data: Dict[str, Any]):
    # Extract JSON-RPC protocol fields
    jsonrpc = data.get('jsonrpc')    # "2.0"
    method = data.get('method')      # "calculate_tax"
    params = data.get('params', [])  # {"income": 50000, "deductions": 5000}
    request_id = data.get('id')      # 1
    
    # Validate protocol compliance
    if jsonrpc != '2.0':
        return error response
    
    # Dispatch to method
    result = self._call_method(method, params)
    
    # Return JSON-RPC response
    return {
        "jsonrpc": "2.0",
        "result": result,
        "id": request_id
    }
```

**Key Point:** JSON-RPC has a standardized request/response format that wraps the actual business logic.

## 🎯 Phase 4: Method Dispatch and Execution

### Step 9: Method Routing Table
```python
def _call_method(self, method: str, params: Union[list, dict]):
    # Method routing table - maps method names to actual functions
    method_map = {
        # Tax service methods
        'calculate_tax': self.tax_service.calculate_tax,
        'calculate_progressive_tax': self.tax_service.calculate_progressive_tax,
        
        # User service methods  
        'create_user': self.user_service.create_user,
        'get_user_by_id': self.user_service.get_user_by_id,
        
        # Calculation service methods
        'add': self.calculation_service.add,
        'subtract': self.calculation_service.subtract,
        
        # System service methods
        'ping': self.system_service.ping
    }
    
    if method not in method_map:
        raise Exception(f"Method '{method}' not found")
    
    func = method_map[method]  # Get the actual Python function
```

**Key Point:** The method name in the JSON-RPC request determines which Python function gets called.

### Step 10: Parameter Handling
```python
# Handle different parameter formats
if isinstance(params, dict):
    # Named parameters: {"income": 50000, "deductions": 5000}
    return func(**params)  # func(income=50000, deductions=5000)
elif isinstance(params, list):
    # Positional parameters: [50000, 5000]
    return func(*params)   # func(50000, 5000)
else:
    # No parameters
    return func()
```

**Key Point:** JSON-RPC supports both named parameters (like keyword arguments) and positional parameters (like regular function calls).

### Step 11: Business Logic Execution
```python
# In TaxService.calculate_tax()
def calculate_tax(self, income: float, deductions: float = 0) -> dict:
    taxable_income = income - deductions
    tax_amount = taxable_income * self.tax_rate
    net_income = income - tax_amount
    
    return {
        'id': self._next_id(),
        'type': 'simple',
        'income': income,
        'deductions': deductions,
        'taxable_income': taxable_income,
        'tax_amount': tax_amount,
        'net_income': net_income,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
```

**Key Point:** The business logic is completely unaware of HTTP or JSON-RPC - it just executes the requested operation.

## 📤 Phase 5: Response Generation

### Step 12: Create JSON-RPC Response
```python
# Back in _process_single_request()
result = self._call_method(method, params)

return {
    "jsonrpc": "2.0",
    "result": {
        "id": 1,
        "type": "simple",
        "income": 50000,
        "deductions": 5000,
        "taxable_income": 45000,
        "tax_amount": 9000,
        "net_income": 41000,
        "created_at": "2025-10-03T...",
        "updated_at": "2025-10-03T..."
    },
    "id": 1
}
```

### Step 13: Convert to HTTP Response
```python
# Back in _handle_request()
response = self._process_single_request(data)
return jsonify(response)  # Flask converts dict to JSON and sets HTTP headers
```

### Step 14: Client Receives Response
The client receives:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "id": 1,
    "type": "simple",
    "income": 50000,
    "deductions": 5000,
    "taxable_income": 45000,
    "tax_amount": 9000,
    "net_income": 41000,
    "created_at": "2025-10-03T10:30:00Z",
    "updated_at": "2025-10-03T10:30:00Z"
  },
  "id": 1
}
```

## 🎓 Key Learning Points

### JSON-RPC Characteristics:
1. **Single Endpoint**: Everything goes through `/jsonrpc`
2. **Action-Oriented**: Focus on "what to do" (method names)
3. **Protocol Wrapper**: JSON-RPC provides structure around business logic
4. **Method Dispatch**: Method name in request determines what executes
5. **Parameter Flexibility**: Supports both named and positional parameters

### Advantages:
- **Simple Routing**: One endpoint handles everything
- **Method Discovery**: Easy to add new operations
- **Batch Requests**: Can send multiple calls in one request
- **Standardized Errors**: Consistent error format

### Flow Summary:
```
HTTP Request → Flask Route → JSON-RPC Parser → Method Dispatch → Business Logic → JSON-RPC Response → HTTP Response
```

## 🧪 Try It Yourself

1. Start the server: `python run.py servers`
2. Make a request:
```bash
curl -X POST http://localhost:8001/jsonrpc \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "calculate_tax", "params": {"income": 50000}, "id": 1}'
```
3. Check the server logs to see the flow in action!

## 🚀 Next Steps
Now that you understand JSON-RPC flow, let's compare it with REST API in the next guide!</content>
<parameter name="filePath">/run/media/fratq/4593fc5e-12d7-4064-8a55-3ad61a661126/CODE/apps/jsonrpc_restapi/REST_API_Code_Flow.md