import React from 'react';

const LoadingOverlay = () => {
  return (
    <div className="loading-overlay">
      <div className="spinner"></div>
      <p>Creating your agent...</p>
    </div>
  );
};

export default LoadingOverlay;