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
  import { useState } from 'react';
  import { useNavigate, Link } from 'react-router-dom'
  import { FaUserAlt, FaLock } from "react-icons/fa";
  import axios from 'axios';

const CFaUserAlt = chakra(FaUserAlt);
const CFaLock = chakra(FaLock);

const Register = () => {
    const [message, setMessage] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [email, setEmail] = useState('');
    const [name, setName] = useState('');
    const [surname, setSurname] = useState('');
    const [username, setUsername]= useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');

    const handleShowClick = () => setShowPassword(!showPassword);

    const register = () => {
      if(password === password2){
        console.log(email)
        console.log(password)
        fetch("http://localhost:8001/api/reg_user/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({"username": username, "password": password, "email": email, 
          "name": name, "surname": surname})
        }).then(() => {
          window.location.replace("/main");
        })
      } else{
        setMessage("Пароли не совпадают")
      }
    }

    const onChangeMail = (event: any) => {
      setEmail(event.target.value);
    }
  
    const onChangePass = (event: any) => {
      setPassword(event.target.value);
    }

    const onChangePass2 = (event: any) => {
      setPassword2(event.target.value);
    }

    return(
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
          <Heading color="teal.400">Register</Heading>
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
                    <Input placeholder="name" onChange={(e: any) => {setName(e.target.value)}}/>
                  </InputGroup>
                </FormControl>
                <FormControl>
                  <InputGroup>
                    <InputLeftElement
                      pointerEvents="none"
                      children={<CFaUserAlt color="gray.300" />}
                    />
                    <Input placeholder="surname" onChange={(e: any) => {setSurname(e.target.value)}}/>
                  </InputGroup>
                </FormControl>
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
                      children={<CFaUserAlt color="gray.300" />}
                    />
                    <Input type="email" placeholder="email address" onChange={onChangeMail}/>
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
                      onChange={onChangePass}
                    />
                    <InputRightElement width="4.5rem">
                      <Button h="1.75rem" size="sm" onClick={handleShowClick}>
                        {showPassword ? "Hide" : "Show"}
                      </Button>
                    </InputRightElement>
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
                      type={showPassword ? password2 : "password"}
                      placeholder="Repeat password"
                      onChange={onChangePass2}
                    />
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
                  onClick={register}
                >
                  Register
                </Button>
              </Stack>
            </form>
          </Box>
        </Stack>
        <Link to="/">
          <Text color="teal.500">Login</Text>
        </Link>
      </Flex>
    )
}

export default Register;