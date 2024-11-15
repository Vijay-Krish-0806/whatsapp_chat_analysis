import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

# Sidebar customization
st.sidebar.title("📊 WhatsApp Chat Analyzer")
st.sidebar.subheader("Upload your chat file for analysis")

uploaded_file = st.sidebar.file_uploader("📂 Choose a file")

# Process uploaded file
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users for selection
    user_list = list(df['user'].unique())
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("👤 Analyze data for", user_list)

    # Show analysis button
    if st.sidebar.button("🔍 Show Analysis"):

        # Main app section
        st.title("📈 WhatsApp Chat Analysis")

        # Top statistics
        num_msgs, count, media_num, num_links = helper.fetch_stats(selected_user, df)
        st.header("🔢 Key Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Messages", num_msgs)
        with col2:
            st.metric("Total Words", count)
        with col3:
            st.metric("Media Shared", media_num)
        with col4:
            st.metric("Links Shared", num_links)

        # Monthly timeline
        st.header("🗓️ Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='blue', linewidth=2)
        ax.set_xlabel("Time")
        ax.set_ylabel("Messages")
        plt.xticks(rotation='vertical', color='blue')
        st.pyplot(fig)

        # Daily timeline
        st.header("📅 Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='green', linewidth=2)
        ax.set_xlabel("Date")
        ax.set_ylabel("Messages")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        st.header("🗺️ Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Active Days")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='yellow')
            ax.set_xlabel("Day")
            ax.set_ylabel("Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("Most Active Months")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            ax.set_xlabel("Month")
            ax.set_ylabel("Messages")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # Busiest users (for group chats)
        if selected_user == "Overall":
            st.header("👥 Most Active Users")
            x, new_df = helper.fetch_most_busy_users(df)
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='red')
                ax.set_xlabel("Users")
                ax.set_ylabel("Message Count")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # Word Cloud
        st.header("☁️ Word Cloud")
        df_wc = helper.create_wordcloud(df, selected_user)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)

        # Most Common Words
        st.header("📝 Most Common Words")
        most_common = helper.most_common(df, selected_user).reset_index(drop=True).head(20)
        fig, ax = plt.subplots()
        ax.barh(most_common['Word'], most_common['Frequency'], color='purple')
        ax.set_xlabel("Frequency")
        ax.set_ylabel("Words")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.header("😃 Emoji Analysis")
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df.head(20), width=350)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(
                emoji_df['Count'].head(5),
                labels=emoji_df['Emoji'].head(5),
                startangle=90,
                autopct="%0.2f%%",
                colors=plt.cm.tab20.colors
            )
            ax.axis('equal')
            st.pyplot(fig)

# Footer
st.sidebar.markdown("---")
