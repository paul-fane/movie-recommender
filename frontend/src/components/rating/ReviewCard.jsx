import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";
import Button from "@mui/material/Button";
import { blue, green } from "@mui/material/colors";
import StarRateIcon from "@mui/icons-material/StarRate";

const SyledCard = styled(Card)(({ theme }) => ({
  display: "flex",
  flexDirection: "column",
  padding: 0,
  //height: "100%",
  borderRadius: "6px",
  marginBottom: "3px",
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

const StyledTitle = styled(Typography)({
  display: "-webkit-box",
  WebkitBoxOrient: "vertical",
  WebkitLineClamp: 1,
  overflow: "hidden",
  textOverflow: "ellipsis",
});

const ReviewCard = ({ rating, ...props }) => {
  const [focusedCardIndex, setFocusedCardIndex] = useState(null);

  const history = useNavigate();

  const handleFocus = (index) => {
    setFocusedCardIndex(index);
  };

  const handleBlur = () => {
    setFocusedCardIndex(null);
  };

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    const yyyy = date.getFullYear();
    let mm = date.getMonth() + 1; // month is zero-based
    let dd = date.getDate();

    if (dd < 10) dd = "0" + dd;
    if (mm < 10) mm = "0" + mm;

    const formatted = dd + "/" + mm + "/" + yyyy;
    return formatted;
  };

  return (
    <SyledCard
      variant="outlined"
      onFocus={() => handleFocus(0)}
      onBlur={handleBlur}
      tabIndex={0}
      className={focusedCardIndex === 0 ? "Mui-focused" : ""}
    >
      <SyledCardContent>
        <StyledTitle
          sx={{ cursor: "pointer" }}
          onClick={() =>
            history(`/playlist/${rating.playlist.type}/${rating.playlist.slug}`)
          }
          gutterBottom
          variant="h6"
          component="div"
        >
          {rating.playlist.title}
        </StyledTitle>

        <Typography
          fontSize={12}
          variant="body2"
          color="text.secondary"
          gutterBottom
        >
          {rating.timestamp && formatDate(rating.timestamp)}
        </Typography>

        <Button
          variant="outlined"
          //size="small"
          sx={{
            color: props.colorStar === "blue" ? blue[700] : green[700],
            border: "none",
          }}
          startIcon={<StarRateIcon />}
        >
          {rating.value}
        </Button>

        {rating.review_text !== null && (
          <StyledTypography variant="body2" color="text.secondary" gutterBottom>
            {rating.review_text}
          </StyledTypography>
        )}
      </SyledCardContent>
    </SyledCard>
  );
};

export default ReviewCard;
