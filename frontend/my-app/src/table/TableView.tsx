// import { spots } from "../spots";

// interface CardProps {
//     spot: string;
//     rating: number;
//     reasons: string[];
// }

// function Card({ spot, rating, reasons }: CardProps) {
//     return <>
//         <h2>{spot}</h2>
//         <h2>{rating}</h2>
//         <h2>{reasons}</h2>
//     </>
// }

// export function TableView() {
//     const local = spots[0].spot_ratings.slice(14, 32);

//     return <>
//         <h1>Spots:</h1>
//         {
//             local.map((spot) => (
//                 <div>
//                     < Card spot={spot.spot} rating={spot.rating} reasons={spot.reasons} />
//                 </div>
//             ))
//         }
//     </>
// }

import './TableView.css';
import { spots } from "../spots";

import star1 from '../assets/1-star.png';
import star2 from '../assets/2-star.png';
import star3 from '../assets/3-star.png';
import star4 from '../assets/4-star.png';
import star5 from '../assets/5-star.png';

const starImages: Record<number, string> = {
    1: star1,
    2: star2,
    3: star3,
    4: star4,
    5: star5,
};

export function TableView() {
    const local = spots[0].spot_ratings.slice(14, 32);

    return (
        <div className="card-container">
            {local.map((spot, index) => {
                const safeRating = Math.min(5, Math.max(1, Math.round(spot.rating)));
                
                return (
                    <div className="spot-card" key={index}>
                        <h2 className="spot-title">{spot.spot}</h2>
                        
                        <div className="image-container">
                            <img 
                                src={starImages[safeRating]} 
                                alt={`${safeRating} stars`} 
                                className="rating-image"
                            />
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
    );
}
