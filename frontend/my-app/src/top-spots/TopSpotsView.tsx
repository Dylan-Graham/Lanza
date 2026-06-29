import { useState, useEffect, useRef } from 'react';
import { useFetch } from '../hooks/useFetch';
import type { SpotForecast } from '../interfaces/SpotRating';
import './TopSpotsView.css';

const ratingColor = (r: number): string => {
    if (r >= 4.0) return '#16a34a';
    if (r >= 3.0) return '#65a30d';
    if (r >= 2.0) return '#ca8a04';
    if (r >= 1.0) return '#ea580c';
    return '#dc2626';
};

// Input: "Monday, Apr 27 01h" → "01:00 27 Apr"
const formatTime = (time: string): string => {
    const match = time.match(/(\w+),\s+(\w+)\s+(\d+)\s+(\d+)h/);
    if (!match) return time;
    const [, , month, day, hh] = match;
    return `${hh}:00 ${day} ${month}`;
};

const stars = (r: number) => {
    const n = Math.min(5, Math.max(1, Math.round(r)));
    return '★'.repeat(n) + '☆'.repeat(5 - n);
};

export function TopSpotsView() {
    const [hour, setHour] = useState(0);
    const [playing, setPlaying] = useState(false);
    const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

    const { data, loading, error } = useFetch<SpotForecast[]>('/top-spots');

    useEffect(() => {
        if (!data) return;
        if (playing) {
            intervalRef.current = setInterval(() => {
                setHour(h => {
                    if (h >= data.length - 1) { setPlaying(false); return h; }
                    return h + 1;
                });
            }, 800);
        }
        return () => { if (intervalRef.current) clearInterval(intervalRef.current); };
    }, [playing, data]);

    if (loading) return <div className="top-spots-wrapper">Loading...</div>;
    if (error) return <div className="top-spots-wrapper">Error: {error.message}</div>;
    if (!data?.length) return <div className="top-spots-wrapper">No data</div>;

    const slot = data[hour];
    const ranked = [...slot.spot_ratings].sort((a, b) => b.rating - a.rating);

    return (
        <div className="top-spots-wrapper">
            <div className="spot-list">
                {ranked.map(({ spot, rating, reasons }, i) => (
                    <div key={spot} className="spot-row" style={{ '--rating-color': ratingColor(rating) } as React.CSSProperties}>
                        <span className="spot-rank">#{i + 1}</span>
                        <div className="spot-info">
                            <div className="spot-name">📍 {spot}</div>
                            <div className="spot-reasons">{reasons.join(' · ')}</div>
                        </div>
                        <div className="spot-score">
                            <div className="score-value">{rating.toFixed(1)}</div>
                            <div className="score-stars">{stars(rating)}</div>
                        </div>
                    </div>
                ))}
            </div>
            <div className="top-spots-controls">
                <button className="play-button" onClick={() => setPlaying(p => !p)}>
                    {playing ? '⏸' : '▶'}
                </button>
                <input
                    type="range" min={0} max={data.length - 1} value={hour}
                    onChange={e => { setPlaying(false); setHour(Number(e.target.value)); }}
                />
                <span className="time-label">{formatTime(slot.time)}</span>
            </div>
        </div>
    );
}
