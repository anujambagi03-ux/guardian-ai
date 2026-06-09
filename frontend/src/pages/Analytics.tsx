import { useEffect, useState } from "react";
import api from "../services/api";

function Analytics() {

  const [data, setData] = useState({
    total_vehicles: 0,
    cars: 0,
    motorcycles: 0,
    buses: 0,
    trucks: 0,
  });

  useEffect(() => {
    api
      .get("/analytics")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <div className="container-fluid">

      <h1 className="mb-4">
        📊 Traffic Analytics
      </h1>

      <div className="row g-4">

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6>Total Vehicles</h6>
              <h2>{data.total_vehicles}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6>Cars</h6>
              <h2>{data.cars}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-4">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6>Motorcycles</h6>
              <h2>{data.motorcycles}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6>Buses</h6>
              <h2>{data.buses}</h2>
            </div>
          </div>
        </div>

        <div className="col-md-6">
          <div className="card shadow border-0">
            <div className="card-body">
              <h6>Trucks</h6>
              <h2>{data.trucks}</h2>
            </div>
          </div>
        </div>

      </div>

    </div>
  );
}

export default Analytics;