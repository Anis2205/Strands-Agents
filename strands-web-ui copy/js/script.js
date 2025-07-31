document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded and parsed');
    
    // DOM Elements
    const welcomeSection = document.getElementById('welcome-section');
    const formSection = document.getElementById('form-section');
    const successSection = document.getElementById('success-section');
    const createAgentBtn = document.getElementById('create-agent-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const agentForm = document.getElementById('agent-form');
    const addCustomToolBtn = document.getElementById('add-custom-tool');
    const customToolsContainer = document.getElementById('custom-tools-container');
    const customToolTemplate = document.getElementById('custom-tool-template');
    const createAnotherBtn = document.getElementById('create-another-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    
    // Ensure loading overlay is hidden on page load
    loadingOverlay.classList.add('hidden');
    loadingOverlay.style.display = 'none';
    
    // Fetch and display existing agents when the page loads
    fetchAgents();
    
    console.log('Elements initialized:', {
        welcomeSection: !!welcomeSection,
        formSection: !!formSection,
        successSection: !!successSection,
        createAgentBtn: !!createAgentBtn,
        cancelBtn: !!cancelBtn,
        agentForm: !!agentForm,
        addCustomToolBtn: !!addCustomToolBtn,
        customToolsContainer: !!customToolsContainer,
        customToolTemplate: !!customToolTemplate,
        createAnotherBtn: !!createAnotherBtn,
        loadingOverlay: !!loadingOverlay
    });

    // Success section elements
    const successAgentName = document.getElementById('success-agent-name');
    const successAgentDescription = document.getElementById('success-agent-description');
    const successAgentTools = document.getElementById('success-agent-tools');

    // Counter for custom tool IDs
    let customToolCounter = 0;

    // Event Listeners
    createAgentBtn.addEventListener('click', showFormSection);
    cancelBtn.addEventListener('click', showWelcomeSection);
    addCustomToolBtn.addEventListener('click', addCustomTool);
    agentForm.addEventListener('submit', handleFormSubmit);
    createAnotherBtn.addEventListener('click', function() {
        showWelcomeSection();
        fetchAgents(); // Refresh the agents list
    });

    // Functions
    function showWelcomeSection() {
        welcomeSection.classList.remove('hidden');
        formSection.classList.add('hidden');
        successSection.classList.add('hidden');
        // Reset form
        agentForm.reset();
        customToolsContainer.innerHTML = '';
        customToolCounter = 0;
    }

    function showFormSection() {
        console.log('showFormSection called');
        console.log('Before: welcomeSection hidden:', welcomeSection.classList.contains('hidden'));
        console.log('Before: formSection hidden:', formSection.classList.contains('hidden'));
        
        welcomeSection.classList.add('hidden');
        formSection.classList.remove('hidden');
        successSection.classList.add('hidden');
        
        console.log('After: welcomeSection hidden:', welcomeSection.classList.contains('hidden'));
        console.log('After: formSection hidden:', formSection.classList.contains('hidden'));
    }

    function showSuccessSection(agentData) {
        welcomeSection.classList.add('hidden');
        formSection.classList.add('hidden');
        successSection.classList.remove('hidden');
        
        // Update success section with agent details
        successAgentName.textContent = agentData.name;
        successAgentDescription.textContent = agentData.description;
        successAgentTools.textContent = agentData.tools.join(', ');
    }

    function addCustomTool() {
        const toolId = customToolCounter++;
        const toolHtml = customToolTemplate.innerHTML
            .replace(/{id}/g, toolId)
            .replace('custom-tool-template', '');
        
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = toolHtml;
        const customToolElement = tempDiv.firstElementChild;
        
        // Add event listener to remove button
        const removeBtn = customToolElement.querySelector('.remove-tool-btn');
        removeBtn.addEventListener('click', function() {
            customToolElement.remove();
        });
        
        customToolsContainer.appendChild(customToolElement);
    }

    async function handleFormSubmit(event) {
        event.preventDefault();
        
        // Show loading overlay
        loadingOverlay.classList.remove('hidden');
        loadingOverlay.style.display = 'flex';
        
        // Get form data
        const agentName = document.getElementById('agent-name').value;
        const agentDescription = document.getElementById('agent-description').value;
        
        // Get selected standard tools
        const standardTools = [];
        document.querySelectorAll('.standard-tools input[type="checkbox"]:checked').forEach(checkbox => {
            standardTools.push(checkbox.value);
        });
        
        // Get custom tools
        const customTools = [];
        document.querySelectorAll('.custom-tool').forEach(toolElement => {
            const nameInput = toolElement.querySelector('input[name="custom-tool-name"]');
            const descriptionInput = toolElement.querySelector('textarea[name="custom-tool-description"]');
            
            if (nameInput && nameInput.value && descriptionInput && descriptionInput.value) {
                customTools.push({
                    name: nameInput.value,
                    description: descriptionInput.value
                });
            }
        });
        
        // Prepare data for API
        const agentData = {
            name: agentName,
            description: agentDescription,
            standardTools: standardTools,
            customTools: customTools
        };
        
        try {
            // Call the backend API
            const response = await createAgent(agentData);
            
            // Hide loading overlay
            loadingOverlay.classList.add('hidden');
            loadingOverlay.style.display = 'none';
            
            // Show success section
            showSuccessSection({
                name: agentName,
                description: agentDescription,
                tools: [...standardTools, ...customTools.map(tool => tool.name)]
            });
        } catch (error) {
            console.error('Error creating agent:', error);
            alert('An error occurred while creating the agent. Please try again.');
            loadingOverlay.classList.add('hidden');
            loadingOverlay.style.display = 'none';
        }
    }

    async function createAgent(agentData) {
        // Make a POST request to the backend
        const response = await fetch('/api/create-agent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(agentData)
        });
        
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        return response.json();
    }
    
    async function fetchAgents() {
        try {
            const response = await fetch('/api/agents');
            if (!response.ok) {
                throw new Error('Failed to fetch agents');
            }
            
            const data = await response.json();
            if (data.success && data.agents && data.agents.length > 0) {
                displayAgents(data.agents);
            } else {
                console.log('No agents found or empty response');
            }
        } catch (error) {
            console.error('Error fetching agents:', error);
        }
    }
    
    function displayAgents(agents) {
        // Create agents container if it doesn't exist
        let agentsContainer = document.querySelector('.agents-container');
        if (!agentsContainer) {
            agentsContainer = document.createElement('div');
            agentsContainer.className = 'agents-container';
            
            // Add a heading
            const heading = document.createElement('h3');
            heading.textContent = 'Your Agents';
            heading.className = 'agents-heading';
            
            // Insert the heading and container before the create button
            welcomeSection.insertBefore(heading, createAgentBtn);
            welcomeSection.insertBefore(agentsContainer, createAgentBtn);
        } else {
            // Clear existing agents
            agentsContainer.innerHTML = '';
        }
        
        // Create agent widgets
        agents.forEach(agent => {
            const agentWidget = document.createElement('div');
            agentWidget.className = 'agent-widget';
            
            const statusClass = agent.status === 'active' ? 'status-active' : 'status-inactive';
            
            agentWidget.innerHTML = `
                <div class="agent-header">
                    <h4>${agent.name}</h4>
                    <span class="agent-status ${statusClass}">${agent.status}</span>
                </div>
                <p class="agent-description">${agent.description}</p>
                <div class="agent-tools">
                    <strong>Tools:</strong> ${agent.tools.join(', ')}
                </div>
                <div class="agent-actions">
                    <button class="use-agent-btn" data-agent-name="${agent.name}">Use Agent</button>
                </div>
            `;
            
            agentsContainer.appendChild(agentWidget);
        });
        
        // Add event listeners to the "Use Agent" buttons
        document.querySelectorAll('.use-agent-btn').forEach(button => {
            button.addEventListener('click', function() {
                const agentName = this.getAttribute('data-agent-name');
                alert(`Using agent: ${agentName} - This functionality is not implemented yet.`);
            });
        });
    }
});
