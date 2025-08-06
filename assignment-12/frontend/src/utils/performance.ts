import React from 'react';

// Performance monitoring utilities
export class PerformanceMonitor {
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

// Performance HOC for React components
export const withPerformanceMonitoring = <P extends Record<string, unknown>>(
  Component: React.ComponentType<P>,
  componentName: string
): React.ComponentType<P> => {
  const WrappedComponent = React.memo((props: P) => {
    React.useEffect(() => {
      PerformanceMonitor.startTimer(`${componentName} render`);
      return () => {
        PerformanceMonitor.endTimer(`${componentName} render`);
      };
    });

    return React.createElement(Component, props);
  });

  WrappedComponent.displayName = `withPerformanceMonitoring(${componentName})`;
  return WrappedComponent;
}; 