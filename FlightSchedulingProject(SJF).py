"""
Improved Flight Scheduling with No Unnecessary Waiting
- Removes artificial delays when no competing flights exist
- Still maintains SJF non-preemptive scheduling
- Enhanced time handling and validation
"""

def validate_time(time_str):
    """Validate time in HH:MM format and convert to minutes"""
    try:
        hours, minutes = map(int, time_str.split(':'))
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return hours * 60 + minutes
        return None
    except (ValueError, AttributeError):
        return None

def minutes_to_time(total_minutes):
    """Convert minutes back to HH:MM format"""
    hours = total_minutes // 60
    minutes = total_minutes % 60
    return f"{hours:02d}:{minutes:02d}"

# Get number of flights
while True:
    try:
        n = int(input("Enter number of flights to schedule: "))
        if n > 0: break
        print("Please enter a positive number")
    except ValueError:
        print("Invalid input. Please enter a number")

flights = []

# Input flight details with validation
for i in range(n):
    flight_id = f"F{i+1}"
    print(f"\nEnter details for {flight_id}:")
    dFrom = input("  Departing from: ").strip()
    dest = input("  Destination: ").strip()
    
    # Validate arrival time
    while True:
        arrival = input("  Arrival time (HH:MM): ").strip()
        arrival_min = validate_time(arrival)
        if arrival_min is not None: break
        print("Invalid time. Use HH:MM (00:00-23:59)")
    
    # Validate duration
    while True:
        duration = input("  Flight duration (HH:MM): ").strip()
        duration_min = validate_time(duration)
        if duration_min is not None and duration_min > 0: break
        print("Invalid duration. Use HH:MM with positive duration")

    flights.append({
        "flight_id": flight_id,
        "dFrom": dFrom,
        "dest": dest,
        "arrival_time": arrival,
        "arrival_minutes": arrival_min,
        "duration": duration,
        "duration_minutes": duration_min,
        "start_time": "00:00",
        "start_minutes": 0,
        "completion_time": "00:00",
        "completion_minutes": 0,
        "turnaround_time": "00:00",
        "turnaround_minutes": 0,
        "waiting_time": "00:00",
        "waiting_minutes": 0,
        "completed": False
    })

# Sort by arrival time
flights.sort(key=lambda x: x["arrival_minutes"])

# Improved SJF scheduling without artificial delays
current_time = 0
completed = 0
schedule_order = []

while completed < n:
    # Get all ready flights
    ready_queue = [f for f in flights if f["arrival_minutes"] <= current_time and not f["completed"]]
    
    if ready_queue:
        # Find the flight with shortest duration
        current_flight = min(ready_queue, key=lambda x: x["duration_minutes"])
        
        # Start immediately at arrival time if no earlier flights are waiting
        start_time = max(current_time, current_flight["arrival_minutes"])
        
        current_flight["start_minutes"] = start_time
        current_flight["start_time"] = minutes_to_time(start_time)
        
        completion_time = start_time + current_flight["duration_minutes"]
        current_flight["completion_minutes"] = completion_time
        current_flight["completion_time"] = minutes_to_time(completion_time)
        
        current_flight["turnaround_minutes"] = completion_time - current_flight["arrival_minutes"]
        current_flight["turnaround_time"] = minutes_to_time(current_flight["turnaround_minutes"])
        
        current_flight["waiting_minutes"] = start_time - current_flight["arrival_minutes"]
        current_flight["waiting_time"] = minutes_to_time(current_flight["waiting_minutes"])
        
        current_flight["completed"] = True
        current_time = completion_time
        schedule_order.append(current_flight["flight_id"])
        completed += 1
    else:
        # Only advance time if no flights are ready
        current_time += 1

# Display results
header = ["Flight", "Departure", "Destination", "Arrival", "Duration", "Start", "Complete", "TAT", "Wait"]
widths = [6, 18, 18, 8, 10, 8, 10, 10, 10]
separator = "+".join(["-"*(w+2) for w in widths])

print("\n" + separator)
print("| " + " | ".join(f"{h:^{w}}" for h,w in zip(header, widths)) + " |")
print(separator)

flights.sort(key=lambda x: x["flight_id"])
for f in flights:
    values = [
        f["flight_id"], f["dFrom"], f["dest"],
        f["arrival_time"], f["duration"],
        f["start_time"], f["completion_time"],
        f["turnaround_time"], f["waiting_time"]
    ]
    print("| " + " | ".join(f"{v:<{w}}" for v,w in zip(values, widths)) + " |")

print(separator)

# Calculate averages
avg_tat = sum(f["turnaround_minutes"] for f in flights) / n
avg_wt = sum(f["waiting_minutes"] for f in flights) / n

print(f"\nAverage Turnaround Time: {minutes_to_time(int(avg_tat))}")
print(f"Average Waiting Time: {minutes_to_time(int(avg_wt))}")
print("-"*50)
print("Execution Order:", " → ".join(schedule_order))
print("-"*50)