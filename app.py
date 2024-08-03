import pandas as pd
from flask import Flask, render_template

app = Flask(__name__)

# Define the data

data = {
    'Timestamp': [
        '2024-08-03 10:00:00', '2024-08-03 10:01:52', '2024-08-03 10:03:44', 
        '2024-08-03 10:05:36', '2024-08-03 10:07:28', '2024-08-03 10:09:20',
        '2024-08-03 10:11:12', '2024-08-03 10:13:04', '2024-08-03 10:14:56', 
        '2024-08-03 10:16:48', '2024-08-03 10:18:40', '2024-08-03 10:20:32',
        '2024-08-03 10:22:24', '2024-08-03 10:24:16', '2024-08-03 10:26:08', 
        '2024-08-03 10:28:00'
    ],
    'Accel_X': [0.02, 0.03, 0.05, 0.01, -0.03, 0.10, 0.00, 0.02, 0.04, -0.02, 0.01, 0.03, -0.05, 0.12, 0.00, 0.02],
    'Accel_Y': [0.10, 0.15, -0.10, -0.20, 0.05, 0.30, 0.20, -0.25, 0.10, 0.15, -0.10, -0.20, 0.05, 0.30, 0.20, -0.25],
    'Accel_Z': [9.81, 9.80, 9.82, 9.83, 9.80, 9.78, 9.79, 9.85, 9.81, 9.80, 9.82, 9.83, 9.80, 9.78, 9.79, 9.85],
    'Gyro_Pitch': [0.01, 0.01, 0.00, -0.01, -0.02, 0.03, 0.02, 0.01, 0.00, -0.01, 0.00, -0.01, -0.02, 0.03, 0.02, 0.01],
    'Gyro_Roll': [0.02, 0.02, -0.01, -0.02, -0.01, 0.05, 0.03, -0.03, 0.02, 0.02, -0.01, -0.02, -0.01, 0.05, 0.03, -0.03],
    'Gyro_Yaw': [0.00, 0.05, -0.10, -0.15, -0.05, 0.10, 0.05, -0.20, 0.00, 0.05, -0.10, -0.15, -0.05, 0.10, 0.05, -0.20]
}






# Create DataFrame
df = pd.DataFrame(data)
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Initialize driving behavior counts and timing
smooth_driving_duration = 0
sharp_turns = 0
sudden_braking = 0
sudden_acceleration = 0

# Define thresholds for behaviors
hard_braking_threshold = -0.30
sharp_turn_accel_threshold = 0.15
sharp_turn_gyro_threshold = 0.05
sudden_accel_threshold = 0.20
sudden_braking_threshold = -0.20

# Calculate time intervals and classify driving behavior
previous_time = df['Timestamp'].iloc[0]
for index, row in df.iterrows():
    current_time = row['Timestamp']
    time_diff = (current_time - previous_time).total_seconds() / 60.0  # in minutes

    if row['Accel_Y'] < sudden_braking_threshold:
        sudden_braking += time_diff
    elif row['Accel_Y'] < hard_braking_threshold:
        sudden_braking += time_diff
    elif row['Accel_Y'] > sudden_accel_threshold:
        sudden_acceleration += time_diff
    elif abs(row['Accel_X']) > sharp_turn_accel_threshold or abs(row['Gyro_Yaw']) > sharp_turn_gyro_threshold:
        sharp_turns += time_diff
    else:
        smooth_driving_duration += time_diff

    previous_time = current_time

# Calculate trip summary
distance_traveled = 15  # Dummy value
trip_duration = str(df['Timestamp'].iloc[-1] - df['Timestamp'].iloc[0])

# Calculate scores
smooth_driving_score = smooth_driving_duration
sharp_turns_score = -2 * sharp_turns
sudden_braking_score = -5 * sudden_braking
sudden_acceleration_score = -3 * sudden_acceleration

total_score = smooth_driving_score + sharp_turns_score + sudden_braking_score + sudden_acceleration_score

# Determine driving behavior type
if total_score <= -20:
    driving_behavior = "Aggressive Driving: The driver consistently engages in risky and aggressive behaviors, such as hard braking, rapid acceleration, and potentially serious traffic violations. These actions pose a significant safety concern."
elif total_score <= -10:
    driving_behavior = "Moderate Negative Score: The driver may display occasional instances of aggressive driving. The driver has room for improvement in certain areas of their driving habits."
elif total_score <= -1:
    driving_behavior = "Low Negative Score: The driver demonstrates generally safe driving behavior, with only minor issues or occasional lapses in judgment."
else:
    driving_behavior = "Positive Score: The driver consistently showcases safe and smooth driving habits."

@app.route('/')
def index():
    return render_template('dashboard.html',
                          distance_traveled=distance_traveled,
                          trip_duration=trip_duration,
                          smooth_driving_duration=smooth_driving_duration,
                          sharp_turns=sharp_turns,
                          sudden_braking=sudden_braking,
                          sudden_acceleration=sudden_acceleration,
                          total_score=total_score,
                          driving_behavior=driving_behavior)

if __name__ == '__main__':
    app.run(debug=True)
