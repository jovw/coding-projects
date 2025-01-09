import React from "react";
import './BusinessInfo.css';

const BusinessInfo = ({ companyTitle, companyDescription}) => {
    return (
        <div className="business-container">
            <div className="headline-small">{companyTitle}</div>
            <div className="body-medium">{companyDescription}</div>
        </div>
    );
};

export default BusinessInfo;