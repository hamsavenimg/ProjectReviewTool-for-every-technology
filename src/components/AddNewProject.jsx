import React from "react";
import styles from "./csscomponents/addnewproject.module.css";
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import SaveAltSharpIcon from '@mui/icons-material/SaveAltSharp';
import { useState } from "react";
import {Link, useNavigate} from 'react-router-dom';

const AddNewProject =() =>{
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");

    const navigate = useNavigate();
       const handlegoBack = () => {
        navigate(-1);
      }
    
    // const handleFileChange = (event) => {
    //     setFile(event.target.files[0]);
    //   };
      
    // const handleUpload = async () => {
    //     if (!file) {
    //       setMessage("Please select a .zip file first!");
    //       return;
    //     }
    //   const formData = new FormData();
    //   formData.append("file", file);
  
    //   try {
    //     const response = await axios.post("http://localhost:8000/upload", formData, {
    //       headers: { "Content-Type": "multipart/form-data" },
    //     });
  
    //     setMessage(response.data.message);
    //   } catch (error) {
    //     setMessage("Error uploading file.");
    //   }
    // };
    

return (
    <div className={styles.addprojectcontainer}>
        {/* Header  */}
        <div className={styles.headercontainer}><tbody >
          <td><button onClick={() => handlegoBack()}><KeyboardArrowLeftIcon /></button></td>
          <td><label className={styles.header}>Add a New Project</label></td>
          </tbody >
        </div>
        {/* Input form  */}
        <form className ={styles.addform}>
          <div>
              <label for="name" className ={styles.modernLabel1} >Project Name</label><br/>
              <input className ={styles.modernInput1} 
                 type = "text" name="name"  placeholder="web Development" 
              /> 
          </div>

          <div>
              <label for="name" className ={styles.modernLabel1} >Short Description of the Project</label><br/>
              <input className ={styles.modernInput1} 
                type = "text" name="name"  placeholder="Building fully responsive website for an e-commerce website" 
                /> 
              {/* <input className ={styles.modernLabel1}  type="file" accept=".zip" onChange={handleFileChange} />   */}
          </div>

          <div>
              <label for="name" className ={styles.modernLabel1} >Technology</label><br/>
              <select  name="technology" id="technology">
                  <option value="">Java</option>
                  <option value="">Python</option>
                  <option value="">React</option>
                  <option value="">C++</option>
                  <option value="">Java + React</option>
                  <option value="">Java + Angular</option>
                  <option value="">Java + Python</option>
                  
              </select>
          </div>
             <div><button className={styles.uploadbutton} >
                                    Upload Project</button>
                                    {message && <p>{message}</p>} </div>  
             <div><button className={styles.savebutton}><SaveAltSharpIcon /> Run Project</button></div>
         </form>  
    </div>
);

};
export default AddNewProject;