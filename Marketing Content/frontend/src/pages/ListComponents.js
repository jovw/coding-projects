import React from 'react';
import Buttons from '../components/Buttons/Buttons';
import UserInfo from '../components/Profile/UserInfo';
import BusinessInfo from '../components/Profile/BusinessInfo';
import Header from '../components/Header/Header';
import InputField from '../components/Input Fields/InputField'
import ContentTable from '../components/Tables/ContentTables';



const ListComponents = () => {
  const handleClick = () => {
    console.log('Button clicked!');
  };

  /* Example inputs array for InputField component */
  const inputs = [
    { label: 'Company Name', type: 'text', placeholder: 'Enter your company name.' },
    { label: 'Company Description', type: 'text', placeholder: 'Enter your company description.' },
  ];

  const tableColumns = ['Product Name', 'Product Description'];
  const tableRows = [
    ['Product 1', 'Product 1 Description'],
    ['Product 2', 'Product 2 Description'],
    ['Product 3', 'Product 3 Description'],
  ];

  return (
    <div className="App">
      <main className="App-main">
        <h1>List of Components</h1>
        
        <Header />
        <Header isLoggedIn="true"/>

        <h2>Text Title</h2>
        <div className="display">Display</div>
        <div className="headline-small">Headline</div>
        <div className="title">Form Titles</div>
        <div className="body-medium">Content Body</div>
        <div className="input-field-title">Input Field Titles</div>

        {/* Primary Button with User Icon */}
        <h2>Primary Button</h2>
        <Buttons onClick={handleClick} variant="primary" icon="user" color="primary-color">
          Login
        </Buttons>
        <br /><br />

        {/* Primary Button with Robot Icon */}
        <Buttons onClick={handleClick} variant="primary" icon="robot" color="secondary-color">
          Generate
        </Buttons>

        <h2>Secondary Button</h2>
        {/* Secondary Button with Plus icon */}
        <Buttons onClick={handleClick} variant="secondary" icon="add" color="secondary-color">
          Set up your company
        </Buttons>
        <br /><br />

        {/* Secondary Button with Check icon */}
        <Buttons onClick={handleClick} variant="secondary" icon="check" color="secondary-color">
          Submit Company info
        </Buttons>

        <h2>User Info</h2>
        {/* User Info with no image */}
        <UserInfo userName="Jo van Wyk" userEmail="jo@vanwyks.net"/>
        <br /><br />

        {/* Use Info with an image */}
        <UserInfo userName="Jo van Wyk" userEmail="jo@vanwyks.net" imageUrl="https://images.unsplash.com/photo-1573865526739-10659fec78a5?q=80&w=1015&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"/>

        <h2>Business Info</h2>
        {/* Business Info */}
        <BusinessInfo 
          companyTitle="Little Leaf Nursery"
          companyDescription="Little Leaf Nursery specializes in cultivating a wide variety of premium indoor and outdoor plants. With a passion for sustainability and quality, we provide lush greenery and floral delights to enhance any environment."
        />

        <h2>Input Field</h2>
        {/* Input Field */}
        <InputField 
          title = "Company Information"
          inputs = {inputs}
        />

        <h2>Content Table</h2>
        {/* Content Table */}
        <ContentTable 
        tableTitle="Products" 
        columns={tableColumns} 
        rows={tableRows} 
        />

      </main>
    </div>
  );
};

export default ListComponents;
