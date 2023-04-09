"""Streamlit app."""
# Import standard libraries
import datetime
# Import 3rd party libraries
import streamlit as st
import streamlit.components.v1 as components

# Import modules
import twitter as twi

# Define functions
@st.cache_data(ttl=60*60*12, show_spinner=True)
def check_data(account: str) -> list:
    twitter = twi.Twitter(account=account)
    if twitter:
        st.write(twitter)
    return []

@st.cache_data(ttl=60*60*12, show_spinner=True)
def top_authors(account: str, da: str, to: str, top: int) -> list:
    twitter = twi.Twitter(account=account)
    likes = twitter.fetch_all_likes_since(since=da, until=to)
    st.write(likes)
    if likes:
        return twitter.get_liked_authors(likes=likes, number=top)
    return []


# Configure Streamlit page and state
st.set_page_config(page_title="Twitter Top Most Liked", page_icon=":shark:")

# Force responsive layout for columns also on mobile
st.write(
    """<style>
    @media (max-width: 480px) {
        [data-testid="column"] {
            min-width: calc(9% - 1rem);
            padding: 0 0.2rem;
        }
    }
    </style>""",
    unsafe_allow_html=True,
)

# Render Streamlit page
st.title("Twitter Account Most Liked")
st.markdown(
    """
        Generate an overview of a Twitter account's most liked Tweet authors. You can find the code for this mini-app on [GitHub](https://github.com/alikon/twitter-wrapped) and the author on [Twitter](https://twitter.com/alikon).
    """
)
account = st.text_input(label="Twitter account").replace("@", "")
datefrom = st.sidebar.date_input(
    "From ",
    datetime.date(2023, 1, 1))

dateto = st.sidebar.date_input(
    "To ",
     datetime.date.today())

numero = st.sidebar.slider('Top Liked', 1, 100, 10)

da = datefrom.strftime('%F')
to = dateto.strftime('%F')

if account:
    check_data(account=account)
   # getch top authors
    top_authors = top_authors(account=account, da=da, to=to, top=numero)
    if top_authors:
        st.markdown("""---""")
        st.markdown(
            f"""
                Top {numero} authors for [@{account}](https://twitter.com/{account}) from {da} to {to}
            """
        )
        for i, author in enumerate(top_authors):
            cols = st.columns([1, 2, 13])
            cols[0].markdown(f"**{i + 1}**")
            cols[1].image(author[0][1], width=35)
            cols[2].markdown(
                f"**[@{author[0][0]}](https://twitter.com/{author[0][0]})**"
            )
        st.markdown("""---""")
        formatted_top_authors = "\n".join(
            [f"{i+1}) @{a[0][0]} " for i, a in enumerate(top_authors)]
        )
        #st.markdown("**Share your result**")
        components.html(
            f"""
               <a href="https://twitter.com/share?ref_src=twsrc%5Etfw" class="twitter-share-button" data-size="large" data-text="#TwitterMostLiked \n\n@{account}'s most liked accounts:\n{formatted_top_authors}\n\nMade with" data-url="https://github.com/alikon/twitter-wrapped" data-show-count="false">Share your result</a><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
            """,
            height=40,
        )
    else:
      st.info("No liked found")
