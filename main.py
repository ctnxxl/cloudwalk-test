import pandas as pd
import os

try:
    os.system('cls') # Clear the console cls for windows and clear
    file = './data/transactional-sample.csv'
    df = pd.read_csv(file)
except FileNotFoundError:
    os.system('cls')
    print('Error')

# We convert the ids to int, to show treat the null data right
if 'user_id' in df.columns:
    df['user_id'] = df['user_id'].astype('Int64')
if 'device_id' in df.columns:
    df['device_id'] = df['device_id'].astype('Int64')
if 'merchant_id' in df.columns:
    df['merchant_id'] = df['merchant_id'].astype('Int64')

# First Rule - Sistematic use of distinct credit cards by the same user.
print('-- Analysis of the First Rule')

df['transaction_date'] = pd.to_datetime(df['transaction_date'])
df['transaction_day'] = df['transaction_date'].dt.date

## DANGER ZONE 
cards_per_user_per_day = df.groupby(['user_id', 'transaction_day'])['card_number'].nunique()
threshold_same_day_danger = 3 # Maximum of distinct card per day

danger_users_daily_multiple_cards = cards_per_user_per_day[cards_per_user_per_day >= threshold_same_day_danger]
danger_user_ids = danger_users_daily_multiple_cards.index.get_level_values('user_id').unique()

## SUSPECT ZONE
cards_per_user_overall = df.groupby('user_id')['card_number'].nunique()
threshold_overall_suspect = 3
suspect_users_overall_multiple_cards = cards_per_user_overall[cards_per_user_overall >= threshold_overall_suspect]

# Remove who is aldready in danger zone 
suspect_user_ids_set = set(suspect_users_overall_multiple_cards.index) - set(danger_user_ids)
suspect_users_final = cards_per_user_overall[cards_per_user_overall.index.isin(list(suspect_user_ids_set))]


if not danger_users_daily_multiple_cards.empty:
    danger_users_daily_multiple_cards.to_csv('./results/danger_users_multiple_cards.csv', header=['distinct_cards'])
    print("Results were saved in 'danger_users_multiple_cards.csv'.")
else:
    print('Nobody were found for this rule in this zone at this moment.')

if not suspect_users_overall_multiple_cards.empty:
    suspect_users_overall_multiple_cards.to_csv('./results/suspicious_users_multiple_cards.csv', header=['distinct_cards'])
    print("Results were saved in 'suspicious_users_multiple_cards.csv'.")
else:
    print('Nobody were found for this rule in this zone at this moment.')

# Second Rul
# Rule: Identify and block devices associated with chargebacks (has_cbk = True).

print('-- Analysis of the Second Rule')

# Filter the DataFrame to include only transactions with chargebacks
devices_with_cbk = df[df['has_cbk'] == True]

# Get the unique device IDs from these transactions
blocked_devices = devices_with_cbk['device_id'].unique()

if blocked_devices.size > 0:
    # Convert the array of device IDs to a DataFrame for saving to CSV
    blocked_devices_df = pd.DataFrame(blocked_devices, columns=['device_id'])
    os.makedirs('./results', exist_ok=True) 
    blocked_devices_df.to_csv('./results/blocked_devices.csv', index=False)
    print("Results for 'blocked_devices.csv' were saved.")
else:
    print('No devices with chargebacks were found.')

# Third Rule 
# Merchants transacting only with fraudulent users.
print('-- Analysis of the Third Rule')
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
    merchants_with_single_fraudulent_user_df.to_csv('./results/merchants_with_single_fraudulent_user_cbk.csv', index=False)
    print("Results for 'merchants_with_single_fraudulent_user_cbk.csv' were saved.")

else:
    print('No merchants with a single fraudulent user (has_cbk == True) were found.')

# Fourth Rule
print('-- Analysis of the Fourth')

# Get only the transactions with has_cbk == True
cbk_df = df[df['has_cbk'] == True].copy()

# Get only the transactions with has_cbk == False
approved_df = df[df['has_cbk'] == False].copy()

# Add a column with the minimum count of days = 3
# If the approved transaction happend in D, we count by D-2
approved_df['min_date_window'] = approved_df['transaction_day'] - pd.Timedelta(days=2)

# Merge the approved transactions with the transactions with has_cbk == True by the user_id
# This create all the patterns of approved and chargebacks transactions for the same user
merged_potential_cbks = pd.merge(
    approved_df,
    cbk_df,
    on='user_id',
    suffixes=('_approved', '_cbk')
)

# Filter the transactions of chargeback that are in the same window of 3 days for each approved transaction
relevant_cbks_in_window = merged_potential_cbks[
    (merged_potential_cbks['transaction_day_cbk'] >= merged_potential_cbks['min_date_window']) &
    (merged_potential_cbks['transaction_day_cbk'] <= merged_potential_cbks['transaction_day_approved'])
]

# Count the number of relevants chargebacks for each approved transaction
# Group by transaction_id of the approved transaction and count how many times it appears
cbk_counts_for_approved_tx = relevant_cbks_in_window.groupby('transaction_id_approved').size()

# Identify the IDs of the approved transactions that had two or more chargebacks in the window of 3 days.
suspicious_approved_tx_ids = cbk_counts_for_approved_tx[cbk_counts_for_approved_tx >= 2].index

# Select the suspicious transactions of the original DataFrame of approved transactions
# This garantees that we got all of the original columns of the suspicious transaction
suspicious_approved_transactions = approved_df[
    approved_df['transaction_id'].isin(suspicious_approved_tx_ids)
]

# Remove columns that are unecessary
suspicious_approved_transactions = suspicious_approved_transactions.drop(columns=['min_date_window'])

# Save the results in a CSV file
if not suspicious_approved_transactions.empty:
    suspicious_approved_transactions.to_csv(
        './results/suspicious_approved_transactions_user_3day_cbk.csv',
        index=False
    )
    print("Results for 'suspicious_approved_transactions_user_3day_cbk.csv' were saved.")
else:
    print('Didnt find a single user with this Rule.')