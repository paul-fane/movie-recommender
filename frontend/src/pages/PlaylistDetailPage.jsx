import React, { useState, useEffect, useContext } from "react";
import { useParams } from "react-router-dom";
import AuthContext from "../context/AuthContext";

import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Grid from "@mui/material/Grid2";
import RateButton from "../components/playlist-card/RateButton";
import ShowRating from "../components/playlist-card/ShowRating";
import WatchlistButton from "../components/playlist-card/WatchlistButton";
import RateModal from "../components/rating/RateModal";
import SeasonCard from "../components/SeasonCard";
import RatingsModal from "../components/rating/RatingsModal";

const PlaylistDetailPage = () => {
  let { authTokens } = useContext(AuthContext);

  const [openRatingsModal, setOpenRatingsModal] = useState(false);
  const [openRateModal, setOpenRateModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [playlist, setPlaylist] = useState(null);
  // Parameters of the current URL
  let params = useParams();

  useEffect(() => {
    fetchPlaylist(params.type);
  }, [params]);

  const handleOpenRateModal = (item) => {
    setOpenRateModal(true);
  };

  const handleCloseRateModal = () => {
    setOpenRateModal(false);
  };

  const handleOpenRatingsModal = () => {
    setOpenRatingsModal(true);
  };

  const updateWatchlist = (playlist_id, newValue) => {
    setPlaylist((prevItem) => ({
      ...prevItem,
      in_watchlist: newValue,
    }));
  };

  const updateRate = (playlist_id, newValue) => {
    setPlaylist((prevItem) => ({
      ...prevItem,
      user_rate: newValue,
    }));
  };

  const fetchPlaylist = async (type) => {
    let url;
    if (type === "MOV") {
      url = `http://127.0.0.1:8000/api/playlists/movie-detail/${params.slug}/`;
    } else if (type === "TVS") {
      url = `http://127.0.0.1:8000/api/playlists/tvshow-detail/${params.slug}/`;
    } else if (type === "PLY") {
      url = `http://127.0.0.1:8000/api/playlists/playlist-detail/${params.slug}/`;
    } else if (type === "SEA") {
      url = `http://127.0.0.1:8000/api/playlists/season-detail/${params.slug}/`;
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
        setPlaylist(data);
      }
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (params.type === "PLY") {
    return (
      <>
        {playlist && (
          <Box>
            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                gap: 2,
                alignItems: "center",
                justifyContent: "space-between",
              }}
            >
              <Typography gutterBottom variant="caption" component="div">
                {playlist.type}
              </Typography>

              <WatchlistButton
                playlist={playlist}
                updateWatchlist={updateWatchlist}
                authTokens={authTokens}
              />
            </Box>
            <Typography
              onClick={() => history(`/playlist/${playlist.slug}`)}
              gutterBottom
              variant="h6"
              component="div"
            >
              {playlist.title}{" "}
              {playlist.release_date && `(${playlist.release_date})`}
            </Typography>

            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                gap: 1,
                alignItems: "center",
                flexWrap: "wrap",
              }}
            >
              {playlist.category.map((item, index) => (
                <Chip
                  key={index}
                  label={item.title}
                  color="primary"
                  //variant="outlined"
                  sx={{
                    backgroundColor: "#f5c518",
                    color: "black",
                    border: "none",
                  }}
                />
              ))}
            </Box>

            <Typography variant="body2" color="text.secondary" gutterBottom>
              {playlist.overview}
            </Typography>

            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                gap: 2,
                alignItems: "center",
                justifyContent: "space-between",
                padding: "6px",
              }}
            >
              <Box
                sx={{
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "center",
                }}
              >
                <ShowRating
                  handleOpenRatingsModal={handleOpenRatingsModal}
                  playlist={playlist}
                />
              </Box>

              <Box
                sx={{
                  display: "flex",
                  flexDirection: "row",
                  alignItems: "center",
                }}
              >
                <RateButton
                  playlist={playlist}
                  handleOpenRateModal={handleOpenRateModal}
                />
              </Box>
            </Box>
            {playlist.type === "PLY" && (
              <Box
                sx={{
                  borderRadius: "12px",
                  border: "1px solid",
                  p: 2,
                  borderColor: "#E8E8E8",
                }}
              >
                <Typography variant="h6" color="info" gutterBottom>
                  Titles
                </Typography>

                {playlist.related.length > 0 ? (
                  <Grid container spacing={2} columns={12}>
                    {playlist.related.map((playlist, index) => (
                      <Grid key={playlist.id} size={{ xs: 12, md: 12 }}>
                        <SeasonCard
                          rank={index + 1}
                          key={playlist.id}
                          playlist={playlist}
                        />
                      </Grid>
                    ))}
                  </Grid>
                ) : (
                  <Typography gutterBottom variant="h6" component="div">
                    The list is empty
                  </Typography>
                )}
              </Box>
            )}

            <RateModal
              openRateModal={openRateModal}
              handleCloseRateModal={handleCloseRateModal}
              playlist={playlist}
              updateRate={updateRate}
              authTokens={authTokens}
            />

            <RatingsModal
              openRatingsModal={openRatingsModal}
              handleCloseRatingsModal={() => setOpenRatingsModal(false)}
              playlist={playlist}
              authTokens={authTokens}
            />
          </Box>
        )}
      </>
    );
  }

  return (
    <>
      {playlist && (
        <Box>
          {playlist.parent && (
            <Typography
              sx={{ color: "#666666" }}
              gutterBottom
              variant="h6"
              component="div"
            >
              {playlist.parent}
            </Typography>
          )}
          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              gap: 2,
              alignItems: "center",
              justifyContent: "space-between",
            }}
          >
            <Typography gutterBottom variant="caption" component="div">
              {playlist.type}
            </Typography>

            <WatchlistButton
              playlist={playlist}
              updateWatchlist={updateWatchlist}
              authTokens={authTokens}
            />
          </Box>
          <Typography
            onClick={() => history(`/playlist/${playlist.slug}`)}
            gutterBottom
            variant="h6"
            component="div"
          >
            {playlist.title}{" "}
            {playlist.release_date && `(${playlist.release_date})`}
          </Typography>

          {/* {playlist.video !== null && (
            <iframe
              width="560"
              height="315"
              src={`https://www.youtube.com/embed/${playlist.video.video_id}`}
              title="YouTube video player"
              //frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
              //allowfullscreen
            ></iframe>
          )} */}

          {playlist.video !== null && (
            <div className="container">
              <iframe
                // width="100%"
                // height="1080"
                src={`https://www.youtube.com/embed/${playlist.video.video_id}`}
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen
              ></iframe>
            </div>
          )}

          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              gap: 1,
              alignItems: "center",
              flexWrap: "wrap",
            }}
          >
            {playlist.category.map((item, index) => (
              <Chip
                key={index}
                label={item.title}
                color="primary"
                //variant="outlined"
                sx={{
                  backgroundColor: "#f5c518",
                  color: "black",
                  border: "none",
                }}
              />
            ))}
          </Box>

          <Typography variant="body2" color="text.secondary" gutterBottom>
            {playlist.overview}
          </Typography>

          <Box
            sx={{
              display: "flex",
              flexDirection: "row",
              gap: 2,
              alignItems: "center",
              justifyContent: "space-between",
              padding: "6px",
            }}
          >
            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                alignItems: "center",
              }}
            >
              <ShowRating
                handleOpenRatingsModal={handleOpenRatingsModal}
                playlist={playlist}
              />
            </Box>

            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                alignItems: "center",
              }}
            >
              <RateButton
                playlist={playlist}
                handleOpenRateModal={handleOpenRateModal}
              />
            </Box>
          </Box>
          {playlist.type === "TVS" && (
            <Box
              sx={{
                borderRadius: "12px",
                border: "1px solid",
                p: 2,
                borderColor: "#E8E8E8",
              }}
            >
              <Typography variant="h6" color="info" gutterBottom>
                Seasons
              </Typography>

              {playlist.seasons.length > 0 ? (
                <Grid container spacing={2} columns={10}>
                  {playlist.type === "TVS" &&
                    playlist.seasons.map((season) => (
                      <Grid key={season.id} size={{ xs: 10, md: 2 }}>
                        <SeasonCard key={season.id} playlist={season} />
                      </Grid>
                    ))}
                </Grid>
              ) : (
                <Typography gutterBottom variant="h6" component="div">
                  No season yet
                </Typography>
              )}
            </Box>
          )}

          {openRateModal && (
            <RateModal
              openRateModal={openRateModal}
              handleCloseRateModal={handleCloseRateModal}
              playlist={playlist}
              updateRate={updateRate}
              authTokens={authTokens}
            />
          )}

          {openRatingsModal && (
            <RatingsModal
              openRatingsModal={openRatingsModal}
              handleCloseRatingsModal={() => setOpenRatingsModal(false)}
              playlist={playlist}
              authTokens={authTokens}
            />
          )}
        </Box>
      )}
    </>
  );
};

export default PlaylistDetailPage;
