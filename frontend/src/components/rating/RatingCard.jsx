import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";
import Rating from "@mui/material/Rating";

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

const RatingCard = ({ rating, ...props }) => {
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
        <Typography
          sx={{ cursor: "pointer" }}
          onClick={() => history(`/user/${rating.username}`)}
          gutterBottom
          variant="h6"
          component="div"
        >
          {rating.username}
        </Typography>

        <Rating
          name="simple-controlled"
          value={rating.value}
          precision={1}
          size="small"
        />
        {rating.review_text !== null && (
          <Typography variant="body2" gutterBottom>
            {rating.review_text}
          </Typography>
        )}

        <Typography variant="body2" color="text.secondary" gutterBottom>
          {rating.timestamp && formatDate(rating.timestamp)}
        </Typography>
      </SyledCardContent>
    </SyledCard>
  );
};

export default RatingCard;
