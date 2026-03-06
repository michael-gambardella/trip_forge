const API_BASE = "/api";

export interface ItineraryItem {
  id: number;
  day: number;
  time: string;
  activity: string;
  notes: string;
}

export interface Trip {
  id: number;
  destination: string;
  start_date: string;
  end_date: string;
  budget: string;
  budget_currency: string;
  purpose: string;
  created_at: string;
}

export interface TripDetail extends Trip {
  itinerary_items: ItineraryItem[];
}

export interface CreateTripPayload {
  destination: string;
  start_date: string;
  end_date: string;
  budget: string;
  budget_currency: string;
  purpose: string;
}

export async function createTrip(payload: CreateTripPayload): Promise<TripDetail> {
  const response = await fetch(`${API_BASE}/trips/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown error" }));
    throw new Error(
      (error as { detail?: string }).detail ?? `Request failed: ${response.status}`
    );
  }

  return response.json() as Promise<TripDetail>;
}

export async function getTrip(id: number): Promise<TripDetail> {
  const response = await fetch(`${API_BASE}/trips/${id}/`);
  if (!response.ok) {
    throw new Error(`Trip not found: ${response.status}`);
  }
  return response.json() as Promise<TripDetail>;
}

export async function listTrips(): Promise<Trip[]> {
  const response = await fetch(`${API_BASE}/trips/`);
  if (!response.ok) {
    throw new Error(`Failed to fetch trips: ${response.status}`);
  }
  return response.json() as Promise<Trip[]>;
}
