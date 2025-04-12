import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel("C:/Users/rudra/OneDrive/Documents/DSPYTH/1617fedschoolcodelist.xls")

# ---------------------- DATA CLEANING ----------------------

# Drop duplicates
df.drop_duplicates(inplace=True)

# Drop rows with missing key values
df.dropna(subset=['SchoolCode', 'SchoolName', 'StateCode'], inplace=True)

# Strip whitespace and uppercase standardization
df['SchoolName'] = df['SchoolName'].str.strip().str.upper()
df['City'] = df['City'].str.strip().str.title()
df['StateCode'] = df['StateCode'].str.strip().str.upper()

# Objective 1: Pie Chart – Top 5 States by School Count
state_counts = df['StateCode'].value_counts().head(5)
plt.figure(figsize=(8, 8))
plt.pie(state_counts.values, labels=state_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Blues"))
plt.title("Top 5 States by School Count")
plt.axis('equal')
plt.tight_layout()
plt.show()

# Objective 2: Horizontal Bar – Top 10 Cities
city_counts = df['City'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=city_counts.values, y=city_counts.index, palette='Greens_d')
plt.title("Top 10 Cities with Most Schools")
plt.xlabel("Number of Schools")
plt.ylabel("City")
plt.tight_layout()
plt.show()

# Objective 3: Line Plot – Top 10 ZIP Codes
zip_counts = df['ZipCode'].value_counts().head(10)
plt.figure(figsize=(10, 6))
sns.lineplot(x=zip_counts.index.astype(str), y=zip_counts.values, marker='o', color='orange')
plt.title("Top 10 ZIP Codes by School Count")
plt.xlabel("ZIP Code")
plt.ylabel("Number of Schools")
plt.tight_layout()
plt.show()

# Objective 4: Grouped Bar Chart – Top Cities vs States
top_states = df['StateCode'].value_counts().head(5).index.tolist()
top_cities = df['City'].value_counts().head(5).index.tolist()
group_data = df[df['StateCode'].isin(top_states) & df['City'].isin(top_cities)]
grouped = group_data.groupby(['StateCode', 'City']).size().reset_index(name='SchoolCount')

plt.figure(figsize=(10, 6))
sns.barplot(data=grouped, x='City', y='SchoolCount', hue='StateCode', palette='muted')
plt.title("Comparison of School Counts in Top Cities Across Top States")
plt.xlabel("City")
plt.ylabel("Number of Schools")
plt.legend(title="State")
plt.tight_layout()
plt.show()

# Objective 5: Number of Schools in Each Top 10 Cities of Top 3 States
top_3_states = df['StateCode'].value_counts().head(3).index.tolist()
filtered_df = df[df['StateCode'].isin(top_3_states)]
city_counts = filtered_df.groupby(['City', 'StateCode']).size().reset_index(name='SchoolCount')
top_10_cities = city_counts.sort_values('SchoolCount', ascending=False).head(10)
pivot_data = top_10_cities.pivot(index='City', columns='StateCode', values='SchoolCount').fillna(0)
pivot_data.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Set2')
plt.title("Top 10 Cities by School Count (Top 3 States)")
plt.xlabel("City")
plt.ylabel("Number of Schools")
plt.legend(title="State")
plt.tight_layout()
plt.show()


# Objective 6: Heatmap – State vs City (Top 10)
top_states = df['StateCode'].value_counts().head(10).index
top_cities = df['City'].value_counts().head(10).index
heatmap_data = df[df['StateCode'].isin(top_states) & df['City'].isin(top_cities)]
pivot = heatmap_data.pivot_table(index='StateCode', columns='City', aggfunc='size', fill_value=0)

plt.figure(figsize=(12, 6))
sns.heatmap(pivot, annot=True, fmt="d", cmap="YlGnBu")
plt.title("Heatmap: Number of Schools by State and City")
plt.xlabel("City")
plt.ylabel("State")
plt.tight_layout()
plt.show()

# Objective 7: Region-wise School Count – Bar Chart
region_map = {
    'NORTHEAST': ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA'],
    'MIDWEST': ['IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD'],
    'SOUTH': ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'DC', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX'],
    'WEST': ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']
}

def assign_region(state):
    for region, states in region_map.items():
        if state in states:
            return region
    return 'Other'

df['Region'] = df['StateCode'].apply(assign_region)
region_counts = df['Region'].value_counts()

plt.figure(figsize=(10, 6))
sns.barplot(x=region_counts.index, y=region_counts.values, palette='coolwarm')
plt.title("Number of Schools by U.S. Region")
plt.xlabel("Region")
plt.ylabel("Number of Schools")
plt.tight_layout()
plt.show()
