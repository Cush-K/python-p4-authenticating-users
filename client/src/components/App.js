import Login from "./Login"
import Navbar from "./Navbar"
import { useState, useEffect } from "react";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/check_session").then((response) => {
      if (response.ok) {
        response.json().then((user) => setUser(user));
      }
    });
  }, []);

  function handleLogout() {
    setUser(null); 
  }

  if (user) {
    return (
      <div>
        <Navbar onLogout={handleLogout}/>
        <h2>Welcome, {user.username}!</h2>
      </div>
  );
  } else {
    return(
    <div>
      <Navbar onLogout={handleLogout}/>
      <Login onLogin={setUser} />
    </div>)
    ;
  }
}

export default App;
