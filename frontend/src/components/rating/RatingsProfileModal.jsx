import  { useState, useEffect } from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Modal from "@mui/material/Modal";
import ReviewCard from "./ReviewCard";
import CircularProgress from "@mui/material/CircularProgress";
import KeyboardArrowDownIcon from "@mui/icons-material/KeyboardArrowDown";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";

const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 500,
  height: "80vh",
  //maxHeight: "80vh", // To restrict the height within the viewport
  overflowY: "auto", // Enable scrolling

  bgcolor: "background.paper",
  //border: "2px solid #000",
  boxShadow: 24,
  p: 4,
  // display: "flex",
  // flexDirection: "column",
  // alignItems: "center",
};

const RatingsProfileModal = ({ ...props }) => {
  const [loading, setLoading] = useState(false);
  const [ratings, setRatings] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [queryStars, setQueryStars] = useState("see_all");

  useEffect(() => {
    fetchRatings(props.profileUsername);
  }, [props.profileUsername, queryStars]);

  const fetchRatings = async (profileUsername, url) => {
    if (!url) {
      url = `http://127.0.0.1:8000/api/ratings/user-list/${profileUsername}?query=${queryStars}`;
      if (props.compar) {
        url = `http://127.0.0.1:8000/api/ratings/compar-list/${profileUsername}?query=${queryStars}`;
      }
    }

    setLoading(true);
    if (props.user){
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + String(props.authTokens.access),
          },
        });
  
        if (response.status === 200) {
          const data = await response.json();
          setRatings((prevItems) => [...prevItems, ...data.results]);
          //setRatings(data.results);
          setNextPage(data.next);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    } else {
      try {
        const response = await fetch(url, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });
  
        if (response.status === 200) {
          const data = await response.json();
          setRatings((prevItems) => [...prevItems, ...data.results]);
          //setRatings(data.results);
          setNextPage(data.next);
        }
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        setLoading(false);
      }
    }
    
  };

  const handleQueryChange = (event) => {
    setRatings([]);
    setQueryStars(event.target.value);
  };

  return (
    <Modal
      open={props.openRatingsModal}
      onClose={props.handleCloseRatingsModal}
      aria-labelledby="modal-modal-title"
      aria-describedby="modal-modal-description"
    >
      <Box sx={style}>
        <Typography
          id="modal-modal-description"
          variant="h4"
          component="h2"
          sx={{ mt: 2, color: "grey" }}
        >
          {props.profileUsername}
        </Typography>
        <Typography
          sx={{
            marginBottom: "1rem",
          }}
          variant="h2"
          component="h2"
        >
          {props.compar ? "User comparison reviews" : "User reviews"}
        </Typography>

        <FormControl
          sx={{
            width: { xs: "100%", md: "25ch" },
            display: "flex",
            flexDirection: "row",
            alignItems: "flex-end",
            marginBottom: "1rem",
          }}
          variant="outlined"
        >
          <Typography
            fontSize={"1.3rem"}
            sx={{
              marginRight: "1rem",
            }}
          >
            Ratings
          </Typography>
          <Select
            value={queryStars}
            size="small"
            onChange={handleQueryChange}
            name="stars"
            sx={{ flexGrow: 1 }}
            //label="Show all"
          >
            <MenuItem value="see_all">Show all</MenuItem>
            <MenuItem value="1">1 star</MenuItem>
            <MenuItem value="2">2 stars</MenuItem>
            <MenuItem value="3">3 stars</MenuItem>
            <MenuItem value="4">4 stars</MenuItem>
            <MenuItem value="5">5 stars</MenuItem>
          </Select>
        </FormControl>

        {ratings
          .filter((item) => item.playlist !== null)
          .map((rating) => (
            <ReviewCard
              key={rating.id}
              rating={rating}
              colorStar={
                props.user && props.user.username === props.profileUsername
                  ? "blue"
                  : "green"
              }
            />
          ))}

        {nextPage !== null && loading === false && (
          <Button
            onClick={() => fetchRatings(props.profileUsername, nextPage)}
            variant="text"
            endIcon={<KeyboardArrowDownIcon />}
          >
            Load 20 more
          </Button>
        )}

        {loading === true && (
          <Box
            sx={{
              display: "flex",
              justifyContent: "center",
              marginTop: "30px",
            }}
          >
            <CircularProgress />
          </Box>
        )}
      </Box>
    </Modal>
  );
};

export default RatingsProfileModal;
