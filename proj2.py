def time_to_minutes(time_str):
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def minutes_to_time(minutes):
    return f"{minutes // 60:02}:{minutes % 60:02}"

def calculate_free_intervals(busy_intervals, daily_start, daily_end):
    free_intervals = []
    last_end = daily_start
    for start, end in busy_intervals:
        if last_end < start:
            free_intervals.append([last_end, start])
        last_end = max(last_end, end)
    if last_end < daily_end:
        free_intervals.append([last_end, daily_end])
    return free_intervals

def find_common_intervals(all_free_intervals, meeting_duration):
    common_intervals = all_free_intervals[0]
    for free_intervals in all_free_intervals[1:]:
        new_common = []
        i = j = 0
        while i < len(common_intervals) and j < len(free_intervals):
            start = max(common_intervals[i][0], free_intervals[j][0])
            end = min(common_intervals[i][1], free_intervals[j][1])
            if end - start >= meeting_duration:
                new_common.append([start, end])
            if common_intervals[i][1] < free_intervals[j][1]:
                i += 1
            else:
                j += 1
        common_intervals = new_common
    return [[minutes_to_time(start), minutes_to_time(end)] for start, end in common_intervals]

def group_schedule_match(schedules, working_periods, meeting_duration):
    all_free_intervals = []
    for busy_intervals, (login, logout) in zip(schedules, working_periods):
        busy_intervals = [[time_to_minutes(start), time_to_minutes(end)] for start, end in busy_intervals]
        daily_start = time_to_minutes(login)
        daily_end = time_to_minutes(logout)
        free_intervals = calculate_free_intervals(busy_intervals, daily_start, daily_end)
        all_free_intervals.append(free_intervals)
    return find_common_intervals(all_free_intervals, meeting_duration)

def main():
   
    with open('input.txt', 'r') as infile:
        
        num_participants = int(infile.readline().strip())
        schedules = []
        working_periods = []
        
       
        for _ in range(num_participants):
            
            daily_login, daily_logout = infile.readline().strip().split()
            working_periods.append([daily_login, daily_logout])
            
            
            busy_intervals = []
            num_busy_periods = int(infile.readline().strip())
            
            for _ in range(num_busy_periods):
                start, end = infile.readline().strip().split()
                busy_intervals.append([start, end])
            
            schedules.append(busy_intervals)
        
        
        meeting_duration = int(infile.readline().strip())
    
   
    available_slots = group_schedule_match(schedules, working_periods, meeting_duration)
    
    with open('output.txt', 'w') as outfile:
        if available_slots:
            outfile.write("Available meeting times:\n")
            for start, end in available_slots:
                outfile.write(f"{start} - {end}\n")
        else:
            outfile.write("No common available times meet the required duration.\n")

if __name__ == "__main__":
    main()
