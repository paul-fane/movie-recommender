import Rating from "@mui/material/Rating";
import React, { useState, useEffect } from "react";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";

const SyledTypography = styled(Typography)(({ theme }) => ({
  cursor: "pointer",
  //textDecoration: "underline",
  "&:hover": {
    textDecoration: "underline",
  },
}));

export default function ShowRating({ ...props }) {

  return (
    <>
      <Typography variant="caption">{props.playlist.rating_avg}</Typography>
      <Rating
        name="half-rating-read"
        //defaultValue={parseFloat(props.playlist.rating_avg)}
        value={props.playlist.rating_avg}
        precision={0.1}
        readOnly
        size="small"
      />
      <SyledTypography onClick={()=>props.handleOpenRatingsModal(props.playlist)} variant="caption">
        ({props.playlist.rating_count} reviews)
      </SyledTypography>
    </>
  );
}
