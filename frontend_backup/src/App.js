// src/App.js

import React, { useState, useEffect } from "react";
import { Container, Typography, Box, Button } from "@mui/material";
import FamilyTree from "./FamilyTree";
import fullData from "../data/data.json";

const App = () => {
  const [currentTree, setCurrentTree] = useState(null);
  const [mainTree, setMainTree] = useState(null);

  useEffect(() => {
    const main = fullData.find((branch) =>
        branch.treeBranch.includes("Шабльовських")
    );
    if (main) {
      setMainTree(main.treeData);
      setCurrentTree(main.treeData);
    }
  }, []);

  const handleGoToBranch = (surname) => {
    const branch = fullData.find((b) => b.treeBranch.includes(surname));
    if (branch) setCurrentTree(branch.treeData);
  };

  const handleBackToMain = () => {
    if (mainTree) setCurrentTree(mainTree);
  };

  return (
      <Container>
        <Box my={4}>
          <Typography variant="h4" align="center" gutterBottom>
            Родинне дерево Шабльовських
          </Typography>

          {currentTree ? (
              <>
                <FamilyTree
                    treeData={currentTree}
                    onNavigateToBranch={handleGoToBranch}
                />
                <Box mt={3} textAlign="center">
                  <Button variant="contained" onClick={handleBackToMain}>
                    Повернутись до основної гілки
                  </Button>
                </Box>
              </>
          ) : (
              <Typography>Завантаження...</Typography>
          )}
        </Box>
      </Container>
  );
};

export default App;
