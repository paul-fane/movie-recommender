import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PrivateRoutes from "./utils/PrivateRoutes";
import { AuthProvider } from "./context/AuthContext";

import NavBar from "./components/header/NavBar";
import SignIn from "./pages/auth/SignIn";
import SignUp from "./pages/auth/SignUp";
import HomePage from "./pages/HomePage";
import SuggestionsPage from "./pages/SuggestionsPage"
import WatchlistPage from "./pages/WatchlistPage"
import PlaylistDetailPage from "./pages/PlaylistDetailPage"
import ProfilePage from "./pages/ProfilePage";

import CssBaseline from "@mui/material/CssBaseline";
import Container from "@mui/material/Container";

// import MainContent from "./components/MainContent";
// import Latest from "./components/Latest";
// import Footer from './components/Footer';
import AppTheme from "./shared-theme/AppTheme";

function App() {
  return (
    <div>
      <Router>
        <AuthProvider>
          <AppTheme >
            <CssBaseline enableColorScheme />
            <NavBar />
            <Container
              maxWidth="lg"
              component="main"
              sx={{ display: "flex", flexDirection: "column", my: 16, gap: 4 }}
            >
              {/* <MainContent />
              <Latest /> */}
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/user/:username" element={<ProfilePage />} />
                <Route path="/login" element={<SignIn />} />
                <Route path="/register" element={<SignUp />} />
                <Route element={<PrivateRoutes />}>
                  <Route exact path="/" element={<HomePage />} />
                  <Route path="/suggestions" element={<SuggestionsPage />} />
                  <Route path="/watchlist" element={<WatchlistPage />} />
                  <Route path="/playlist/:type/:slug" element={<PlaylistDetailPage />} />
                  <Route path="/user/:username" element={<ProfilePage />} />
                </Route>
              </Routes>
            </Container>
            {/* <Footer /> */}
          </AppTheme>
        </AuthProvider>
      </Router>
    </div>
  );
}

export default App;
