import React, { useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import './App.css';
import Home from './pages/Home/Home';
import Profile from './pages/Profile/Profile';
import SetUpCompany from './pages/Set Up Company/SetUpCompany';
import GenerateContent from './pages/Content Generator/GenerateContent';

const AppContent = () => {
  const location = useLocation();

  useEffect(() => {
    // Function to update body class based on route
    const updateBodyClass = () => {
      if (location.pathname === '/set-up-company' || location.pathname === '/generate-content') {
        document.body.classList.add('company-setup-background');
      } else {
        document.body.classList.remove('company-setup-background');
      }
    };

    updateBodyClass();

    // Clean up function
    return () => {
      document.body.classList.remove('company-setup-background');
    };
  }, [location]);

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/set-up-company" element={<SetUpCompany />} />
      <Route path="/generate-content" element={<GenerateContent />} />
    </Routes>
  );
};

const App = () => (
  <Router>
    <AppContent />
  </Router>
);

export default App;
