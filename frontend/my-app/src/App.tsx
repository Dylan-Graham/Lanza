import { useState } from 'react';
import './App.css'
import { Switch } from './components/Switch'
import { MapView } from './map/MapView'
import { TableView } from './table/TableView';

function App() {
  const [isMapVisible, setIsMapVisible] = useState(false);

  const handleToggle = () => {
    setIsMapVisible(!isMapVisible);
  };

  return (
    <>
      <section>
        <div className="hero">
          < Switch isOn={isMapVisible} handleToggle={handleToggle} />
          {isMapVisible ? <MapView /> : <TableView />}
        </div>
        <div>
        </div>
      </section>
    </>
  )
}

export default App
