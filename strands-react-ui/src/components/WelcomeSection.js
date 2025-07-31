import React from 'react';

const WelcomeSection = ({ agents, onCreateAgent }) => {
  return (
    <div className="welcome-section">
      <h2>Welcome to KTern.AI Agent Creator</h2>
      <p>Create intelligent AI agents with custom tools and capabilities.</p>
      
      {agents.length > 0 && (
        <>
          <h3 className="agents-heading">Your Agents</h3>
          <div className="agents-container">
            {agents.map((agent, index) => (
              <div key={index} className="agent-widget">
                <div className="agent-header">
                  <h4>{agent.name}</h4>
                  <span className={`agent-status ${agent.status === 'active' ? 'status-active' : 'status-inactive'}`}>
                    {agent.status}
                  </span>
                </div>
                <p className="agent-description">{agent.description}</p>
                <div className="agent-tools">
                  <strong>Tools:</strong> {agent.tools.join(', ')}
                </div>
                <div className="agent-actions">
                  <button className="use-agent-btn" onClick={() => alert(`Using agent: ${agent.name} - This functionality is not implemented yet.`)}>
                    Use Agent
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
      
      <button className="primary-btn" onClick={onCreateAgent}>
        <i className="fas fa-plus-circle"></i> Create New Agent
      </button>
    </div>
  );
};

export default WelcomeSection;