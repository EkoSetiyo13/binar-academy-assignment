import time
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryOptimizer:
    def __init__(self):
        self.query_history = []
        self.performance_metrics = {}
    
    def explain_analyze(self, query_name: str, query_func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """
        Execute a query with EXPLAIN ANALYZE functionality
        Returns detailed performance metrics
        """
        start_time = time.time()
        start_memory = self._get_memory_usage()
        
        # Execute query
        try:
            result = query_func(*args, **kwargs)
            execution_time = time.time() - start_time
            end_memory = self._get_memory_usage()
            
            # Calculate metrics
            memory_used = end_memory - start_memory
            result_size = self._calculate_result_size(result)
            
            # Store metrics
            metrics = {
                'query_name': query_name,
                'execution_time_ms': execution_time * 1000,
                'memory_used_mb': memory_used,
                'result_size': result_size,
                'timestamp': datetime.now().isoformat(),
                'success': True,
                'error': None
            }
            
            self.query_history.append(metrics)
            self.performance_metrics[query_name] = metrics
            
            logger.info(f"Query '{query_name}' executed in {execution_time*1000:.2f}ms")
            
            return {
                'result': result,
                'metrics': metrics
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            metrics = {
                'query_name': query_name,
                'execution_time_ms': execution_time * 1000,
                'memory_used_mb': 0,
                'result_size': 0,
                'timestamp': datetime.now().isoformat(),
                'success': False,
                'error': str(e)
            }
            
            self.query_history.append(metrics)
            logger.error(f"Query '{query_name}' failed: {e}")
            
            return {
                'result': None,
                'metrics': metrics
            }
    
    def compare_queries(self, query1_name: str, query1_func: Callable, 
                       query2_name: str, query2_func: Callable,
                       *args, **kwargs) -> Dict[str, Any]:
        """
        Compare performance of two different query implementations
        """
        logger.info(f"Comparing queries: {query1_name} vs {query2_name}")
        
        # Execute both queries
        result1 = self.explain_analyze(query1_name, query1_func, *args, **kwargs)
        result2 = self.explain_analyze(query2_name, query2_func, *args, **kwargs)
        
        # Calculate improvement
        if result1['metrics']['success'] and result2['metrics']['success']:
            time_improvement = ((result1['metrics']['execution_time_ms'] - 
                               result2['metrics']['execution_time_ms']) / 
                              result1['metrics']['execution_time_ms']) * 100
            
            memory_improvement = ((result1['metrics']['memory_used_mb'] - 
                                 result2['metrics']['memory_used_mb']) / 
                                max(result1['metrics']['memory_used_mb'], 0.001)) * 100
            
            comparison = {
                'query1': {
                    'name': query1_name,
                    'metrics': result1['metrics']
                },
                'query2': {
                    'name': query2_name,
                    'metrics': result2['metrics']
                },
                'improvement': {
                    'time_improvement_percent': time_improvement,
                    'memory_improvement_percent': memory_improvement,
                    'faster_query': query2_name if time_improvement > 0 else query1_name,
                    'more_efficient_query': query2_name if memory_improvement > 0 else query1_name
                }
            }
        else:
            comparison = {
                'query1': {
                    'name': query1_name,
                    'metrics': result1['metrics']
                },
                'query2': {
                    'name': query2_name,
                    'metrics': result2['metrics']
                },
                'improvement': {
                    'error': 'Cannot compare due to query failures'
                }
            }
        
        return comparison
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report"""
        if not self.query_history:
            return {'error': 'No queries executed yet'}
        
        # Calculate statistics
        successful_queries = [q for q in self.query_history if q['success']]
        failed_queries = [q for q in self.query_history if not q['success']]
        
        if successful_queries:
            avg_execution_time = sum(q['execution_time_ms'] for q in successful_queries) / len(successful_queries)
            avg_memory_usage = sum(q['memory_used_mb'] for q in successful_queries) / len(successful_queries)
            fastest_query = min(successful_queries, key=lambda x: x['execution_time_ms'])
            slowest_query = max(successful_queries, key=lambda x: x['execution_time_ms'])
        else:
            avg_execution_time = avg_memory_usage = fastest_query = slowest_query = None
        
        report = {
            'summary': {
                'total_queries': len(self.query_history),
                'successful_queries': len(successful_queries),
                'failed_queries': len(failed_queries),
                'success_rate': len(successful_queries) / len(self.query_history) * 100
            },
            'performance': {
                'average_execution_time_ms': avg_execution_time,
                'average_memory_usage_mb': avg_memory_usage,
                'fastest_query': fastest_query,
                'slowest_query': slowest_query
            },
            'query_breakdown': {},
            'recent_queries': self.query_history[-10:]  # Last 10 queries
        }
        
        # Group queries by name
        for query in successful_queries:
            name = query['query_name']
            if name not in report['query_breakdown']:
                report['query_breakdown'][name] = {
                    'count': 0,
                    'total_time_ms': 0,
                    'total_memory_mb': 0,
                    'avg_time_ms': 0,
                    'avg_memory_mb': 0
                }
            
            report['query_breakdown'][name]['count'] += 1
            report['query_breakdown'][name]['total_time_ms'] += query['execution_time_ms']
            report['query_breakdown'][name]['total_memory_mb'] += query['memory_used_mb']
        
        # Calculate averages for each query type
        for name, stats in report['query_breakdown'].items():
            stats['avg_time_ms'] = stats['total_time_ms'] / stats['count']
            stats['avg_memory_mb'] = stats['total_memory_mb'] / stats['count']
        
        return report
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            import psutil
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # Convert to MB
        except ImportError:
            # Fallback if psutil is not available
            return 0.0
    
    def _calculate_result_size(self, result: Any) -> int:
        """Calculate approximate size of result in bytes"""
        try:
            return len(json.dumps(result, default=str))
        except:
            return 0
    
    def clear_history(self):
        """Clear query history and metrics"""
        self.query_history.clear()
        self.performance_metrics.clear()
        logger.info("Query history cleared")

# Example query functions for demonstration
def slow_get_tasks_due_this_week(db_instance) -> List[Dict]:
    """Original slow implementation"""
    data = db_instance.read_db()
    due_this_week = []
    today = datetime.now().date()
    
    for lst in data.get("lists", []):
        for task in lst.get("tasks", []):
            if "deadline" in task:
                try:
                    deadline_date = datetime.fromisoformat(task["deadline"]).date()
                    
                    if 0 <= days_difference <= 7:
                        task_with_list = task.copy()
                        task_with_list["list_id"] = lst.get("id")
                        task_with_list["list_name"] = lst.get("name")
                        due_this_week.append(task_with_list)
                except ValueError:
                    continue
                    
    return due_this_week

def optimized_get_tasks_due_this_week(db_instance) -> List[Dict]:
    """Optimized implementation with better date handling"""
    data = db_instance.read_db()
    due_this_week = []
    today = datetime.now().date()
    week_end = today + timedelta(days=7)
    
    for lst in data.get("lists", []):
        list_id = lst.get("id")
        list_name = lst.get("name")
        
        for task in lst.get("tasks", []):
            if "deadline" in task:
                try:
                    deadline_date = datetime.fromisoformat(task["deadline"].replace('Z', '+00:00')).date()
                    
                    if today <= deadline_date <= week_end:
                        task_with_list = task.copy()
                        task_with_list["list_id"] = list_id
                        task_with_list["list_name"] = list_name
                        due_this_week.append(task_with_list)
                except (ValueError, AttributeError):
                    continue
                    
    return due_this_week

def main():
    """Main function to demonstrate query optimization"""
    from app.db.database import db
    
    optimizer = QueryOptimizer()
    
    print("="*60)
    print("QUERY OPTIMIZATION DEMONSTRATION")
    print("="*60)
    
    # Compare slow vs optimized query
    comparison = optimizer.compare_queries(
        "Slow Query", slow_get_tasks_due_this_week,
        "Optimized Query", optimized_get_tasks_due_this_week,
        db
    )
    
    print(f"\nQuery Comparison Results:")
    print(f"Slow Query: {comparison['query1']['metrics']['execution_time_ms']:.2f}ms")
    print(f"Optimized Query: {comparison['query2']['metrics']['execution_time_ms']:.2f}ms")
    
    if 'improvement' in comparison and 'time_improvement_percent' in comparison['improvement']:
        improvement = comparison['improvement']['time_improvement_percent']
        print(f"Improvement: {improvement:.1f}%")
        print(f"Faster query: {comparison['improvement']['faster_query']}")
    
    # Generate performance report
    report = optimizer.generate_performance_report()
    
    print(f"\nPerformance Report:")
    print(f"Total queries executed: {report['summary']['total_queries']}")
    print(f"Success rate: {report['summary']['success_rate']:.1f}%")
    
    if report['performance']['average_execution_time_ms']:
        print(f"Average execution time: {report['performance']['average_execution_time_ms']:.2f}ms")
    
    print("="*60)

if __name__ == "__main__":
    main() 