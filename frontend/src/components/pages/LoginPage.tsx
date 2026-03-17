import { useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { loginUser } from '../../helpers/api/auth'

function LoginPage() {
  const navigate = useNavigate()
  const [formValues, setFormValues] = useState({
    email: '',
    password: '',
  })
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    setFormValues((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    if (isSubmitting) return

    const email = formValues.email.trim()
    const password = formValues.password

    setError(null)
    setIsSubmitting(true)

    try {
      const auth = await loginUser({ email, password })

      // Simple client-side auth persistence; can be replaced with context later
      window.localStorage.setItem('flashly_token', auth.token)
      window.localStorage.setItem('flashly_user', JSON.stringify(auth.user))

      navigate('/')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Something went wrong. Please try again.'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
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
              value={formValues.email}
              onChange={handleChange}
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
              value={formValues.password}
              onChange={handleChange}
              required
            />
          </label>

          {error && <p className="form-error">{error}</p>}

          <button type="submit" className="button button--primary form-submit" disabled={isSubmitting}>
            {isSubmitting ? 'Logging in...' : 'Login'}
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
