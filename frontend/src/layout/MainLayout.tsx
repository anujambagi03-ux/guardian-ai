import { Link, Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <div className="d-flex">
      {/* Sidebar */}
      <div
        className="bg-dark text-white p-3"
        style={{
          width: "250px",
          minHeight: "100vh",
        }}
      >
        <h3>Guardian AI</h3>

        <hr />

        <ul className="nav flex-column">

          <li className="nav-item">
            <Link className="nav-link text-white" to="/">
              Dashboard
            </Link>
          </li>

          <li className="nav-item">
            <Link className="nav-link text-white" to="/vehicles">
              Vehicle Detection
            </Link>
          </li>

          <li className="nav-item">
            <Link className="nav-link text-white" to="/violations">
              Violations
            </Link>
          </li>

          <li className="nav-item">
            <Link className="nav-link text-white" to="/accidents">
              Accident Detection
            </Link>
          </li>

          <li className="nav-item">
            <Link className="nav-link text-white" to="/analytics">
              Analytics
            </Link>
          </li>

          <li className="nav-item">
            <Link className="nav-link text-white" to="/reports">
              Reports
            </Link>
          </li>

          <li className="nav-item">
            <Link className="nav-link text-white" to="/settings">
              Settings
            </Link>
          </li>

        </ul>
      </div>

      {/* Content */}

      <div className="container-fluid p-4">
        <Outlet />
      </div>
    </div>
  );
}

export default MainLayout;