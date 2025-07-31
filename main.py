import pandas as pd
import os

try:
    os.system('cls') # Clear the console cls for windows and clear
    file = './data/transactional-sample.csv'
    df = pd.read_csv(file)
except FileNotFoundError:
    os.system('cls')
    print('Error')

# First Rule - Sistematic use of distinct credit cards by the same user.
print('\n--Analysis of the First Anti-Fraud Rule\n')
print('Rule: Sistematic use of distinct credit cards by the same user.')

# Logic to count 

df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['transaction_day'] = df['transaction_date'].dt.date

## DANGER ZONE 
cards_per_user_per_day = df.groupby(['user_id', 'transaction_day', 'transaction_id'])['card_number'].nunique()
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

# Second Rule - Devices used in a others fraudulent transactions.
# Rule: Identify and block devices associated with chargebacks (has_cbk = True).
print('\n--- Analysis of the Second Anti-Fraud Rule')

# Filter the DataFrame to include only transactions with chargebacks
devices_with_cbk = df[df['has_cbk'] == True]

# Get the unique device IDs from these transactions
blocked_devices = devices_with_cbk['device_id'].unique()

if blocked_devices.size > 0:
    print(f'Total unique devices identified with chargebacks: {len(blocked_devices)}')
    # Convert the array of device IDs to a DataFrame for saving to CSV
    blocked_devices_df = pd.DataFrame(blocked_devices, columns=['device_id'])
    os.makedirs('./results', exist_ok=True) 
    blocked_devices_df.to_csv('./results/blocked_devices.csv', index=False)
    print("Identified devices with chargebacks were saved in 'blocked_devices.csv'.")
else:
    print('No devices with chargebacks were found.')

# Third Rule - Merchants transacting only with fraudulent users.
# Group by merchant and count unique users
users_per_merchant = df.groupby('merchant_id')['user_id'].nunique()

# Filter merchants who have only transacted with one user
merchants_with_one_user = users_per_merchant[users_per_merchant == 1].index

# Filter transactions involving these merchants
df_one_user_merchants = df[df['merchant_id'].isin(merchants_with_one_user)]

# Group by merchant and check if the single user has fraudlent transactions
merchants_with_single_fraudulent_user = df_one_user_merchants.groupby('merchant_id')['has_cbk'].any()

# Filter for merchants where the single user has fraudlent transactions
merchants_with_single_fraudulent_user = merchants_with_single_fraudulent_user[merchants_with_single_fraudulent_user == True].index

if merchants_with_single_fraudulent_user.size > 0:
    merchants_with_single_fraudulent_user_df = pd.DataFrame(merchants_with_single_fraudulent_user, columns=['merchant_id'])
    os.makedirs('./results', exist_ok=True)
    merchants_with_single_fraudulent_user_df.to_csv('./results/merchants_with_single_fraudulent_user_cbk.csv', index=False)
else:
    print('No merchants with a single fraudulent user (has_cbk == True) were found.')