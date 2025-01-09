import React from "react";
import './ImageDisplay.css';

const ImageDisplay = ({ imageUrl, altText, description }) => {
  return (
    <div className="image-container">
      <div className={`title image-title`}>Generated Image</div>
      <img className = "image-display" src={imageUrl} alt={altText} />
      <div className="image-description">
        <div className="input-field-title">Image Description</div>
        <textarea
          className= {`description-textarea body-medium `}
          value={description}
          readOnly
        />
      </div>
    </div>
  );
};

export default ImageDisplay;