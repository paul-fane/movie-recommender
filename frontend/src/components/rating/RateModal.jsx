import React, { useState, useEffect, useContext } from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import Rating from "@mui/material/Rating";
import TextField from "@mui/material/TextField";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 500,
  bgcolor: "background.paper",
  //border: "2px solid #000",
  boxShadow: 24,
  p: 4,
  display: "flex",
  flexDirection: "column",
  alignItems: "center",
  gap: 1
};

const RateModal = ({ ...props }) => {
  const [ratingValue, setRatingValue] = useState(0);
  const [reviewValue, setReviewValue] = useState("");

  useEffect(() => {
    if (props.playlist.user_rate === null) {
      setRatingValue(0);
    } else {
      setRatingValue(props.playlist.user_rate);
    }
  }, [props.playlist]);

  const ratePlaylist = async (playlist) => {
    const response = await fetch("http://127.0.0.1:8000/api/ratings/create/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + String(props.authTokens.access),
      },
      body: JSON.stringify({
        object_id: playlist.id,
        rating_value: ratingValue,
        ctype: playlist.type,
        review_text: reviewValue
      }),
    });
    
    if (response.status === 201) {
      props.updateRate(playlist.id, ratingValue);
      props.handleCloseRateModal();
    }
  };
  return (
    <Modal
      open={props.openRateModal}
      onClose={props.handleCloseRateModal}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <Typography id="modal-modal-title" variant="h6" component="h2">
          RATE THIS
        </Typography>
        <Typography id="modal-modal-description" sx={{ mt: 2 }}>
          {props.playlist.title}
        </Typography>
        <Rating
          name="simple-controlled"
          value={ratingValue}
          precision={1}
          onChange={(event, newValue) => {
            setRatingValue(newValue);
          }}
        />

        <TextField
          id="outlined-multiline-static"
          label="Write your review here"
          value={reviewValue}
          multiline
          rows={4}
          onChange={(event) => {
            setReviewValue(event.target.value);
          }}
          sx={{
            // Optional custom styling
            "& .MuiOutlinedInput-root": {
              height: "100%",
            },
          }}
        />
        <Button
          onClick={() => ratePlaylist(props.playlist)}
          variant="contained"
        >
          Submit
        </Button>
      </Box>
    </Modal>
  );
};

export default RateModal;
