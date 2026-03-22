import { useState } from 'react'
import type { ChangeEvent, FormEvent } from 'react'
import { Link, useNavigate } from 'react-router-dom'

import { registerUser } from '../../../helpers/api/auth'
import Page from '../../layout/Page';

const RegisterPage = () => {
  const navigate = useNavigate();

  const [formValues, setFormValues] = useState({
    firstName: '',
    lastName: '',
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = event.target
    setFormValues((prev) => ({
      ...prev,
      [name]: value,
    }))
  };

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()

    if (isSubmitting) return

    const { firstName, lastName, username, email, password, confirmPassword } = formValues

    if (password !== confirmPassword) {
      setError('Passwords do not match')
      return
    }

    setError(null)
    setIsSubmitting(true)

    try {
      const auth = await registerUser({
        firstName: firstName.trim(),
        lastName: lastName.trim(),
        username: username.trim(),
        email: email.trim(),
        password,
      })

      window.localStorage.setItem('flashly_token', auth.token)
      window.localStorage.setItem('flashly_user', JSON.stringify(auth.user))

      navigate('/login')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Something went wrong. Please try again.'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <Page>
      <section className="page-card">
        <header className="page-header">
          <h1 className="page-title">Create your account</h1>
          <p className="page-subtitle">
            Start building decks in a few seconds.
          </p>
        </header>

        <form className="form" onSubmit={handleSubmit}>
          <label className="form-field">
            <span className="form-label">First name</span>
            <input
              type="text"
              name="firstName"
              className="form-input"
              placeholder="Jane"
              autoComplete="given-name"
              value={formValues.firstName}
              onChange={handleChange}
              required
            />
          </label>

          <label className="form-field">
            <span className="form-label">Last name</span>
            <input
              type="text"
              name="lastName"
              className="form-input"
              placeholder="Doe"
              autoComplete="family-name"
              value={formValues.lastName}
              onChange={handleChange}
              required
            />
          </label>

          <label className="form-field">
            <span className="form-label">Username</span>
            <input
              type="text"
              name="username"
              className="form-input"
              placeholder="flashlyfan"
              autoComplete="username"
              value={formValues.username}
              onChange={handleChange}
              required
            />
          </label>

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
              placeholder="Create a password"
              autoComplete="new-password"
              value={formValues.password}
              onChange={handleChange}
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
              value={formValues.confirmPassword}
              onChange={handleChange}
              required
            />
          </label>

          {error && <p className="form-error">{error}</p>}

          <button type="submit" className="button button--primary form-submit" disabled={isSubmitting}>
            {isSubmitting ? 'Creating account...' : 'Create account'}
          </button>
        </form>

        <p className="page-footer-text">
          Already have an account? <Link to="/login">Login</Link>
        </p>
        <p className="page-footer-text">
          <Link to="/">Back to home</Link>
        </p>
      </section>
    </Page>
  )
}

export default RegisterPage
