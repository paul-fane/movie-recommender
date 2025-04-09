import  { useState, useEffect, useContext, useCallback } from "react";
import AuthContext from "../context/AuthContext";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid2";
import PlaylistCard from "../components/playlist-card/PlaylistCard";
import RateModal from "../components/rating/RateModal";
import RatingsModal from "../components/rating/RatingsModal";

const WatchlistPage = () => {
  const { authTokens, user } = useContext(AuthContext);

  const [selectedRateItem, setSelectedRateItem] = useState(null);
  const [openRateModal, setOpenRateModal] = useState(false);

  const [selectedRatingsItem, setSelectedRatingsItem] = useState(null);
  const [openRatingsModal, setOpenRatingsModal] = useState(false);

  const [playlists, setPlaylists] = useState([]);

  // const [querySearch, setQuerySearch] = useState({
  //   query: "",
  //   sort_by: "popular",
  //   category: "all",
  // });

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
  }, [user]);

  let getPlaylists = async () => {
    const response = await fetch(
      // `http://127.0.0.1:8000/api/watchlists/list?query=${querySearch.query}&sort_by=${querySearch.sort_by}&category=${querySearch.category}`,
      `http://127.0.0.1:8000/api/watchlists/list`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
      }
    );
    const data = await response.json();
    console.log(data);
    if (response.status === 200) {
      setPlaylists(data.results);
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

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 4 }}>
      <div>
        <Typography variant="h2" gutterBottom>
          Your Watchlist
        </Typography>
        <Typography>
          Your Watchlist is the place to track the titles you want to watch.
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
        {/* <Box
          sx={{
            display: { xs: "flex", sm: "flex" },
            flexDirection: "row",
            gap: 1,
            width: { xs: "100%", md: "fit-content" },
            overflow: "auto",
          }}
        >
          <Search querySearch={querySearch} setQuerySearch={setQuerySearch} />
        </Box> */}
      </Box>

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

export default WatchlistPage;
