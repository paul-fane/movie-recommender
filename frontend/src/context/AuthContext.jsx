import { createContext, useState, useEffect } from "react";
// import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";
// import PropTypes from "prop-types";

const AuthContext = createContext();

export default AuthContext;

// eslint-disable-next-line react/prop-types
export const AuthProvider = ({ children }) => {
  // If there are tokens in local storage set it
  let [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("authTokens")
      ? JSON.parse(localStorage.getItem("authTokens"))
      : null
  );

  // Get the user data
  let [user, setUser] = useState(null);
  // The page are loading
  let [loading, setLoading] = useState(true);

  const history = useNavigate();

  useEffect(() => {
    let getUser = async () => {
      let response = await fetch("http://127.0.0.1:8000/api/users/me/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + String(authTokens.access),
        },
      });
      let data = await response.json();
      
      if (user !== data){
        setUser(data);
      }

      
    };
    if (user === null){
      getUser();
    }
    
  }, [authTokens, loading]);

  

  let loginUser = (data) => {
    console.log(data)
    setAuthTokens(data);
    localStorage.setItem("authTokens", JSON.stringify(data));
    history("/");
  };

  let logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("authTokens");
    history("/login");
  };

  let updateToken = async () => {
    let response = await fetch("http://127.0.0.1:8000/api/auth/token/refresh/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ refresh: authTokens?.refresh }),
    });
    let data = await response.json();

    if (response.status === 200) {
      setAuthTokens(data);
      localStorage.setItem("authTokens", JSON.stringify(data));
    } //else{
    //    logoutUser()
    //}

    // After the first load of the page set the loading to false
    if (loading) {
      setLoading(false);
    }
  };

  let contextData = {
    user: user,
    authTokens: authTokens,
    loginUser: loginUser,
    logoutUser: logoutUser,
  };

  useEffect(() => {
    // Refresh the tokens on the first load
    if (loading) {
      updateToken();
    }

    // Update token every 29 minutes
    let time = 1000 * 60 * 29;
    let interval = setInterval(() => {
      if (authTokens) {
        updateToken();
      }
    }, time);
    return () => clearInterval(interval);
  }, [authTokens, loading]);

  return (
    <AuthContext.Provider value={contextData}>
      {
        // If loading is true then the token shuld be update
        loading ? null : children
      }
    </AuthContext.Provider>
  );
};


// AuthProvider.propTypes = {
//   children: PropTypes.node.isRequired, // or PropTypes.node (if it's optional)
// };