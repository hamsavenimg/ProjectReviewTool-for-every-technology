import React from "react";
import styles from "./csscomponents/ownerheader.module.css";
import image from "../assets/uplowner.png";
import LogoutIcon from '@mui/icons-material/Logout'; 

const OwnerHeader = () =>{ 

return (
    <div >
        <div className={styles.logoutcontainer}><tbody >
          <td><img  className={styles.ownerimg} src ={image} /></td>
          <td><label className={styles.ownername}>Mallikarjuna G D</label></td>
          <td className={styles.mydiv}><button title = "Logout" value={"Logout"}><LogoutIcon /></button></td>
          </tbody >
          
        </div>
    </div>
);

};
export default OwnerHeader;