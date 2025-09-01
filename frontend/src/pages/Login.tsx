import { useState, useContext } from "react";
import {
  Container,
  TextField,
  Button,
  Typography,
  Box,
  IconButton,
  InputAdornment,
  Alert,
} from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import { AuthContext } from "../context/AuthContext";

const Login = () => {
  const navigate = useNavigate();
  const { setToken } = useContext(AuthContext);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleLogin = async () => {
    setErrorMsg(null);
    setLoading(true);
    try {
      // FastAPI: POST /auth/login  -> { access_token, token_type }
      const res = await api.post("/auth/login", { email, password });

      const token = res.data?.access_token as string | undefined;
      if (!token) throw new Error("No token returned from server");

      // Save token so axios interceptor will attach it automatically
      localStorage.setItem("token", token);
      setToken(token);

      // Optional: you can navigate to a protected page (e.g., courses)
      navigate("/"); // change to "/courses" once that page exists
    } catch (err: any) {
      const detail =
        err?.response?.data?.detail ||
        err?.message ||
        "Login failed. Please check your credentials.";
      setErrorMsg(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box mt={6}>
        <Typography variant="h4" gutterBottom>
          Login
        </Typography>

        {errorMsg && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {errorMsg}
          </Alert>
        )}

        <TextField
          label="Email"
          fullWidth
          margin="normal"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <TextField
          label="Password"
          type={showPw ? "text" : "password"}
          fullWidth
          margin="normal"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          InputProps={{
            endAdornment: (
              <InputAdornment position="end">
                <IconButton
                  aria-label="toggle password visibility"
                  onClick={() => setShowPw((s) => !s)}
                  edge="end"
                >
                  {showPw ? <VisibilityOff /> : <Visibility />}
                </IconButton>
              </InputAdornment>
            ),
          }}
        />

        <Button
          variant="contained"
          color="primary"
          fullWidth
          sx={{ mt: 2 }}
          onClick={handleLogin}
          disabled={loading || !email || !password}
        >
          {loading ? "Logging in..." : "Login"}
        </Button>
      </Box>
    </Container>
  );
};

export default Login;
