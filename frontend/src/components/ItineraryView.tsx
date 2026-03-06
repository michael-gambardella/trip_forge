import { ItineraryItem, TripDetail } from "../api/trips";

interface Props {
  trip: TripDetail;
}

function groupByDay(items: ItineraryItem[]): Map<number, ItineraryItem[]> {
  return items.reduce((map, item) => {
    const group = map.get(item.day) ?? [];
    map.set(item.day, [...group, item]);
    return map;
  }, new Map<number, ItineraryItem[]>());
}

export default function ItineraryView({ trip }: Props) {
  const dayMap = groupByDay(trip.itinerary_items);
  const sortedDays = Array.from(dayMap.keys()).sort((a, b) => a - b);

  return (
    <div>
      <div className="itinerary-header">
        <h2>
          {trip.destination} &mdash; {trip.start_date} to {trip.end_date}
        </h2>
        <p className="itinerary-meta">
          Budget: {trip.budget} {trip.budget_currency}
          {trip.purpose && ` · ${trip.purpose}`}
        </p>
      </div>

      {sortedDays.map((day) => (
        <div key={day} className="day-card">
          <div className="day-header">
            <span className="day-badge">Day {day}</span>
          </div>
          <table className="itinerary-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Activity</th>
                <th>Notes</th>
              </tr>
            </thead>
            <tbody>
              {dayMap.get(day)!.map((item) => (
                <tr key={item.id}>
                  <td className="time-cell">{item.time}</td>
                  <td>{item.activity}</td>
                  <td className="notes-cell">{item.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  );
}
