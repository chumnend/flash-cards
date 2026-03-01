import type { FormEvent } from 'react'
import { Link } from 'react-router-dom'

function LoginPage() {
  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
  }

  return (
    <main className="page page--centered">
      <section className="page-card">
        <header className="page-header">
          <h1 className="page-title">Login</h1>
          <p className="page-subtitle">
            Welcome back. Enter your details to continue.
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
              placeholder="••••••••"
              autoComplete="current-password"
              required
            />
          </label>

          <button type="submit" className="button button--primary form-submit">
            Login
          </button>
        </form>

        <p className="page-footer-text">
          New here? <Link to="/register">Create an account</Link>
        </p>
        <p className="page-footer-text">
          <Link to="/">Back to home</Link>
        </p>
      </section>
    </main>
  )
}

export default LoginPage
