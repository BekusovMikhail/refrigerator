import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import { useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { ChakraProvider } from '@chakra-ui/react'
import "./App.css";
import NavBar from "./components/NavBar";
import Refrigerator from "./components/Refrigerator";
import Welcome from "./components/Welcome";
import Register from './components/Register';

function App() {

  return (
    <ChakraProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Welcome/>} />
          <Route path="/register" element={<Register />} />
          <Route path="/main" element={<Refrigerator />} />
        </Routes>
      </Router>
    </ChakraProvider>
  );
}

export default App;
