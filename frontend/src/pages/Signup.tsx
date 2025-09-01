import React, { useState } from "react";
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  MenuItem,
} from "@mui/material";
import api from "../api/axios";

const Signup: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("learner");

  const handleSignup = async () => {
    try {
      const res = await api.post("/auth/signup", {
        email,
        password,
        role,
      });
      alert("Signup successful! 🎉 Now you can login.");
      console.log(res.data);
    } catch (err: any) {
      alert("Signup failed: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <Container maxWidth="sm">
      <Box mt={5}>
        <Typography variant="h4" gutterBottom>
          Signup
        </Typography>

        <TextField
          fullWidth
          label="Email"
          margin="normal"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <TextField
          fullWidth
          label="Password"
          type="password"
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <TextField
          select
          fullWidth
          label="Role"
          margin="normal"
          value={role}
          onChange={(e) => setRole(e.target.value)}
        >
          <MenuItem value="learner">Learner</MenuItem>
          <MenuItem value="instructor">Instructor</MenuItem>
          <MenuItem value="admin">Admin</MenuItem>
        </TextField>

        <Button
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 2 }}
          onClick={handleSignup}
        >
          Sign up
        </Button>
      </Box>
    </Container>
  );
};

export default Signup;
