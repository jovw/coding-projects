import React, { useState } from 'react';
import './GenerateContent.css';
import InputFields from '../../components/Input Fields/InputField';
import InputDropdown from "../../components/Input Dropdown/InputDropdown";
import ImageDisplay from '../../components/Image/ImageDisplay';
import Header from '../../components/Header/Header';
import Buttons from '../../components/Buttons/Buttons';
import { multiselectOptions, platformOptions } from '../../constants';
import MultiSelectDropdown from "../../components/MultiSelect Dropdown/MultiSelectDropdown";
import Multiselect from 'multiselect-react-dropdown';
import useFetchData from '../../hooks/useFetchData';
import { generateContent } from '../../services/api';
import LoadingPage from '../../components/Loading/LoadingPage';

const GenerateContent = () => {
  const [tones, setTone] = useState([]);
  const [audience, setAudience] = useState([]);
  const { displayProducts, displayAudiences } = useFetchData();
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [selectedPlatform, setSelectedPlatform] = useState([]);
  const [generatedContent, setGeneratedContent] = useState(null);
  const [loading, setLoading] = useState(false);

  const content = [
    { label: "Post Title", value: generatedContent?.postTitle, placeholder: "Enter post title" },
    { label: "Post Caption", value: generatedContent?.postCaption, placeholder: "Enter post caption" }
  ];

  const handleChangeMultiSelect = (tonesArr) => {
    setTone(tonesArr);
  };

  const handleProductChange = (option) => {
    setSelectedProduct(option.value);
  };

  const handlePlatformChange = (option) => {
    setSelectedPlatform(option.value);
  };

  const products = displayProducts.map(product => ({ label: product.productName, value: product.id }));
  const audiences = displayAudiences.map(audience => ({ name: audience.audienceName, id: audience.id }));

  const handleGenerateContent = async () => {
    setLoading(true);

    const contentData = {
      productId: selectedProduct,
      audienceIds: audience.map(aud => aud.id),
      tone: tones.map(t => t.name),
      platform: selectedPlatform ? [selectedPlatform] : []
    };

    console.log('Request Body:', contentData); // Debugging: Log request body before sending

    const response = await generateContent(contentData);
    if (response) {
      console.log('Response:', response);
      setGeneratedContent(response);
    }

    setLoading(false);
  };

  return (
    <div className="App">
      {loading && <LoadingPage />}
      <main className="App-main">
        <Header />
        <div className="generate-content-container">
          <div className="generate-content-title">
            Generate Content
          </div>
          <div className="content-body">
            <div className="left-content-body">
              <div className="multiSelectContainer">
                <label className="input-field-title input-spacing">Select tone(s)</label>
                <Multiselect
                  className='multiselect'
                  displayValue={"name"}
                  options={multiselectOptions}
                  selectedValues={tones}
                  onRemove={handleChangeMultiSelect}
                  onSelect={handleChangeMultiSelect}
                />
              </div>
              <InputDropdown 
                label="Which product?" 
                options={products} 
                onChange={handleProductChange} 
              />
              <MultiSelectDropdown 
                label="Select audience(s)" 
                options={audiences} 
                selectedOptions={audience} 
                setSelectedOptions={setAudience} 
              />
              <InputDropdown 
                label="Which platform?" 
                options={platformOptions} 
                onChange={handlePlatformChange} 
              />
              <div className="generate-button-container">
                <Buttons 
                  onClick={handleGenerateContent} 
                  variant="primary" 
                  icon="check" 
                  color="secondary-color" 
                  disabled={loading}
                >
                  {loading ? "Loading..." : "Generate Content"}
                </Buttons>
              </div>
              {generatedContent && (
                <InputFields title="Generated Content" inputs={content} values={generatedContent} />
              )}
            </div>
            <div className="right-content-body">
              {generatedContent && (
                <ImageDisplay 
                  imageUrl={generatedContent.image} 
                  altText={generatedContent.imageDescription} 
                  description={generatedContent.imageDescription} 
                />
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default GenerateContent;
