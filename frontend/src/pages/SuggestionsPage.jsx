import React, { useState, useEffect, useContext, useCallback } from "react";
import AuthContext from "../context/AuthContext";

import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Grid from "@mui/material/Grid2";
import Typography from "@mui/material/Typography";
import Accordion from "@mui/material/Accordion";
import AccordionSummary from "@mui/material/AccordionSummary";
import AccordionDetails from "@mui/material/AccordionDetails";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import Stack from "@mui/material/Stack";
import ArrowBackIosIcon from "@mui/icons-material/ArrowBackIos";
import ArrowForwardIosIcon from "@mui/icons-material/ArrowForwardIos";
import Button from "@mui/material/Button";
import CircularProgress from "@mui/material/CircularProgress";

import PlaylistCard from "../components/playlist-card/PlaylistCard";
import RateModal from "../components/rating/RateModal";
import RatingsModal from "../components/rating/RatingsModal";

const SuggestionsPage = () => {
  const { authTokens, user } = useContext(AuthContext);

  const [selectedRateItem, setSelectedRateItem] = useState(null);
  const [openRateModal, setOpenRateModal] = useState(false);

  const [selectedRatingsItem, setSelectedRatingsItem] = useState(null);
  const [openRatingsModal, setOpenRatingsModal] = useState(false);

  const [playlists, setPlaylists] = useState([]);
  const [querySearch, setQuerySearch] = useState({
    category: "movies",
  });
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
      url = `http://127.0.0.1:8000/api/suggestions/list?category=${querySearch.category}`;
    }
    setLoading(true);
    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
      });
      
      if (response.status === 200) {
        const data = await response.json();
        console.log(data);
        setPlaylists(data.results);
        setPreviousPage(data.previous);
        setNextPage(data.next);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
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
      <Grid size={{ xs: 12, md: 12 }}>
        <Accordion>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography variant="h6" component="div">
              How does Movie Reccomender know what I showed interest in?
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" color="text.secondary">
              When you give a movie a positive rating we track that as a movie
              that you are interested in and then compare your data to ratings
              made by other users. We can then find movies and TV shows that
              people with similar tastes to you like.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography variant="h6" component="div">
              How can I improve my personalized recommendations?
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" color="text.secondary">
              To improve your personalized recommendations, find and rate more
              of the titles that you love.
            </Typography>
          </AccordionDetails>
        </Accordion>
        <Accordion>
          <AccordionSummary
            expandIcon={<ExpandMoreIcon />}
            aria-controls="panel1-content"
            id="panel1-header"
          >
            <Typography variant="h6" component="div">
              I've just rated a whole bunch of titles. How long will it take for
              those ratings to impact my recommendations?
            </Typography>
          </AccordionSummary>
          <AccordionDetails>
            <Typography variant="body2" color="text.secondary">
              New ratings will have an immediate impact on your recommendations.
              For every 5 movies you rate, the system will create new
              suggestions for you. After rating, reload the page to see updated
              recommendations. Also, daily, a task on a schedule, for the recent
              new users and active users, will generate new recommendations.
            </Typography>
          </AccordionDetails>
        </Accordion>
      </Grid>
      <div>
        <Typography variant="h2" gutterBottom>
          Recommendations
        </Typography>
        <Typography>
          Discover great movies and TV shows for your Watchlist
        </Typography>
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
          openRatingsModal={openRatingsModal}
          handleCloseRatingsModal={handleCloseRatingsModal}
          playlist={selectedRatingsItem}
          authTokens={authTokens}
        />
      )}
    </Box>
  );
};

export default SuggestionsPage;
