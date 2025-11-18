import styles from "./csscomponents/adminprojectlist.module.css";
import Pagination from "./Pagination";
import OwnerHeader from "./OwnerHeader";
import Ratings from "./Ratings";
import Projects from "../projects.json";
import SearchIcon from '@mui/icons-material/Search';
import StarIcon from '@mui/icons-material/Star';
import CircleIcon from '@mui/icons-material/Circle';
import DeleteIcon from '@mui/icons-material/Delete';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import Rating from '@mui/material/Rating';
import Stack from '@mui/material/Stack';
import {Link, useNavigate} from 'react-router-dom';
import { useState } from "react";

function AdminProjectList() {
       const navigate = useNavigate();
       const[currentPage,setCurrentPage] = useState(1);
       
       const recordsPerPage = 10;  
       let numRecords = 0;   
 
       const lastPostIndex = currentPage * recordsPerPage;
       const firstPostIndex = lastPostIndex - recordsPerPage;
       const currentposts = Projects.slice(firstPostIndex, lastPostIndex);
       const totalPosts = Projects.length;
       const nPage = Math.ceil(Projects.length/recordsPerPage);
       const numbers = [...Array(nPage + 1).keys()].slice(1);   
      

       // Funtion to handle Add button click to go to 'Add new Project Page'
       const handleAddProject = () => {
        navigate(`/upladminaddnewproject`);
      }
    return (
      
        <div className={styles.container}>
               <OwnerHeader />             
         
          {/****************************Project List Page Header****************************************/}
          <div className={styles.tablecontainer}>
            <thead >
              <th className={styles.header}>Project List</th>
              <th className={styles.header}></th>
              <th className={styles.header}></th>
              <th className={styles.header}></th>
              <th className={styles.header} ><input className={styles.search} type="text" placeholder="Search.." name="search"
               /></th>
              <th className={styles.SearchIcon}><button className={styles.searchbutton}><SearchIcon htmlColor="grey"/></button></th>
              <th ><button className={styles.addbutton}
                    aria-label="Add New" onClick={() => handleAddProject()}> + Add New
                   </button></th>
              <th><button className={styles.deletebutton}><DeleteIcon fontSize="large" htmlColor="grey"/></button></th>
            </thead>
          </div>

          {/*****************************Project List Table Header*************************************/}
            <div className={styles.innercontainer}>
               <thead>
            <th className={styles.tableheadcell1}>
                       <input className={styles.checkbox1} type="checkbox" id="checkbox1" name="checkbox1" value="">
                       </input> </th>
            <th className={styles.tableheadcell2}>Project name</th>
            <th className={styles.tableheadcell2}>Developer name</th>
            <th className={styles.tableheadcell1}>Version</th>
            <th className={styles.tableheadcell2}>Technology</th>
            <th className={styles.tableheadcell5}>Date</th>
            <th className={styles.tableheadcell5}>
                     <ul><li><span><button><KeyboardArrowUpIcon /></button></span></li>
                          <li><span><button><KeyboardArrowDownIcon /></button> </span></li>
                     </ul>                  
               </th>
            <th className={styles.tableheadcell4}>Time</th>
            <th className={styles.tableheadcell4}>Status</th>
            <th className={styles.tableheadcell3}>Rating</th>
            <th className={styles.tableheadcell2}>Best Practices</th>
            <th className={styles.tableheadcell2}>Send Email</th>
             </thead>
             {/* *************** Table data display **********************/}
            <tbody>
            {/* {Projects.map(project =>{
              return( */}
              {currentposts.map((project,id) =>(  
                <tr  key ={id}>
                  <td className={styles.tablecell1}>
                       <input className={styles.checkbox1} type="checkbox" id="checkbox1" name="checkbox1" value="">
                       </input> </td>
                  <td className={styles.tablecell2}>{project.projectName}</td>
                  <td className={styles.tablecell2}>{project.developerName}</td>
                  <td className={styles.tablecell1}>{project.version}</td>
                  <td className={styles.tablecell4}>{project.technology}</td>
                  <td className={styles.tablecell2}>{project.date}</td>
                  <td className={styles.tablecell5}>{project.time}</td>
                  <td className={styles.tablecell6}>
                  {project.status.charAt(0) == 'P'? 
                       <CircleIcon fontSize="smaller" htmlColor="green"/>: 
                       <CircleIcon fontSize="smaller" htmlColor="Orange"/>}
                       <StarIcon fontSize="2px" htmlColor="white"/>{project.status}</td>
                  <td className={styles.tablecell4}>
                      <Stack spacing={1}>
                        <Rating name="half-rating-read" 
                                defaultValue={project.rating} size="small"
                                precision={0.5} readOnly />
                      </Stack></td>
                  <td className={styles.tablecell3}>{project.bestPractices}</td>
                  <td><button className={styles.emailbutton}
                             aria-label="send Email"> Send Email
                       </button></td>
                </tr>
              )
            )}
            </tbody>           
            {/* <Pagination /> */}
            <div className={styles.pagination}>            
                <label className={styles.label1}>Showing {currentposts.length} of {totalPosts} items</label>                
                    <button onClick={prePage}>
                      <KeyboardArrowLeftIcon />
                    </button>                  
                {
                  numbers.map((n,i) => (
                    
                      <button  key ={i}
                         onClick={() => changeCPage(n)}> {n}
                    </button>
                  
                  ))
                }               
                  <button onClick={nextPage}>
                      <KeyboardArrowRightIcon />
                  </button>                
              
               </div>
            
             </div>
          </div>
                
    )
    function prePage(){
      if(currentPage !== 1){
        setCurrentPage(currentPage - 1)
      }
    }
  
    function changeCPage(id){
      setCurrentPage(id)
    }
  
    function nextPage(){
      if(currentPage !== nPage){
        setCurrentPage(currentPage + 1)
      }  
    }  
  }
  
  export default AdminProjectList;