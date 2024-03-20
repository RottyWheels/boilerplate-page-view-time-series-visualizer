import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df = pd.read_csv('./fcc-forum-pageviews.csv', parse_dates=['date'])

# Clean data
df = df[(df['value'] < df['value'].quantile(0.975)) &
        (df['value'] > df['value'].quantile(0.025))]

print(df.head())


def draw_line_plot():
    # Create a new figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the line chart
    ax.plot(df['date'], df['value'], color='r', linewidth=1)

    # Set title and labels
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.tick_params(axis='x', rotation=45)

    # Save image and show
    fig.tight_layout()
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    # Convert 'date' column to datetime
    df_bar['date'] = pd.to_datetime(df_bar['date'])

    # Extract year and month from the 'date' column
    df_bar['Year'] = df_bar['date'].dt.year
    df_bar['Month'] = df_bar['date'].dt.month

    # Calculate average page views for each month grouped by year
    avg_page_views = df_bar.groupby(['Year', 'Month'])[
        'value'].mean().unstack()

    # Plotting the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    avg_page_views.plot(kind='bar', ax=ax)

    # Set title and labels
    ax.set_title("Average Daily Page Views by Month")
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title="Months", labels=[
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ])

    # Save image and show
    fig.tight_layout()
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    # Convert 'value' column to float
    df_box['value'] = df_box['value'].astype(float)

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(20, 10), sharex=False, sharey=False)

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0]).set(xlabel="Year", ylabel="Page Views", title="Year-wise Box Plot (Trend)")

    sns.boxplot(x='month', y='value', data=df_box, order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                ax=axes[1]).set(xlabel="Month", ylabel="Page Views", title="Month-wise Box Plot (Seasonality)")

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig

