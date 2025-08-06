#!/usr/bin/env python3
"""
Test script to demonstrate query optimization improvements
for Assignment 13 - AI-Assisted Query Optimization & ETL Pipeline
"""

import sys
import os
import time
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.db.database import db as original_db
from app.db.optimized_database import optimized_db
from app.etl.query_optimizer import QueryOptimizer

def test_query_optimization():
    """Test and compare original vs optimized queries"""
    print("="*60)
    print("QUERY OPTIMIZATION TEST")
    print("="*60)
    
    optimizer = QueryOptimizer()
    
    # Test 1: get_tasks_due_this_week
    print("\n1. Testing get_tasks_due_this_week...")
    
    # Original implementation
    start_time = time.time()
    original_result = original_db.get_tasks_due_this_week()
    original_time = (time.time() - start_time) * 1000
    
    # Optimized implementation
    start_time = time.time()
    optimized_result = optimized_db.get_tasks_due_this_week()
    optimized_time = (time.time() - start_time) * 1000
    
    print(f"Original query: {original_time:.2f}ms")
    print(f"Optimized query: {optimized_time:.2f}ms")
    print(f"Improvement: {((original_time - optimized_time) / original_time * 100):.1f}%")
    print(f"Results match: {len(original_result) == len(optimized_result)}")
    
    # Test 2: get_list with caching
    print("\n2. Testing get_list (caching)...")
    
    # First call (cache miss)
    start_time = time.time()
    list_result1 = optimized_db.get_list("0f2b5669-1465-43ea-b781-5e3bc388e20b")
    first_call_time = (time.time() - start_time) * 1000
    
    # Second call (cache hit)
    start_time = time.time()
    list_result2 = optimized_db.get_list("0f2b5669-1465-43ea-b781-5e3bc388e20b")
    second_call_time = (time.time() - start_time) * 1000
    
    print(f"First call (cache miss): {first_call_time:.2f}ms")
    print(f"Second call (cache hit): {second_call_time:.2f}ms")
    print(f"Cache improvement: {((first_call_time - second_call_time) / first_call_time * 100):.1f}%")
    
    # Test 3: get_tasks_ordered_by_deadline
    print("\n3. Testing get_tasks_ordered_by_deadline...")
    
    list_id = "0f2b5669-1465-43ea-b781-5e3bc388e20b"
    
    # Original implementation
    start_time = time.time()
    original_ordered = original_db.get_tasks_ordered_by_deadline(list_id)
    original_ordered_time = (time.time() - start_time) * 1000
    
    # Optimized implementation
    start_time = time.time()
    optimized_ordered = optimized_db.get_tasks_ordered_by_deadline(list_id)
    optimized_ordered_time = (time.time() - start_time) * 1000
    
    print(f"Original query: {original_ordered_time:.2f}ms")
    print(f"Optimized query: {optimized_ordered_time:.2f}ms")
    print(f"Improvement: {((original_ordered_time - optimized_ordered_time) / original_ordered_time * 100):.1f}%")
    print(f"Results match: {len(original_ordered) == len(optimized_ordered)}")

def test_data_cleaning():
    """Test data cleaning functionality"""
    print("\n" + "="*60)
    print("DATA CLEANING TEST")
    print("="*60)
    
    from app.etl.data_cleaner import DataCleaner
    
    # Initialize cleaner
    cleaner = DataCleaner("app/db/data.json", "app/db/users.json")
    
    # Load original data
    original_data = cleaner.load_data()
    print(f"Original lists count: {len(original_data.get('lists', []))}")
    print(f"Original users count: {len(original_data.get('users', {}))}")
    
    # Count data quality issues
    empty_names = sum(1 for lst in original_data.get('lists', []) if not lst.get('name', '').strip())
    null_descriptions = sum(1 for lst in original_data.get('lists', []) if lst.get('description') is None)
    duplicate_ids = len(original_data.get('lists', [])) - len(set(lst.get('id') for lst in original_data.get('lists', []) if lst.get('id')))
    
    print(f"Data quality issues found:")
    print(f"  - Empty list names: {empty_names}")
    print(f"  - Null descriptions: {null_descriptions}")
    print(f"  - Duplicate IDs: {duplicate_ids}")
    
    # Run cleaning (without saving to avoid modifying test data)
    cleaned_lists = cleaner.clean_lists_data(original_data.get('lists', []))
    cleaned_users = cleaner.clean_users_data(original_data.get('users', {}))
    
    print(f"\nAfter cleaning:")
    print(f"  - Cleaned lists count: {len(cleaned_lists)}")
    print(f"  - Cleaned users count: {len(cleaned_users)}")
    print(f"  - Lists removed: {len(original_data.get('lists', [])) - len(cleaned_lists)}")

def test_performance_monitoring():
    """Test performance monitoring functionality"""
    print("\n" + "="*60)
    print("PERFORMANCE MONITORING TEST")
    print("="*60)
    
    optimizer = QueryOptimizer()
    
    # Test multiple queries
    queries_to_test = [
        ("get_lists", lambda: original_db.get_lists()),
        ("get_tasks_due_this_week", lambda: original_db.get_tasks_due_this_week()),
        ("get_tasks_ordered_by_deadline", lambda: original_db.get_tasks_ordered_by_deadline("0f2b5669-1465-43ea-b781-5e3bc388e20b"))
    ]
    
    for query_name, query_func in queries_to_test:
        result = optimizer.explain_analyze(query_name, query_func)
        metrics = result['metrics']
        print(f"\n{query_name}:")
        print(f"  Execution time: {metrics['execution_time_ms']:.2f}ms")
        print(f"  Memory used: {metrics['memory_used_mb']:.2f}MB")
        print(f"  Result size: {metrics['result_size']} bytes")
        print(f"  Success: {metrics['success']}")
    
    # Generate performance report
    report = optimizer.generate_performance_report()
    print(f"\nPerformance Report Summary:")
    print(f"  Total queries: {report['summary']['total_queries']}")
    print(f"  Success rate: {report['summary']['success_rate']:.1f}%")
    if report['performance']['average_execution_time_ms']:
        print(f"  Average execution time: {report['performance']['average_execution_time_ms']:.2f}ms")

def main():
    """Main test function"""
    print("Assignment 13 - Query Optimization & ETL Pipeline Test")
    print("="*60)
    
    try:
        # Test query optimization
        test_query_optimization()
        
        # Test data cleaning
        test_data_cleaning()
        
        # Test performance monitoring
        test_performance_monitoring()
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 