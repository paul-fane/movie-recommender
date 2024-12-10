import React, { useState, useEffect, useContext, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useParams } from "react-router-dom";
import AuthContext from "../context/AuthContext";

import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";
import Grid from "@mui/material/Grid2";
import IconButton from "@mui/material/IconButton";
import CircularProgress from "@mui/material/CircularProgress";

import Button from "@mui/material/Button";
import PlaylistCard from "../components/playlist-card/PlaylistCard";
import RateModal from "../components/rating/RateModal";
import RatingsProfileModal from "../components/rating/RatingsProfileModal";
import ReviewCard from "../components/rating/ReviewCard";
import KeyboardDoubleArrowRightIcon from "@mui/icons-material/KeyboardDoubleArrowRight";

const ProfilePage = () => {
  const { authTokens, user } = useContext(AuthContext);

  const [openRatingsModal, setOpenRatingsModal] = useState(false);
  const [openComparRatingsModal, setOpenComparRatingsModal] = useState(false);

  const [profileUsername, setProfileUsername] = useState(null);
  const [userRatings, setUserRatings] = useState([]);
  const [userRatingsCount, setUserRatingsCount] = useState(null);
  const [ownRecommendations, setOwnRecommendations] = useState([]);
  const [ownWatchlist, setOwnWatchlist] = useState([]);
  const [ownPlaylists, setOwnPlaylists] = useState([]);
  const [ratingsCompar, setRatingsCompar] = useState([]);

  const [loading, setLoading] = useState(false);

  // Parameters of the current URL
  let params = useParams();
  const history = useNavigate();

  useEffect(() => {
    getProfilePage();
  }, [params]);

  let getProfilePage = async (url) => {
    if (!url) {
      url = `http://127.0.0.1:8000/api/profile/${params.username}/`;
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
        console.log(response);
        console.log(data);
        if (response.status === 200) {
          setProfileUsername(data.profile_username);
          setUserRatings(data.user_ratings);
          setUserRatingsCount(data.user_ratings_count);
          setOwnRecommendations(data.own_recommendations);
          setOwnWatchlist(data.own_watchlist);
          setOwnPlaylists(data.own_playlists);
          setRatingsCompar(data.ratings_compar);
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
          setProfileUsername(data.profile_username);
          setUserRatings(data.user_ratings);
          setUserRatingsCount(data.user_ratings_count);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
      <Typography variant="h2" gutterBottom>
        Username: {profileUsername}
      </Typography>

      <Box
        sx={{
          borderRadius: "12px",
          border: "1px solid",
          p: 2,
          borderColor: "#E8E8E8",
        }}
      >
        <Typography variant="h6" color="info" gutterBottom>
          {user && user.username === profileUsername
            ? "Your Ratings & Reviews"
            : "Ratings & Reviews"}
        </Typography>
        
        <Typography
          sx={{ color: "#666666" }}
          gutterBottom
          variant="h6"
          component="div"
        >
          Most Recently Rated
        </Typography>
        {userRatings.length > 0 ? (
          <>
            <Grid container spacing={2} columns={10}>
              {userRatings
                .filter((item) => item.playlist !== null)
                .map((rating) => (
                  <Grid key={rating.id} size={{ xs: 12, md: 2 }}>
                    <ReviewCard
                      colorStar={
                        user && user.username === profileUsername
                          ? "blue"
                          : "green"
                      }
                      rating={rating}
                    />
                  </Grid>
                ))}
            </Grid>
            <Box sx={{ borderTop: "1px dotted #CCCCCC", marginTop: "10px" }}>
              <Button
                onClick={() => setOpenRatingsModal(true)}
                variant="text"
                endIcon={<KeyboardDoubleArrowRightIcon />}
              >
                See all {userRatingsCount} ratings
              </Button>
            </Box>
          </>
        ) : (
          <Typography gutterBottom variant="h6" component="div">
            {user && user.username !== profileUsername
              ? "Loved or hated a movie or TV show? Write a review and share it with others!"
              : "No review yet!"}
          </Typography>
        )}
        {user && user.username !== profileUsername && (
          <>
            <Typography variant="h6" color="info" gutterBottom>
              Compared to You
            </Typography>
            <Typography
              sx={{ color: "#666666" }}
              gutterBottom
              variant="h6"
              component="div"
            >
              Titles {profileUsername} rated that you haven't rated
            </Typography>

            {ratingsCompar.length > 0 ? (
              <>
                <Grid container spacing={2} columns={10}>
                  {ratingsCompar
                    .filter((item) => item.playlist !== null)
                    .map((rating) => (
                      <Grid key={rating.id} size={{ xs: 12, md: 2 }}>
                        <ReviewCard rating={rating} />
                      </Grid>
                    ))}
                </Grid>
                <Box
                  sx={{ borderTop: "1px dotted #CCCCCC", marginTop: "10px" }}
                >
                  <Button
                    onClick={() => setOpenComparRatingsModal(true)}
                    variant="text"
                    endIcon={<KeyboardDoubleArrowRightIcon />}
                  >
                    See more titles {profileUsername} rated that you haven't
                    rated
                  </Button>
                </Box>
              </>
            ) : (
              <Typography gutterBottom variant="h6" component="div">
                The list is empty
              </Typography>
            )}
          </>
        )}
      </Box>

      {user && user.username === profileUsername && (
        <>
          <Box
            sx={{
              borderRadius: "12px",
              border: "1px solid",
              p: 2,
              borderColor: "#E8E8E8",
            }}
          >
            <Typography variant="h6" color="info" gutterBottom>
              Your Watchlist
            </Typography>
            {ownWatchlist.length > 0 ? (
              <>
                <Grid container spacing={2} columns={12}>
                  {ownWatchlist.map((playlist) => (
                    <Grid key={playlist.id} size={{ xs: 12, md: 3 }}>
                      <PlaylistCard
                        playlist={playlist}
                        authTokens={authTokens}
                        watchlist={false}
                        rate={false}
                      />
                    </Grid>
                  ))}
                </Grid>
                <Box
                  sx={{ borderTop: "1px dotted #CCCCCC", marginTop: "10px" }}
                >
                  <Button
                    onClick={() => history(`/watchlist`)}
                    variant="text"
                    endIcon={<KeyboardDoubleArrowRightIcon />}
                  >
                    See more
                  </Button>
                </Box>
              </>
            ) : (
              <Typography gutterBottom variant="h6" component="div">
                Your Watchlist is empty
              </Typography>
            )}
          </Box>
          <Box
            sx={{
              borderRadius: "12px",
              border: "1px solid",
              p: 2,
              borderColor: "#E8E8E8",
            }}
          >
            <Typography variant="h6" color="info" gutterBottom>
              Recommended For You
            </Typography>

            {ownRecommendations.length > 0 ? (
              <>
                <Grid container spacing={2} columns={12}>
                  {ownRecommendations.map((playlist) => (
                    <Grid key={playlist.id} size={{ xs: 12, md: 3 }}>
                      <PlaylistCard
                        playlist={playlist}
                        watchlist={false}
                        rate={false}
                      />
                    </Grid>
                  ))}
                </Grid>
                <Box
                  sx={{ borderTop: "1px dotted #CCCCCC", marginTop: "10px" }}
                >
                  <Button
                    onClick={() => history(`/suggestions`)}
                    variant="text"
                    endIcon={<KeyboardDoubleArrowRightIcon />}
                  >
                    See more
                  </Button>
                </Box>
              </>
            ) : (
              <Typography gutterBottom variant="h6" component="div">
                No suggestions yet! Start rating movies to get new suggestions!
              </Typography>
            )}
          </Box>
          <Box
            sx={{
              borderRadius: "12px",
              border: "1px solid",
              p: 2,
              borderColor: "#E8E8E8",
            }}
          >
            <Typography variant="h6" color="info" gutterBottom>
              Your Playlists
            </Typography>

            <Typography>{ownPlaylists}</Typography>
          </Box>
        </>
      )}

      {openRatingsModal && (
        <RatingsProfileModal
          openRatingsModal={openRatingsModal}
          handleCloseRatingsModal={() => setOpenRatingsModal(false)}
          profileUsername={params.username}
          user={user}
          authTokens={authTokens}
        />
      )}

      {openComparRatingsModal && (
        <RatingsProfileModal
          openRatingsModal={openComparRatingsModal}
          handleCloseRatingsModal={() => setOpenComparRatingsModal(false)}
          profileUsername={params.username}
          user={user}
          authTokens={authTokens}
          compar={true}
        />
      )}
    </Box>
  );
};

export default ProfilePage;
