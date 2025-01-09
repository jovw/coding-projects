import React, { useEffect, useState } from "react";
import './Header.css';
import Buttons from "../Buttons/Buttons";
import { useNavigate } from 'react-router-dom';

const Header = ({ isLoggedIn }) => {
  const navigate = useNavigate();
  const [loggedIn, setLoggedIn] = useState(isLoggedIn);

  useEffect(() => {
    const accessToken = document.cookie.split('; ').find(row => row.startsWith('access_token='));
    if (accessToken) {
      setLoggedIn(true);
    }
  }, []);

  const handleLogin = () => {
    window.location.href = 'http://localhost:8080/auth/google/login';
  };

  const handleOnClickProfile = () => {
    navigate('/profile', { state: { companySetup: false } });
  };

  const handleOnClickGenerate = () => {
    navigate('/generate-content');
  };

  return (
    <div className="header-container">
      <div className="header-title">
        <div className="web-header">Marketing Content Generator</div>
      </div>
      <div className="header-buttons">
        {isLoggedIn ? (
          <>
            <Buttons onClick={handleLogin} variant="primary" icon="user" color="primary-color">
              Login
            </Buttons>
          </>
        ) : (
          <>
            <Buttons onClick={handleOnClickGenerate} variant="primary" icon="robot" color="secondary-color">
              Generate
            </Buttons>

            <Buttons onClick={handleOnClickProfile} variant="primary" icon="user" color="primary-color">
              Jo van Wyk
            </Buttons>
          </>

        )}
      </div>
    </div>
  );
}

export default Header;
