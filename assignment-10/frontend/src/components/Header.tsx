import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { authApi } from '../api';
import { LogOut, User, Settings, ChevronDown } from 'lucide-react';
import { PasswordChange } from './PasswordChange';

interface HeaderProps {
  onLogout: () => void;
}

export function Header({ onLogout }: HeaderProps) {
  const [showPasswordChange, setShowPasswordChange] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const { data: user, isLoading } = useQuery({
    queryKey: ['user'],
    queryFn: authApi.getCurrentUser,
  });

  const handlePasswordChangeSuccess = () => {
    setShowPasswordChange(false);
    // Optionally show a success message or redirect
  };

  return (
    <>
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">Task Manager</h1>
            </div>
            <div className="flex items-center space-x-4">
              {isLoading ? (
                <div className="animate-pulse bg-gray-200 h-8 w-32 rounded"></div>
              ) : user ? (
                <div className="relative">
                  <button
                    onClick={() => setShowUserMenu(!showUserMenu)}
                    className="flex items-center space-x-2 text-sm text-gray-700 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 rounded-md px-3 py-2"
                  >
                    <User className="h-5 w-5 text-gray-500" />
                    <span>Welcome, {user.username}!</span>
                    <ChevronDown className="h-4 w-4" />
                  </button>
                  
                  {showUserMenu && (
                    <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1 z-10 border border-gray-200">
                      <button
                        onClick={() => {
                          setShowPasswordChange(true);
                          setShowUserMenu(false);
                        }}
                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                      >
                        <Settings className="h-4 w-4 mr-2" />
                        Change Password
                      </button>
                      <button
                        onClick={() => {
                          onLogout();
                          setShowUserMenu(false);
                        }}
                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                      >
                        <LogOut className="h-4 w-4 mr-2" />
                        Logout
                      </button>
                    </div>
                  )}
                </div>
              ) : null}
            </div>
          </div>
        </div>
      </header>

      {/* Password Change Modal */}
      {showPasswordChange && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg shadow-xl max-w-md w-full mx-4">
            <div className="p-6">
              <PasswordChange
                onSuccess={handlePasswordChangeSuccess}
                onCancel={() => setShowPasswordChange(false)}
              />
            </div>
          </div>
        </div>
      )}
    </>
  );
} 