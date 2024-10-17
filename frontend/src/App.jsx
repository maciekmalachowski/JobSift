import React, {useState, useEffect} from 'react';
import './App.css';
import OffersList from './OffersList';

function App() {
  const [job_offers, setJobOffers] = useState([{"name1":"M", "name2":"M2", "name3":"M3"}]);

  useEffect(() => {
    // fetchJobOffers()
  }, []);

  const fetchJobOffers = async () => {
    const response = await fetch("http://127.0.0.1:5000/");
    const data = await response.json();
    setJobOffers(data.job_offers);
    console.log(data.job_offers);
  }

  return (
    <OffersList job_offers={job_offers}/>
  );
}

export default App;
