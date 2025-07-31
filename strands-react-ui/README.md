# Strands Agent Creator - React UI

A modern React-based web interface for creating and managing Strands agents with custom tools and capabilities.

## Technologies Used

- **Frontend**: React 18, JavaScript (ES6+), CSS3
- **HTTP Client**: Axios
- **Backend**: Python Flask (separate server)
- **Database**: MongoDB (Cloud Atlas)
- **AI/ML**: AWS Bedrock (Claude 3.7 Sonnet)

## Prerequisites

- Node.js 16+ and npm
- Python Flask backend server running on port 5000
- All backend requirements (AWS Bedrock, MongoDB, etc.)

## Installation

1. **Install dependencies:**
```bash
npm install
```

2. **Start the React development server:**
```bash
npm start
```

3. **Ensure backend is running:**
```bash
# In the backend directory
python server.py
```

The React app will run on `http://localhost:3000` and communicate with the Flask backend on `http://localhost:5000`.

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm run build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm run eject` - Ejects from Create React App (one-way operation)

## Features

- Modern React component architecture
- Responsive design
- Real-time form validation
- Loading states and error handling
- Component-based UI structure

## Project Structure

```
src/
├── components/
│   ├── WelcomeSection.js
│   ├── FormSection.js
│   ├── SuccessSection.js
│   └── LoadingOverlay.js
├── styles/
│   └── App.css
├── App.js
└── index.js
```