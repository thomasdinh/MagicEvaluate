
import './App.css'
import DeckCard from './components/DeckCard'
import Home from './pages/Home'
import YourDecks from './pages/YourDecks'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/NavBar'

function App() {

  return (
      <>
      <div>
      <main className='main-content'>
        <Routes>
        <Route path="/" element={<Home />}></Route>
        <Route path="/yourdecks" element={<YourDecks />}></Route>
        </Routes>
      </main>
      </div>
      </>
  )
}


export default App

