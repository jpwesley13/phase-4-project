import { useRouteError, NavLink } from "react-router-dom";
import Header from "../components/Header";

function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <>
    <header>
    <nav className="navbar">
            <div className="navbutton">
                <NavLink
                to="/"
                >
                    Home
                </NavLink>
                <NavLink
                to="/trainers"
                >
                    Contributors
                </NavLink>
                <NavLink
                to="/sightings"
                >
                    Rare Sightings
                </NavLink>
            </div>
    </nav>
    </header>
    <Header />
    <hr />
      <main>
        <h1>You're in deep, uncharted territory now. Better play it safe and try another page!</h1>
      </main>
    </>
  );
}

export default ErrorPage;