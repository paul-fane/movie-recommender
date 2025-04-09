import React, { useContext } from "react";
import AuthContext from "../../context/AuthContext";
import { useNavigate } from "react-router-dom";

import {
  alpha,
  styled,
  createTheme,
  ThemeProvider,
} from "@mui/material/styles";
import Box from "@mui/material/Box";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Button from "@mui/material/Button";
import IconButton from "@mui/material/IconButton";
import Container from "@mui/material/Container";
import Divider from "@mui/material/Divider";
import MenuItem from "@mui/material/MenuItem";
import Drawer from "@mui/material/Drawer";
import MenuIcon from "@mui/icons-material/Menu";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import ColorModeIconDropdown from "../../shared-theme/ColorModeIconDropdown";
import LocalMoviesIcon from "@mui/icons-material/LocalMovies";
//import LiveTvIcon from "@mui/icons-material/LiveTv";
import Typography from "@mui/material/Typography";

const theme = createTheme({
  palette: {
    info: {
      main: "#212121",
      light: "#4d4d4d",
      dark: "#333b4d",
      contrastText: "#fff",
    },
    infos: {
      main: "#006064",
      light: "#337f83",
      dark: "#004346",
      contrastText: "#fff",
    },
  },
});

const StyledToolbar = styled(Toolbar)(({ theme }) => ({
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between",
  flexShrink: 0,
  borderRadius: `calc(${theme.shape.borderRadius}px + 8px)`,
  backdropFilter: "blur(24px)",
  border: "1px solid",
  borderColor: (theme.vars || theme).palette.divider,
  backgroundColor: theme.vars
    ? `rgba(${theme.vars.palette.background.defaultChannel} / 0.4)`
    : alpha(theme.palette.background.default, 0.4),
  boxShadow: (theme.vars || theme).shadows[1],
  padding: "8px 12px",
}));

export default function AppAppBar() {
  const [open, setOpen] = React.useState(false);

  const toggleDrawer = (newOpen) => () => {
    setOpen(newOpen);
  };

  let { user, logoutUser } = useContext(AuthContext);
  const history = useNavigate();

  return (
    <AppBar
      position="fixed"
      enableColorOnDark
      sx={{
        boxShadow: 0,
        bgcolor: "transparent",
        backgroundImage: "none",
        mt: "calc(var(--template-frame-height, 0px) + 28px)",
      }}
    >
      <Container maxWidth="lg">
        <StyledToolbar variant="dense" disableGutters>
          <Box
            sx={{ flexGrow: 1, display: "flex", alignItems: "center", px: 0 }}
          >
            <Box sx={{ display: "flex", alignItems: "center", px: 2 }}>
              <LocalMoviesIcon
                sx={{
                  //backgroundColor: "#f5c518",
                  color: "black",
                  border: "none",
                  marginRight: "3px",
                }}
              />
              <Typography
                sx={{
                  //backgroundColor: "#f5c518",
                  color: "black",
                  border: "none",
                }}
              >
                Recommender
              </Typography>
            </Box>

            <Box sx={{ display: { xs: "none", md: "flex" } }}>
              <Button
                onClick={() => history("/")}
                variant="text"
                color="info"
                size="small"
              >
                Home
              </Button>
              {user && (
                <>
                  <Button
                    onClick={() => history("/suggestions")}
                    variant="text"
                    color="info"
                    size="small"
                  >
                    Suggestions
                  </Button>
                  <Button
                    onClick={() => history("/watchlist")}
                    variant="text"
                    color="info"
                    size="small"
                  >
                    Watchlist
                  </Button>
                </>
              )}

              {/* <Button
                onClick={() => history("/infinite")}
                variant="text"
                color="info"
                size="small"
              >
                Infinite Review
              </Button> */}
            </Box>
          </Box>
          <Box
            sx={{
              display: { xs: "none", md: "flex" },
              gap: 1,
              alignItems: "center",
            }}
          >
            {user ? (
              <>
                <Button
                  onClick={() => history(`/user/${user.email}`)}
                  color="primary"
                  variant="text"
                  size="small"
                >
                  {user.email}
                </Button>
                <Button
                  onClick={logoutUser}
                  color="primary"
                  variant="contained"
                  size="small"
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Button
                  onClick={() => history("/login")}
                  color="primary"
                  variant="text"
                  size="small"
                >
                  Sign in
                </Button>
                <Button
                  onClick={() => history("/register")}
                  color="primary"
                  variant="contained"
                  size="small"
                >
                  Sign up
                </Button>
              </>
            )}
            <ColorModeIconDropdown />
          </Box>
          <Box sx={{ display: { xs: "flex", md: "none" }, gap: 1 }}>
            <ColorModeIconDropdown size="medium" />
            <IconButton aria-label="Menu button" onClick={toggleDrawer(true)}>
              <MenuIcon />
            </IconButton>
            <Drawer
              anchor="top"
              open={open}
              onClose={toggleDrawer(false)}
              PaperProps={{
                sx: {
                  top: "var(--template-frame-height, 0px)",
                },
              }}
            >
              <Box sx={{ p: 2, backgroundColor: "background.default" }}>
                <Box
                  sx={{
                    display: "flex",
                    justifyContent: "flex-end",
                  }}
                >
                  <IconButton onClick={toggleDrawer(false)}>
                    <CloseRoundedIcon />
                  </IconButton>
                </Box>
                <MenuItem onClick={() => history("/")}>
                  Movie Recommender
                </MenuItem>
                <MenuItem onClick={() => history("/")}>Home</MenuItem>
                {user && (
                  <MenuItem onClick={() => history("/suggestions")}>
                    Suggestions
                  </MenuItem>
                )}
                {/* <MenuItem onClick={() => history("/infinite")}>
                  Infinite Review
                </MenuItem> */}
                <Divider sx={{ my: 3 }} />
                {user ? (
                  <>
                    <MenuItem>
                      <Button
                        onClick={() => history(`/user/${user.email}`)}
                        color="primary"
                        variant="outlined"
                        fullWidth
                      >
                        {user.email}
                      </Button>
                    </MenuItem>
                    <MenuItem>
                      <Button
                        onClick={logoutUser}
                        color="primary"
                        variant="contained"
                        fullWidth
                      >
                        Logout
                      </Button>
                    </MenuItem>
                  </>
                ) : (
                  <>
                    <MenuItem>
                      <Button
                        onClick={() => history("/login")}
                        color="primary"
                        variant="outlined"
                        fullWidth
                      >
                        Sign in
                      </Button>
                    </MenuItem>
                    <MenuItem>
                      <Button
                        onClick={() => history("/register")}
                        color="primary"
                        variant="contained"
                        fullWidth
                      >
                        Sign up
                      </Button>
                    </MenuItem>
                  </>
                )}
              </Box>
            </Drawer>
          </Box>
        </StyledToolbar>
      </Container>
    </AppBar>
  );
}
