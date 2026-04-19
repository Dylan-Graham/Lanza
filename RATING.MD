# Example

## Data
{
    "time": "Tuesday, Apr 07 01h",
    "wave_height": 1.4,
    "wave_direction": "NNW",
    "wave_period": 13.0,
    "wind_speed": 7.0,
    "wind_gust": 8.0,
    "wind_direction": "NW",
    "cloud_coverage": None,
    "precipitation": 0,
    "air_temperature": 18.0,
}

## Spot guide
{
        "name": "Jameos del Agua",
        "location": "29°09'18.64\"N 13°25'43.26\"W",
        "description": "Long and hollow left during surf season. The right at the windsurf section is short and hollow",
        "wind_direction": ["WNW", "NW", "NNW", "N", "NNE"],
        "swell_direction": ["WNW", "NW", "NNW", "N", "NNE"],
        "tide": ["low", "high"],
        "wave_size": ">3m",
        "wave_type": ["a-frame", "left"],
        "wave_power": ["med", "max"],
        "surf_level_recommendation": {
            "beginner": 1,
            "advanced": 5,
            "expert": 5
        }
    },

## Rating

### Constraints:
- Wave direction
- Wind direction
- Wave height
- Wave period
- Wind speed

### Weights
1. Wave Direction Match (Weight: 30%)
3 points if forecast wave_direction matches spot's preferred swell_direction
1.5 points if adjacent direction (±1 compass point)
0 points if no match

2. Wind Direction Match (Weight: 25%)
2.5 points if forecast wind_direction matches spot's preferred wind_direction
1.25 points if adjacent direction
0 points if no match
Penalty: Subtract points if wind is onshore when spot needs offshore

3. Wave Height Score (Weight: 20%)
2 points if wave_height falls within spot's wave_size range
1 point if slightly outside range (±0.5m)
0 points if far outside range

4. Wave Period Quality (Weight: 15%)
1.5 points for period ≥12s (excellent groundswell)
1 point for period 8-12s (good)
0.5 points for period 6-8s (fair)
0 points for period <6s (poor wind swell)

5. Wind Speed Score (Weight: 10%)
1 point for wind_speed 0-10 km/h (glassy/light)
0.5 points for 10-20 km/h (moderate)
0 points for >20 km/h (choppy)
Formula:

Rating = (wave_direction_score × 0.30) + 
         (wind_direction_score × 0.25) + 
         (wave_height_score × 0.20) + 
         (wave_period_score × 0.15) + 
         (wind_speed_score × 0.10)
Output: 0-10 scale, can convert to 0-5 stars by dividing by 2

Additional Considerations:
Should we also factor in:

Tide matching? (Would need current tide data in forecast)
Skill level adjustment? (Boost rating for spots matching user's skill level)
Time decay? (Prefer closer time slots)
Crowd factor? (Penalize popular spots at peak times)
Questions:

Do you want a 0-5 or 0-10 rating scale?
Should we create separate ratings for different skill levels?
Do you have tide data available in the forecast?
Any other factors you want to prioritize?