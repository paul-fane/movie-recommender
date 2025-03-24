import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import SearchRoundedIcon from "@mui/icons-material/SearchRounded";
import InputAdornment from "@mui/material/InputAdornment";
import OutlinedInput from "@mui/material/OutlinedInput";


export default function Search({ ...props }) {
  
    return (
      <>
        <FormControl
          sx={{
            width: { xs: "100%", md: "25ch" },
            display: "flex",
            flexDirection: "row",
          }}
          variant="outlined"
        >
          <Select
            value={props.querySearch.sort_by}
            onChange={props.handleQueryChange}
            name="sort_by"
            sx={{ flexGrow: 1 }}
          >
            <MenuItem value="popular">Popular</MenuItem>
            <MenuItem value="unpopular">Unpopular</MenuItem>
            <MenuItem value="-rating_avg">Top rated</MenuItem>
            <MenuItem value="rating_avg">Low rated</MenuItem>
            <MenuItem value="-release_date">Recent</MenuItem>
            <MenuItem value="release_date">Old</MenuItem>
          </Select>
        </FormControl>
        <FormControl
          sx={{
            width: { xs: "100%", md: "25ch" },
            display: "flex",
            flexDirection: "row",
          }}
          variant="outlined"
        >
          <OutlinedInput
            size="small"
            name="query"
            onChange={props.handleQueryChange}
            placeholder="Search…"
            sx={{ flexGrow: 1 }}
            startAdornment={
              <InputAdornment position="start" sx={{ color: "text.primary" }}>
                <SearchRoundedIcon fontSize="small" />
              </InputAdornment>
            }
            inputProps={{
              "aria-label": "search",
            }}
          />
        </FormControl>
      </>
    );
  }