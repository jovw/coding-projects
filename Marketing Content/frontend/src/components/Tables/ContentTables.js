import React from 'react';
import './ContentTables.css';

const ContentTable = ({ tableTitle, columns, rows }) => {
  return (
    <div className="content-table-container">
      <div className = {`headline-small content-table-title`}>{tableTitle}</div>
      <table className= "content-table">
        <thead class = "body-medium" >
          <tr>
            {columns.map((column, index) => (
              <th class = "column-titles" key={index}>{column}</th>
            ))}
          </tr>
        </thead>
        <tbody class = "body-medium">
          {rows.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContentTable;
