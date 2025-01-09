import { useState, useEffect } from 'react';
import { fetchUserInfo, fetchCompanyInfo, fetchProducts, fetchAudiences } from '../services/api';

const useFetchProfileData = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [companyInfo, setCompanyInfo] = useState(null);
  const [productData, setProductData] = useState([]);
  const [audienceData, setAudienceData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      const user = await fetchUserInfo();
      const company = await fetchCompanyInfo();
      const products = await fetchProducts();
      const audiences = await fetchAudiences();
      setUserInfo(user);
      setCompanyInfo(company);
      setProductData(products);
      setAudienceData(audiences);
      setLoading(false);
    };

    fetchData();
  }, []);

  return { userInfo, companyInfo, productData, audienceData, loading };
};

export default useFetchProfileData;
