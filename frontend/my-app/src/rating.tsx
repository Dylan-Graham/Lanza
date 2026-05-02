// import onestar from './assets/1-star.png'
// import twostar from './assets/2-star.png'
// import threestar from './assets/3-star.png'
// import fourstar from './assets/4-star.png'
// import fivestar from './assets/5-star.png'
import './rating.css'
import { spots } from './spots';


// export function Rating() {
//   const local = spots[0].spot_ratings.slice(14, 32);

//   const starImages: Record<number, string> = {
//     1: onestar,
//     2: twostar,
//     3: threestar,
//     4: fourstar,
//     5: fivestar
//   };

//   return (
//     <>
//       {local.map((item, index) => {
//         const roundedRating = Math.max(Math.round(item.rating), 1);

//         const starImg: string = starImages[roundedRating];

//         return (
//           <img
//             key={index}
//             src={starImg}
//             alt={`Rating: ${item.rating}`}
//             className="overlay-star pulsing-image"
//             style={{
//               top: `${10 + (index * 5)}%`,
//               right: `${20 + (index * 2)}%`,
//             }}
//           />
//         );
//       })}
//     </>
//   );
// }

export function Rating() {
  const local = spots[0].spot_ratings.slice(14, 32);

  const getBlendedColor = (rating: number) => {
    // Map rating 0-5 to Hue 0-120
    // 0 * 24 = 0 (Red)
    // 2.5 * 24 = 60 (Yellow/Orange-ish) 
    // 5 * 24 = 120 (Green)
    const hue = rating * 24; 
    return `hsl(${hue}, 100%, 50%)`;
  };

  return (
    <>
      {local.map((item, index) => {
        const circleColor = getBlendedColor(item.rating);

        return (
          <div
            key={index}
            className="pulsing-image circle"
            style={{
              top: `${10 + index * 5}%`,
              right: `${20 + index * 2}%`,
              backgroundColor: circleColor,
              boxShadow: `0 0 10px ${circleColor}`,
            }}
            title={`Spot: ${item.spot}, Rating: ${item.rating}`}
          />
        );
      })}
    </>
  );
}