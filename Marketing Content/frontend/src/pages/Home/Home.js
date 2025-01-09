import './Home.css';
import Header from '../../components/Header/Header';
import Buttons from '../../components/Buttons/Buttons';

const Home = () => {
  const handleLogin = () => {
    window.location.href = 'http://localhost:8080/auth/google/login';
  };

  return (
    <div className="App">
      <main className="App-main">
        <Header isLoggedIn />
        <div className='home-container'>
          <div className='background-square'></div>
          <div className='login-screen-content'>
            <div className='greeting-container'>
              <div className='display'>Welcome to PRODUCT NAME</div>
              <div className='headline-small caption'>
                Transform Your Marketing Strategy with AI-Powered Content Generation.
              </div>
              <div className='login-button-container'>
                <Buttons onClick={handleLogin} variant="primary" icon="user" color="primary-color">
                  Get Started
                </Buttons>
              </div>
            </div>
            <div className='greeting-image-container'>
              <img src="/login-screen-image.png" alt="Placeholder" />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
