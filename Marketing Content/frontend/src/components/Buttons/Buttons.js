import React from "react";
import PropTypes from 'prop-types'
import './Buttons.css'
import { FaUserCircle, FaRobot } from 'react-icons/fa';
import { HiOutlinePlusCircle, HiCheck } from "react-icons/hi";

const Buttons = ({ onClick, children, variant = 'primary', icon = 'user', color = 'primary' }) => {
    const renderIcon = () => {
        if (icon === 'user') return <FaUserCircle className="btn-icon" />;
        if (icon === 'robot') return <FaRobot className="btn-icon" />;
        if (icon === 'add') return <HiOutlinePlusCircle className="btn-icon" />;
        if (icon === 'check') return <HiCheck className="btn-icon" />;
        return null;
    };
    
    return (
        <button className={`btn btn-${variant} btn-${color} shadow-button`} onClick={onClick}>
            {renderIcon()}
            {children}
        </button>
    );
};

Buttons.propTypes ={
    onClick: PropTypes.func.isRequired,
    children: PropTypes.node.isRequired,
    variant: PropTypes.oneOf(['primary', 'secondary']),
    icon: PropTypes.oneOf(['user', 'robot', 'add', 'check']),
    color: PropTypes.oneOf(['primary-color', 'secondary-color']),
};

export default Buttons;