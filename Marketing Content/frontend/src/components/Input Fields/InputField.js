import React from 'react';
import './InputField.css';

const InputFields = ({ title, inputs }) => {
  return (
    <div className="input-fields-container">
      <div className = {`title title-spacing`}>{title}</div>
      {inputs.map((input, index) => (
        <div key={index} className={`body-medium input-group`}>
          <label className={`input-field-title input-spacing`}>{input.label}</label>
          {index === 0 ? (
            <input 
              type={input.type || 'text'} 
              placeholder={input.placeholder} 
              className="input-bar"
              value={input.value}
              onChange={input.onChange} />
          ) : (
            <textarea 
              placeholder={input.placeholder} 
              className="input-bar"
              value={input.value}
              onChange={input.onChange} />
          )}
        </div>
      ))}
    </div>
  );
};

export default InputFields;
