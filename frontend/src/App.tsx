import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';
import { useState } from "react";
import { useAuthState } from "react-firebase-hooks/auth";
import { ChakraProvider } from '@chakra-ui/react'
import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'
import "./App.css";
import NavBar from "./components/NavBar";
import Refrigerator from "./components/Refrigerator";
import Welcome from "./components/Welcome";
import Register from './components/Register';

const queryClient = new QueryClient()

function App() {

  return (
    <QueryClientProvider client={queryClient}>
      <ChakraProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Welcome/>} />
            <Route path="/register" element={<Register />} />
            <Route path="/main/:username" element={<Refrigerator />} />
          </Routes>
        </Router>
      </ChakraProvider>
    </QueryClientProvider>
  );
}

export default App;
