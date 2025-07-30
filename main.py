import pandas as pd
import os

try:
    os.system('cls') # Clear the console
    file = './data/transactional-sample.csv'
    df = pd.read_csv(file)
    print('File ' + file + ' loaded successfully')
except FileNotFoundError:
    os.system('cls')
    print('Error: The file ' + file + ' was not found in the specified folder.')
    print('Verify the pathing or the existence of the file.')
    exit()

# Firs Rule - Sistematic use of distinct credit cards by the same user.
print('\n--Analysis of the First Anti-Fraud Rule\n')
print('Rule: Sistematic use of distinct credit cards by the same user.')

# Logic to count 

df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['transaction_day'] = df['transaction_date'].dt.date

## DANGER ZONE 
cards_per_user_per_day = df.groupby(['user_id', 'transaction_day'])['card_number'].nunique()
threshold_same_day_danger = 3 # Maximum of distinct card per day

print (f'\nMaximum of suspicious used cards per user per day defined to: {threshold_same_day_danger} or more.') 

danger_users_daily_multiple_cards = cards_per_user_per_day[cards_per_user_per_day >= threshold_same_day_danger]
danger_user_ids = danger_users_daily_multiple_cards.index.get_level_values('user_id').unique()

print('\nCount of distinct used credit cards per user of  or more. (first 10 attempts):')
print(danger_users_daily_multiple_cards .head(10)) # Show the frist ten attempts 

## SUSPECT ZONE
cards_per_user_overall = df.groupby('user_id')['card_number'].nunique()
threshold_overall_suspect = 3
suspect_users_overall_multiple_cards = cards_per_user_overall[cards_per_user_overall >= threshold_overall_suspect]
# Remove who is aldready in danger zone 
suspect_user_ids_set = set(suspect_users_overall_multiple_cards.index) - set(danger_user_ids)
suspect_users_final = cards_per_user_overall[cards_per_user_overall.index.isin(list(suspect_user_ids_set))]

print('\n-- Suspicious Users (First Rule)')
if not danger_users_daily_multiple_cards.empty:
    print(f'Total of suspicious users found in suspect zone: {len(danger_users_daily_multiple_cards)}')
    danger_users_daily_multiple_cards.to_csv('./results/danger_users_multiple_cards.csv', header=['distinct_cards'])
    print("\nResults were saved in 'danger_users_multiple_cards.csv'.")
else:
    print('Nobody were found for this rule in this zone at this moment.')

if not suspect_users_overall_multiple_cards.empty:
    print(f'Total of suspicious users found in suspect zone: {len(suspect_users_overall_multiple_cards)}')
    suspect_users_overall_multiple_cards.to_csv('./results/suspicious_users_multiple_cards.csv', header=['distinct_cards'])
    print("\nResults were saved in 'suspicious_users_multiple_cards.csv'.")
else:
    print('Nobody were found for this rule in this zone at this moment.')