# KibokoDAO Quests DApp

[![kibokoques.png](https://i.postimg.cc/cL2K4Jcm/kibokoques.png)](https://postimg.cc/tsdRBpwZ)

---

## Project Overview

The **KibokoDAO Quests DApp** is a decentralized application built on the Solana blockchain. It allows users to connect their Phantom wallet, complete social media quests, and claim **$MLINK** tokens as rewards. This DApp is designed to engage users in a series of interactive quests to promote community engagement and token distribution.

## Features

- **Phantom Wallet Integration**: Users can connect their Solana Phantom wallet.
- **Quest Completion**: Users complete tasks such as following KibokoDAO on Twitter, Telegram, and other platforms.
- **Claim $MLINK Tokens**: Once the quests are completed, users can claim 100 MLINK tokens.
- **Solana-Based Transactions**: Handles token transfers using the Solana blockchain.

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript (with Solana Web3.js)
- **Backend**: Flask (Python)
- **Blockchain**: Solana (SPL Token Program)
- **Wallet Integration**: Phantom Wallet

## Installation and Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/kiboko_dao_quests.git
    cd kiboko_dao_quests
    ```

2. **Create and activate a virtual environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file in the root directory with the following variables:

    ```bash
    FLASK_SECRET_KEY=your_secret_key
    TWITTER_API_KEY=your_twitter_api_key
    TWITTER_API_SECRET=your_twitter_api_secret
    SOLANA_WALLET_ADDRESS=your_solana_wallet_address
    SOLANA_PRIVATE_KEY=your_solana_private_key
    TOKEN_MINT_ADDRESS=your_token_mint_address
    SENDER_TOKEN_ACCOUNT_ADDRESS=your_sender_token_account_address
    ```

5. **Run the Flask application**:

    ```bash
    flask run
    ```

## Usage

1. Visit the application in your browser.
2. Connect your Phantom Wallet.
3. Complete the listed quests (follow on social platforms).
4. Once completed, click the **Claim $MLINK** button to receive 100 MLINK tokens.

## File Structure

```plaintext
├── app.py                     # Flask backend application
├── static/
│   ├── styles.css             # Custom styles for the frontend
├── templates/
│   ├── index.html             # Main frontend HTML page
├── .env                       # Environment variables (not tracked)
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

## Future Enhancements

- **Vesting Schedule**: Add vesting for the token rewards.
- **More Social Media Integrations**: Expand to include more platforms.
- **Token Staking**: Enable users to stake $MLINK tokens for more rewards.

## Contributing

1. Fork the repository.
2. Create a new feature branch.
3. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License.


