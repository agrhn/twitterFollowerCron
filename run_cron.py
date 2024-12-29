import os
import time
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from socketserver import TCPServer
from http.server import SimpleHTTPRequestHandler


# Start a simple HTTP server to keep the Render service alive
def start_server():
    PORT = 8080  # Render expects the service to listen on a port (e.g., 8080)
    with TCPServer(("", PORT), SimpleHTTPRequestHandler) as httpd:
        print(f"Serving HTTP on port {PORT}...")
        httpd.serve_forever()


# Your cron job logic
def run_cron_job():
    while True:
        print("Running cron job...")
        run()
        time.sleep(3600)  # Wait for an hour


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


if __name__ == "__main__":
    from threading import Thread

    # Run the web server in a separate thread
    server_thread = Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # Run your cron job in the main thread
    run_cron_job()
