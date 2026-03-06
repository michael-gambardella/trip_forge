import { useState } from "react";

import ItineraryView from "./components/ItineraryView";
import TripForm from "./components/TripForm";
import { TripDetail } from "./api/trips";

export default function App() {
  const [trip, setTrip] = useState<TripDetail | null>(null);

  return (
    <div
      style={{
        maxWidth: 800,
        margin: "0 auto",
        padding: "2rem 1rem",
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <header style={{ marginBottom: "2rem" }}>
        <h1 style={{ margin: 0 }}>TripForge</h1>
        <p style={{ color: "#555", marginTop: "0.25rem" }}>
          AI-powered business travel planner
        </p>
      </header>

      <TripForm onTripCreated={setTrip} />

      {trip && <ItineraryView trip={trip} />}
    </div>
  );
}
