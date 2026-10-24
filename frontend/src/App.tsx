
import { useEffect, useState } from "react";
import "./App.css";
import api from "./api/axios";

function App() {
  const [apiMessage, setApiMessage] = useState("Connecting to Flask...");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loginMessage, setLoginMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleLogin(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setLoginMessage("");
    setLoading(true);

    try {
      const csrfResponse = await api.get("/api/csrf-token");
      const csrfToken = csrfResponse.data.csrf_token;

      const loginResponse = await api.post<{
        message: string;
        role: string;
      }>(
        "/api/login",
        { email, password },
        {
          headers: {
            "X-CSRFToken": csrfToken,
          },
        }
      );

      setLoginMessage(loginResponse.data.message);

      // Open the existing Flask booking page after login.
      window.location.href = "http://localhost:5000/";
    } catch (error: any) {
      console.error("Login error:", error);
      console.log("Server response:", error.response?.data);

      setLoginMessage(
        error.response?.data?.error ||
          "Unable to log in. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    api
      .get("/api/health")
      .then((response) => {
        setApiMessage(response.data.message);
      })
      .catch(() => {
        setApiMessage("Could not connect to Flask API.");
      });
  }, []);

  return (
    <main className="login-page">
      <section className="login-card">
        <p>{apiMessage}</p>

        <div className="brand">
          <div className="brand-icon">✚</div>
          <h1>MediCare</h1>
          <p>Medical Appointment Portal</p>
        </div>

        <div className="welcome">
          <h2>Welcome back</h2>
          <p>Sign in to manage your appointments.</p>
        </div>

        <form className="login-form" onSubmit={handleLogin}>
          <label htmlFor="email">Email address</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="you@example.com"
            required
          />

          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="Enter your password"
            required
          />

          <button type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <p role="status">{loginMessage}</p>

        <p className="login-note">
          Secure access to your medical appointments.
        </p>
      </section>
    </main>
  );
}

export default App;
