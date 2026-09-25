import pandas as pd

file_path = "/Users/dheea/Downloads/aihw-mhc-hpf-16-immunisation-datasheet-report-hc42.xlsx"

tab1 = pd.read_excel(file_path, sheet_name= "TAB 1", header = 15 )
print(tab1.columns)
tab1.columns =['Reporting_Year', 'Age_group',
                'All_registered', 'All_fully_immunised', 'All_not_fully_immunised', 'All_percent',
                'blank',
                'Indig_registered', 'Indig_fully_immunised', 'Indig_not_fully_immunised', 'Indig_percent_fi']
tab1 = tab1.drop(columns=['blank'])
tab1 = tab1.dropna(subset=['Reporting_Year'])
tab1 = tab1.dropna(subset=['Indig_fully_immunised'])
print(tab1.head())
tab1.to_csv("TAB1_national_clean.csv", index=False)
print("TAB 1 saved:", tab1.shape)

 #TAB 2
tab2 = pd.read_excel(file_path, sheet_name="TAB 2", header=12)
tab2.columns = ['State', 'PHN_code', 'PHN_name', 'Reporting_Year', 'Age_group',
                'Registered_children', 'Fully_immunised', 'Not_fully_immunised', 'Percent_fully_immunised']
tab2 = tab2.dropna(subset=['State'])
tab2.to_csv("TAB2_state_phn_clean.csv", index=False)
print("TAB 2 saved:", tab2.shape)

#TAB 3
tab3 = pd.read_excel(file_path, sheet_name="TAB 3", header=15)
tab3.columns = ['State', 'SA3_code', 'SA3_name', 'Reporting_Year', 'Age_group',
                'Registered_children', 'Fully_immunised', 'Not_fully_immunised',
                'Percent_fully_immunised', 'Interpret_with_caution']
tab3 = tab3.drop(columns=['Interpret_with_caution'])
tab3 = tab3.dropna()
print(tab3.head())
tab3.to_csv("TAB3_sa3_clean.csv", index=False)
print("TAB 3 saved:", tab3.shape)

# TAB 4
tab4 = pd.read_excel(file_path, sheet_name="TAB 4", header=16)
tab4.columns = ['State', 'Postcode', 'Associated_areas', 'Reporting_Year', 'Age_group',
                'Percent_fully_immunised_range', 'Interpret_with_caution']
tab4 = tab4.drop(columns= ['Interpret_with_caution'])
tab4 = tab4.dropna(subset=['State'])
tab4.to_csv("TAB4_postcode_clean.csv", index=False)
print("TAB 4 saved:", tab4.shape)

#TAB 5
tab5 = pd.read_excel(file_path, sheet_name="TAB 5", header=16)
tab5.columns = ['State', 'PHN_code', 'PHN_name', 'Reporting_Year', 'Age_group',
                'Registered_children', 'Fully_immunised', 'Not_fully_immunised',
                'Percent_fully_immunised', 'Interpret_with_caution']
tab5= tab5.drop(columns= ['Interpret_with_caution'])
tab5 = tab5.dropna(subset=['State'])
tab5.to_csv("TAB5_indigenous_phn_clean.csv", index=False)
print("TAB 5 saved:", tab5.shape)
# TAB 6
tab6 = pd.read_excel(file_path, sheet_name="TAB 6", header=16)
tab6.columns = ['State', 'SA4_code', 'SA4_name', 'Reporting_Year', 'Age_group',
                'Registered_children', 'Fully_immunised', 'Not_fully_immunised',
                'Percent_fully_immunised', 'Interpret_with_caution']
tab6 = tab6.drop(columns=['Interpret_with_caution'])
tab6 = tab6.dropna(subset=['State'])
tab6.to_csv("TAB6_indigenous_sa4_clean.csv", index=False)
print("TAB 6 saved:", tab6.shape)



file_path = "/Users/dheea/Downloads/Diphtheria Tetanus Toxoid and Pertussis (DTP) vaccination coverage 2026-16-09 12-14 UTC.xlsx"
df = pd.read_excel(file_path, sheet_name="Sheet1")

dtp3 = df[
    (~df['NAME'].str.contains('Region', na=False)) &
    (df['ANTIGEN'] == 'DTPCV3') &
    (df['COVERAGE_CATEGORY'] == 'WUENIC') &
    (df['YEAR'] >= 2010)
].copy()

dtp3_clean = dtp3[['NAME', 'YEAR', 'COVERAGE']].copy()
dtp3_clean.columns = ['Country', 'Year', 'Coverage']
dtp3_clean = dtp3_clean.dropna(subset=['Country', 'Coverage'])

dtp3_clean['Rank'] = dtp3_clean.groupby('Year')['Coverage'].rank(ascending=False, method='first').astype(int)

# Fixed snapshot: only countries ranked 18-33 in the MOST RECENT year (2025)
latest_band = dtp3_clean[
    (dtp3_clean['Year'] == 2025) & (dtp3_clean['Rank'] >= 18) & (dtp3_clean['Rank'] <= 33)
]['Country'].unique()

print(f"Countries in the 18-33 band in 2025: {len(latest_band)}")
print(sorted(latest_band))

# Keep their FULL trajectories across all years
chart_data = dtp3_clean[dtp3_clean['Country'].isin(latest_band)].copy()
chart_data['Is_Australia'] = chart_data['Country'] == 'Australia'
chart_data = chart_data.sort_values(['Country', 'Year'])

chart_data.to_csv("dtp3_australia_peer_band_fixed.csv", index=False)
print("\nSaved! Shape:", chart_data.shape)
# Build a label showing "Country (#Rank)" at the final year, for chart annotation
label_data = chart_data[chart_data['Year'] == chart_data['Year'].max()].copy()
label_data['Label'] = label_data['Country'] + ' (#' + label_data['Rank'].astype(str) + ')'
label_data.to_csv("dtp3_peer_band_labels.csv", index=False)
print(label_data[['Country', 'Year', 'Rank', 'Label']])
chart_data = chart_data.sort_values(['Year', 'Rank'])
chart_data.to_csv("dtp3_australia_peer_band_fixed.csv", index=False)
print(chart_data.head(20))