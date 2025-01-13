import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit Page Configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add Custom CSS for Styling
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&family=Pacifico&display=swap');
    .stApp {
        background-image:
        radial-gradient(circle, rgba(0, 0, 0, 0.2) 80%, rgba(0, 0, 0, 1) 100%),
        url("https://w0.peakpx.com/wallpaper/79/587/HD-wallpaper-mask-black-vendetta-broken-logo-steel-joker-pink-love-white.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        font-family: 'Roboto', sans-serif;
    }
    .title {
        text-align: center;
        font-size: 2.5em;
        color: white;
        margin-bottom: 20px;
        font-family: 'Pacifico', cursive;
    }
    .stButton>button {
        background-color: transparent;
        color: white;
        border: 2px solid #orange;
        border-radius: 5px;
        font-size: 16px;
        padding: 10px 20px;
        margin-top: 10px;
        font-family: 'Roboto', sans-serif;
    }
    .stButton>button:hover {
        background-color: white;
        color: black;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown(
    """
    <h1 class='title' style='color: black; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>
        WhatsApp Chat Analyzer
    </h1>
    """,
    unsafe_allow_html=True
)


# Sidebar
st.sidebar.title("📊 WhatsApp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        # Display statistics
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        # Title with Text Border
        st.markdown(
            """
            <h1 style='color: white; -webkit-text-stroke: 1px black; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-size: 2.2em;'>
                📈 Top Statistics
            </h1>
            """,
            unsafe_allow_html=True,
        )
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div style='text-align: center; background-color: #FAF3E0; padding: 10px; border-radius: 10px'>
                    <h1 style='color: #A52A2A; font-size: 1.8em; border: 2px solid black; padding: 5px; border-radius: 5px;'>Total Messages</h1>
                    <h1 style='color: black; font-size: 2em; margin-top: 10px;'>{num_messages}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div style='text-align: center; background-color: #FFE3E0; padding: 10px; border-radius: 10px; margin-top: 10px;'>
                    <h1 style='color: #A52A2A; font-size: 1.8em; border: 2px solid black; padding: 5px; border-radius: 5px;'>Total Words</h1>
                    <h1 style='color: black; font-size: 2em; margin-top: 10px;'>{words}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div style='text-align: center; background-color: #f0f5ff; padding: 10px; border-radius: 10px; margin-top: 10px;'>
                    <h1 style='color: #A52A2A; font-size: 1.8em; border: 2px solid black; padding: 5px; border-radius: 5px;'>Media Shared</h1>
                    <h1 style='color: black; font-size: 2em; margin-top: 10px;'>{num_media_messages}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col4:
            st.markdown(
                f"""
                <div style='text-align: center; background-color: #fff0fc; padding: 10px; border-radius: 10px; margin-top: 10px;'>
                    <h1 style='color: #A52A2A; font-size: 1.8em; border: 2px solid black; padding: 5px; border-radius: 5px;'>Links Shared</h1>
                    <h1 style='color: black; font-size: 2em; margin-top: 10px;'>{num_links}</h1>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Monthly timeline
        # Title with Text Border
        st.markdown(
            """
            <h1 style='color: white; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); -webkit-text-stroke: 1px black; font-size: 2em; text-align: left;'>
                📅 Monthly Timeline
            </h1>
            """,
            unsafe_allow_html=True,
        )

        timeline = helper.monthly_timeline(selected_user, df)
        # Create a plot with a customized background
        fig, ax = plt.subplots(figsize=(10, 6))

        # Change the background color of the plot
        ax.set_facecolor('#2E2E2E')  # Dark background for the plot
        fig.patch.set_facecolor('#1C1C1C')  # Dark background for the figure

        # Plot the timeline data with custom color
        ax.plot(timeline['time'], timeline['message'], color='red', linewidth=2)

        # Add gridlines with a different color
        ax.grid(True, color='white', linestyle='--', linewidth=0.5)

        # Customize x-axis labels (rotate them for better visibility)
        plt.xticks(rotation='vertical', color='white', fontsize=12)

        # Customize y-axis labels and set the color to white
        plt.yticks(color='white', fontsize=12)

        plt.title(" ") #to make gap in top

        # Add y-axis and x-axis labels (optional)
        ax.set_xlabel('Time', fontsize=14, color='white', labelpad=15)
        ax.set_ylabel('Messages', fontsize=14, color='white', labelpad=15)

        # Adjust layout to avoid clipping
        plt.tight_layout()

        # Show the plot in the Streamlit app
        st.pyplot(fig)

        # Daily timeline
        # Title with Text Border
        st.markdown(
            """
            <h1 style='color: white; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); -webkit-text-stroke: 1px black; font-size: 2em;'>
                📅 Daily Timeline
            </h1>
            """,
            unsafe_allow_html=True,
        )
        # Create the daily timeline plot with a customized background
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 6))

        # Change the background color of the plot
        ax.set_facecolor('#2E2E2E')  # Dark background for the plot
        fig.patch.set_facecolor('#1C1C1C')  # Dark background for the figure

        # Plot the daily timeline data with a custom color
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green', linewidth=2)

        # Add gridlines with a different color
        ax.grid(True, color='white', linestyle='--', linewidth=0.5)

        # Customize x-axis labels (rotate them for better visibility) and set the color to white
        plt.xticks(rotation='vertical', color='white', fontsize=12)

        # Customize y-axis labels and set the color to white
        plt.yticks(color='white', fontsize=12)

        # Add x-axis and y-axis labels (optional)
        ax.set_xlabel('Date', fontsize=14, color='white', labelpad=20)
        ax.set_ylabel('Messages', fontsize=14, color='white', labelpad=18)

        # Title
        plt.title(" ")

        # Adjust layout to avoid clipping
        plt.tight_layout()

        # Show the plot in the Streamlit app
        st.pyplot(fig)

        # Activity Map
        # Title with Text Border
        st.markdown(
            """
            <h1 style='color: white; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); -webkit-text-stroke: 1px black; font-size: 2.1em;'>
                🗺️ Activity Map
            </h1>
            """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)

        # Most Busy Day
        with col1:
            # Use custom HTML for header styling
            st.markdown(
                """
                <h2 style='color: white; font-size: 2em; -webkit-text-stroke: 1px black; font-weight: bold;'>
                    Most Busy Day
                </h2>
                """, unsafe_allow_html=True
            )
            # Get the busy day data
            busy_day = helper.week_activity_map(selected_user, df)

            # Create the figure and axis for the plot
            fig, ax = plt.subplots(figsize=(10, 6))

            # Set background color for the plot
            ax.set_facecolor('#2E2E2E')  # Dark background for the plot
            fig.patch.set_facecolor('#1C1C1C')  # Dark background for the figure

            # Bar plot for busy day
            ax.bar(busy_day.index, busy_day.values, color='purple', edgecolor='black', linewidth=1.5)

            # Customize x-axis labels and rotate them
            plt.xticks(rotation='vertical', color='white', fontsize=12)

            # Customize y-axis labels
            plt.yticks(color='white', fontsize=12)

            plt.title(" ")

            # Set axis labels with padding
            ax.set_xlabel('Day of the Week', fontsize=14, color='white', labelpad=15)
            ax.set_ylabel('Number of Messages', fontsize=14, color='white', labelpad=15)

            # Add gridlines with a lighter color and dashed lines for style
            ax.grid(True, color='white', linestyle='--', linewidth=0.5)

            # Adjust layout to avoid clipping
            plt.tight_layout()

            # Display the plot in Streamlit
            st.pyplot(fig)

        # Most Busy Month
        with col2:
            # Use custom HTML for header styling
            st.markdown(
                """
                <h2 style='color: white; font-size: 2em; -webkit-text-stroke: 1px black; font-weight: bold;'>
                    Most Busy Month
                </h2>
                """, unsafe_allow_html=True
            )
            # Get the busy month data
            busy_month = helper.month_activity_map(selected_user, df)

            # Create the figure and axis for the plot
            fig, ax = plt.subplots(figsize=(10, 6))

            # Set background color for the plot
            ax.set_facecolor('#2E2E2E')  # Dark background for the plot
            fig.patch.set_facecolor('#1C1C1C')  # Dark background for the figure

            # Bar plot for busy month
            ax.bar(busy_month.index, busy_month.values, color='orange', edgecolor='black', linewidth=1.5)

            # Customize x-axis labels and rotate them
            plt.xticks(rotation='vertical', color='white', fontsize=12)

            # Customize y-axis labels
            plt.yticks(color='white', fontsize=12)

            # Set axis labels with padding
            ax.set_xlabel('Month', fontsize=14, color='white', labelpad=15)
            ax.set_ylabel('Number of Messages', fontsize=14, color='white', labelpad=15)

            plt.title(" ")

            # Add gridlines with a lighter color and dashed lines for style
            ax.grid(True, color='white', linestyle='--', linewidth=0.5)

            # Adjust layout to avoid clipping
            plt.tight_layout()

            # Display the plot in Streamlit
            st.pyplot(fig)

        # Heatmap
        # Title with Text Border
        st.markdown(
            """
            <h1 style='color: white; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); -webkit-text-stroke: 1px black; font-size: 1.7em;'>
                📅 Weekly Activity Map
            </h1>
            """,
            unsafe_allow_html=True,
        )

        user_heatmap = helper.activity_heatmap(selected_user, df)

        # Create the figure and axis for the plot
        fig, ax = plt.subplots()

        # Set the background color for the plot and figure to a lighter shade
        ax.set_facecolor('#2E2E2E')  # Light background for the plot
        fig.patch.set_facecolor('#1C1C1C')  # Light background for the figure

        # Create the heatmap without annotations and customize the color bar
        ax = sns.heatmap(
            user_heatmap,
            cmap='YlGnBu',
            cbar_kws={
                'shrink': 0.8,
                'ticks': [0, 50, 100, 150, 200, 250, 300],  # Adjust tick range as per your data
                'format': "%.0f"  # Format ticks as integers
            },
            annot=False  # Remove numbers inside the heatmap
        )

        # Customize the color bar appearance
        cbar = ax.collections[0].colorbar
        cbar.ax.tick_params(colors='white')  # Change color bar tick labels to black
        cbar.ax.yaxis.label.set_color('white')  # Change color of the color bar label (if any)

        # Customize x-axis labels and rotate them
        plt.xticks(rotation='vertical', color='white', fontsize=8)

        # Customize y-axis labels
        plt.yticks(color='white', fontsize=12)

        # Set axis labels with padding
        ax.set_xlabel('Month', fontsize=10, color='white', labelpad=15)
        ax.set_ylabel('Number of Messages', fontsize=10, color='white')

        plt.title(" ")

        # Display the plot in Streamlit
        st.pyplot(fig)

        # Busiest Users
        if selected_user == 'Overall':
            # Title with subtle styling
            st.markdown(
                """
                <h1 style='color: white; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); -webkit-text-stroke: 1px black; font-size: 2em;'>
                    👥 Most Busy Users
                </h1>
                """,
                unsafe_allow_html=True,
            )

            # Get data for busiest users
            x, new_df = helper.most_busy_users(df)

            # Format column 2 to display only 2 decimal places
            new_df.iloc[:, 1] = new_df.iloc[:, 1].apply(lambda x: f"{x:.2f}")

            fig, ax = plt.subplots()

            # Split the layout into two columns
            col1, col2 = st.columns(2)

            with col1:
                # Customize the bar plot with minimal styling
                ax.bar(
                    x.index, x.values,
                    color=['#FF6F61', '#FFA07A', '#FA8072', '#E9967A', '#FF4500'],
                    edgecolor='black',
                    linewidth=1
                )

                # Rotate x-axis labels for better readability
                plt.xticks(rotation='vertical', fontsize=10, color='black')
                plt.yticks(fontsize=10, color='black')

                # Add title and labels with slight padding
                plt.title(" ")
                ax.set_xlabel('Users', fontsize=12, labelpad=10)
                ax.set_ylabel('Message Count', fontsize=12, labelpad=10)

                # Set light grey background for the plot
                ax.set_facecolor('#F9F9F9')
                fig.patch.set_facecolor('#FFFFFF')

                # Display the plot
                st.pyplot(fig)

                # Rename the columns in new_df
                new_df.columns = ['Name', 'Count']
            with col2:
                # Style the DataFrame for a cleaner look
                styled_df = new_df.style.set_properties(**{
                    'background-color': '#FFFFFF',
                    'color': '#333333',
                    'border-color': '#DDDDDD',
                    'font-size': '14px',
                    'padding': '5px',
                })
                st.dataframe(styled_df)

        # WordCloud
        # Add a styled title for better visual appeal
        st.markdown(
            """
            <h1 style='color: white; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); -webkit-text-stroke: 1px #3498DB; font-size: 2.7em;'>
                ☁️ WordCloud
            </h1>
            """,
            unsafe_allow_html=True,
        )

        try:
            # Generate the WordCloud
            df_wc = helper.create_wordcloud(selected_user, df)

            # Create the figure and axis for displaying the WordCloud
            fig, ax = plt.subplots(figsize=(8, 6))  # Adjust size for better visibility
            ax.imshow(df_wc, interpolation='bilinear')
            ax.axis('off')  # Turn off axis to focus on the WordCloud
            fig.patch.set_facecolor('#F0F8FF')  # Light blue background for the figure

            # Display the WordCloud
            st.pyplot(fig)
        except ValueError:
            # Display an error message if WordCloud generation fails
            st.error(
                """
                <h3 style='color: #E74C3C; text-align: center;'>
                    Not enough data to generate a WordCloud. Please select another user or overall.
                </h3>
                """,
                unsafe_allow_html=True,
            )

        # Most Common Words
        st.markdown(
            """
            <h1 style='color: #FFFFFF; -webkit-text-stroke: 1px black; font-size: 2.5em; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); text-align: center;'>
                📝 Most Common <br> Words
            </h1>
            """,
            unsafe_allow_html=True
        )

        most_common_df = helper.most_common_words(selected_user, df)

        if most_common_df.empty:
            st.error("No words found for this user.")
        else:
            # Create figure and axis for the plot
            fig, ax = plt.subplots(figsize=(10, 6))

            # Create a horizontal bar plot with a cool color palette
            bars = ax.barh(most_common_df[0], most_common_df[1], color='lightblue', edgecolor='black')

            # Add value labels on bars for clarity
            for bar in bars:
                width = bar.get_width()
                ax.text(
                    width + 0.8,
                    bar.get_y() + bar.get_height() / 2,
                    f'{width:.0f}',
                    va='center',
                    fontsize=12,
                    color='black'
                )

            # Set x-axis label and y-axis label with styling
            ax.set_xlabel('Frequency', fontsize=14, color='black', labelpad=15)
            ax.set_ylabel('Words', fontsize=14, color='black', labelpad=15)
            plt.title(" ")

            # Set a soft gradient background for the plot
            ax.set_facecolor('#F0F8FF')  # Light blue color for the plot background

            # Customize the background of the figure
            fig.patch.set_facecolor('#fbaed2')  # Sky blue color for the figure background

            # Customize x-ticks and y-ticks
            plt.xticks(rotation='vertical', fontsize=12, color='black')
            plt.yticks(fontsize=15, color='black')

            # Display the plot in Streamlit
            st.pyplot(fig)

        # Emoji Analysis
        st.markdown(
            """
            <h1 style='color: #FFFFFF; -webkit-text-stroke: 1px black; font-size: 2.2em; font-family: "Arial", sans-serif; text-shadow: 2px 2px 4px rgba(0,0,0,0.5)'>
                😊 Emoji Analysis
            </h1>
            """,
            unsafe_allow_html=True
        )

        # Get emoji data
        emoji_df = helper.emoji_helper(selected_user, df)

        if emoji_df.empty:
            st.error("Not enough data for emoji analysis.")
        else:
            # Rename the columns in emoji_df
            emoji_df.columns = ['Emoji', 'Count']
            # Split the layout into two columns
            col1, col2 = st.columns(2)

            # Column 1: Display DataFrame
            with col1:

                # Adjust the table dimensions and styling
                styled_emoji_df = emoji_df.style.set_properties(
                    **{
                        'background-color': '#1E1E1E',  # Dark background for cells
                        'color': 'white',  # White text
                        'border-color': '#555555',  # Subtle border color
                        'border-width': '1px',
                        'border-style': 'solid',
                        'font-size': '16px',  # Larger font size
                        'padding': '10px',  # Padding for better spacing
                    }
                ).highlight_max(axis=0, color='#FFD700')  # Highlight max values in yellow

                # Use Streamlit's styling to increase table size
                st.markdown(
                    """
                    <style>
                    .dataframe tbody tr th {
                        font-size: 18px;  /* Larger font size for row headers */
                    }
                    .dataframe tbody tr td {
                        font-size: 16px;  /* Larger font size for cell values */
                    }
                    .dataframe {
                        margin: 20px auto;  /* Center align table */
                        width: 95%;  /* Make the table wider */
                        background-color: #2E2E2E; /* Match background to table */
                        border-radius: 10px; /* Rounded edges */
                        overflow: hidden; /* Keep table clean */
                    }
                    </style>
                    """,
                    unsafe_allow_html=True,
                )
                # Display the styled DataFrame
                st.dataframe(styled_emoji_df, use_container_width=True)
