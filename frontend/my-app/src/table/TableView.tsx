import './TableView.css';
import { useState } from 'react';

import star1 from '../assets/1-star.png';
import star2 from '../assets/2-star.png';
import star3 from '../assets/3-star.png';
import star4 from '../assets/4-star.png';
import star5 from '../assets/5-star.png';
import { useFetch } from '../hooks/useFetch';
import type { SpotForecast, SpotRating } from '../interfaces/SpotRating';

const starImages: Record<number, string> = {
    1: star1,
    2: star2,
    3: star3,
    4: star4,
    5: star5,
};


export function TableView() {
    const [sortOrder, setSortOrder] = useState<'asc' | 'desc' | 'none'>('none');
    const [selectedRatings, setSelectedRatings] = useState<number[]>([]);

    const { data, loading, error } = useFetch<SpotForecast[]>("/ratings");

    if (loading) {
        return <>Loading...</>
    }

    if (error) {
        return <>Server Error: Unable to retrieve data</>
    }

    if (data == null) {
        return <>No Data</>
    }

    const rawData: SpotRating[] = data[0].spot_ratings.slice(14, 32) || [];

    const handleFilterChange = (rating: number) => {
        setSelectedRatings(prev =>
            prev.includes(rating)
                ? prev.filter(r => r !== rating)
                : [...prev, rating]
        );
    };

    const filteredData = rawData.filter(spot => {
        if (selectedRatings.length === 0) return true;
        const rounded = Math.min(5, Math.max(1, Math.round(spot.rating)));
        return selectedRatings.includes(rounded);
    });

    const sortedData = [...filteredData].sort((a, b) => {
        if (sortOrder === 'asc') return a.rating - b.rating;
        if (sortOrder === 'desc') return b.rating - a.rating;
        return 0;
    });

    return (
        <div className="view-wrapper">
            <div className="controls">
                <div className="filter-group">
                    {[1, 2, 3, 4, 5].map(num => (
                        <label key={num} className={`filter-label ${selectedRatings.includes(num) ? 'active' : ''}`}>
                            <input
                                type="checkbox"
                                checked={selectedRatings.includes(num)}
                                onChange={() => handleFilterChange(num)}
                            />
                            {num} ★
                        </label>
                    ))}
                </div>

                <button className="sort-button" onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}>
                    Sort: {sortOrder === 'asc' ? '↑' : '↓'}
                </button>
            </div>

            <div className="card-container">
                {sortedData.map((spot, index) => {
                    const safeRating = Math.min(5, Math.max(1, Math.round(spot.rating)));
                    return (
                        <div className="spot-card" key={index}>
                            <h2 className="spot-title">
                                <div className="spot-name">
                                    📍{spot.spot}
                                </div>
                                <div className="stars-display">
                                    {'★'.repeat(safeRating)}{'☆'.repeat(5 - safeRating)}
                                </div>
                            </h2>
                            <div className="image-container">
                                <img src={starImages[safeRating]} alt="rating" className="rating-image" />
                            </div>
                            <div className="reasons-footer">
                                {spot.reasons.map((reason, i) => (
                                    <span key={i} className="reason-tag">{reason}</span>
                                ))}
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
