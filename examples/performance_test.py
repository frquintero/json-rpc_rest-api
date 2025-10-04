"""
Performance comparison between JSON-RPC and REST API approaches.
Tests latency, throughput, and resource usage.
"""
import time
import threading
import statistics
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from clients.jsonrpc_client import JSONRPCClient
from clients.rest_client import RESTAPIClient


class PerformanceTester:
    """Performance testing framework for API comparisons."""
    
    def __init__(self, num_requests=100, num_threads=10):
        self.num_requests = num_requests
        self.num_threads = num_threads
        self.jsonrpc_client = JSONRPCClient()
        self.rest_client = RESTAPIClient()
    
    def time_request(self, func, *args, **kwargs):
        """Time a single request."""
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            return end_time - start_time, result, None
        except Exception as e:
            end_time = time.time()
            return end_time - start_time, None, str(e)
    
    def run_concurrent_test(self, test_func, *args, **kwargs):
        """Run concurrent performance test."""
        latencies = []
        errors = []
        
        def worker():
            latency, result, error = self.time_request(test_func, *args, **kwargs)
            latencies.append(latency)
            if error:
                errors.append(error)
        
        start_time = time.time()
        
        # Run requests concurrently
        threads = []
        for _ in range(self.num_requests):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        return {
            'total_requests': self.num_requests,
            'total_time': total_time,
            'throughput': self.num_requests / total_time,
            'latencies': latencies,
            'avg_latency': statistics.mean(latencies),
            'min_latency': min(latencies),
            'max_latency': max(latencies),
            'p95_latency': statistics.quantiles(latencies, n=20)[18],  # 95th percentile
            'p99_latency': statistics.quantiles(latencies, n=100)[98],  # 99th percentile
            'errors': len(errors),
            'error_rate': len(errors) / self.num_requests
        }
    
    def test_tax_calculation_performance(self):
        """Compare tax calculation performance."""
        print("=" * 60)
        print("TAX CALCULATION PERFORMANCE TEST")
        print("=" * 60)
        
        # JSON-RPC test
        print("\\nTesting JSON-RPC tax calculation...")
        jsonrpc_results = self.run_concurrent_test(
            self.jsonrpc_client.calculate_tax,
            income=50000,
            deductions=5000,
            tax_rate=0.22
        )
        
        print(f"JSON-RPC Results:")
        print(f"  Total requests: {jsonrpc_results['total_requests']}")
        print(f"  Total time: {jsonrpc_results['total_time']:.2f}s")
        print(f"  Throughput: {jsonrpc_results['throughput']:.2f} req/s")
        print(f"  Avg latency: {jsonrpc_results['avg_latency']*1000:.2f}ms")
        print(f"  95th percentile: {jsonrpc_results['p95_latency']*1000:.2f}ms")
        print(f"  99th percentile: {jsonrpc_results['p99_latency']*1000:.2f}ms")
        print(f"  Errors: {jsonrpc_results['errors']}")
        
        # REST API test
        print("\\nTesting REST API tax calculation...")
        rest_results = self.run_concurrent_test(
            self.rest_client.create_tax_calculation,
            income=50000,
            deductions=5000,
            tax_rate=0.22
        )
        
        print(f"REST API Results:")
        print(f"  Total requests: {rest_results['total_requests']}")
        print(f"  Total time: {rest_results['total_time']:.2f}s")
        print(f"  Throughput: {rest_results['throughput']:.2f} req/s")
        print(f"  Avg latency: {rest_results['avg_latency']*1000:.2f}ms")
        print(f"  95th percentile: {rest_results['p95_latency']*1000:.2f}ms")
        print(f"  99th percentile: {rest_results['p99_latency']*1000:.2f}ms")
        print(f"  Errors: {rest_results['errors']}")
        
        # Comparison
        print("\\nPerformance Comparison:")
        throughput_diff = ((jsonrpc_results['throughput'] - rest_results['throughput']) / rest_results['throughput']) * 100
        latency_diff = ((rest_results['avg_latency'] - jsonrpc_results['avg_latency']) / jsonrpc_results['avg_latency']) * 100
        
        print(".1f")
        print(".1f")
        
        return jsonrpc_results, rest_results
    
    def test_user_operations_performance(self):
        """Compare user operations performance."""
        print("\\n" + "=" * 60)
        print("USER OPERATIONS PERFORMANCE TEST")
        print("=" * 60)
        
        # JSON-RPC user creation
        print("\\nTesting JSON-RPC user operations...")
        jsonrpc_create_results = self.run_concurrent_test(
            self.jsonrpc_client.create_user,
            name="Test User",
            email=f"test{random.randint(1000,9999)}@example.com",
            age=30
        )
        
        print(f"JSON-RPC User Creation:")
        print(f"  Throughput: {jsonrpc_create_results['throughput']:.2f} req/s")
        print(f"  Avg latency: {jsonrpc_create_results['avg_latency']*1000:.2f}ms")
        
        # REST API user creation
        print("\\nTesting REST API user operations...")
        rest_create_results = self.run_concurrent_test(
            self.rest_client.create_user,
            name="Test User",
            email=f"test{random.randint(1000,9999)}@example.com",
            age=30
        )
        
        print(f"REST API User Creation:")
        print(f"  Throughput: {rest_create_results['throughput']:.2f} req/s")
        print(f"  Avg latency: {rest_create_results['avg_latency']*1000:.2f}ms")
        
        return jsonrpc_create_results, rest_create_results
    
    def test_batch_vs_sequential(self):
        """Compare batch operations vs sequential operations."""
        print("\\n" + "=" * 60)
        print("BATCH VS SEQUENTIAL OPERATIONS TEST")
        print("=" * 60)
        
        # Prepare batch operations
        batch_operations = [
            {"operation": "add", "a": 10, "b": 20},
            {"operation": "multiply", "a": 5, "b": 6},
            {"operation": "divide", "a": 100, "b": 4}
        ]
        
        # JSON-RPC batch
        print("\\nTesting JSON-RPC batch operations...")
        jsonrpc_batch_results = self.run_concurrent_test(
            self.jsonrpc_client.batch_calculate,
            batch_operations
        )
        
        print(f"JSON-RPC Batch (3 operations per request):")
        print(f"  Throughput: {jsonrpc_batch_results['throughput']:.2f} req/s")
        print(f"  Avg latency: {jsonrpc_batch_results['avg_latency']*1000:.2f}ms")
        print(f"  Effective throughput: {jsonrpc_batch_results['throughput'] * 3:.2f} operations/s")
        
        # REST API sequential (simulated)
        print("\\nTesting REST API sequential operations...")
        
        def rest_sequential_operations():
            """Perform 3 REST operations sequentially."""
            try:
                self.rest_client.add_numbers(10, 20)
                self.rest_client.multiply_numbers(5, 6)
                self.rest_client.divide_numbers(100, 4)
                return True
            except:
                return False
        
        rest_sequential_results = self.run_concurrent_test(rest_sequential_operations)
        
        print(f"REST API Sequential (3 operations per request):")
        print(f"  Throughput: {rest_sequential_results['throughput']:.2f} req/s")
        print(f"  Avg latency: {rest_sequential_results['avg_latency']*1000:.2f}ms")
        print(f"  Effective throughput: {rest_sequential_results['throughput'] * 3:.2f} operations/s")
        
        # Comparison
        batch_efficiency = (jsonrpc_batch_results['throughput'] * 3) / (rest_sequential_results['throughput'] * 3)
        print(".2f")
        
        return jsonrpc_batch_results, rest_sequential_results
    
    def test_memory_usage_simulation(self):
        """Simulate memory usage patterns."""
        print("\\n" + "=" * 60)
        print("MEMORY USAGE SIMULATION")
        print("=" * 60)
        
        print("\\nJSON-RPC Memory Characteristics:")
        print("  ✓ Single endpoint reduces routing complexity")
        print("  ✓ Method dispatch table (constant memory)")
        print("  ✓ Batch requests reduce connection overhead")
        print("  ✗ All methods loaded in memory")
        print("  ✗ Session state may be maintained")
        
        print("\\nREST API Memory Characteristics:")
        print("  ✓ Resource-based routing")
        print("  ✓ Stateless (no session memory)")
        print("  ✓ Selective resource loading")
        print("  ✗ More complex routing tables")
        print("  ✗ Multiple endpoints to maintain")
        
        # Simulate creating many resources
        print("\\nSimulating resource creation...")
        
        # JSON-RPC: Create many users
        jsonrpc_users = []
        for i in range(50):
            try:
                user = self.jsonrpc_client.create_user(
                    f"User {i}",
                    f"user{i}@example.com",
                    age=25 + (i % 30)
                )
                jsonrpc_users.append(user)
            except:
                pass
        
        # REST API: Create many users
        rest_users = []
        for i in range(50):
            try:
                user = self.rest_client.create_user(
                    f"User {i}",
                    f"user{i}@example.com",
                    age=25 + (i % 30)
                )
                rest_users.append(user)
            except:
                pass
        
        print(f"  JSON-RPC created {len(jsonrpc_users)} users")
        print(f"  REST API created {len(rest_users)} users")
    
    def run_all_tests(self):
        """Run all performance tests."""
        print("API Performance Comparison Test Suite")
        print("=====================================")
        print(f"Configuration: {self.num_requests} requests, {self.num_threads} threads")
        print()
        
        try:
            # Tax calculation test
            tax_results = self.test_tax_calculation_performance()
            
            # User operations test
            user_results = self.test_user_operations_performance()
            
            # Batch vs sequential test
            batch_results = self.test_batch_vs_sequential()
            
            # Memory usage simulation
            self.test_memory_usage_simulation()
            
            # Summary
            print("\\n" + "=" * 60)
            print("PERFORMANCE SUMMARY")
            print("=" * 60)
            print("JSON-RPC Advantages:")
            print("  • Lower latency for simple operations")
            print("  • Efficient batch operations")
            print("  • Reduced connection overhead")
            print("  • Better for real-time applications")
            print()
            print("REST API Advantages:")
            print("  • Better caching support")
            print("  • More scalable for large systems")
            print("  • Easier to monitor and debug")
            print("  • Better for public APIs")
            print()
            print("Choose based on your use case:")
            print("  • JSON-RPC: Internal APIs, real-time systems, complex workflows")
            print("  • REST API: Public APIs, web applications, resource management")
            
        except Exception as e:
            print(f"\\nTest suite failed: {e}")
            print("Make sure both servers are running:")
            print("  JSON-RPC: python -m jsonrpc_server.server")
            print("  REST API: python -m rest_server.server")


def main():
    """Run performance tests."""
    import random
    
    # Set random seed for reproducible results
    random.seed(42)
    
    # Run tests with different configurations
    tester = PerformanceTester(num_requests=50, num_threads=5)
    tester.run_all_tests()


if __name__ == '__main__':
    main()