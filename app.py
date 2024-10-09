from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_oauthlib.client import OAuth
from solders.pubkey import Pubkey
from solana.rpc.async_api import AsyncClient
from solana.transaction import Transaction
from spl.token.instructions import TransferParams, transfer as spl_transfer
from solana.rpc.commitment import Confirmed
from spl.token.constants import TOKEN_PROGRAM_ID
from solana.rpc.types import TxOpts
from solders.keypair import Keypair
from spl.token.instructions import get_associated_token_address

import os, json, requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')
oauth = OAuth(app)

# OAuth settings for Twitter
twitter = oauth.remote_app(
    'twitter',
    consumer_key=os.getenv('TWITTER_API_KEY'),
    consumer_secret=os.getenv('TWITTER_API_SECRET'),
    request_token_params={'scope': 'email'},
    base_url='https://api.twitter.com/1.1/',
    request_token_url=None,
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authorize'
)

# Twitter account to check if followed
KIBOKO_TWITTER_ID = 'KIBOKO_TWITTER_ID'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/connect_wallet', methods=['POST'])
def connect_wallet():
    data = json.loads(request.data)
    user_wallet = data['wallet_address']
    session['wallet_address'] = user_wallet  # Save wallet address in session
    return jsonify({"status": "success", "message": "Wallet connected", "wallet": user_wallet})

# Twitter OAuth flow
@app.route('/login_twitter')
def login_twitter():
    return twitter.authorize(callback=url_for('twitter_authorized', _external=True))

@app.route('/twitter_authorized')
def twitter_authorized():
    response = twitter.authorized_response()
    if response is None or response.get('oauth_token') is None:
        return 'Access denied: reason={} error={}'.format(request.args['error_reason'], request.args['error_description'])

    session['twitter_token'] = (response['oauth_token'], response['oauth_token_secret'])

    # Check if user follows KibokoDAO
    if check_if_follows_kiboko():
        session['twitter_following'] = True
        return redirect(url_for('index', success=True))
    else:
        return redirect(url_for('index', success=False, message="Please follow KibokoDAO on Twitter to proceed."))

@twitter.tokengetter
def get_twitter_oauth_token():
    return session.get('twitter_token')

# Check if the user follows KibokoDAO
def check_if_follows_kiboko():
    twitter_token = session.get('twitter_token')
    if not twitter_token:
        return False

    # Twitter API request to check friendship (follower relationship)
    url = f"https://api.twitter.com/1.1/friendships/show.json?source_screen_name=YOUR_TWITTER_SCREEN_NAME&target_id={KIBOKO_TWITTER_ID}"
    headers = {
        "Authorization": f"Bearer {twitter_token[0]}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['relationship']['source']['following']  # Check if following KibokoDAO

    return False

@app.route('/complete_quest', methods=['POST'])
async def complete_quest():
    data = json.loads(request.data)
    quests_completed = data['quests']

    # Ensure all quests are completed and user follows KibokoDAO on Twitter
    if all(quests_completed.values()) and session.get('twitter_following', False):
        user_wallet = session.get('wallet_address')
        # Trigger token distribution asynchronously
        success = await send_mlnk_tokens(user_wallet)  # Make this async
        if success:
            return jsonify({"status": "success", "message": "100 MLNK Tokens dripped!"})
        else:
            return jsonify({"status": "fail", "message": "Token transfer failed. Try again later."})

    return jsonify({"status": "fail", "message": "Complete all quests and follow KibokoDAO on Twitter to receive rewards."})

@app.route('/claim_mlink', methods=['POST'])
async def claim_mlink():
    data = json.loads(request.data)
    user_wallet = data['wallet_address']
    
    # Logic for sending 100 MLNK tokens to the user's wallet
    success = await send_mlnk_tokens(user_wallet)  # Call the function to send tokens
    if success:
        return jsonify({"status": "success", "message": "100 MLNK Tokens claimed!"})
    return jsonify({"status": "fail", "message": "Token claim failed. Try again later."})





async def send_mlnk_tokens(user_wallet):
    try:
        client = AsyncClient("https://api.mainnet-beta.solana.com", commitment=Confirmed)
        sender = Pubkey(os.getenv("SOLANA_WALLET_ADDRESS"))  # Sender's public key
        recipient = Pubkey(user_wallet)  # Recipient's wallet public key

        # Load the private key for the sender and parse it to a Keypair
        private_key = os.getenv("SOLANA_PRIVATE_KEY")
        sender_keypair = Keypair.from_secret_key(bytes(map(int, private_key.split(','))))

        # Define the token mint address
        token_mint_address = Pubkey(os.getenv("TOKEN_MINT_ADDRESS"))  # MLNK token mint address

        # Define the token accounts (associated token accounts for both sender and recipient)
        sender_token_account = Pubkey(os.getenv("SENDER_TOKEN_ACCOUNT_ADDRESS"))  # Associated token account of the sender
        recipient_token_account = await get_associated_token_address(recipient, token_mint_address)

        # Create the transfer transaction for 100 MLNK tokens (adjust decimals based on the token's configuration)
        transaction = Transaction().add(
            spl_transfer(
                TransferParams(
                    program_id=TOKEN_PROGRAM_ID,
                    source=sender_token_account,
                    dest=recipient_token_account,
                    owner=sender,
                    amount=100 * (10 ** 9)  # Adjust this amount based on token decimals
                )
            )
        )

        # Send the transaction
        response = await client.send_transaction(transaction, sender_keypair, opts=TxOpts(skip_confirmation=False))

        # Close the Solana client connection
        await client.close()

        # Check response
        if response and 'result' in response:
            print("MLNK Tokens successfully transferred.")
            return True
        else:
            print(f"Error during transaction: {response.get('error')}")
            return False

    except Exception as e:
        print(f"Exception occurred during token transfer: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)
