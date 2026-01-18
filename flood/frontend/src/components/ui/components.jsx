import React from 'react';

export const Button = ({ children, onClick, disabled, className = '', ...props }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={`px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};

export const Label = ({ children, htmlFor, className = '' }) => {
  return (
    <label htmlFor={htmlFor} className={`block text-sm font-medium text-gray-700 ${className}`}>
      {children}
    </label>
  );
};

export const Select = ({ children, value, onValueChange, ...props }) => {
  return (
    <select
      value={value}
      onChange={(e) => onValueChange(e.target.value)}
      className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
      {...props}
    >
      {children}
    </select>
  );
};

export const SelectContent = ({ children }) => {
  return <>{children}</>;
};

export const SelectItem = ({ value, children }) => {
  return <option value={value}>{children}</option>;
};

export const SelectTrigger = ({ children, ...props }) => {
  return <div {...props}>{children}</div>;
};

export const SelectValue = ({ placeholder }) => {
  return <option value="" disabled>{placeholder}</option>;
};

export const Card = ({ children, className = '' }) => {
  return (
    <div className={`bg-white border border-gray-200 rounded-lg shadow ${className}`}>
      {children}
    </div>
  );
};

export const Badge = ({ children, className = '' }) => {
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${className}`}>
      {children}
    </span>
  );
};