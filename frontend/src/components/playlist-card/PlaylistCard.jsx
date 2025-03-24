import React, { useState, memo } from "react";
import { useNavigate } from "react-router-dom";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import CardMedia from "@mui/material/CardMedia";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Chip from "@mui/material/Chip";

import RateButton from "./RateButton";
import ShowRating from "./ShowRating";
import WatchlistButton from "./WatchlistButton";

const SyledCard = styled(Card)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  padding: 0,
  height: "100%",
  backgroundColor: (theme.vars || theme).palette.background.paper,
  "&:hover": {
    backgroundColor: "transparent",
    //cursor: "pointer",
  },
  "&:focus-visible": {
    outline: "3px solid",
    outlineColor: "hsla(210, 98%, 48%, 0.5)",
    outlineOffset: "2px",
  },
}));

const SyledCardContent = styled(CardContent)({
  display: "flex",
  flexDirection: "column",
  gap: 4,
  padding: 16,
  flexGrow: 1,
  "&:last-child": {
    paddingBottom: 16,
  },
});

const StyledTypography = styled(Typography)({
  display: "-webkit-box",
  WebkitBoxOrient: "vertical",
  WebkitLineClamp: 2,
  overflow: "hidden",
  textOverflow: "ellipsis",
});

const PlaylistCard = ({ authTokens, playlist, ...props }) => {
  const [focusedCardIndex, setFocusedCardIndex] = useState(null);

  const history = useNavigate();

  const handleFocus = (index) => {
    setFocusedCardIndex(index);
  };

  const handleBlur = () => {
    setFocusedCardIndex(null);
  };

  return (
    <SyledCard
      variant="outlined"
      onFocus={() => handleFocus(0)}
      onBlur={handleBlur}
      tabIndex={0}
      className={focusedCardIndex === 0 ? "Mui-focused" : ""}
    >
      {/* <CardMedia
            component="img"
            alt={playlist.title}
            //image={`https://image.tmdb.org/t/p/w500${playlist.poster_path}`}
            image={`https://picsum.photos/800/450?random=${playlist.id}`}
            sx={{
            aspectRatio: "16 / 9",
            borderBottom: "1px solid",
            borderColor: "divider",
            }}
        /> */}
      <SyledCardContent>
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
          {props.watchlist !== false && (
            <WatchlistButton
              playlist={playlist}
              updateWatchlist={props.updateWatchlist}
              authTokens={authTokens}
            />
          )}
        </Box>

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

        <Typography
          sx={{ cursor: "pointer" }}
          onClick={() => history(`/playlist/${playlist.type}/${playlist.slug}`)}
          gutterBottom
          variant="h6"
          component="div"
        >
          {playlist.title} {playlist.release_date && `(${playlist.release_date})`}
        </Typography>
        <StyledTypography variant="body2" color="text.secondary" gutterBottom>
          {playlist.overview}
        </StyledTypography>

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
              playlist={playlist}
              handleOpenRatingsModal={props.handleOpenRatingsModal}
            />
          </Box>

          {props.rate !== false && (
            <Box
              sx={{
                display: "flex",
                flexDirection: "row",
                alignItems: "center",
              }}
            >
              <RateButton
                playlist={playlist}
                handleOpenRateModal={props.handleOpenRateModal}
              />
            </Box>
          )}
        </Box>
      </SyledCardContent>
    </SyledCard>
  );
};

export default memo(PlaylistCard);
// export default PlaylistCard
