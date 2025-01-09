import React, { useState, useEffect } from 'react';
import './SetUpCompany.css';
import Header from '../../components/Header/Header';
import Buttons from '../../components/Buttons/Buttons';
import { useNavigate } from 'react-router-dom';
import InputFields from '../../components/Input Fields/InputField';
import ContentTable from '../../components/Tables/ContentTables';
import useFetchProfileData from '../../hooks/useFetchProfileData';
import axios from 'axios';
import { getCookie } from '../../utils/cookies';

const SetUpCompany = () => {
  const { companyInfo, productData, audienceData, loading } = useFetchProfileData();
  const [newProductData, setNewProductData] = useState([]);
  const [newAudienceData, setNewAudienceData] = useState([]);
  const [productName, setProductName] = useState('');
  const [productDescription, setProductDescription] = useState('');
  const [audienceName, setAudienceName] = useState('');
  const [audienceDescription, setAudienceDescription] = useState('');
  const [companyName, setCompanyName] = useState(companyInfo?.companyName || '');
  const [companyDescription, setCompanyDescription] = useState(companyInfo?.companyDescription || '');

  const navigate = useNavigate();
  const goToProfile = () => navigate('/profile', { state: { companySetup: true } });

  useEffect(() => {
    setCompanyName(companyInfo?.companyName || '');
    setCompanyDescription(companyInfo?.companyDescription || '');
  }, [companyInfo]);

  const handleAdd = (type) => {
    const name = type === 'product' ? productName : audienceName;
    const description = type === 'product' ? productDescription : audienceDescription;
    if (name.trim() && description.trim()) {
      if (type === 'product') {
        setNewProductData([...newProductData, { productName: name, productDescription: description }]);
        setProductName('');
        setProductDescription('');
      } else {
        setNewAudienceData([...newAudienceData, { audienceName: name, audienceDescription: description }]);
        setAudienceName('');
        setAudienceDescription('');
      }
    } else {
      alert('Both name and description are required.');
    }
  };

  const handleSubmit = async () => {
    try {
      const accessToken = getCookie('access_token');
      const idToken = getCookie('id_token');
      if (!accessToken || !idToken) {
        console.error('Access token or ID token is missing.');
        return;
      }

      const headers = {
        Authorization: `Bearer ${accessToken}`,
        idToken: `Bearer ${idToken}`
      };

      await axios.post('http://localhost:8080/users/company', { companyName, companyDescription }, { headers, withCredentials: true });

      const newProducts = newProductData.filter(newProduct =>
        !productData.some(existingProduct => existingProduct.productName === newProduct.productName)
      );
      const newAudiences = newAudienceData.filter(newAudience =>
        !audienceData.some(existingAudience => existingAudience.audienceName === newAudience.audienceName)
      );

      await Promise.all([
        ...newProducts.map(product =>
          axios.post('http://localhost:8080/users/products', product, { headers, withCredentials: true })
        ),
        ...newAudiences.map(audience =>
          axios.post('http://localhost:8080/users/audiences', audience, { headers, withCredentials: true })
        )
      ]);

      goToProfile();
    } catch (error) {
      console.error('Error sending data:', error);
    }
  };

  const createInputs = (type) => {
    const inputs = {
      company: [
        { label: 'Company Name', type: 'text', placeholder: 'Enter your company name.', value: companyName, onChange: (e) => setCompanyName(e.target.value) },
        { label: 'Company Description', type: 'text', placeholder: 'Enter your company description.', value: companyDescription, onChange: (e) => setCompanyDescription(e.target.value) }
      ],
      product: [
        { label: 'Product Name', type: 'text', placeholder: 'Enter your product name.', value: productName, onChange: (e) => setProductName(e.target.value) },
        { label: 'Product Description', type: 'text', placeholder: 'Enter your product description.', value: productDescription, onChange: (e) => setProductDescription(e.target.value) }
      ],
      audience: [
        { label: 'Audience Name', type: 'text', placeholder: 'Enter your target audience.', value: audienceName, onChange: (e) => setAudienceName(e.target.value) },
        { label: 'Audience Description', type: 'text', placeholder: 'Enter your target audience description.', value: audienceDescription, onChange: (e) => setAudienceDescription(e.target.value) }
      ]
    };
    return inputs[type];
  };

  const createTableData = (type) => {
    const columns = {
      product: ['Product Name', 'Product Description'],
      audience: ['Audience Name', 'Audience Description']
    };
    const rows = {
      product: [...productData, ...newProductData].map(product => [product.productName, product.productDescription]),
      audience: [...audienceData, ...newAudienceData].map(audience => [audience.audienceName, audience.audienceDescription])
    };
    return { columns: columns[type], rows: rows[type] };
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div className="App company-setup-background">
      <main className="App-main">
        <Header />
        <div className='content-container-company-setup'>
          <div className='display'> Set up company </div>

          <div className='form-part1-container'>
            <div className='left-form-part1-container'>
              <InputFields title="Company Information" inputs={createInputs('company')} />
              <InputFields title="Target Product" inputs={createInputs('product')} />
              <div className='add-button-wrapper'>
                <Buttons onClick={() => handleAdd('product')} color='secondary-color' variant='secondary' icon='add'>
                  Add Product
                </Buttons>
              </div>
            </div>
            <div className='right-form-part2-container'>
              <img className="set-up-company-image" src="/set-up-company.png" alt="SetUpCompany" />
            </div>
          </div>

          {productData.length > 0 || newProductData.length > 0 ? (
            <div className='setup-content-table-wrapper'>
              <ContentTable tableTitle="Product" columns={createTableData('product').columns} rows={createTableData('product').rows} />
            </div>
          ) : null}

          <div className='form-part1-container'>
            <div className='left-form-part1-container'>
              <InputFields title="Audience" inputs={createInputs('audience')} />
              <div className='add-button-wrapper'>
                <Buttons onClick={() => handleAdd('audience')} color='secondary-color' variant='secondary' icon='add'>
                  Add Audience
                </Buttons>
              </div>
            </div>
            <div className='right-form-part2-container'></div>
          </div>

          {audienceData.length > 0 || newAudienceData.length > 0 ? (
            <div className='setup-content-table-wrapper'>
              <ContentTable tableTitle="Audiences" columns={createTableData('audience').columns} rows={createTableData('audience').rows} />
            </div>
          ) : null}

          <Buttons onClick={handleSubmit} color='secondary-color' variant='secondary' icon='check'>
            Set company info
          </Buttons>
        </div>
      </main>
    </div>
  );
};

export default SetUpCompany;
