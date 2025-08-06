// This file contains intentional code smells to demonstrate SonarCloud quality gate failure
// This should be removed after testing

import React, { useState, useEffect } from 'react';

// Code Smell 1: Unused imports
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

// Code Smell 2: Hardcoded values (security issue)
const API_KEY = "sk-1234567890abcdef"; // Hardcoded API key
const DATABASE_URL = "https://api.example.com/db"; // Hardcoded URL

// Code Smell 3: Magic numbers
const calculateTax = (price: number): number => {
  return price * 0.08; // Magic number 0.08 should be a constant
};

// Code Smell 4: Long function with too many responsibilities
const processUserData = (userData: any): any => {
  // This function does too many things - violates Single Responsibility Principle
  
  // Validate user data
  if (!userData.name || !userData.email || !userData.age) {
    throw new Error("Missing required fields");
  }
  
  // Process user data
  const processedData = {
    name: userData.name.toUpperCase(),
    email: userData.email.toLowerCase(),
    age: parseInt(userData.age),
    category: userData.age < 18 ? 'minor' : userData.age < 65 ? 'adult' : 'senior',
    processedAt: new Date().toISOString()
  };
  
  // Log the processing
  console.log(`Processed user: ${processedData.name}`);
  
  // Save to database (simulated)
  saveToDatabase(processedData);
  
  // Send notification (simulated)
  sendNotification(processedData);
  
  return processedData;
};

// Code Smell 5: Empty function
const emptyFunction = (): void => {
  // This function does nothing
};

// Code Smell 6: Duplicate code
const validateEmail = (email: string): boolean => {
  return email.includes('@') && email.includes('.');
};

const validateEmailDuplicate = (email: string): boolean => { // Duplicate of above function
  return email.includes('@') && email.includes('.');
};

// Code Smell 7: Dead code
const unusedFunction = (): string => {
  return "This function is never called";
};

// Code Smell 8: Inconsistent naming
const getUserData = (): any => { // Should be camelCase
  return { name: "John", age: 30 };
};

const process_user_data_2 = (userData: any): any => { // Should be camelCase
  return userData;
};

// Code Smell 9: Complex conditional
const determineUserStatus = (user: any): string => {
  if (user.age && user.age > 0 && user.age < 150 && user.name && user.name.length > 0 && user.email && user.email.includes('@') && user.email.includes('.')) {
    return "valid";
  } else {
    return "invalid";
  }
};

// Code Smell 10: Exception handling without specific exception
const riskyOperation = (): any => {
  try {
    const result = 10 / 0;
    return result;
  } catch { // Should catch specific exceptions
    return null;
  }
};

// Code Smell 11: Global variable
let globalCounter = 0;

const incrementCounter = (): number => {
  globalCounter += 1;
  return globalCounter;
};

// Code Smell 12: Long parameter list
const createUser = (
  name: string,
  email: string,
  age: number,
  phone: string,
  address: string,
  city: string,
  state: string,
  zipCode: string,
  country: string,
  preferences: any,
  settings: any,
  metadata: any
): any => {
  // Too many parameters - should use an interface or object
  return {
    name,
    email,
    age,
    phone,
    address,
    city,
    state,
    zipCode,
    country,
    preferences,
    settings,
    metadata
  };
};

// Code Smell 13: Unused variables
const unusedVariable = "This variable is never used";

// Code Smell 14: Console statements in production code
const debugFunction = (): void => {
  console.log("Debug information");
  console.error("Error message");
  console.warn("Warning message");
};

// Code Smell 15: Inline styles
const inlineStyleComponent = (): JSX.Element => {
  return (
    <div style={{ 
      backgroundColor: 'red', 
      color: 'white', 
      padding: '10px', 
      margin: '5px',
      border: '1px solid black',
      borderRadius: '5px',
      fontSize: '14px',
      fontWeight: 'bold',
      textAlign: 'center',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '50px'
    }}>
      Inline styles are bad practice
    </div>
  );
};

// Code Smell 16: Any type usage
const anyTypeFunction = (data: any): any => {
  return data;
};

// Code Smell 17: Unused parameters
const unusedParameterFunction = (unusedParam: string, usedParam: string): string => {
  return usedParam; // unusedParam is never used
};

// Code Smell 18: Nested ternary operators
const complexTernary = (user: any): string => {
  return user.age < 18 ? 'minor' : user.age < 65 ? 'adult' : user.age < 80 ? 'senior' : 'elderly';
};

// Code Smell 19: Direct DOM manipulation
const directDomManipulation = (): void => {
  const element = document.getElementById('myElement');
  if (element) {
    element.innerHTML = 'Direct DOM manipulation';
    element.style.color = 'red';
  }
};

// Code Smell 20: Missing key prop in list
const listWithoutKeys = (): JSX.Element => {
  const items = ['item1', 'item2', 'item3'];
  return (
    <ul>
      {items.map(item => (
        <li>{item}</li> // Missing key prop
      ))}
    </ul>
  );
};

// Helper functions (these are fine)
const saveToDatabase = (data: any): void => {
  // Simulated database save
  console.log('Saving to database:', data);
};

const sendNotification = (data: any): void => {
  // Simulated notification
  console.log('Sending notification:', data);
};

// Main component with code smells
const CodeSmellExample: React.FC = () => {
  const [state, setState] = useState<any>(null);
  
  // Code Smell: useEffect with missing dependency
  useEffect(() => {
    setState({ name: 'John', age: 30 });
  }, []); // Missing dependency array or missing dependencies
  
  // Code Smell: Unused state
  const [unusedState, setUnusedState] = useState<string>('');
  
  // Code Smell: Direct state mutation
  const updateState = (): void => {
    state.name = 'Jane'; // Direct mutation instead of using setState
  };
  
  return (
    <div>
      <h1>Code Smell Example Component</h1>
      <p>This component contains intentional code smells for testing</p>
      {inlineStyleComponent()}
      {listWithoutKeys()}
      <button onClick={updateState}>Update State (Wrong Way)</button>
      <button onClick={debugFunction}>Debug Function</button>
    </div>
  );
};

export default CodeSmellExample; 