import { useState } from 'react'
import { Link } from 'react-router-dom'

import { checkApiStatus  } from '../helpers/api'

type StatusState = {
  message: string
}

function HomePage() {
  const [status, setStatus] = useState<StatusState | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleCheckApiStatus = async () => {
    try {
      setIsLoading(true)
      setError(null)
      setStatus(null)

      const { message } = await checkApiStatus()
      setStatus({ message })
    } catch (err) {
      const errorMessage =
        err instanceof Error ? err.message : 'Unable to reach API.'
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="page page--centered">
      <section className="page-card">
        <header className="page-header">
          <h1 className="page-title">Flashly</h1>
          <p className="page-subtitle">
            A smarter way to build and review your decks.
          </p>
        </header>

        <div className="button-row">
          <Link to="/login" className="button button--primary">
            Login
          </Link>
          <span> / </span>
          <Link to="/register" className="button button--secondary">
            Create account
          </Link>
        </div>

        <section className="status-section">
          <h2 className="status-title">API connection</h2>
          <button
            type="button"
            className="button button--ghost"
            onClick={handleCheckApiStatus}
            disabled={isLoading}
          >
            {isLoading ? 'Checking…' : 'Check API status'}
          </button>
          <div className="status-output">
            {isLoading && <p>Contacting backend…</p>}
            {!isLoading && status && (
              <p className="status-ok">Status: {status.message}</p>
            )}
            {!isLoading && error && (
              <p className="status-error">Error: {error}</p>
            )}
            {!isLoading && !status && !error && (
              <p className="status-muted">
                Click &quot;Check API status&quot; to verify the connection.
              </p>
            )}
          </div>
        </section>
      </section>
    </main>
  )
}

export default HomePage
