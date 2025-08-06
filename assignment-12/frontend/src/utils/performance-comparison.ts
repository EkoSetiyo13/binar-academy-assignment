// Performance comparison utilities for demonstrating refactoring benefits
export class PerformanceComparison {
  private static measurements: Map<string, number[]> = new Map();

  static recordMeasurement(label: string, duration: number): void {
    if (!this.measurements.has(label)) {
      this.measurements.set(label, []);
    }
    this.measurements.get(label)!.push(duration);
  }

  static getAverageTime(label: string): number {
    const measurements = this.measurements.get(label);
    if (!measurements || measurements.length === 0) {
      return 0;
    }
    return measurements.reduce((sum, time) => sum + time, 0) / measurements.length;
  }

  static getMinTime(label: string): number {
    const measurements = this.measurements.get(label);
    if (!measurements || measurements.length === 0) {
      return 0;
    }
    return Math.min(...measurements);
  }

  static getMaxTime(label: string): number {
    const measurements = this.measurements.get(label);
    if (!measurements || measurements.length === 0) {
      return 0;
    }
    return Math.max(...measurements);
  }

  static generateReport(): void {
    console.log('📊 Performance Comparison Report');
    console.log('================================');
    
    for (const [label, measurements] of this.measurements.entries()) {
      const avg = this.getAverageTime(label);
      const min = this.getMinTime(label);
      const max = this.getMaxTime(label);
      const count = measurements.length;
      
      console.log(`\n🔍 ${label}:`);
      console.log(`   Count: ${count} measurements`);
      console.log(`   Average: ${avg.toFixed(2)}ms`);
      console.log(`   Min: ${min.toFixed(2)}ms`);
      console.log(`   Max: ${max.toFixed(2)}ms`);
      console.log(`   Range: ${(max - min).toFixed(2)}ms`);
    }
  }

  static compareBeforeAfter(beforeLabel: string, afterLabel: string): void {
    const beforeAvg = this.getAverageTime(beforeLabel);
    const afterAvg = this.getAverageTime(afterLabel);
    
    if (beforeAvg === 0 || afterAvg === 0) {
      console.log('⚠️  Not enough data for comparison');
      return;
    }

    const improvement = ((beforeAvg - afterAvg) / beforeAvg) * 100;
    const isFaster = improvement > 0;
    
    console.log(`\n⚡ Performance Comparison: ${beforeLabel} vs ${afterLabel}`);
    console.log(`   Before: ${beforeAvg.toFixed(2)}ms`);
    console.log(`   After:  ${afterAvg.toFixed(2)}ms`);
    console.log(`   ${isFaster ? '✅' : '❌'} ${Math.abs(improvement).toFixed(1)}% ${isFaster ? 'faster' : 'slower'}`);
  }

  static clearMeasurements(): void {
    this.measurements.clear();
  }
}

// Enhanced performance monitor with comparison capabilities
export class EnhancedPerformanceMonitor {
  private static timers: Map<string, number> = new Map();

  static startTimer(label: string): void {
    console.time(`⏱️ ${label}`);
    this.timers.set(label, performance.now());
  }

  static endTimer(label: string): void {
    console.timeEnd(`⏱️ ${label}`);
    const startTime = this.timers.get(label);
    if (startTime) {
      const duration = performance.now() - startTime;
      console.log(`📊 ${label} took ${duration.toFixed(2)}ms`);
      PerformanceComparison.recordMeasurement(label, duration);
      this.timers.delete(label);
    }
  }

  static measureAsync<T>(label: string, fn: () => Promise<T>): Promise<T> {
    this.startTimer(label);
    return fn().finally(() => this.endTimer(label));
  }

  static measureSync<T>(label: string, fn: () => T): T {
    this.startTimer(label);
    try {
      const result = fn();
      this.endTimer(label);
      return result;
    } catch (error) {
      this.endTimer(label);
      throw error;
    }
  }
} 