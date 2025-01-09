import React, { useEffect } from "react";
import './InputDropdown.css';

const InputDropdown = ({ label, options, onChange }) => {
  // useEffect(() => {
  //   console.log('Dropdown options:', options); // Debugging
  // }, [options]);

  const handleChange = (event) => {
    const selectedValue = event.target.value;
    // console.log('Selected value from dropdown:', selectedValue); // Debugging
  
    const selectedOption = options.find(option => {
      return typeof option.value === 'number'
        ? option.value === parseInt(selectedValue, 10)
        : option.value === selectedValue;
    });
  
    // console.log('Matched option:', selectedOption); // Debugging
  
    if (selectedOption) {
      onChange(selectedOption);
    } else {
      console.error('Selected option not found in the options list');
    }
  };
  

  return (
    <div className="dropdown-group">
      <label className="input-field-title input-spacing">{label}</label>
      <select className="input-bar input-dropdown" onChange={handleChange}>
        <option value="">Select an option</option>
        {options.map((option, index) => (
          <option key={index} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export default InputDropdown;
