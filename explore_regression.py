import seaborn as sns
import matplotlib.pyplot as plt


def plot_categorical_and_continuous_vars (df, cat_col, cont_col):
    """takes df, categorical column, and continuous column of user choice and plots a box/violin/and bar plot of relationship to user chosen columns
    """
    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))
    sns.boxplot(x=cat_col, y=cont_col, data=df, ax=axes[0])
    axes[0].set_title('Boxenplot')

    sns.violinplot(x=cat_col, y=cont_col, data=df, ax=axes[1])
    axes[1].set_title('Violinplot')

    sns.barplot(x=cat_col, y=cont_col, data=df, ax=axes[2])
    axes[2].set_title('Barplot')
    
    return plt.show()


def plot_variable_pairs(df):
    """
    takes correlated variable(.corr) and returns plot based on user inputted info
    """
    sns.pairplot(data=df, kind='reg', corner=True)
    return plt.show()


def visualize(df):
    """
    Creates visualizations for our dataframe to visualize relationships between categorical and continuous variables.
    Excludes categorical columns for plotting.
    """
    # Identify continuous columns excluding 'county'
    continuous_cols = [col for col in df.columns if col != 'county']

    # Plot for each continuous column against 'county'
    for col in continuous_cols:
        plot_categorical_and_continuous_vars(df, 'county', col)

# Call the visualize function with your DataFrame 'train'
