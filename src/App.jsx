import ProjectList from "./components/ProjectList";
import AdminProjectList from "./components/AdminProjectList";
import CapstoneSidebar from "./components/CapstoneSidebar";
import CapstoneAdminSidebar from "./components/CapstoneAdminSidebar";
import AddNewProject from "./components/AddNewProject";
import DetailedProject from "./components/DetailedProject";
import JavaQuality from "./components/JavaQuality";
import OwnerHeader from "./components/OwnerHeader";
import AddProject from "./components/AddProject";
import ProjectDetails from "./components/ProjectDetails";
import {BrowserRouter as Router,Route,Routes} from 'react-router-dom';
function App() {
  
  return (
    <>
      <div>
       <Router>        
         <Routes>
             <Route index element={<><CapstoneSidebar/><OwnerHeader /></>} /> 
             <Route path = "/uplprojectlist"  element={<><CapstoneSidebar/><OwnerHeader /><ProjectList/></>} /> 
             <Route path ='/upladmin' element={<><CapstoneAdminSidebar/><AdminProjectList/></>} /> 
             {/* <Route path ='/admin' element={<><AdminProjectList/></>}    />                 */}

             <Route path = "/upladminaddnewproject" 
                 element ={<><CapstoneAdminSidebar/><AdminProjectList/><AddNewProject /></>} />

             <Route path = "/upladdnewproject" 
                 element ={<><CapstoneSidebar/><ProjectList/><AddNewProject /></>} />  
                 
             <Route path ='/upldetail' element={<><CapstoneSidebar/><DetailedProject/></>} />
             <Route path ='/upljava' element={<><CapstoneSidebar/><JavaQuality/></>} />  
             <Route path ='/addproject' element={<><AddProject/></>} /> 
             <Route path ='/details/:id' element={<><CapstoneSidebar/><ProjectDetails/></>} /> 
         </Routes>
       </Router>
      </div>
      
    </>
  )
}

export default App
