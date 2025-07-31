import React from 'react';

const SuccessSection = ({ agent, onCreateAnother }) => {
  return (
    <div className="success-section">
      <div className="success-icon">
        <i className="fas fa-check-circle"></i>
      </div>
      <h2>Agent Created Successfully!</h2>
      <div className="agent-details">
        <p><strong>Name:</strong> {agent?.name}</p>
        <p><strong>Description:</strong> {agent?.description}</p>
        <p><strong>Tools:</strong> {agent?.tools?.join(', ')}</p>
      </div>
      <button className="primary-btn" onClick={onCreateAnother}>
        Create Another Agent
      </button>
    </div>
  );
};

export default SuccessSection;