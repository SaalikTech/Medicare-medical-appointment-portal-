import { useState } from "react";
import api from "./api/axios";

function BookingForm() {
  const [doctor, setDoctor] = useState("");
  const [date, setDate] = useState("");
  const [time, setTime] = useState("");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();
    setMessage("");
    setLoading(true);

    try {
      const csrfResponse = await api.get("/api/csrf-token");
      const csrfToken = csrfResponse.data.csrf_token;

      const response = await api.post(
        "/api/book",
        { dr: doctor, date, time, reason },
        {
          headers: {
            "X-CSRFToken": csrfToken,
          },
        }
      );

      setMessage(
        response.data.message || "Appointment booked successfully!"
      );

      setDoctor("");
      setDate("");
      setTime("");
      setReason("");
    } catch (error: any) {
      setMessage(
        error.response?.data?.error ||
          "Unable to book your appointment. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="booking-page">
      <section className="booking-card">
        <h1>Book an Appointment</h1>
        <p>Choose your doctor and preferred appointment time.</p>

        <form onSubmit={handleSubmit}>
          <label htmlFor="doctor">Doctor</label>
          <input
            id="doctor"
            value={doctor}
            onChange={(event) => setDoctor(event.target.value)}
            placeholder="Enter doctor's name"
            required
          />

          <label htmlFor="date">Appointment date</label>
          <input
            id="date"
            type="date"
            min={new Date().toISOString().split("T")[0]}
            value={date}
            onChange={(event) => setDate(event.target.value)}
            required
          />

          <label htmlFor="time">Appointment time</label>
          <input
            id="time"
            type="time"
            value={time}
            onChange={(event) => setTime(event.target.value)}
            required
          />

          <label htmlFor="reason">Reason for visit (optional)</label>
          <textarea
            id="reason"
            value={reason}
            onChange={(event) => setReason(event.target.value)}
            placeholder="Briefly describe your reason for visiting"
          />

          <button type="submit" disabled={loading}>
            {loading ? "Booking..." : "Book Appointment"}
          </button>
        </form>

        {message && <p role="status">{message}</p>}
      </section>
    </main>
  );
}

export default BookingForm;
