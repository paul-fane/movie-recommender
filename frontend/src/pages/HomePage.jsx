import { useState, useEffect, useContext, useCallback } from "react";
import AuthContext from "../context/AuthContext";

import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Grid from "@mui/material/Grid2";
import IconButton from "@mui/material/IconButton";
import RssFeedRoundedIcon from "@mui/icons-material/RssFeedRounded";
import CircularProgress from "@mui/material/CircularProgress";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";

import Search from "../components/Search";
import PlaylistCard from "../components/playlist-card/PlaylistCard";
import RateModal from "../components/rating/RateModal";
import RatingsModal from "../components/rating/RatingsModal";

const HomePage = () => {
  const { authTokens, user } = useContext(AuthContext);
  const [selectedRateItem, setSelectedRateItem] = useState(null);
  const [openRateModal, setOpenRateModal] = useState(false);

  const [selectedRatingsItem, setSelectedRatingsItem] = useState(null);
  const [openRatingsModal, setOpenRatingsModal] = useState(false);

  const [playlists, setPlaylists] = useState([]);
  const [querySearch, setQuerySearch] = useState({
    //query: "",
    sort_by: "popular",
    category: "movies",
  });
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [previousPage, setPreviousPage] = useState(null);
  const [nextPage, setNextPage] = useState(null);

  const handleOpenRatingsModal = useCallback((item) => {
    setSelectedRatingsItem(item);
    setOpenRatingsModal(true);
  }, []);

  const handleCloseRatingsModal = () => {
    setSelectedRatingsItem(null);
    setOpenRatingsModal(false);
  };

  const handleOpenRateModal = useCallback((item) => {
    setSelectedRateItem(item);
    setOpenRateModal(true);
  }, []);

  const handleCloseRateModal = () => {
    setSelectedRateItem(null);
    setOpenRateModal(false);
  };

  useEffect(() => {
    getPlaylists();
  }, [querySearch, user]);

  let getPlaylists = async (url) => {
    if (!url) {
      url = `http://127.0.0.1:8000/api/dashboard/list?query=${query}&sort_by=${querySearch.sort_by}&category=${querySearch.category}`;
    }
    if (user) {
      setLoading(true);
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + String(authTokens.access),
          },
        });
        const data = await response.json();
        console.log(data);
        if (response.status === 200) {
          setPlaylists(data.results);
          setPreviousPage(data.previous);
          setNextPage(data.next);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(true);
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
        const data = await response.json();
        console.log(data);
        if (response.status === 200) {
          setPlaylists(data.results);
          setPreviousPage(data.previous);
          setNextPage(data.next);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }
  };

  const updateWatchlist = useCallback((playlist_id, newValue) => {
    setPlaylists((prevItems) =>
      prevItems.map((item) => {
        return item.id !== playlist_id
          ? item
          : {
              ...item,
              in_watchlist: newValue,
            };
      })
    );
  }, []);

  const updateRate = (playlist_id, newValue) => {
    const updateList = playlists.map((item) => {
      return item.id !== playlist_id
        ? item
        : {
            ...item,
            user_rate: newValue,
          };
    });
    setPlaylists(updateList);
  };

  const handleCategory = (category) => {
    setQuerySearch((prevFormData) => {
      return {
        ...prevFormData,
        category: category,
      };
    });
  };

  const handleQueryChange = (event) => {
    if (event.target.name === "sort_by") {
      setQuerySearch((prevFormData) => {
        return {
          ...prevFormData,
          [event.target.name]: event.target.value,
        };
      });
    } else if (event.target.name === "query") {
      setQuery(event.target.value);
    }
  };

  const handleNextPage = () => {
    if (nextPage) {
      getPlaylists(nextPage);
    }
  };

  const handlePreviousPage = () => {
    if (previousPage) {
      getPlaylists(previousPage);
    }
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
      <div>
        <Typography variant="h2" gutterBottom>
          Suggestions, Ratings, Reviews and where to create your Watchlist!
        </Typography>
        <Typography>Start rating movies to get new suggestions!</Typography>
      </div>

      <Box
        sx={{
          display: "flex",
          flexDirection: { xs: "column", md: "row" },
          width: "100%",
          justifyContent: "space-between",
          alignItems: { xs: "start", md: "center" },
          gap: 4,
          overflow: "auto",
        }}
      >
        <Box
          sx={{
            display: "inline-flex",
            flexDirection: "row",
            gap: 3,
            overflow: "auto",
          }}
        >
          
          <Chip
            onClick={() => handleCategory("movies")}
            size="medium"
            label="Movies"
            sx={
              querySearch.category === "movies"
                ? {}
                : { backgroundColor: "transparent", border: "none" }
            }
          />
          <Chip
            onClick={() => handleCategory("shows")}
            size="medium"
            label="TV shows"
            sx={
              querySearch.category === "shows"
                ? {}
                : { backgroundColor: "transparent", border: "none" }
            }
          />
          <Chip
            onClick={() => handleCategory("playlists")}
            size="medium"
            label="Playlists"
            sx={
              querySearch.category === "playlists"
                ? {}
                : { backgroundColor: "transparent", border: "none" }
            }
          />
        </Box>
        <Box
          sx={{
            display: { xs: "flex", sm: "flex" },
            flexDirection: "row",
            gap: 1,
            width: { xs: "100%", md: "fit-content" },
            overflow: "auto",
          }}
        >
          <Search
            querySearch={querySearch}
            handleQueryChange={handleQueryChange}
          />
          <IconButton
            onClick={() => getPlaylists()}
            size="small"
            aria-label="RSS feed"
          >
            <RssFeedRoundedIcon />
          </IconButton>
        </Box>
      </Box>

      {loading === true ? (
        <Box
          sx={{ display: "flex", justifyContent: "center", marginTop: "30px" }}
        >
          <CircularProgress />
        </Box>
      ) : (
        <>
          <Grid container spacing={2} columns={12}>
            {playlists.length > 0 ? (
              playlists.map((playlist) => (
                <Grid key={playlist.id} size={{ xs: 12, md: 6 }}>
                  <PlaylistCard
                    playlist={playlist}
                    updateWatchlist={updateWatchlist}
                    handleOpenRateModal={handleOpenRateModal}
                    handleOpenRatingsModal={handleOpenRatingsModal}
                    authTokens={authTokens}
                  />
                </Grid>
              ))
            ) : (
              <Typography gutterBottom variant="h6" component="div">
                No data in database
              </Typography>
            )}
          </Grid>
          <Stack direction="row" justifyContent="center" spacing={1}>
            <Button
              onClick={handlePreviousPage}
              variant="text"
              size="small"
              startIcon={<ArrowBackIosIcon />}
              disabled={!previousPage}
            >
              Previous
            </Button>
            <Button
              onClick={handleNextPage}
              variant="text"
              size="small"
              endIcon={<ArrowForwardIosIcon />}
              disabled={!nextPage}
            >
              Next
            </Button>
          </Stack>
        </>
      )}

      {selectedRateItem && (
        <RateModal
          openRateModal={openRateModal}
          handleCloseRateModal={handleCloseRateModal}
          playlist={selectedRateItem}
          updateRate={updateRate}
          authTokens={authTokens}
        />
      )}

      {selectedRatingsItem && (
        <RatingsModal
          user={user}
          openRatingsModal={openRatingsModal}
          handleCloseRatingsModal={handleCloseRatingsModal}
          playlist={selectedRatingsItem}
          authTokens={authTokens}
        />
      )}
    </Box>
  );
};

export default HomePage;
