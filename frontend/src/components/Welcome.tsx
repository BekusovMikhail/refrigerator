import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom'
import {
  Flex,
  Heading,
  Input,
  Button,
  InputGroup,
  Stack,
  InputLeftElement,
  chakra,
  Box,
  Avatar,
  FormControl,
  InputRightElement,
  Text
} from "@chakra-ui/react";
import { FaUserAlt, FaLock } from "react-icons/fa";
import NavBar from "./NavBar";

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

const Welcome = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const handleShowClick = () => setShowPassword(!showPassword);
  //const navigate = useNavigate()
  
  const signIn = () => {
    fetch("http://localhost:8001/api/login_user/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({"username": username, "password": password, "rememberMe": true})
    }).then((res) => {
      return res.json()
    }).then((res) => {
      if (res["success"]){
        window.location.replace("/main");
      }
      else{
        setMessage(res["message"])
        console.log(res["message"])
      }
    })
  };
  

  return (
    <Flex
    flexDirection="column"
    width="100wh"
    height="100vh"
    backgroundColor="gray.200"
    justifyContent="center"
    alignItems="center"
  >
      <Stack
        flexDir="column"
        mb="2"
        justifyContent="center"
        alignItems="center"
      >
        <Avatar bg="teal.500" />
        <Heading color="teal.400">Welcome</Heading>
        <Box minW={{ base: "90%", md: "468px" }}>
          <form>
            <Stack
              spacing={4}
              p="1rem"
              backgroundColor="whiteAlpha.900"
              boxShadow="md"
            >
              <FormControl>
                <InputGroup>
                  <InputLeftElement
                    pointerEvents="none"
                    children={<CFaUserAlt color="gray.300" />}
                  />
                  <Input placeholder="username" onChange={(e: any) => {setUsername(e.target.value)}}/>
                </InputGroup>
              </FormControl>
              <FormControl>
                <InputGroup>
                  <InputLeftElement
                    pointerEvents="none"
                    color="gray.300"
                    children={<CFaLock color="gray.300" />}
                  />
                  <Input
                    type={showPassword ? password : "password"}
                    placeholder="Password"
                    onChange={(e: any) => {setPassword(e.target.value)}}
                  />
                  <InputRightElement width="4.5rem">
                    <Button h="1.75rem" size="sm" onClick={handleShowClick}>
                      {showPassword ? "Hide" : "Show"}
                    </Button>
                  </InputRightElement>
                </InputGroup>
                <Text textAlign="right" color="red">
                  {message}
                </Text >
              </FormControl>
              <Button
                borderRadius={0}
                variant="solid"
                colorScheme="teal"
                width="full"
                onClick={signIn}
              >
                Login
              </Button>
            </Stack>
          </form>
        </Box>
      </Stack>
      <Link to="/register">
        <Text color="teal.500">Sign Up</Text>
      </Link>
    </Flex>
  );
};

export default Welcome;
