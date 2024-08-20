import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import API_URL from '../_helpers';

const Index = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [outputImage, setOutputImage] = useState(null);
    const [extraData, setExtraData] = useState(null);
    const [inputImageURL, setInputImageURL] = useState(null);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        setSelectedFile(file);

        // Create a URL for the selected input image
        if (file) {
            const imageURL = URL.createObjectURL(file);
            setInputImageURL(imageURL);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedFile) {
            alert('Please select an image to upload');
            return;
        }

        const formData = new FormData();
        formData.append('email', Cookies.get('email')); // Assuming the email is stored in a cookie
        formData.append('image', selectedFile);

        try {
            const response = await axios.post(`${API_URL}/process-image`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            if (response.data.status === 'success') {
                setOutputImage(response.data.output_image);
                setExtraData(response.data.data);
            } else {
                alert(response.data.message);
            }
        } catch (error) {
            alert('An error occurred: ' + error.response.data.message);
        }
    };

    return (
        <div className="container mt-5">
            <div className="row">
                <div className="col-lg-5 col-md-5 col-sm-10">
                <h2 className="text-center">Image Upload and Analysis</h2>
            <form onSubmit={handleSubmit} className="mt-4">
                <div className="form-group">
                    <label htmlFor="imageUpload">Upload Image:</label>
                    <input 
                        type="file" 
                        className="form-control-file" 
                        id="imageUpload" 
                        onChange={handleFileChange} 
                        accept="image/*" 
                    />
                </div>
                
                {inputImageURL && (
                <div className="mt-5">
                    <h4 className="text-center">Input Image</h4>
                    <div className="text-center">
                        <img src={inputImageURL} alt="Input" className="img-fluid" />
                    </div>
                </div>
            )}
                <button type="submit" className="btn btn-primary mt-3">Submit</button>
            </form>
                </div>
                <div className="col-lg-5 col-md-5 col-sm-10">
                    <h3>Output Screen</h3>
                {outputImage && (
                <div className="mt-5">
                    <h4 className="text-center">Processed Output</h4>
                    <div className="text-center">
                        <img src={`data:image/png;base64,${outputImage}`} alt="Output" className="img-fluid" />
                    </div>
                </div>
            )}

            {extraData && (
                <div className="mt-4">
                    <h4>Additional Data:</h4>
                    <pre>{JSON.stringify(extraData, null, 2)}</pre>
                </div>
            )}
                </div>
            </div>
            

            
        </div>
    );
};

export default Index;
