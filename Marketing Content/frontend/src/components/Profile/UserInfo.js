import React from "react";
import './UserInfo.css';
import { FaRegUser } from 'react-icons/fa';

const UserInfo = ({ imageUrl, userName, userEmail }) => {
  return (
    <div className="container">
      <div className="image-container">
        {imageUrl ? (
          <img src={imageUrl} alt="User" className="image" />
        ) : (
          <div className="placeholder">
              <FaRegUser className="icon" />
          </div>
        )}
      </div>
      <div className="text-container">
        <div className="headline-small">{userName}</div>
        <div className="body-medium">{userEmail}</div>
      </div>
    </div>
  );
};

export default UserInfo;