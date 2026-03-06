import { FormEvent, useState } from "react";

import { CreateTripPayload, TripDetail, createTrip } from "../api/trips";

interface Props {
  onTripCreated: (trip: TripDetail) => void;
}

const EMPTY_FORM: CreateTripPayload = {
  destination: "",
  start_date: "",
  end_date: "",
  budget: "",
  budget_currency: "USD",
  purpose: "",
};

export default function TripForm({ onTripCreated }: Props) {
  const [form, setForm] = useState<CreateTripPayload>(EMPTY_FORM);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function handleChange(
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const trip = await createTrip(form);
      onTripCreated(trip);
      setForm(EMPTY_FORM);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ marginBottom: "2rem" }}>
      <h2>Plan a Business Trip</h2>

      <div style={{ marginBottom: "0.75rem" }}>
        <label htmlFor="destination" style={{ display: "block", marginBottom: "0.25rem" }}>
          Destination *
        </label>
        <input
          id="destination"
          name="destination"
          value={form.destination}
          onChange={handleChange}
          required
          placeholder="e.g. New York, NY"
          style={{ width: "100%", padding: "0.5rem" }}
        />
      </div>

      <div style={{ display: "flex", gap: "1rem", marginBottom: "0.75rem" }}>
        <div style={{ flex: 1 }}>
          <label htmlFor="start_date" style={{ display: "block", marginBottom: "0.25rem" }}>
            Start Date *
          </label>
          <input
            id="start_date"
            name="start_date"
            type="date"
            value={form.start_date}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        <div style={{ flex: 1 }}>
          <label htmlFor="end_date" style={{ display: "block", marginBottom: "0.25rem" }}>
            End Date *
          </label>
          <input
            id="end_date"
            name="end_date"
            type="date"
            value={form.end_date}
            onChange={handleChange}
            required
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
      </div>

      <div style={{ display: "flex", gap: "1rem", marginBottom: "0.75rem" }}>
        <div style={{ flex: 2 }}>
          <label htmlFor="budget" style={{ display: "block", marginBottom: "0.25rem" }}>
            Budget *
          </label>
          <input
            id="budget"
            name="budget"
            type="number"
            step="0.01"
            min="0"
            value={form.budget}
            onChange={handleChange}
            required
            placeholder="e.g. 2500"
            style={{ width: "100%", padding: "0.5rem" }}
          />
        </div>
        <div style={{ flex: 1 }}>
          <label
            htmlFor="budget_currency"
            style={{ display: "block", marginBottom: "0.25rem" }}
          >
            Currency
          </label>
          <select
            id="budget_currency"
            name="budget_currency"
            value={form.budget_currency}
            onChange={handleChange}
            style={{ width: "100%", padding: "0.5rem" }}
          >
            <option value="USD">USD</option>
            <option value="EUR">EUR</option>
            <option value="GBP">GBP</option>
            <option value="JPY">JPY</option>
            <option value="CAD">CAD</option>
          </select>
        </div>
      </div>

      <div style={{ marginBottom: "0.75rem" }}>
        <label htmlFor="purpose" style={{ display: "block", marginBottom: "0.25rem" }}>
          Trip Purpose
        </label>
        <textarea
          id="purpose"
          name="purpose"
          value={form.purpose}
          onChange={handleChange}
          placeholder="e.g. Q2 sales conference, client meetings"
          rows={3}
          style={{ width: "100%", padding: "0.5rem" }}
        />
      </div>

      {error && (
        <p style={{ color: "crimson", marginBottom: "0.75rem" }}>{error}</p>
      )}

      <button
        type="submit"
        disabled={loading}
        style={{ padding: "0.6rem 1.5rem", cursor: loading ? "not-allowed" : "pointer" }}
      >
        {loading ? "Generating itinerary…" : "Generate Itinerary"}
      </button>
    </form>
  );
}
