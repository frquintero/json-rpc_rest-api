#!/usr/bin/env python3
"""
Convenience script to run both JSON-RPC and REST API servers.
"""
import subprocess
import sys
import time
import signal
import os


def run_servers():
    """Run both servers concurrently."""
    print("Starting JSON-RPC vs REST API Demo Servers")
    print("=" * 50)
    
    # Start JSON-RPC server
    print("Starting JSON-RPC server on port 8001...")
    jsonrpc_process = subprocess.Popen([
        sys.executable, "-m", "jsonrpc_server.server"
    ], cwd=os.getcwd())
    
    # Wait a moment
    time.sleep(2)
    
    # Start REST API server
    print("Starting REST API server on port 8002...")
    rest_process = subprocess.Popen([
        sys.executable, "-m", "rest_server.server"
    ], cwd=os.getcwd())
    
    print("\\nBoth servers are now running!")
    print("\\nJSON-RPC Server:")
    print("  URL: http://localhost:8001")
    print("  Endpoint: http://localhost:8001/jsonrpc")
    print("  Info: http://localhost:8001/")
    print("\\nREST API Server:")
    print("  URL: http://localhost:8002")
    print("  Info: http://localhost:8002/")
    print("\\nPress Ctrl+C to stop both servers.")
    
    def signal_handler(sig, frame):
        print("\\nStopping servers...")
        jsonrpc_process.terminate()
        rest_process.terminate()
        jsonrpc_process.wait()
        rest_process.wait()
        print("Servers stopped.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Wait for processes
    try:
        jsonrpc_process.wait()
        rest_process.wait()
    except KeyboardInterrupt:
        signal_handler(signal.SIGINT, None)


def run_demo():
    """Run the comparison demo."""
    print("Running API Comparison Demo")
    print("=" * 30)
    
    try:
        subprocess.run([
            sys.executable, "examples/comparison_demo.py"
        ], cwd=os.getcwd(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Demo failed: {e}")
        sys.exit(1)


def run_performance_test():
    """Run performance tests."""
    print("Running Performance Tests")
    print("=" * 25)
    
    try:
        subprocess.run([
            sys.executable, "examples/performance_test.py"
        ], cwd=os.getcwd(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Performance test failed: {e}")
        sys.exit(1)


def run_tests():
    """Run unit tests."""
    print("Running Unit Tests")
    print("=" * 18)
    
    try:
        subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], cwd=os.getcwd(), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed: {e}")
        sys.exit(1)


def show_help():
    """Show help information."""
    print("JSON-RPC vs REST API Learning Project")
    print("=" * 40)
    print()
    print("Usage: python run.py <command>")
    print()
    print("Commands:")
    print("  servers     - Start both JSON-RPC and REST API servers")
    print("  demo        - Run the comparison demonstration")
    print("  perf        - Run performance tests")
    print("  test        - Run unit tests")
    print("  help        - Show this help message")
    print()
    print("Examples:")
    print("  python run.py servers    # Start both servers")
    print("  python run.py demo       # Run comparison demo")
    print("  python run.py test       # Run all tests")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "servers":
        run_servers()
    elif command == "demo":
        run_demo()
    elif command == "perf":
        run_performance_test()
    elif command == "test":
        run_tests()
    elif command == "help":
        show_help()
    else:
        print(f"Unknown command: {command}")
        show_help()
        sys.exit(1)


if __name__ == '__main__':
    main()