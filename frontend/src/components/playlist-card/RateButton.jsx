import React from "react";
import Button from "@mui/material/Button";
import { blue } from "@mui/material/colors";
import StarRateIcon from "@mui/icons-material/StarRate";
import StarBorderIcon from "@mui/icons-material/StarBorder";

export default function RateButton({ ...props }) {

  return (
    <>
      {props.playlist.user_rate ? (
        <Button
          variant="outlined"
          //size="small"
          sx={{ color: blue[700], border: "none" }}
          startIcon={<StarRateIcon />}
          onClick={() => props.handleOpenRateModal(props.playlist)}
        >
          {props.playlist.user_rate}
        </Button>
      ) : (
        <Button
          variant="outlined"
          //size="small"
          sx={{ color: blue[700], border: "none" }}
          startIcon={<StarBorderIcon />}
          onClick={() => props.handleOpenRateModal(props.playlist)}
        >
          Rate
        </Button>
      )}
    </>
  );
}
