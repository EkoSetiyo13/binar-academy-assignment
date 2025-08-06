// This file contains clean code after fixing all code smells
// This demonstrates quality gate success

import React, { useState, useEffect, useCallback } from 'react';

// Constants instead of magic numbers
const TAX_RATE = 0.08;
const MINOR_AGE = 18;
const SENIOR_AGE = 65;
const MAX_AGE = 150;

// Environment variables for sensitive data
const API_KEY = process.env.REACT_APP_API_KEY || '';
const DATABASE_URL = process.env.REACT_APP_DATABASE_URL || '';

// Types and interfaces
interface UserData {
  name: string;
  email: string;
  age: number;
  phone?: string;
  address?: string;
  city?: string;
  state?: string;
  zipCode?: string;
  country?: string;
  preferences?: Record<string, any>;
  settings?: Record<string, any>;
  metadata?: Record<string, any>;
}

interface ProcessedUserData {
  name: string;
  email: string;
  age: number;
  category: string;
  processedAt: string;
}

// Utility functions
const calculateTax = (price: number): number => {
  return price * TAX_RATE;
};

const validateEmail = (email: string): boolean => {
  return email.includes('@') && email.includes('.');
};

const validateAge = (age: number): boolean => {
  return age > 0 && age < MAX_AGE;
};

const validateName = (name: string): boolean => {
  return Boolean(name && name.trim());
};

const calculateCategory = (age: number): string => {
  if (age < MINOR_AGE) return 'minor';
  if (age < SENIOR_AGE) return 'adult';
  return 'senior';
};

// Class for user validation
class UserValidator {
  static validateEmail(email: string): boolean {
    return validateEmail(email);
  }

  static validateAge(age: number): boolean {
    return validateAge(age);
  }

  static validateName(name: string): boolean {
    return validateName(name);
  }
}

// Class for user processing
class UserProcessor {
  static processUserData(userData: UserData): ProcessedUserData {
    // Validate user data
    if (!UserValidator.validateName(userData.name)) {
      throw new Error('Name is required');
    }
    if (!UserValidator.validateEmail(userData.email)) {
      throw new Error('Email is required');
    }
    if (!UserValidator.validateAge(userData.age)) {
      throw new Error('Valid age is required');
    }

    // Process user data
    return {
      name: userData.name.toUpperCase(),
      email: userData.email.toLowerCase(),
      age: userData.age,
      category: calculateCategory(userData.age),
      processedAt: new Date().toISOString(),
    };
  }
}

// Class for user status determination
class UserStatusDeterminer {
  static determineUserStatus(user: UserData): string {
    const hasValidAge = UserValidator.validateAge(user.age);
    const hasValidName = UserValidator.validateName(user.name);
    const hasValidEmail = UserValidator.validateEmail(user.email);

    if (hasValidAge && hasValidName && hasValidEmail) {
      return 'valid';
    }
    return 'invalid';
  }
}

// Class for safe operations
class SafeOperationHandler {
  static safeDivision(numerator: number, denominator: number): number | null {
    try {
      if (denominator === 0) {
        throw new Error('Division by zero');
      }
      return numerator / denominator;
    } catch (error) {
      console.error('Division error:', error);
      return null;
    }
  }
}

// Class for user creation
class UserCreator {
  static createUser(userData: UserData): Record<string, any> {
    return {
      name: userData.name,
      email: userData.email,
      age: userData.age,
      phone: userData.phone,
      address: userData.address,
      city: userData.city,
      state: userData.state,
      zipCode: userData.zipCode,
      country: userData.country,
      preferences: userData.preferences,
      settings: userData.settings,
      metadata: userData.metadata,
    };
  }
}

// Database manager class
class DatabaseManager {
  static saveToDatabase(data: Record<string, any>): void {
    console.log('Saving to database:', data);
  }

  static sendNotification(data: Record<string, any>): void {
    console.log('Sending notification:', data);
  }
}

// Styled components (instead of inline styles)
const StyledContainer = ({ children }: { children: React.ReactNode }) => (
  <div className="clean-code-container">
    {children}
  </div>
);

const StyledButton = ({ 
  onClick, 
  children 
}: { 
  onClick: () => void; 
  children: React.ReactNode;
}) => (
  <button className="clean-code-button" onClick={onClick}>
    {children}
  </button>
);

const StyledList = ({ items }: { items: string[] }) => (
  <ul className="clean-code-list">
    {items.map((item, index) => (
      <li key={`item-${index}`} className="clean-code-list-item">
        {item}
      </li>
    ))}
  </ul>
);

// Main component
const CleanCodeExample: React.FC = () => {
  const [userData, setUserData] = useState<UserData>({
    name: 'John Doe',
    email: 'john@example.com',
    age: 30,
  });

  const [processedUser, setProcessedUser] = useState<ProcessedUserData | null>(null);
  const [status, setStatus] = useState<string>('');
  const [taxAmount, setTaxAmount] = useState<number>(0);
  const [divisionResult, setDivisionResult] = useState<number | null>(null);

  // Memoized callback to prevent unnecessary re-renders
  const handleProcessUser = useCallback(() => {
    try {
      const processed = UserProcessor.processUserData(userData);
      setProcessedUser(processed);
      
      const userStatus = UserStatusDeterminer.determineUserStatus(userData);
      setStatus(userStatus);
      
      const tax = calculateTax(100);
      setTaxAmount(tax);
      
      const result = SafeOperationHandler.safeDivision(10, 2);
      setDivisionResult(result);
      
      // Simulate database operations
      DatabaseManager.saveToDatabase(processed);
      DatabaseManager.sendNotification(processed);
      
    } catch (error) {
      console.error('Processing error:', error);
    }
  }, [userData]);

  // Effect with proper dependencies
  useEffect(() => {
    handleProcessUser();
  }, [handleProcessUser]);

  const handleUpdateUser = useCallback(() => {
    setUserData(prev => ({
      ...prev,
      name: 'Jane Doe',
      age: 25,
    }));
  }, []);

  const items = ['Clean Code Item 1', 'Clean Code Item 2', 'Clean Code Item 3'];

  return (
    <StyledContainer>
      <h1>Clean Code Example Component</h1>
      <p>This component demonstrates clean code practices</p>
      
      <div className="user-info">
        <h2>User Information</h2>
        <p>Name: {userData.name}</p>
        <p>Email: {userData.email}</p>
        <p>Age: {userData.age}</p>
      </div>

      {processedUser && (
        <div className="processed-info">
          <h2>Processed Information</h2>
          <p>Name: {processedUser.name}</p>
          <p>Email: {processedUser.email}</p>
          <p>Age: {processedUser.age}</p>
          <p>Category: {processedUser.category}</p>
          <p>Processed At: {processedUser.processedAt}</p>
        </div>
      )}

      <div className="calculations">
        <h2>Calculations</h2>
        <p>Status: {status}</p>
        <p>Tax Amount: ${taxAmount.toFixed(2)}</p>
        <p>Division Result: {divisionResult}</p>
      </div>

      <StyledList items={items} />

      <div className="actions">
        <StyledButton onClick={handleUpdateUser}>
          Update User
        </StyledButton>
        <StyledButton onClick={handleProcessUser}>
          Process User
        </StyledButton>
      </div>
    </StyledContainer>
  );
};

export default CleanCodeExample; 