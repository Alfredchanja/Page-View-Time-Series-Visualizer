import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore
import seaborn as sns # type: ignore
from pandas.plotting import register_matplotlib_converters # type: ignore
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'])
df.set_index('date', inplace=True)

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & 
        (df['value'] <= df['value'].quantile(.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize = (10, 5))

    ax.plot(df.index, df['value'], color = 'red', linewidth = 1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()

    df_bar['Year'] = df.index.year
    df_bar['Month'] = df.index.month
    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean().unstack()

    # Draw bar plot
    fig, ax = plt.subplots(figsize = (10, 6))
    df_bar.plot(kind = 'bar', ax=ax)

    ax.set_title('Year-wise Box Plot (Trend)')
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    ax.legend(title = 'Month', labels = ('January', 'February', 'March', 'April',
                                         'May', 'June', 'July', 'August',
                                         'September', 'October', 'November', 'December'))


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # 1st Plot: Year-wise Box Plot (Trend)
    ax1 = sns.boxplot(x ='year', y='value', data=df_box, ax=ax1, palette='Set2')
    ax1.set_title("Year-wise Box Plot (Trend)")
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Page Views')

    # 2nd Plot: Month-wise Box Plot (Seasonality)
    ax2 = sns.boxplot(x='month', y='value', data=df_box, ax=ax2,
                      order=['Jan', 'Feb', 'Mar', 'Apr',
                             'May', 'Jun', 'Jul','Aug',
                             'Sep', 'Oct', 'Nov', 'Dec'], palette='Set2')
    ax2.set_title("Month-wise Box Plot (Seasonality)")
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig