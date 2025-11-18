import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import styles from "./csscomponents/projectdetails.module.css";
import OwnerHeader from "./OwnerHeader"; 
import SearchIcon from '@mui/icons-material/Search';
import CircleIcon from '@mui/icons-material/Circle';
import axios from "axios";

const LINES_PER_PAGE = 50;

const ProjectDetails = () => {  
  const [msg, setMsg] = useState(''); 
  const [err1, setErr1] = useState([]);  
  const [filteredErr1, setFilteredErr1] = useState([]); // For search results
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState(""); // Store search input
  const { id } = useParams();

  useEffect(() => {
    fetchEvents();
  }, [id]);

  const fetchEvents = async () => {
    try {
      console.log(id)
      const response = await axios.get(`http://localhost:8000/api/data/${id}`);
      setMsg(response.data.Errors._id);
      setErr1(response.data.Errors.files || []);
      setFilteredErr1(response.data.Errors.files || []); // Initially set both to full data
      setPage(1);
    } catch (err) {
      console.log("Error fetching data:", err);
    }
  };

  const handleSearch = () => {
    const filteredData = err1.filter(file =>
      file.file_name.toLowerCase().includes(searchQuery.toLowerCase())
    );
    setFilteredErr1(filteredData);
    setPage(1); // Reset to first page after search
  };

  const paginateData = () => {
    let linesCount = 0;
    let paginatedFiles = [];
    let tempPage = [];

    for (const file of filteredErr1) {
      if (linesCount + 1 > LINES_PER_PAGE) {
        paginatedFiles.push(tempPage);
        tempPage = [];
        linesCount = 0;
      }

      tempPage.push({ type: "file", data: file });
      linesCount++;

      for (const violation of file.violations) {
        if (linesCount + 1 > LINES_PER_PAGE) {
          paginatedFiles.push(tempPage);
          tempPage = [];
          linesCount = 0;
        }
        tempPage.push({ type: "violation", data: violation, fileName: file.file_name });
        linesCount++;
      }
    }

    if (tempPage.length > 0) {
      paginatedFiles.push(tempPage);
    }

    return paginatedFiles;
  };

  const paginatedData = paginateData();
  const totalPages = paginatedData.length;
  const currentPageData = paginatedData[page - 1] || [];
  const totalItems = filteredErr1.reduce((sum, file) => sum + 1 + file.violations.length, 0);

  return (
    <div>
      <OwnerHeader />
      <div className={styles.tablecontainer}>
        <thead>
          <th className={styles.header}>Detailed Errorlist :</th>
          <th className={styles.header}></th>
          <th className={styles.header}></th>
          <th className={styles.header}>
            <input 
              className={styles.search} 
              type="text" 
              placeholder="Search by filename..." 
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)} 
            />
          </th>
          <th className={styles.SearchIcon}>
            <button className={styles.searchButton} onClick={handleSearch}>
              <SearchIcon htmlColor="grey"/>
            </button>
          </th>
        </thead>
      </div>

      <div className={styles.innercontainer}>
        <thead>
          <th className={styles.tableheadcell1}>Error Message</th>
          <th className={styles.tableheadcell3}>Line No.</th>
          <th className={styles.tableheadcell2}>Severity</th>
          <th className={styles.tableheadcell2}>Category</th>
          <th className={styles.tableheadcell2}>Rule</th>
        </thead>

        <table>
          <tbody>
            {currentPageData.length > 0 ? (
              currentPageData.map((item, index) => 
                item.type === "file" ? (
                  <tr key={`filename-${index}`}>
                    <td className={styles.tablefilenamecell} colSpan={5}>{item.data.file_name}</td>
                  </tr>
                ) : (
                  <tr key={`error-${index}`}>
                    <td className={styles.tablecell1}>{item.data.message}</td>
                    <td className={styles.tablecell3}>{item.data.line}</td>
                    <td className={styles.tablecell2}>
                      <CircleIcon
                        style={{ fontSize: "15px", marginRight: "4px" }} 
                        className={styles[`severity-${item.data.severity}`]} 
                      />
                      {item.data.severity}
                    </td> 
                    <td className={styles.tablecell2}>{item.data.category}</td>
                    <td className={styles.tablecell2}>{item.data.rule}</td>
                  </tr>
                )
              )
            ) : (
              <tr>
                <td className={styles.tableheadcell1} colSpan={5}>No data available</td>
              </tr>
            )}
          </tbody>
        </table>

        {/* Pagination Controls */}
        <div className={styles.paginationContainer}>
          <div className={styles.paginationInfo}>
            Showing {Math.min(LINES_PER_PAGE, totalItems - (page - 1) * LINES_PER_PAGE)} of {totalItems} items
          </div>
          <div className={styles.paginationButtons}>
            <button onClick={() => setPage((prev) => Math.max(prev - 1, 1))} disabled={page === 1}>&lt;</button>
            {[...Array(totalPages)].map((_, i) => (
              <button
                key={i}
                onClick={() => setPage(i + 1)}
                className={page === i + 1 ? styles.activePage : ""}
              >
                {i + 1}
              </button>
            ))}
            <button onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))} disabled={page === totalPages}>&gt;</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetails;
