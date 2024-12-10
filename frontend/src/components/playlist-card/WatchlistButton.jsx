import React, { useState } from "react";
import Button from "@mui/material/Button";
import CheckIcon from "@mui/icons-material/Check";
import AddIcon from "@mui/icons-material/Add";
import CircularProgress from '@mui/material/CircularProgress';
import { blue } from "@mui/material/colors";

export default function WatchlistButton({ ...props }) {

    const [progress, setProgress] = useState(false)

  const addToWatchlist = async (playlist) => {
    setProgress(true)
    const response = await fetch(
      "http://127.0.0.1:8000/api/watchlists/create/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(props.authTokens.access),
        },
        body: JSON.stringify({ object_id: playlist.id, ctype: playlist.type }),
      }
    );

    if (response.status === 201) {
      props.updateWatchlist(playlist.id, true)
      setProgress(false)
    }
  };

  const removeFromWatchlist = async (playlist) => {
    setProgress(true)
    const response = await fetch(
      `http://127.0.0.1:8000/api/watchlists/delete/${playlist.id}/`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(props.authTokens.access),
        },
      }
    );
    if (response.status === 204) {
      props.updateWatchlist(playlist.id, false)
      setProgress(false)
    }
  };
  
  if (progress){
    return(
        <Button
          variant="outlined"
          size="small"
          sx={{ color: blue[700] }}
          startIcon={<CircularProgress size="1rem" />}
        >
          Watchlist
        </Button>
    )
  }

  return (
    <>
      {props.playlist.in_watchlist ? (
        <Button
          onClick={() => removeFromWatchlist(props.playlist)}
          variant="outlined"
          size="small"
          sx={{ color: blue[700] }}
          startIcon={<CheckIcon />}
        >
          Watchlist
        </Button>
      ) : (
        <Button
          onClick={() => addToWatchlist(props.playlist)}
          variant="outlined"
          size="small"
          sx={{ color: blue[700] }}
          startIcon={<AddIcon />}
        >
          Watchlist
        </Button>
      )}
    </>
  );
}
