import { useEffect, useState } from "react";
import api from "../services/api";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Legend,
} from "recharts";

function Analytics() {
  const [data, setData] = useState({
    total_vehicles: 0,
    cars: 0,
    motorcycles: 0,
    buses: 0,
    trucks: 0,
    total_violations: 0,
    total_accidents: 0,
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

  const vehicleData = [
    {
      name: "Cars",
      value: data.cars,
    },
    {
      name: "Motorcycles",
      value: data.motorcycles,
    },
    {
      name: "Buses",
      value: data.buses,
    },
    {
      name: "Trucks",
      value: data.trucks,
    },
  ];

  const summaryData = [
    {
      name: "Violations",
      count: data.total_violations,
    },
    {
      name: "Accidents",
      count: data.total_accidents,
    },
  ];

  const COLORS = [
    "#0d6efd",
    "#20c997",
    "#ffc107",
    "#dc3545",
  ];

  return (
    <div className="container-fluid">

      <h1 className="mb-4 fw-bold">
        📊 Guardian AI Analytics Dashboard
      </h1>

      {/* Top Stats */}

      <div className="row g-4 mb-4">

        <div className="col-lg-3 col-md-6">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h6>Total Vehicles</h6>
              <h2>{data.total_vehicles}</h2>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h6>Cars</h6>
              <h2>{data.cars}</h2>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h6>Buses</h6>
              <h2>{data.buses}</h2>
            </div>
          </div>
        </div>

        <div className="col-lg-3 col-md-6">
          <div className="card shadow border-0">
            <div className="card-body text-center">
              <h6>Trucks</h6>
              <h2>{data.trucks}</h2>
            </div>
          </div>
        </div>

      </div>

      {/* Charts */}

      <div className="row g-4">

        <div className="col-lg-6">

          <div className="card shadow border-0">
            <div className="card-body">

              <h4 className="mb-4">
                🚗 Vehicle Distribution
              </h4>

              <ResponsiveContainer
                width="100%"
                height={350}
              >
                <PieChart>

                  <Pie
                    data={vehicleData}
                    cx="50%"
                    cy="50%"
                    outerRadius={120}
                    dataKey="value"
                    label
                  >
                    {vehicleData.map((entry, index) => (
                      <Cell
                        key={index}
                        fill={
                          COLORS[
                            index % COLORS.length
                          ]
                        }
                      />
                    ))}
                  </Pie>

                  <Tooltip />

                </PieChart>
              </ResponsiveContainer>

            </div>
          </div>

        </div>

        <div className="col-lg-6">

          <div className="card shadow border-0">
            <div className="card-body">

              <h4 className="mb-4">
                🚨 Incident Overview
              </h4>

              <ResponsiveContainer
                width="100%"
                height={350}
              >

                <BarChart
                  data={summaryData}
                >

                  <CartesianGrid strokeDasharray="3 3" />

                  <XAxis dataKey="name" />

                  <YAxis />

                  <Tooltip />

                  <Legend />

                  <Bar
                    dataKey="count"
                    fill="#0d6efd"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>
          </div>

        </div>

      </div>

      {/* Alert Cards */}

      <div className="row mt-4 g-4">

        <div className="col-md-6">

          <div className="card shadow border-0">

            <div className="card-body text-center">

              <h4>
                🚨 Violations
              </h4>

              <h1 className="text-danger">
                {data.total_violations}
              </h1>

              <p className="text-muted">
                Total violations detected
              </p>

            </div>

          </div>

        </div>

        <div className="col-md-6">

          <div className="card shadow border-0">

            <div className="card-body text-center">

              <h4>
                🚑 Accident Alerts
              </h4>

              <h1 className="text-warning">
                {data.total_accidents}
              </h1>

              <p className="text-muted">
                Total accident alerts generated
              </p>

            </div>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Analytics;