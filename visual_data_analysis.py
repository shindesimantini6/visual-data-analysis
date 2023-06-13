# Import all required packages
import pandas as pd
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import seaborn as sns

# Read fertility rate per country per year file
fert = pd.read_csv('./data/gapminder_total_fertility.csv', index_col=0)

# Convert columns to integers
fert.columns = fert.columns.astype(int)

# Replace index name to country
fert.index.name = 'country'

# Reset index while converting to long format
fert = fert.reset_index()

# Convert from wide to long form 
fert = fert.melt(id_vars='country', var_name='year', value_name='fertility_rate')

# Read life expectancy per country per year file
life = pd.read_excel('./data/gapminder_lifeexpectancy.xlsx', index_col=0)

# Rename the Life Expectancy column to country
life.index.name = 'country'

# Reset index while converting to long format
life = life.reset_index()

# Convert from wide to long form
life = life.melt(id_vars='country', var_name='year', value_name='life_expectancy')

# Read population per country per year data
pop = pd.read_excel('./data/gapminder_population.xlsx', index_col=0)

# Rename the Total population column to country
pop.index.name = 'country'

# Reset index while converting to long format
pop = pop.reset_index()

# Convert from wide to long form
pop = pop.melt(id_vars='country', var_name='year', value_name='total_population')

# Read the country per continents data
continents = pd.read_csv('./data/continents.csv',  sep = ";")

# Read the income per capita per country per year data
income = pd.read_csv('/home/shinde/Documents/trainings/Spiced_Academy/Spiced_projects/Week_1/data/income_per_person_gdppercapita_ppp_inflation_adjusted.csv')
# income.head(10)

# Melt the data
income = income.melt(id_vars='country', var_name='year', value_name='income')

# Convert year to int
income["year"]= income.year.astype(int)

# Replace k with 1000 # Data Pre-processing
income['income'] = income['income'].replace({'k': '*1e3'}, regex=True).map(pd.eval)


# Merge all datasets
df_fert_pop = fert.merge(pop)
df_fert_pop_life = df_fert_pop.merge(life)
df_2 = df_fert_pop_life.merge(continents)
df = df_2.merge(income)

# Create a subset which has all years above 1960 and above 2015
df_subset = df.loc[(df['year'] <= 2015) & (df['year'] >= 1960)]

# Average of the total population for all continents
mean_pop = df_subset["total_population"].agg("mean")

# Create plots for each year and save them in a folder
for year in df_subset["year"].unique():
    fig, ax = plt.subplots(2, 1, figsize=(12, 12), dpi=200, constrained_layout=False, sharex=True)

    sns.axes_style("ticks")
    sns.set_context("talk", font_scale=1, rc={"lines.linewidth": 2.5})
    clarity_ranking = df_subset["continent"].unique()

    # Average of the population for a single year
    mean_year = data=df_subset[df_subset["year"] == year]["total_population"].agg('mean')

    # Ratio of the total population for one year to all years
    mean_factor = mean_year/mean_pop
    
    # Plot fertility rates in first row
    sns.scatterplot(ax=ax[0], data=df_subset[df_subset["year"] == year],
                    hue_order=clarity_ranking, x='life_expectancy', y='fertility_rate',
                    size="total_population", hue="continent", sizes=(20*mean_factor, 2000*mean_factor),
                    palette="tab10", legend="brief", alpha=0.5)
    ax[0].legend([], [], frameon=False)
    fig.text(0.43, 0.52, year, fontsize=50, ha="left", va="top", color="Brown", alpha=0.5)
    h, l = ax[0].get_legend_handles_labels()
    fig.legend(h[0:7], l[0:7], bbox_to_anchor=(0.4, 0.6), loc=1, borderaxespad=1, fontsize=13, )  # title ="Continent")
    ax[0].set_title("Life expectancy, fertility rates and "+ "\n "+"income per person for all countries in the world")
    ax[0].set_ylabel('Fertility Rates', fontsize=20)
    ax[0].set_xlim([50, 90.0])
    ax[0].set_ylim([0, 8])

    # Plot income plot in second row
    sns.scatterplot(ax=ax[1], data=df_subset[df_subset["year"] == year],
                    hue_order=clarity_ranking, x='life_expectancy', y='income',
                    size="total_population", hue="continent", sizes=(20*mean_factor, 2000*mean_factor),
                    palette="tab10", legend=False, alpha=0.5)

    ax[1].set_xlabel('Life Expectancy', fontsize=20)
    ax[1].set_ylabel("Income per person ($US)", fontsize=20)
    ax[1].set_xlim([50, 90.0])
    ax[1].set_ylim([0, 140000])
    sns.set_theme(style="darkgrid")
    plt.savefig('./project_results/life'+ "_" + str(year)+'.png')
    plt.close()

# Create GIF
images = []
for i in sorted(range(1960, 2016)):
    filename = './project_results/life_{}.png'.format(i)
    images.append(imageio.imread(filename))

imageio.mimsave('final_gif_with_income_png.gif', images, fps = 2)
