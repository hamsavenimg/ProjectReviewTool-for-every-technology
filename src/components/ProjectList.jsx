import styles from "./csscomponents/projectlist.module.css";
import Pagination from "./Pagination";
import OwnerHeader from "./OwnerHeader";
import Projects from "../projects.json";
import SearchIcon from '@mui/icons-material/Search';
import StarIcon from '@mui/icons-material/Star';
import {Link, useNavigate} from 'react-router-dom';
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown';
import CircleIcon from '@mui/icons-material/Circle';
import Rating from '@mui/material/Rating';
import Stack from '@mui/material/Stack';
import { useState , useEffect} from "react";
import axios from "axios"

function ProjectList() {
      const navigate = useNavigate();
      const [projRatings, setProjRatings] = useState([]); // Store API data
      const [searchQuery, setSearchQuery] = useState(""); // Store search input
      const [filteredProj, setFilteredProj] = useState([]); // For search results
      const[currentPage,setCurrentPage] = useState(1); 
      const recordsPerPage = 10;  
        
      // Fetch data from API
      useEffect(() => {
           axios
           .get("http://localhost:8000/api/rating") // Update with your API URL
           .then((response) => {
            setProjRatings(response.data.Ratings|| []); // Store fetched data
            setFilteredProj(response.data.Ratings|| []);
            setCurrentPage(1);
                  })
           .catch((error) => {
                console.error("Error fetching data:", error);
                  });
           }, []);
      
    //   console.log(projRatings[0].project_name)
    //   // Filter projects based on search query
    //    const filteredProjects = projRatings.filter((project) => 
    //    project.project_name.toLowerCase().includes(searchQuery.toLowerCase()));   
       
       
      // Pagination logic     
      const lastPostIndex = currentPage * recordsPerPage;
      const firstPostIndex = lastPostIndex - recordsPerPage;
      const currentposts = projRatings.slice(firstPostIndex, lastPostIndex);
      const totalPosts = projRatings.length;
      const nPage = Math.ceil(projRatings.length/recordsPerPage);
      const numbers = [...Array(nPage + 1).keys()].slice(1);   
                  
      // Handle search input change
       const handleSearch = () => {
        const filteredData = projRatings.filter(project =>
            project.project_name.toLowerCase().includes(searchQuery.toLowerCase())
          );
          setFilteredProj(filteredData);
          setCurrentPage(1); // Reset to first page after search
        };
      // Funtion to handle Add button click to go to 'Add new Project Page'
      const handleAddProject = () => {
       navigate(`/upladdnewproject`);
     }
  
    return (      
        <div className={styles.container}>    
              {/* <OwnerHeader /> */}
          <div className={styles.tablecontainer}>
            <thead >
              <th className={styles.header}>Project List</th>
              <th className={styles.header}></th>
              <th className={styles.header}></th>
              <th className={styles.header}></th>
              <th className={styles.header} ><input className={styles.search} type="text" 
                   placeholder="Search Project..." name="search" /></th>
              <th className={styles.SearchIcon} onClick={handleSearch}>
                         <button className={styles.searchbutton}>
                   <SearchIcon htmlColor="grey"/></button></th>
              <th ><button className={styles.addbutton}
                   aria-label="Add New" onClick={() => handleAddProject()}> + Add New
                   </button></th>
            </thead>
          </div>
          {/*********  Project List Table Header *******************************/}
          <div className={styles.innercontainer}>
            <thead>
               <th className={styles.tableheadcell1}><input className={styles.checkbox1} type="checkbox" id="checkbox1" name="checkbox1" value="">
                                                  </input> </th>
               <th className={styles.tableheadcell2}>Project name</th>
               <th className={styles.tableheadversion}>Version</th>
               <th className={styles.tableheadcell2}>Technology</th>
               <th className={styles.tableheadcell3}> Date </th>
                <th className={styles.tableheadcell3}>
                     <ul><li><span><button><KeyboardArrowUpIcon /></button></span></li>
                          <li><span><button><KeyboardArrowDownIcon /></button> </span></li>
                     </ul>                  
               </th>
               <th className={styles.tableheadcell4}>Time</th>
               <th className={styles.tableheadcell2}>Status</th>
               <th className={styles.tableheadcell2}>Rating</th>
               <th className={styles.tableheadcell2}>Project Score</th>
            </thead>
          {/* *************** Table data display **********************/}
          <tbody>
            {currentposts.map((project,id) =>(              
                <tr key ={id}>
                  <td className={styles.tablecell1}>
                       <input className={styles.checkbox1} type="checkbox" id="checkbox1" name="checkbox1" value="">
                       </input> </td>
                  <td className={styles.tablecell2}><a 
                        href={`/details/${project.project_name}_v${project.version}_${project.date}${project.time}`} 
                        className={styles.link}>
                         {project.project_name}
                       </a></td>
                  <td className={styles.tablecell3}>{project.version}</td>
                  <td className={styles.tablecell2}>{project.technology}</td>
                  <td className={styles.tablecell5}>{project.date}</td>
                  <td className={styles.tablecell3}>{project.time}</td>
                  <td className={styles.tablecell4}>
                     {project.status.charAt(0) == 'P'? 
                       <CircleIcon fontSize="smaller" htmlColor="green"/>: 
                       <CircleIcon fontSize="smaller" htmlColor="Orange"/>}
                       <StarIcon fontSize="2px" htmlColor="white"/>{project.status}</td>
                  <td className={styles.tablecell4}> 
                    {/* { <div> {stars.map((_, index) =>{
                       return   (<StarIcon htmlColor={(project.rating) > index ? "orange" : "grey"} 
                               fontSize="12px"/>)})}
                               </div> } */}
                      <Stack spacing={1}>
                        <Rating name="half-rating-read" 
                                defaultValue={project.project_score / 20} size="small" precision={0.5} readOnly />
                      </Stack>
                    </td>
                  <td className={styles.tablecell3}>{project.project_score}</td>
                </tr>
              )
            )}
            </tbody>           
            {/* <Pagination totalPosts={Projects.length}
                        postsPerPage = {postsPerPage}
                        setCurrentPage={setCurrentPage}
                        currentPage ={currentPage}
            />  */}
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
  export default ProjectList;