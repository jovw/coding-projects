import React from 'react';
import './Profile.css';
import Header from '../../components/Header/Header';
import UserInfo from '../../components/Profile/UserInfo';
import Buttons from '../../components/Buttons/Buttons';
import BusinessInfo from '../../components/Profile/BusinessInfo';
import ContentTable from '../../components/Tables/ContentTables';
import { useNavigate } from 'react-router-dom';
import useFetchProfileData from '../../hooks/useFetchProfileData';

const Profile = () => {
  const { userInfo, companyInfo, productData, audienceData, loading } = useFetchProfileData();
  const navigate = useNavigate();

  const goToSetUpCompany = () => {
    navigate('/set-up-company', { state: { companySetup: false } });
  };

  const productColumn = ['Product Name', 'Product Description'];
  const productRow = productData.map(product => [product.productName, product.productDescription]);

  const audienceColumn = ['Audience Name', 'Audience Description'];
  const audienceRow = audienceData.map(audience => [audience.audienceName, audience.audienceDescription]);

  if (loading) {
    return <div>Loading...</div>; // Show loading indicator while data is being fetched
  }

  return (
    <div className="App">
      <main className="App-main">
        <Header />
        <div className='content-container'>
          <div className='background-square bottom-square'></div>
          <div className='background-square top-square'></div>

          {companyInfo ? (
            <div className='user-container'>
              <div className='display'> User Profile </div>
              {userInfo && (
                <UserInfo 
                  userName={userInfo.firstName} 
                  userEmail={userInfo.email} 
                  imageUrl={userInfo.profilePicUrl || null}
                />
              )}
              {companyInfo && (
                <BusinessInfo 
                  companyTitle={companyInfo.companyName}
                  companyDescription={companyInfo.companyDescription}
                />
              )}
            </div>
          ) : (
            <div className='user-container'>
              <div className='display'> User Profile </div>
              {userInfo && (
                <UserInfo 
                  userName={userInfo.firstName + ' ' + userInfo.lastName} 
                  userEmail={userInfo.email}
                  imageUrl={userInfo.profilePicUrl || null}
                />
              )}
            </div>
          )}

          {companyInfo ? (
            <div className='content-table-profile'>
              <ContentTable 
                tableTitle="Products" 
                columns={productColumn} 
                rows={productRow} 
              />
              <ContentTable 
                tableTitle="Audiences" 
                columns={audienceColumn} 
                rows={audienceRow} 
              />
            </div>
          ) : (
            <div className='placeholder-container'>
              <img 
                className="image-placeholder"
                src="/profile-no-company.png"
                alt="Profile" 
              />
              <Buttons onClick={goToSetUpCompany} color='secondary-color' icon='add' variant='secondary' >
                Set up company
              </Buttons>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Profile;
