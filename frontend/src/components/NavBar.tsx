import { Box, Button } from "@chakra-ui/react";

const NavBar = () => {
  const signOut = () => {
    window.location.replace("/");
  };

  return (
    <div className="box-1">
      <Button onClick={signOut} style={{background: "teal", color: "white", left: "90vw"}}>Log out</Button>
    </div>
  );
};

export default NavBar;
