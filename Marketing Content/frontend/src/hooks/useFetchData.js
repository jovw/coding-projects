import { useState, useEffect } from 'react';
import { fetchProducts, fetchAudiences } from '../services/api';

const useFetchData = () => {
  const [displayProducts, setDisplayProducts] = useState([]);
  const [displayAudiences, setDisplayAudiences] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const products = await fetchProducts();
      const audiences = await fetchAudiences();
      setDisplayProducts(products);
      setDisplayAudiences(audiences);
    };

    fetchData();
  }, []);

  return { displayProducts, displayAudiences };
};

export default useFetchData;
