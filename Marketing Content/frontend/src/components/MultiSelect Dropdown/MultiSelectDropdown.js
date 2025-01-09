import React, { useState } from 'react';
import './MultiSelectDropdown.css';

const MultiSelectDropdown = ({ label, options = [], selectedOptions, setSelectedOptions }) => {
  console.log('Dropdown options:', options);
  console.log('Selected options:', selectedOptions);
  const [isOpen, setIsOpen] = useState(false);

  const toggleDropdown = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (option) => {
    if (selectedOptions.some(selected => selected.id === option.id)) {
      setSelectedOptions(selectedOptions.filter(selected => selected.id !== option.id));
    } else {
      setSelectedOptions([...selectedOptions, option]);
    }
  };

  return (
    <div className="multi-select-dropdown">
      <label>{label}</label>
      <div className={`dropdown-header body-medium-size`} onClick={toggleDropdown}>
        {selectedOptions.length > 0 
          ? selectedOptions.map(opt => opt.name).join(', ') 
          : 'Select audiences'}
        <span className={`arrow ${isOpen ? 'open' : ''}`}>&#9662;</span>
      </div>
      {isOpen && (
        <div className="dropdown-list">
          {options.map(option => (
            <div
              key={option.id}
              className="body-medium-size dropdown-option"
              onClick={() => handleOptionClick(option)}
            >
              <input
                type="checkbox"
                checked={selectedOptions.some(selected => selected.id === option.id)}
                readOnly
              />
              {option.name}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MultiSelectDropdown;
