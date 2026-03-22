import { Link } from 'react-router-dom'

import Page from '../../layout/Page'

const NotFoundPage = () => {
  return (
    <Page>
      <section className="page-card">
        <header className="page-header">
          <h1 className="page-title">Page not found</h1>
          <p className="page-subtitle">
            The page you are looking for does not exist.
          </p>
        </header>

        <p className="page-footer-text">
          <Link to="/">Return to home</Link>
        </p>
      </section>
    </Page>
  )
}

export default NotFoundPage

