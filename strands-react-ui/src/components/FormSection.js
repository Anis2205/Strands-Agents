import React, { useState } from 'react';

const FormSection = ({ onSubmit, onCancel }) => {
  const [agentName, setAgentName] = useState('');
  const [agentDescription, setAgentDescription] = useState('');
  const [standardTools, setStandardTools] = useState([]);
  const [customTools, setCustomTools] = useState([]);

  const handleStandardToolChange = (tool, checked) => {
    if (checked) {
      setStandardTools([...standardTools, tool]);
    } else {
      setStandardTools(standardTools.filter(t => t !== tool));
    }
  };

  const addCustomTool = () => {
    setCustomTools([...customTools, { name: '', description: '' }]);
  };

  const removeCustomTool = (index) => {
    setCustomTools(customTools.filter((_, i) => i !== index));
  };

  const updateCustomTool = (index, field, value) => {
    const updated = customTools.map((tool, i) => 
      i === index ? { ...tool, [field]: value } : tool
    );
    setCustomTools(updated);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validCustomTools = customTools.filter(tool => tool.name && tool.description);
    
    onSubmit({
      name: agentName,
      description: agentDescription,
      standardTools,
      customTools: validCustomTools
    });
  };

  return (
    <div className="form-section">
      <h2>Create Your Agent</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="agent-name">Agent Name</label>
          <input
            type="text"
            id="agent-name"
            value={agentName}
            onChange={(e) => setAgentName(e.target.value)}
            placeholder="Enter agent name"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="agent-description">Agent Description</label>
          <textarea
            id="agent-description"
            value={agentDescription}
            onChange={(e) => setAgentDescription(e.target.value)}
            placeholder="Describe what your agent does"
            required
          />
        </div>

        <div className="form-group">
          <label>Select Tools</label>
          <div className="tools-container">
            <div className="standard-tools">
              <h3>Standard Tools</h3>
              <div className="checkbox-group">
                {['http_request', 'file_read', 'file_write', 'search', 'browse'].map(tool => (
                  <div key={tool} className="checkbox-item">
                    <input
                      type="checkbox"
                      id={tool}
                      onChange={(e) => handleStandardToolChange(tool, e.target.checked)}
                    />
                    <label htmlFor={tool}>{tool.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}</label>
                  </div>
                ))}
              </div>
            </div>

            <div className="custom-tools">
              <h3>Custom Tools</h3>
              <div className="custom-tools-container">
                {customTools.map((tool, index) => (
                  <div key={index} className="custom-tool">
                    <div className="form-group">
                      <label>Tool Name</label>
                      <input
                        type="text"
                        value={tool.name}
                        onChange={(e) => updateCustomTool(index, 'name', e.target.value)}
                        placeholder="Enter tool name"
                        required
                      />
                    </div>
                    <div className="form-group">
                      <label>Tool Description</label>
                      <textarea
                        value={tool.description}
                        onChange={(e) => updateCustomTool(index, 'description', e.target.value)}
                        placeholder="Describe what this tool does"
                        required
                      />
                    </div>
                    <button
                      type="button"
                      className="remove-tool-btn"
                      onClick={() => removeCustomTool(index)}
                    >
                      <i className="fas fa-trash"></i> Remove
                    </button>
                  </div>
                ))}
              </div>
              <button type="button" className="secondary-btn" onClick={addCustomTool}>
                <i className="fas fa-plus"></i> Add Custom Tool
              </button>
            </div>
          </div>
        </div>

        <div className="form-actions">
          <button type="button" className="cancel-btn" onClick={onCancel}>
            Cancel
          </button>
          <button type="submit" className="primary-btn">
            Create Agent
          </button>
        </div>
      </form>
    </div>
  );
};

export default FormSection;