# REST API Request Code Flow: A Step-by-Step Guide

## 🎯 Learning Objective
By the end of this guide, you'll understand how a REST API request flows through the entire system, from the initial HTTP request to the final response. REST API uses a **resource-oriented** approach where different URLs represent different resources.

## 📋 Prerequisites
- Basic understanding of HTTP methods (GET, POST, PUT, DELETE)
- Familiarity with URL routing
- Knowledge of client-server architecture

## 🏗️ System Architecture Overview

```
Client Browser/Terminal → HTTP Method + URL → Flask Router → Resource Handler → Business Logic → HTTP Response
```

## 📚 Phase 1: Server Startup and Initialization

### Step 1: Starting the Server Process
When you run `python run.py servers`, this happens:

```python
# In run.py - run_servers() function
rest_process = subprocess.Popen([
    sys.executable, "-m", "rest_server.server"
], cwd=os.getcwd())
```

**What this does:**
- Creates a separate process running the REST API server
- The server module (`rest_server/server.py`) gets executed
- This starts a Flask web server on port 8002

### Step 2: Server Initialization
The `main()` function in `rest_server/server.py` runs:

```python
def main():
    server = RESTAPIServer()  # Create server instance
    server.run()              # Start Flask app
```

### Step 3: RESTAPIServer Constructor
```python
def __init__(self):
    self.app = Flask(__name__)

    # Initialize resource managers (business logic)
    self.tax_calculations = TaxCalculationResource()
    self.users = UserResource()
    self.calculations = CalculationResource()

    # Set up URL routes
    self._register_routes()
```

**Key Point:** The server creates instances of resource manager classes that handle CRUD operations for each resource type.

### Step 4: Route Registration
```python
def _register_routes(self):
    # Tax Calculations Resource - Multiple endpoints
    @self.app.route('/api/tax-calculations', methods=['GET', 'POST'])
    def tax_calculations_collection():
        if request.method == 'GET':
            return self._get_tax_calculations()
        elif request.method == 'POST':
            return self._create_tax_calculation()

    @self.app.route('/api/tax-calculations/<int:calc_id>', methods=['GET', 'PUT', 'DELETE'])
    def tax_calculations_item(calc_id: int):
        if request.method == 'GET':
            return self._get_tax_calculation(calc_id)
        elif request.method == 'PUT':
            return self._update_tax_calculation(calc_id)
        elif request.method == 'DELETE':
            return self._delete_tax_calculation(calc_id)
```

**Important:** REST API uses **MULTIPLE endpoints** - each resource type has its own URL pattern, and different HTTP methods perform different operations.

## 🌐 Phase 2: Handling an Incoming Request

### Step 5: Client Makes HTTP Request
A client sends an HTTP request using the appropriate method and URL:

```bash
# Create a tax calculation (POST to collection)
curl -X POST http://localhost:8002/api/tax-calculations \
  -H "Content-Type: application/json" \
  -d '{"income": 50000, "deductions": 5000}'

# Get a specific tax calculation (GET to item)
curl -X GET http://localhost:8002/api/tax-calculations/1

# Update a tax calculation (PUT to item)
curl -X PUT http://localhost:8002/api/tax-calculations/1 \
  -H "Content-Type: application/json" \
  -d '{"income": 60000}'

# Delete a tax calculation (DELETE to item)
curl -X DELETE http://localhost:8002/api/tax-calculations/1
```

### Step 6: Flask Routes Based on URL + HTTP Method
Flask matches the URL pattern and HTTP method to the registered route:

```python
# For POST /api/tax-calculations
@self.app.route('/api/tax-calculations', methods=['GET', 'POST'])
def tax_calculations_collection():
    if request.method == 'GET':
        return self._get_tax_calculations()  # List all
    elif request.method == 'POST':
        return self._create_tax_calculation()  # Create new
```

**Key Point:** REST API uses URL patterns + HTTP methods to determine what operation to perform.

### Step 7: Resource Handler Processes Request
```python
def _create_tax_calculation(self) -> Tuple[Dict[str, Any], int]:
    try:
        # Parse JSON from HTTP request body
        data = request.get_json()

        # Extract resource data
        income = data.get('income')
        deductions = data.get('deductions', 0)
        tax_rate = data.get('tax_rate', 0.20)
        calculation_type = data.get('type', 'simple')

        # Call business logic
        calculation = self.tax_calculations.create_calculation(
            income=income,
            deductions=deductions,
            tax_rate=tax_rate,
            calculation_type=calculation_type
        )

        # Return HTTP response
        return jsonify(calculation), 201  # 201 = Created

    except ValueError as e:
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
```

**Key Point:** The handler extracts data from the HTTP request and calls the appropriate business logic method.

## 🔍 Phase 3: Business Logic Execution

### Step 8: Resource Manager Handles Operation
```python
# In TaxCalculationResource.create_calculation()
def create_calculation(self, income: float, deductions: float = 0,
                      tax_rate: float = 0.20, calculation_type: str = 'simple') -> dict:

    # Business logic - calculate tax
    taxable_income = income - deductions
    tax_amount = taxable_income * tax_rate
    net_income = income - tax_amount

    # Create resource representation
    calculation = {
        'id': self._next_id(),
        'type': calculation_type,
        'income': income,
        'deductions': deductions,
        'taxable_income': taxable_income,
        'tax_amount': tax_amount,
        'net_income': net_income,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }

    # Store in memory (in real app, would save to database)
    self.calculations[calculation['id']] = calculation

    return calculation
```

**Key Point:** The resource manager contains all the business logic for CRUD operations on that specific resource type.

### Step 9: Different HTTP Methods, Different Operations

```python
# GET /api/tax-calculations (list all)
def _get_tax_calculations(self):
    result = self.tax_calculations.get_all_calculations()
    return jsonify(result), 200

# GET /api/tax-calculations/1 (get specific)
def _get_tax_calculation(self, calc_id: int):
    calculation = self.tax_calculations.get_calculation(calc_id)
    if not calculation:
        return jsonify({"error": "Not Found", "message": f"Tax calculation {calc_id} not found"}), 404
    return jsonify(calculation), 200

# PUT /api/tax-calculations/1 (update specific)
def _update_tax_calculation(self, calc_id: int):
    data = request.get_json()
    calculation = self.tax_calculations.update_calculation(calc_id, **data)
    if not calculation:
        return jsonify({"error": "Not Found"}), 404
    return jsonify(calculation), 200

# DELETE /api/tax-calculations/1 (delete specific)
def _delete_tax_calculation(self, calc_id: int):
    success = self.tax_calculations.delete_calculation(calc_id)
    if not success:
        return jsonify({"error": "Not Found"}), 404
    return '', 204  # 204 = No Content
```

**Key Point:** Each HTTP method on the same URL performs a different operation (CRUD).

## 📤 Phase 4: HTTP Response Generation

### Step 10: Standard HTTP Status Codes
REST API uses meaningful HTTP status codes:

```python
# Success responses
return jsonify(data), 200  # OK - GET success
return jsonify(data), 201  # Created - POST success
return jsonify(data), 204  # No Content - DELETE success

# Error responses
return jsonify({"error": "Not Found"}), 404  # Resource doesn't exist
return jsonify({"error": "Bad Request"}), 400  # Invalid input
return jsonify({"error": "Internal Server Error"}), 500  # Server error
```

### Step 11: Consistent Response Format
```python
# Successful creation response
{
  "id": 1,
  "type": "simple",
  "income": 50000,
  "deductions": 5000,
  "taxable_income": 45000,
  "tax_amount": 9000,
  "net_income": 41000,
  "created_at": "2025-10-03T10:30:00Z",
  "updated_at": "2025-10-03T10:30:00Z"
}

# Error response
{
  "error": "Not Found",
  "message": "Tax calculation 999 not found"
}
```

### Step 12: Client Receives HTTP Response
The client receives a standard HTTP response with:
- Status code (200, 201, 404, etc.)
- JSON body with resource data or error details
- Appropriate HTTP headers

## 🎓 Key Learning Points

### REST API Characteristics:
1. **Multiple Endpoints**: Different URLs for different resources
2. **Resource-Oriented**: Focus on "what resource" (nouns in URLs)
3. **HTTP Semantics**: Uses HTTP methods (GET, POST, PUT, DELETE) meaningfully
4. **Status Codes**: Standardized HTTP status codes for responses
5. **Stateless**: Each request contains all needed information

### Advantages:
- **Standardized**: Uses existing HTTP standards
- **Cacheable**: GET requests can be cached by browsers/proxies
- **Discoverable**: URL structure is self-documenting
- **Scalable**: Stateless design works well with load balancers

### Flow Summary:
```
HTTP Request (Method + URL) → Flask Router → Resource Handler → Business Logic → HTTP Response (Status + JSON)
```

## 🧪 Try It Yourself

1. Start the server: `python run.py servers`
2. Try different operations:
```bash
# Create (POST)
curl -X POST http://localhost:8002/api/tax-calculations \
  -H "Content-Type: application/json" \
  -d '{"income": 50000}'

# Read (GET)
curl -X GET http://localhost:8002/api/tax-calculations/1

# Update (PUT)
curl -X PUT http://localhost:8002/api/tax-calculations/1 \
  -H "Content-Type: application/json" \
  -d '{"income": 60000}'

# Delete (DELETE)
curl -X DELETE http://localhost:8002/api/tax-calculations/1
```
3. Check the different HTTP status codes and response formats!

## 🔄 Comparison with JSON-RPC

| Aspect | REST API | JSON-RPC |
|--------|----------|----------|
| **Endpoints** | Multiple URLs | Single `/jsonrpc` endpoint |
| **Routing** | URL + HTTP Method | Method name in JSON payload |
| **Protocol** | HTTP standards | JSON-RPC specification |
| **Discovery** | URL structure | Method enumeration |
| **Caching** | Built-in HTTP caching | No standard caching |
| **Batch Ops** | Multiple requests | Native batch support |

## 🚀 Next Steps
Now you understand both approaches! REST API is great for resource management with standard HTTP semantics, while JSON-RPC excels at remote procedure calls with method-oriented design.</content>
<parameter name="filePath">/run/media/fratq/4593fc5e-12d7-4064-8a55-3ad61a661126/CODE/apps/jsonrpc_restapi/JSON_RPC_Code_Flow.md