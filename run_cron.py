import os
import time
import requests
import http.server
import socketserver
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# Add a dummy server to bind to a port
def start_dummy_server():
    PORT = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving dummy server on port {PORT}")
        while True:
            run()
            time.sleep(3600)  # Replace with your actual task logic


def run():
    headers = {
        'accept': '*/*',
        'accept-language': 'tr-TR,tr;q=0.9',
        'authorization': os.environ.get("authorization"),
        'content-type': 'application/json',
        'origin': 'https://x.com',
        'referer': 'https://x.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'x-guest-token': os.environ.get("guest_token")
    }
    
    params = {
        'variables': '{"screen_name":"keremakturkoglu"}',
        'features': '{"hidden_profile_subscriptions_enabled":true,"profile_label_improvements_pcf_label_in_post_enabled":false,"rweb_tipjar_consumption_enabled":true,"responsive_web_graphql_exclude_directive_enabled":true,"verified_phone_label_enabled":false,"subscriptions_verification_info_is_identity_verified_enabled":true,"subscriptions_verification_info_verified_since_enabled":true,"highlights_tweets_tab_ui_enabled":true,"responsive_web_twitter_article_notes_tab_enabled":true,"subscriptions_feature_can_gift_premium":true,"creator_subscriptions_tweet_preview_api_enabled":true,"responsive_web_graphql_skip_user_profile_image_extensions_enabled":false,"responsive_web_graphql_timeline_navigation_enabled":true}',
        'fieldToggles': '{"withAuxiliaryUserLabels":false}',
    }
    
    response = requests.get(
        'https://api.x.com/graphql/QGIw94L0abhuohrr76cSbw/UserByScreenName',
        params=params,
        headers=headers,
    )
    
    followers_count = response.json()["data"]["user"]["result"]["legacy"]["followers_count"]
    
    message = Mail(
        from_email="kafessizinsta@gmail.com",
        to_emails="ahmetgrhn@gmail.com",
        subject="Kerem Akturkuglu Followers",
        html_content=f"<strong>Followers: {followers_count}</strong>")
    try:
        sg = SendGridAPIClient(os.environ.get("sendgrid_api_key"))
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e)


# Call the dummy server
if __name__ == "__main__":
    start_dummy_server()
