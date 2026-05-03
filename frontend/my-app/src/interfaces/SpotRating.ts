export interface SpotRating {
    spot: string;
    rating: number;
    reasons: string[];
}

export interface SpotForecast {
    time: string;
    spot_ratings: SpotRating[];
}
