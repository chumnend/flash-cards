import { Route, Routes } from 'react-router-dom'

import Header from '../../layout/Header'
import Footer from '../../layout/Footer'
import HomePage from '../../pages/HomePage'
import LoginPage from '../../pages/LoginPage'
import RegisterPage from '../../pages/RegisterPage'
import NotFoundPage from '../../pages/NotFoundPage'

const App = () => {
  return (
      <div className='app'>
        <Header />
        <div className='app-main'>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </div>
        <Footer />
      </div>
  )
}
export default App
