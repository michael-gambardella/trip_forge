import { useState } from "react";

import ItineraryView from "./components/ItineraryView";
import TripForm from "./components/TripForm";
import { TripDetail } from "./api/trips";

export default function App() {
  const [trip, setTrip] = useState<TripDetail | null>(null);

  return (
    <div className="app">
      <header className="app-header">
        <h1>TripForge</h1>
        <p>AI-powered business travel planner</p>
      </header>

      <TripForm onTripCreated={setTrip} />

      {trip && <ItineraryView trip={trip} />}
    </div>
  );
}
