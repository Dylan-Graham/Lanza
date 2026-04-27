import lanzaroteImg from './assets/lanzarote-hi-res.jpg'
import onestar from './assets/1-star.png'
import './App.css'

function App() {

  return (
    <>
      <section>
        <div className="hero">
          <img src={lanzaroteImg} className="base-image" alt="Lanzarote" />
          <img src={onestar} className="overlay-star pulsing-image"/>
        </div>
        <div>
        </div>
      </section>
    </>
  )
}

export default App
