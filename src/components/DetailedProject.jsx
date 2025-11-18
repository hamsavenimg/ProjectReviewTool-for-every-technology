import React from "react";
import styles from "./csscomponents/detailedproject.module.css";
import OwnerHeader from "./OwnerHeader";
import image from "../assets/uplowner.png";
import LogoutIcon from '@mui/icons-material/Logout'; 
import SearchIcon from '@mui/icons-material/Search';


const DetailedProject =() =>{
    

return (
    <div className={styles.container}>
             <OwnerHeader />
          <div className={styles.tablecontainer}>
          <thead >
          <th className={styles.header}>AI Disha - Java - V1</th>
          <th className={styles.header}></th>
          <th className={styles.header}></th>
          <th className={styles.header}></th>
          <th className={styles.header} ><input className={styles.search} type="text" placeholder="Search.." name="search"
        /></th>
        <th className={styles.SearchIcon}><SearchIcon htmlColor="grey"/></th>
          </thead></div>


          <div className={styles.innercontainer}>
                    <thead>

                    <th className={styles.tableheadcell1}>Problem</th>
                    <th className={styles.tableheadcell3}>Line No.</th>
                    <th className={styles.tableheadcell2}>Category</th>
                    <th className={styles.tableheadcell2}>Type</th>
                          </thead>


                          <thead>

                    <th className={styles.tablecell1}>Automation.java</th>
                    <th className={styles.tablecell3}></th>
                    <th className={styles.tablecell2}></th>
                    <th className={styles.tablecell2}></th>
                          </thead>

                          <tbody>
                
          <td className={styles.tablecell1}>Class name should start with upper case</td>
          <td className={styles.tablecell3}>1</td>
          <td className={styles.tablecell2}>Naming Convention</td>
          <td className={styles.tablecell2}>Code Quality</td>
         
          </tbody>
          <tbody>
                
                <td className={styles.tablecell1}>Method name should start with lower case</td>
          <td className={styles.tablecell3}>8</td>
          <td className={styles.tablecell2}>Naming Convention</td>
          <td className={styles.tablecell2}>Code Quality</td>
         
          </tbody>

          <thead>

                    <th className={styles.tablecell1}>Random.java</th>
                    <th className={styles.tablecell3}></th>
                    <th className={styles.tablecell2}></th>
                    <th className={styles.tablecell2}></th>
                          </thead>
                          <tbody>
                
                <td className={styles.tablecell1}>Code Duplication</td>
          <td className={styles.tablecell3}>20</td>
          <td className={styles.tablecell2}>Duplication</td>
          <td className={styles.tablecell2}>Code Quality</td>
         
          </tbody>
                          </div>

    </div>
);

};
export default DetailedProject;