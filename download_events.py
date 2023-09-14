import pandas as pd
from statsbombpy import sb
import warnings
import csv
from collections import Counter

def download_all_events():
    # Save events into events.csv and return events
    warnings.filterwarnings("ignore")

    match_ids = []

    for idx, row in sb.competitions()[['season_id', 'competition_id']].iterrows():
        print(idx)

        try:
            match_ids.append(sb.matches(competition_id=row['competition_id'], season_id=row['season_id'])['match_id'].to_list())
        except:
            pass

        break # remove this for all of the data

    flat = [item for sublist in match_ids for item in sublist]

    print(flat)

    n_events = 3

    events = []
    counter = 0
    lenf = len(flat)

    for selected_game in flat:
        try:
            counter += 1
            if counter % 100 == 0:
                print("{0:0.2f}".format(counter / lenf))
            df = sb.events(match_id=selected_game)
            df['timestamp'] = pd.to_datetime(df['timestamp'], format='%H:%M:%S.%f')
            df = df.sort_values(by=['period', 'timestamp', 'id'])
            df = df.reset_index(drop=True)
            goal_entries = df[df['shot_outcome'] == 'Goal']

            for index, goal_row in goal_entries.iterrows():
                goal_index = index
                start_index = max(0, goal_index - n_events)
                end_index = goal_index + 1
                previous_entries = df.iloc[start_index:end_index-1]
                events.append(previous_entries['location'].to_list()) # type
        except Exception as e:
            print(e)

        break # remove this for all of the data
    
    with open('events.csv', mode='w') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for event in events:
            flat_positions = [item for sublist in event for item in sublist]
            csv_writer.writerow(flat_positions)
            #csv_writer.writerow(event)


    return events

def count_events(events):
    # Convert lists to tuples for counting
    tuple_lists = [tuple(lst) for lst in events]

    # Use Counter to count occurrences of each tuple
    list_counts = Counter(tuple_lists)

    # Find the most common list
    most_common_list_tuple = list_counts.most_common(1)[0][0]

    # Convert the most common tuple back to a list
    most_common_list = list(most_common_list_tuple)

    print("Most common list:", most_common_list)

    return list_counts # list_counts.most_common(10)