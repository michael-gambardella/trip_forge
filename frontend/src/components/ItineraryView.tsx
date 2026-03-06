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
      <h2 style={{ marginBottom: "0.25rem" }}>
        {trip.destination} &mdash; {trip.start_date} to {trip.end_date}
      </h2>
      <p style={{ color: "#555", marginBottom: "1.5rem" }}>
        Budget: {trip.budget} {trip.budget_currency}
        {trip.purpose && ` · ${trip.purpose}`}
      </p>

      {sortedDays.map((day) => (
        <section key={day} style={{ marginBottom: "1.5rem" }}>
          <h3 style={{ marginBottom: "0.5rem" }}>Day {day}</h3>
          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              fontSize: "0.9rem",
            }}
          >
            <thead>
              <tr style={{ borderBottom: "2px solid #ddd" }}>
                <th style={{ textAlign: "left", padding: "0.4rem 0.6rem", width: 70 }}>
                  Time
                </th>
                <th style={{ textAlign: "left", padding: "0.4rem 0.6rem" }}>Activity</th>
                <th style={{ textAlign: "left", padding: "0.4rem 0.6rem", color: "#555" }}>
                  Notes
                </th>
              </tr>
            </thead>
            <tbody>
              {dayMap.get(day)!.map((item) => (
                <tr key={item.id} style={{ borderBottom: "1px solid #eee" }}>
                  <td style={{ padding: "0.4rem 0.6rem", fontVariantNumeric: "tabular-nums" }}>
                    {item.time}
                  </td>
                  <td style={{ padding: "0.4rem 0.6rem" }}>{item.activity}</td>
                  <td style={{ padding: "0.4rem 0.6rem", color: "#666" }}>{item.notes}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      ))}
    </div>
  );
}
