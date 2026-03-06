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
    <div className="card">
      <h2 className="form-title">Plan a Business Trip</h2>

      <form onSubmit={handleSubmit}>
        <div className="field">
          <label htmlFor="destination">Destination *</label>
          <input
            id="destination"
            name="destination"
            value={form.destination}
            onChange={handleChange}
            required
            placeholder="e.g. New York, NY"
          />
        </div>

        <div className="field-row">
          <div className="field">
            <label htmlFor="start_date">Start Date *</label>
            <input
              id="start_date"
              name="start_date"
              type="date"
              value={form.start_date}
              onChange={handleChange}
              required
            />
          </div>
          <div className="field">
            <label htmlFor="end_date">End Date *</label>
            <input
              id="end_date"
              name="end_date"
              type="date"
              value={form.end_date}
              onChange={handleChange}
              required
            />
          </div>
        </div>

        <div className="field-row">
          <div className="field">
            <label htmlFor="budget">Budget *</label>
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
            />
          </div>
          <div className="field narrow">
            <label htmlFor="budget_currency">Currency</label>
            <select
              id="budget_currency"
              name="budget_currency"
              value={form.budget_currency}
              onChange={handleChange}
            >
              <option value="USD">USD</option>
              <option value="EUR">EUR</option>
              <option value="GBP">GBP</option>
              <option value="JPY">JPY</option>
              <option value="CAD">CAD</option>
            </select>
          </div>
        </div>

        <div className="field">
          <label htmlFor="purpose">Trip Purpose</label>
          <textarea
            id="purpose"
            name="purpose"
            value={form.purpose}
            onChange={handleChange}
            placeholder="e.g. Q2 sales conference, client meetings"
            rows={3}
          />
        </div>

        {error && <p className="error-msg">{error}</p>}

        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading && <span className="spinner" />}
          {loading ? "Generating itinerary…" : "Generate Itinerary"}
        </button>
      </form>
    </div>
  );
}
