import React from 'react';
import './LoadingPage.css';

const LoadingPage = () => {
  return (
    <div className="loading-page">
      <video className="loading-video" autoPlay loop muted>
        <source src="frontend/public/loading-video.mp4" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <div className="loading-text">Loading...</div>
    </div>
  );
};

export default LoadingPage;