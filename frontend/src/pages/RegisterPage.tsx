import type { FormEvent } from 'react'
import { Link } from 'react-router-dom'

function RegisterPage() {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
  }

  return (
    <main className="page page--centered">
      <section className="page-card">
        <header className="page-header">
          <h1 className="page-title">Create your account</h1>
          <p className="page-subtitle">
            Start building decks in a few seconds.
          </p>
        </header>

        <form className="form" onSubmit={handleSubmit}>
          <label className="form-field">
            <span className="form-label">Email</span>
            <input
              type="email"
              name="email"
              className="form-input"
              placeholder="you@example.com"
              autoComplete="email"
              required
            />
          </label>

          <label className="form-field">
            <span className="form-label">Password</span>
            <input
              type="password"
              name="password"
              className="form-input"
              placeholder="Create a password"
              autoComplete="new-password"
              required
            />
          </label>

          <label className="form-field">
            <span className="form-label">Confirm password</span>
            <input
              type="password"
              name="confirmPassword"
              className="form-input"
              placeholder="Repeat your password"
              autoComplete="new-password"
              required
            />
          </label>

          <button type="submit" className="button button--primary form-submit">
            Create account
          </button>
        </form>

        <p className="page-footer-text">
          Already have an account? <Link to="/login">Login</Link>
        </p>
        <p className="page-footer-text">
          <Link to="/">Back to home</Link>
        </p>
      </section>
    </main>
  )
}

export default RegisterPage
