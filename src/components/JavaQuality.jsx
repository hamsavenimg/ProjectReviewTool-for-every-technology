import React, { useState, useEffect } from "react";
import styles from "./csscomponents/javaquality.module.css";
import OwnerHeader from "./OwnerHeader"; 
import SearchIcon from '@mui/icons-material/Search';
import CircleIcon from '@mui/icons-material/Circle';
import axios from "axios"


const LINES_PER_PAGE = 20; // Total lines per page (including file names & violations)

const JavaQuality = () => {  
  const [msg, setMsg] = useState(''); 
  const [err1, setErr1] = useState([]);  
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/data");
      setMsg(response.data.Errors._id);
      setErr1(response.data.Errors.files || []);
      setPage(1);
    } catch (err) {
      console.log("Error fetching data:", err);
    }
  };

  const paginateData = () => {
    let linesCount = 0;
    let paginatedFiles = [];
    let tempPage = [];

    for (const file of err1) {
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

  return (
    <div>
      <OwnerHeader />
      <div className={styles.tablecontainer}>
        <thead>
          <th className={styles.header}>Problems in Code</th>
          <th className={styles.header}></th>
          {/* <th className={styles.header}>
            <button aria-label="Event List" onClick={fetchEvents}>Errors</button>
          </th> */}
          <th className={styles.header}></th>
          <th className={styles.header}>
            <input className={styles.search} type="text" placeholder="Search by filename.." name="search" />
          </th>
          <th className={styles.SearchIcon}><SearchIcon htmlColor="grey"/></th>
        </thead>
      </div>

      <div className={styles.innercontainer}>
        <thead>
          <th className={styles.tableheadcell1}>Problem</th>
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
                    <td className={styles.tablecell4}>
                      <CircleIcon
                        style={{ fontSize: "11px", marginRight: "4px" }} 
                        className={styles[`severity-${item.data.severity}`]} 
                      />
                      {item.data.severity}
                    </td> 
                    <td className={styles.tablecell2}>{item.data.category.trim()}</td>
                    <td className={styles.tablecell2}>{item.data.rule.trim()}</td>
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
        {totalPages > 1 && (
          <div className={styles.pagination}>
            <button onClick={() => setPage((prev) => Math.max(prev - 1, 1))} disabled={page === 1}>Previous</button>
            <span>Page {page} of {totalPages}</span>
            <button onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))} disabled={page === totalPages}>Next</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default JavaQuality;