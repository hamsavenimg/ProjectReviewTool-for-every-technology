import styles from "./csscomponents/capstoneadminsidebar.module.css";
import {Sidebar, Menu, MenuItem,SubMenu } from 'react-pro-sidebar';
import image from "../assets/uplLogo.png";
import GridViewRoundedIcon from '@mui/icons-material/GridViewRounded';
import InsertChartRoundedIcon from '@mui/icons-material/InsertChartRounded';

function CapstoneAdminSidebar() {
   
    return (
      <div>
        <Sidebar>
          <Menu className={styles.sidenav}> 
             <MenuItem><thead><th><img className={styles.logoimg} src ={image} /></th>
             <th className={styles.sidenavheader}>Snipe</th></thead></MenuItem>  


            <MenuItem className ={styles.sidenavmenuitem1} id="Dashboard"
                     label ="Dashboard" icon={<GridViewRoundedIcon />}>                
                  Dashboard                  
            </MenuItem> 

            <MenuItem className ={styles.sidenavmenuitem2} id = "Projects" label ="Projects" 
                      icon={<InsertChartRoundedIcon />} >
                    Projects                  
            </MenuItem> 

            <SubMenu  className ={styles.sidenavmenuitem2} label="Utilities" icon={<InsertChartRoundedIcon />}> 
                 <MenuItem label ="AddTechnology" >   Add Technology               
                 </MenuItem>
            </SubMenu>

          </Menu>
        </Sidebar>
      </div>
    )
  }
  
  export default CapstoneAdminSidebar