import React, { useState, useEffect } from 'react';
import axios from 'axios';
import WelcomeSection from './components/WelcomeSection';
import FormSection from './components/FormSection';
import SuccessSection from './components/SuccessSection';
import LoadingOverlay from './components/LoadingOverlay';

const API_BASE_URL = 'http://localhost:5000';

function App() {
  const [currentSection, setCurrentSection] = useState('welcome');
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(false);
  const [createdAgent, setCreatedAgent] = useState(null);

  useEffect(() => {
    fetchAgents();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/agents`);
      if (response.data.success) {
        setAgents(response.data.agents);
      }
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const createAgent = async (agentData) => {
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/create-agent`, agentData);
      if (response.data.success) {
        setCreatedAgent(response.data.agent);
        setCurrentSection('success');
        fetchAgents();
      }
    } catch (error) {
      console.error('Error creating agent:', error);
      alert('An error occurred while creating the agent. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const showWelcome = () => {
    setCurrentSection('welcome');
    setCreatedAgent(null);
  };

  const showForm = () => {
    setCurrentSection('form');
  };

  return (
    <div className="container">
      <header>
        <h1><i className="fas fa-robot"></i> KTern.AI Agent Creator</h1>
        <p>Create custom AI agents with powerful tools</p>
      </header>

      <main>
        {currentSection === 'welcome' && (
          <WelcomeSection 
            agents={agents} 
            onCreateAgent={showForm}
          />
        )}
        
        {currentSection === 'form' && (
          <FormSection 
            onSubmit={createAgent}
            onCancel={showWelcome}
          />
        )}
        
        {currentSection === 'success' && (
          <SuccessSection 
            agent={createdAgent}
            onCreateAnother={showWelcome}
          />
        )}
      </main>

      <footer>
        <p>&copy; 2025 KTern.AI Agent Creator | Powered by Strands Framework</p>
      </footer>

      {loading && <LoadingOverlay />}
    </div>
  );
}

export default App;