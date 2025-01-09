const axios = require('axios');

const axiosInstance = axios.create({
    withCredentials: true  // Ensure cookies are sent with requests
});

const setAuthToken = token => {
    if (token) {
        console.log(token);
        axiosInstance.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    } else {
        delete axiosInstance.defaults.headers.common['Authorization'];
    }
};

// Login
const handleLogin = () => {
  const windowSize = 'width=500,height=600,left=100,top=100,toolbar=0';
  window.open('http://localhost:8080/auth/google/login', '_blank', windowSize);
};

// Logout
const handleLogOut = () => {
  const windowSize = 'width=500,height=600,left=100,top=100,toolbar=0';
  window.open('http://localhost:8080/auth/google/logout', '_blank', windowSize);
};

// Get All Users
const getAllUsers = async () => {
  try {
      const response = await axiosInstance.get('http://localhost:8080/users');
      console.log('Users:', response.data);
  } catch (error) {
      console.error('Error getting users:', error.response?.data || error.message);
  }
}

// Get User via token
const getUserBySub = async () => {
  try {
      const response = await axiosInstance.get('http://localhost:8080/users/sub');
      console.log('User:', response.data);
  } catch (error) {
      console.error('Error getting user:', error.response?.data || error.message);
  }
}

// Add a product to users profile
const addUserProducts = async () => {
  const productData = {
      productName: " Nishis Succulent Collection",
      productDescription: "A curated assortment of low-maintenance succulents"
  };
  try {
      const response = await axiosInstance.post('http://localhost:8080/users/products', productData);
      console.log('Product added:', response.data);
  } catch (error) {
      console.error('Error adding product:', error.response?.data || error.message);
  }
}

// Get all products
const getProducts = async () => {
  try {
      const response = await axiosInstance.get('http://localhost:8080/products');
      console.log('Products:', response.data);
  } catch (error) {
      console.error('Error getting products:', error.response?.data || error.message);
  }
}

// Get a product from users profile
const getUsersProducts = async () => {
  try {
      const response = await axiosInstance.get('http://localhost:8080/users/products');
      console.log('Users Products:', response.data);
  } catch (error) {
      console.error('Error getting user products:', error.response?.data || error.message);
  }
}

// Add a audience to users profile
const addUserAudiences = async () => {
  const audienceData = {
      audienceName: "UrbanDwellers",
      audienceDescription: "Individuals living in city apartments..."
  };
  try {
      const response = await axiosInstance.post('http://localhost:8080/users/audiences', audienceData);
      console.log('Audience added:', response.data);
  } catch (error) {
      console.error('Error adding audience:', error.response?.data || error.message);
  }
}

// Get all audiences
const getAudience = async () => {
  try {
      const response = await axiosInstance.get('http://localhost:8080/audiences');
      console.log('Audiences:', response.data);
  } catch (error) {
      console.error('Error getting audiences:', error.response?.data || error.message);
  }
}

// Get a audience from users profile
const getUsersAudiences = async () => {
  try {
      const response = await axiosInstance.get('http://localhost:8080/users/audiences');
      console.log('Users Audiences:', response.data);
  } catch (error) {
      console.error('Error getting user audiences:', error.response?.data || error.message);
  }
}

// Add a company to users profile
const addUserCompany = async () => {
  const companyData = {
      companyName: "Succulent Collection",
      companyDescription: "A curated assortment of low-maintenance succulents"
  };
  try {
      const response = await axiosInstance.post('http://localhost:8080/users/company', companyData);
      console.log('Company info added:', response.data);
  } catch (error) {
      console.error('Error adding company:', error.response?.data || error.message);
  }
}

// Get a company from users profile
const getUserCompany = async () => {
  try {
      const response = await axiosInstance.get('http://localhost:8080/users/company');
      console.log('Users company:', response.data);
  } catch (error) {
      console.error('Error getting company:', error.response?.data || error.message);
  }
}

// Save generated post
const addProductContent = async () => {
    const postData = {
        postTitle: "Test",
        postCaption: "Test test test",
        imageDescription: "test"
    };
    try {
        const response = await axiosInstance.post('http://localhost:8080/contents/post', postData);
        console.log('Post content saved successfully:', response.data);
    } catch(error) {
        console.error('Error saving post:', error.response?.data || error.message);
    }
}

module.exports = {
    setAuthToken,
    handleLogin,
    handleLogOut,
    getAllUsers,
    getUserBySub,
    addUserProducts,
    getProducts,
    getUsersProducts,
    addUserAudiences,
    getAudience,
    getUsersAudiences,
    addUserCompany,
    getUserCompany,
    addProductContent
};
