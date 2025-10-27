# === CRYPTO CHATBOT ===
"""
CryptoBuddy GUI Chatbot (Tkinter)
- Integrates a 133-entry Cryptocurrency & Blockchain Q&A dataset (embedded).
- Uses fuzzy matching to answer user questions; falls back to rule-based guidance.
Usage:
    python crypto_chatbot_gui.py
"""

import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from difflib import SequenceMatcher, get_close_matches
import datetime
import re

# ---------------- Paths & Data Loading ----------------
HERE = os.path.dirname(__file__) if '__file__' in globals() else '.'
EXTERNAL_QA_PATH = os.path.join(HERE, 'data', 'qa_db.json')  # optional external override

# Embedded 133 Q&A dataset 
# Added greetings as requested
EMBEDDED_QA = [
    ("Hello", "Hello there! How can I assist you with crypto today?"),
    ("Hi", "Hi! What's on your mind about cryptocurrencies?"),
    ("Hey", "Hey! Ready to dive into the world of crypto?"),
    ("Good morning", "Good morning! How can I help you explore crypto today?"),
    ("Good afternoon", "Good afternoon! What crypto questions do you have?"),
    ("Good evening", "Good evening! Let's talk crypto."),
    ("How are you?", "I'm a bot, so I don't have feelings, but I'm ready to help you with crypto info!"),
    ("What's up?", "Not much, just here to answer your crypto questions! What's up with you?"),
    # --- Added general conversation data ---
    ("Who are you?", "I am CryptoBuddy, a chatbot designed to answer your questions about cryptocurrency and blockchain technology."),
    ("What are you?", "I'm a friendly chatbot, your CryptoBuddy! I'm here to provide information about the world of crypto."),
    ("What can you do?", "I can answer a wide range of questions about cryptocurrencies, blockchain, DeFi, NFTs, and more. I can also offer some basic crypto recommendations. Just ask away!"),
    ("Tell me a joke.", "Why did the Bitcoin investor break up with the Ethereum developer? Because he felt like he was living in her shadow!"),
    ("Tell me another joke.", "How many miners does it take to change a lightbulb? None, they just wait for the next block and the problem solves itself."),
    ("What is your name?", "You can call me CryptoBuddy. It's a pleasure to meet you!"),
    ("Thank you", "You're welcome! Happy to help. Is there anything else I can assist you with?"),
    ("Thanks", "Anytime! Let me know if you have more questions."),
    ("How old are you?", "I'm as young as the latest code push! In the digital world, age is just a version number."),
    ("Where are you from?", "I exist in the cloud, powered by code and a love for all things crypto. You could say I'm from the decentralized world!"),
    ("What is the weather like?", "I don't have access to real-time weather data, but I can tell you if the crypto market is looking bullish or bearish!"),
    ("What time is it?", "I don't have a clock, but it's always a good time to learn about blockchain! What can I help you with?"),
    ("Can you help me?", "Of course! That's what I'm here for. Ask me anything about cryptocurrency or blockchain."),
    ("What is a cryptocurrency?", "A cryptocurrency is a digital or virtual currency that is secured by cryptography, making it nearly impossible to counterfeit or double-spend. Many are based on decentralized blockchain technology."),
    ("What is a blockchain?", "A blockchain is a decentralized, distributed, and public digital ledger that is used to record transactions across many computers so that the record cannot be altered retroactively without the alteration of all subsequent blocks and the consensus of the network."),
    ("Who invented Bitcoin?", "Bitcoin was invented by an unknown person or group of people using the name Satoshi Nakamoto."),
    ("When was Bitcoin launched?", "The Bitcoin whitepaper was released in October 2008, and the network officially launched in January 2009."),
    ("What is decentralization?", "Decentralization means that a system or network operates without a single central authority (like a bank or government). Control is distributed among participants."),
    ("What is the difference between a coin and a token?", "A coin (like Bitcoin or Ether) is a native asset of its own blockchain. A token is a digital asset built on top of an existing blockchain (e.g., an ERC-20 token on Ethereum)."),
    ("What is a whitepaper?", "A whitepaper is a formal document published by the founders of a crypto project, outlining the concept, technology, purpose, and plan for their new currency or protocol."),
    ("What is Bitcoin's supply limit?", "Bitcoin has a hard cap supply limit of 21 million coins."),
    ("What is a Public Key?", "A public key is a cryptographic code that allows a user to receive cryptocurrencies into their account. It is similar to an account number and can be shared freely."),
    ("What is a Private Key?", "A private key is a secret, alphanumeric code that proves ownership of a cryptocurrency wallet and is used to authorize transactions. It must be kept absolutely secure."),
    ("What is a wallet address?", "A wallet address is a hashed (shorter) version of a public key, used as the destination for sending cryptocurrency."),
    ("What is the role of cryptography in cryptocurrency?", "Cryptography is used to secure transactions, control the creation of new units, verify the transfer of assets, and protect users' private keys."),
    ("What is a block in a blockchain?", "A block is a file on the blockchain that contains a bundle of verified and confirmed transaction data, along with a timestamp and a link (hash) to the previous block."),
    ("What is a hash/hashing?", "A hash is a fixed-length string of numbers and letters generated by a cryptographic function. It acts as a unique digital fingerprint for a block of data."),
    ("What is an immutable ledger?", "An immutable ledger means that once data is recorded on the blockchain, it cannot be changed or deleted."),
    ("What is an 'Altcoin'?", "Altcoin is a blanket term for any cryptocurrency other than Bitcoin (BTC)."),
    ("What is the purpose of the Bitcoin Halving?", "The Halving event cuts the reward for mining new blocks by half, reducing the rate at which new Bitcoin is created, ensuring scarcity, and controlling inflation."),
    ("What is the main difference between Bitcoin and Ethereum?", "Bitcoin is primarily a digital store of value and payment system, while Ethereum is a decentralized computing platform that allows for the creation of smart contracts and dApps."),
    ("What is the 'genesis block'?", "The genesis block is the very first block of a blockchain, block number 0."),
    ("What is a stablecoin?", "A stablecoin is a cryptocurrency designed to have a stable value relative to a 'stable' asset, like the US Dollar (e.g., USDC, USDT)."),
    ("Name the three main types of stablecoins.", "Fiat-backed, Crypto-backed, and Algorithmic."),
    ("What does P2P mean in crypto?", "P2P stands for Peer-to-Peer, meaning transactions occur directly between two users without an intermediary."),
    ("What is a cryptocurrency exchange?", "A cryptocurrency exchange is a platform where you can buy, sell, or trade cryptocurrencies for other digital assets or traditional fiat currency."),
    ("What is 'Gas' on Ethereum?", "Gas is the fee required to successfully conduct a transaction or execute a contract on the Ethereum blockchain."),
    ("What is a dApp?", "A dApp (Decentralized Application) is an application built to run on a decentralized network, usually a blockchain, that is not controlled by a single entity."),
    ("What is the maximum number of decimal places for a Bitcoin?", "The smallest unit of Bitcoin is a Satoshi, which is 0.00000001 BTC (8 decimal places)."),
    ("What is a transaction fee?", "A transaction fee is a small amount of cryptocurrency paid to the miners or validators to process and confirm a transaction on the blockchain."),
    ("What is a fork in the blockchain?", "A fork occurs when a blockchain splits into two separate, independent chains, typically due to a change in the network's rules (software update)."),
    ("What is the difference between a Hard Fork and a Soft Fork?", "A Hard Fork creates two incompatible blockchains, requiring all participants to upgrade their software. A Soft Fork is a backward-compatible upgrade that old nodes can still validate, but not enforce the new rules."),
    ("What is a Distributed Ledger Technology (DLT)?", "DLT is a decentralized database managed by multiple participants, used to record and share information, with blockchain being a type of DLT."),
    ("What is a Consensus Mechanism?", "A consensus mechanism is a fault-tolerant method used by blockchain networks to agree on a single, true state of the distributed ledger and validate new blocks."),
    ("What is Proof-of-Work (PoW)?", "PoW is a consensus mechanism where miners compete to solve complex cryptographic puzzles to validate transactions and add a new block to the chain. (Used by Bitcoin)."),
    ("What is Proof-of-Stake (PoS)?", "PoS is a consensus mechanism where validators lock up (stake) their coins to gain the right to validate transactions and earn rewards. (Used by Ethereum post-Merge)."),
    ("How does a 51% attack work?", "A 51% attack occurs when a single entity or group gains control of more than half of the network's computing power (PoW) or staked coins (PoS), allowing them to manipulate transaction order and potentially double-spend."),
    ("What is 'mining' in cryptocurrency?", "Mining is the process of validating transactions and adding them to the public ledger (blockchain). In PoW, it involves solving complex computational problems to earn cryptocurrency as a reward."),
    ("What is a 'Smart Contract'?", "A smart contract is a self-executing contract with the terms of the agreement directly written into code. It runs on a blockchain and automatically executes when conditions are met."),
    ("Which blockchain is famous for pioneering Smart Contracts?", "Ethereum."),
    ("What is the ERC-20 standard?", "ERC-20 is a technical standard used for smart contracts on the Ethereum blockchain for implementing fungible tokens. It defines a common list of rules for tokens."),
    ("What is 'Layer 2' (L2)?", "Layer 2 is a secondary framework or protocol built on top of an existing blockchain (Layer 1) to improve its scalability, speed, and efficiency (e.g., Polygon, Arbitrum, Optimism)."),
    ("What is a 'bridge' in crypto?", "A bridge is a protocol that connects two different blockchains, allowing users to transfer tokens and data between them."),
    ("What is 'Transaction Throughput' or TPS?", "Transaction Throughput (TPS - Transactions Per Second) is the measure of how many transactions a blockchain network can process in one second."),
    ("What is 'Finality' in a blockchain?", "Finality is the guarantee that once a transaction is added to the blockchain, it cannot be reversed, altered, or canceled."),
    ("What is 'Sharding'?", "Sharding is a scaling technique that divides a blockchain into smaller, more manageable parts (shards) to allow for parallel processing of transactions, increasing throughput."),
    ("What is an 'Oracle' in blockchain?", "An Oracle is a third-party service that connects smart contracts to real-world data and information (off-chain data)."),
    ("What is 'Impermanent Loss'?", "Impermanent Loss is the temporary loss of funds a liquidity provider experiences due to the volatility of token prices within a liquidity pool compared to simply holding the tokens."),
    ("What is an NFT?", "NFT stands for Non-Fungible Token. It is a unique digital asset that represents ownership of a unique item or piece of content, usually on a blockchain like Ethereum."),
    ("What does 'Fungible' mean?", "Fungible means that an asset can be easily exchanged or replaced by another identical item (e.g., a dollar bill or one Bitcoin)."),
    ("What is 'Wrapping' a coin (e.g., wBTC)?", "Wrapping a coin involves locking the original asset (like BTC) in a smart contract to create a tokenized version on another chain (like wBTC on Ethereum), allowing it to be used in that chain's ecosystem."),
    ("What is 'Proof-of-History' (PoH)?", "PoH is a consensus component used by Solana to create a historical record of events on the chain, which speeds up block creation and transaction finalization."),
    ("What is 'Interoperability' in crypto?", "Interoperability is the ability of different blockchain networks to communicate, share data, and transfer value with each other."),
    ("What is 'Staking'?", "Staking is the act of locking up cryptocurrency to participate in the PoS consensus mechanism of a blockchain, earning rewards for helping to secure the network."),
    ("What is 'Yield Farming'?", "Yield farming is the practice of staking or lending crypto assets to generate high returns or rewards in the form of additional cryptocurrency."),
    ("What is 'Liquidity Mining'?", "Liquidity mining is a subset of yield farming where users provide liquidity to a DEX pool and are rewarded with the protocol's native token (governance token) in addition to trading fees."),
    ("What is a 'Decentralized Exchange' (DEX)?", "A DEX is a cryptocurrency exchange that allows peer-to-peer transactions without the need for a centralized intermediary to hold the user's funds."),
    ("What is an 'Automated Market Maker' (AMM)?", "An AMM is a protocol used by DEXs that uses smart contracts and mathematical formulas (like x*y=k) to automatically determine the price of assets in a liquidity pool."),
    ("What is a 'DAO'?", "DAO stands for Decentralized Autonomous Organization, an organization represented by rules encoded as a computer program, transparent, controlled by members, and not influenced by a central government."),
    ("What is the maximum number of Bitcoin that will ever be mined?", "21 million."),
    ("What is the total supply of Ethereum?", "Ethereum does not have a fixed maximum supply, but with the EIP-1559 upgrade, a portion of transaction fees (gas) is \"burned\" (destroyed), making its supply potentially deflationary."),
    ("What is a Merkle Tree?", "A Merkle tree (or hash tree) is a data structure used to efficiently and securely verify the contents of large data structures using cryptographic hashing, most notably used to summarize all the transactions in a block."),
    ("What is 'Time-lock' in crypto?", "A Time-lock is a cryptographic script or function that prevents a transaction from being spent or a contract from being executed until a specific future time or block number has been reached."),
    ("What is 'HODL'?", "HODL is a common crypto term (a misspelling of 'hold') which means to buy a cryptocurrency and hold it for the long term, regardless of price fluctuations."),
    ("What is 'FUD'?", "FUD stands for Fear, Uncertainty, and Doubt, a strategy to influence perception by disseminating negative, misleading, or false information."),
    ("What is 'FOMO'?", "FOMO stands for Fear Of Missing Out, which can lead to impulsive and emotional investing decisions during a rapid price increase."),
    ("What is a 'crypto whale'?", "A crypto whale is an individual or entity that holds a very large amount of a particular cryptocurrency, giving them the potential to significantly impact the market price."),
    ("What is 'Market Cap'?", "Market Cap (Market Capitalization) is the total dollar value of a cryptocurrency's circulating supply. It is calculated as: Circulating Supply × Current Price."),
    ("What is 'DCA'?", "DCA stands for Dollar-Cost Averaging, an investment strategy where you invest a fixed amount of money at regular intervals, regardless of the asset's price, to reduce the impact of volatility."),
    ("What is a 'Hardware Wallet' (Cold Storage)?", "A hardware wallet is a physical, electronic device that stores a user's private keys offline, providing the highest level of security against hacks and viruses."),
    ("What is a 'Software Wallet' (Hot Storage)?", "A software wallet is a digital wallet application (desktop, mobile, or web) that stores private keys online, making it convenient but less secure than a hardware wallet."),
    ("What is a 'seed phrase' or 'recovery phrase'?", "A seed phrase (usually 12 or 24 words) is a master key to all cryptocurrency associated with a wallet. It is essential for restoring access to a wallet if the device is lost or damaged."),
    ("What is 'KYC'?", "KYC stands for Know Your Customer, a process of verifying the identity of clients, usually required by centralized exchanges and financial institutions to comply with anti-money laundering (AML) laws."),
    ("What is 'AML'?", "AML stands for Anti-Money Laundering, a set of regulations and procedures designed to prevent criminals from disguising illegally obtained funds as legitimate income."),
    ("What is 'Slippage'?", "Slippage is the difference between the expected price of a trade and the price at which the trade is actually executed. It is common in volatile markets or with large orders on DEXs."),
    ("What is a 'Rug Pull' scam?", "A rug pull is a malicious maneuver in which crypto developers attract investors and then suddenly drain the liquidity pool and abandon the project, leaving investors with worthless tokens."),
    ("What is 'Airdrop'?", "An airdrop is a method of distributing new tokens or coins to a large number of wallet addresses, usually for promotional purposes or as a reward to existing users."),
    ("What is a 'Bear Market'?", "A bear market is a period where prices in a financial market, including crypto, are generally declining, and pessimism and selling sentiment prevail."),
    ("What is a 'Bull Market'?", "A bull market is a period where prices are generally rising, and optimism and buying sentiment prevail."),
    ("What are 'Limit Orders'?", "A limit order is an order to buy or sell a cryptocurrency at a specific price or better. The trade will only execute if the market reaches the limit price."),
    ("What is 'Portfolio Diversification' in crypto?", "Diversification is the strategy of spreading investments across various cryptocurrencies, sectors, and assets to mitigate risk."),
    ("How can I prevent losing my crypto?", "Use a secure wallet (preferably hardware), never share your private key or seed phrase, enable 2FA on exchanges, and be wary of phishing scams."),
    ("What is 'Pump and Dump'?", "A pump and dump scheme is a form of market manipulation where a group artificially inflates the price of a low-cap coin (the \"pump\") and then sells off their own holdings at the peak (the \"dump\")."),
    ("What is 'Market Dominance'?", "Market Dominance is the percentage of the total crypto market capitalization that is held by a specific coin, often used in reference to Bitcoin Dominance."),
    ("What is a 'Margin Trade'?", "Margin trading involves borrowing funds to trade cryptocurrencies, allowing traders to increase their potential profits (and losses) through leverage."),
    ("What does it mean to 'short' a crypto asset?", "Shorting is a trading strategy where an investor bets on the price of a crypto asset going down. They borrow the asset, sell it, and aim to buy it back later at a lower price to return it and profit from the difference."),
    ("What is 'Futures Trading'?", "Futures trading involves making an agreement to buy or sell a specific cryptocurrency at a predetermined price on a specified future date."),
    ("What is a 'Decentralized Identity' (DID)?", "DID is a concept and technology that allows individuals to create and control their own digital identities without relying on a central authority."),
    ("What is the 'Lightning Network'?", "The Lightning Network is a Layer 2 scaling solution for Bitcoin that allows for faster, cheaper, and more frequent off-chain transactions."),
    ("What is 'Tokenomics'?", "Tokenomics is the study of a cryptocurrency's economics, including its supply, distribution, governance, utility, and deflationary or inflationary mechanisms."),
    ("What is a 'Self-Custodial Wallet'?", "A self-custodial wallet gives the user complete control over their private keys and funds, meaning the user is solely responsible for security."),
    ("What is a 'Custodial Wallet'?", "A custodial wallet is one where a third party (like a centralized exchange) holds your private keys for you, meaning they have control of your funds."),
    ("What is 'Vaporware' in crypto?", "Vaporware refers to a cryptocurrency project or product that has been publicly announced but has yet to be released, often used to describe projects with significant hype but no functional product."),
    ("What is DeFi?", "DeFi (Decentralized Finance) is an umbrella term for financial applications and services built on blockchain technology (primarily Ethereum) that eliminate the need for traditional intermediaries."),
    ("Name three common DeFi use cases.", "Lending/Borrowing, Decentralized Exchanges (DEXs), and Yield Aggregators."),
    ("What is 'EVM'?", "EVM stands for Ethereum Virtual Machine, the runtime environment for smart contracts on Ethereum. It allows developers to deploy code that executes exactly as programmed."),
    ("What is an 'ICO'?", "ICO stands for Initial Coin Offering, a fundraising method where a crypto project sells a new cryptocurrency or token to early investors."),
    ("What is a 'Launchpad' or 'IDO'?", "A Launchpad is a platform that hosts token sales for new crypto projects (Initial DEX Offering - IDO), allowing users to participate in the early distribution of tokens."),
    ("What is 'Web3'?", "Web3 is a proposed evolution of the internet that is decentralized and built on blockchain technology, incorporating concepts like tokenization, dApps, and ownership of data."),
    ("What is a 'zero-knowledge proof' (ZKP)?", "A ZKP is a cryptographic method where one party can prove a statement is true without revealing any information beyond the validity of the statement itself."),
    ("What is 'MEV'?", "MEV (Maximal Extractable Value) is the profit that validators/miners can gain by arbitrarily including, excluding, or reordering transactions within a block."),
    ("What is the EIP-1559 upgrade?", "EIP-1559 is an Ethereum upgrade that changed the transaction fee mechanism by introducing a \"base fee\" that is burned (destroyed), making the supply potentially deflationary, and a priority fee for validators."),
    ("What is a 'Sidechain'?", "A sidechain is a separate blockchain that is connected to its parent blockchain by a two-way peg, allowing assets to be moved between the two chains (e.g., Polygon/Matic)."),
    ("What is 'CBDC'?", "CBDC stands for Central Bank Digital Currency, a digital form of a country's fiat currency, issued and backed by the nation's central bank."),
    ("What is 'Collateral' in a DeFi loan?", "Collateral is an asset (like a crypto token) that a borrower must lock up in a smart contract to secure a loan. If the borrower fails to repay, the collateral is liquidated."),
    ("What is 'Over-Collateralization'?", "Over-collateralization is when the value of the collateral pledged for a loan is significantly higher than the loan amount, a common practice in decentralized lending to account for asset volatility."),
    ("What is 'Gas War'?", "A gas war is a phenomenon, often during highly anticipated NFT or token launches, where users rapidly bid up the gas price to ensure their transaction is included in the next block."),
    ("What is 'Governance' in a crypto project?", "Governance refers to the process by which a decentralized project makes decisions and implements changes, usually via the holders of its governance token voting on proposals."),
    ("What is a 'Hard Cap' for a token sale?", "The hard cap is the maximum amount of money or crypto a project will accept from investors during a funding round, like an ICO or IDO."),
    ("What is the 'Trilemma' in blockchain?", "The blockchain trilemma states that a decentralized network can only achieve two of the three core properties (Decentralization, Security, and Scalability) at any given time, requiring a trade-off."),
    ("What is a 'Decentralized Autonomous Organization' (DAO)?", "A DAO is an organization without a central leader, governed by rules encoded in smart contracts, with decisions made by its token holders through voting."),
    ("What is 'Liquidation' in margin trading/lending?", "Liquidation is the forced closure of a leveraged trading position or a collateralized loan when the collateral's value drops below a certain threshold."),
    ("What is the 'Burn' mechanism for a token?", "A burn mechanism is when a developer permanently removes tokens from the circulating supply by sending them to an unspendable wallet address, typically to increase scarcity and value."),
    ("What fundamental problem did Bitcoin solve?", "Bitcoin solved the \"Double-Spending Problem\" for digital currency without requiring a central authority. It achieved this by using a decentralized ledger (the blockchain) and a consensus mechanism (Proof-of-Work) to chronologically order and validate every transaction."),
    ("What is the difference between the UTXO model and the Account model?", "The UTXO (Unspent Transaction Output) model (used by Bitcoin) tracks funds as discrete inputs and outputs (like digital cash). The Account model (used by Ethereum) tracks a single, long-lived balance for each address, similar to a bank account."),
    ("What is the specific role of the Merkle Root in a block header?", "The Merkle Root is a single hash that efficiently summarizes all the transactions in a block. This allows the network to verify the integrity and inclusion of any single transaction (using a Merkle Proof) without needing to download the entire block's data."),
    ("How does ECDSA secure a transaction?", "ECDSA (Elliptic Curve Digital Signature Algorithm) uses the private key to sign a transaction, proving ownership of the funds without ever revealing the private key. The signature can be publicly verified using the corresponding public key."),
    ("What is the security advantage of a Multisignature (Multisig) wallet?", "A Multisig wallet requires multiple private keys (signatures) from a predetermined group (e.g., 2 out of 3) to authorize a transaction. This prevents a single point of failure and is ideal for treasury management."),
    ("Explain the core difference between Optimistic Rollups and ZK-Rollups.", "Optimistic Rollups assume transactions are valid and rely on a Fraud Proof challenge period (a few days) to catch bad actors. ZK-Rollups prove transactions are valid with a cryptographic Validity Proof (a ZK-Proof) before they are posted to Layer 1, offering near-instant finality."),
    ("What is a Reentrancy Attack in smart contracts?", "A Reentrancy Attack occurs when a smart contract function makes an external call to a malicious contract, which is coded to call back into the original function repeatedly before the initial execution has completed its state update (e.g., updating a user's balance), allowing funds to be drained."),
    ("What is the function of the nonReentrant modifier in smart contract code?", "It is a security control (a mutex lock) used to prevent the execution flow of a function from being re-entered before its initial execution has fully completed, serving as the primary defense against reentrancy attacks."),
    ("What is Delegated Proof-of-Stake (DPoS)?", "DPoS is a consensus mechanism where users vote for a smaller, fixed number of \"delegates\" or \"witnesses\" who are responsible for validating transactions and producing blocks."),
    ("What is Data Availability (DA) in the context of rollups?", "DA is the guarantee that the data for a Layer 2 transaction is published and accessible to all nodes, allowing any party to reconstruct the chain state and verify its validity, which is fundamental to the security of rollups."),
    ("What is the \"Passphrase\" (25th word) and its security function?", "The passphrase is an optional, user-defined word added to the standard 12 or 24-word seed phrase. It creates a hidden wallet and provides an extra layer of security, especially against physical theft of a hardware wallet."),
    ("What is a \"Honeypot\" scam?", "A honeypot is a malicious smart contract coded to attract investor deposits but designed with a hidden backdoor that allows only the creator to withdraw the total funds, trapping the investors' money."),
    ("What is Liquidation Risk in DeFi lending?", "Liquidation risk is the danger that the value of the borrower's collateral will fall below the required threshold, causing the protocol to automatically sell that collateral at a loss to repay the loan."),
    ("What is a \"Sandwich Attack\"?", "A sandwich attack is a form of MEV where a trader sees a large transaction pending, front-runs it by buying before it executes, and then back-runs it by selling after it executes, capturing the price movement and profiting at the original trader's expense."),
    ("What is the difference between the ERC-721 and ERC-1155 NFT standards?", "ERC-721 is the standard for Non-Fungible tokens (one-of-a-kind). ERC-1155 is the standard for Multi-Token contracts, which can manage both fungible tokens and multiple types of NFTs within a single contract."),
    ("What is Account Abstraction (AA)?", "AA is a proposal to make user wallets operate like smart contracts rather than just externally owned accounts. This allows for features like paying gas with any token, social recovery, and automated transactions."),
    ("What is the Tokenization of Real-World Assets (RWA)?", "RWA tokenization is the process of putting ownership (or fractional ownership) of real-world tangible assets (like real estate, stocks, or gold) onto a blockchain as a security token, increasing liquidity and accessibility."),
    ("What are Decentralized Physical Infrastructure Networks (DePIN)?", "DePIN uses crypto tokens to incentivize and coordinate communities to build and maintain real-world decentralized infrastructure, such as wireless networks, energy grids, or cloud storage."),
    ("What is the Howey Test and why is it important for crypto projects?", "The Howey Test is a U.S. Supreme Court framework used to determine if a financial transaction is an \"investment contract,\" and therefore subject to regulation as a security."),
    ("What is the key regulatory concern regarding algorithmic stablecoins?", "The primary concern is that algorithmic stablecoins, which lack full fiat or crypto collateral, are susceptible to death spirals (rapid, uncontrollable de-pegging) if market conditions trigger a run."),
    ("How does quantum computing pose a threat to existing cryptocurrencies?", "Quantum computers could potentially run Shor's algorithm, allowing them to calculate a private key from a public key, thus compromising the security of Bitcoin and other public key cryptography systems."),
    ("What is Post-Quantum Cryptography?", "It is a field of cryptography focused on developing new algorithms that are secure against attacks by both classical and quantum computers, which blockchains will need to adopt to remain secure in the future."),
    ("What is Cognitive Bias and how does it affect crypto trading?", "Cognitive bias is a systematic pattern of irrational judgment. In crypto, this includes Confirmation Bias and Hindsight Bias, often leading to emotional decisions (like FOMO or FUD) instead of rational analysis."),
]

# Convert to dict for quick lookup, preserve original questions list for fuzzy matching
QA_DICT = {q.lower(): a for q, a in EMBEDDED_QA}
QA_QUESTIONS = [q for q, _ in EMBEDDED_QA]

# Optionally override with external JSON if available (format: list of {"q": "...", "a": "..."})
if os.path.exists(EXTERNAL_QA_PATH):
    try:
        with open(EXTERNAL_QA_PATH, 'r', encoding='utf-8') as f:
            loaded = json.load(f)
        if isinstance(loaded, list):
            QA_DICT = {}
            QA_QUESTIONS = []
            for item in loaded:
                q = item.get('q') or item.get('question')
                a = item.get('a') or item.get('answer')
                if q and a:
                    QA_DICT[q.lower()] = a
                    QA_QUESTIONS.append(q)
    except Exception:
        # ignore and keep embedded
        pass

# ---------------- Small rule-based crypto_db (kept for fallback recommendations) ----------------
crypto_db = {
    "Bitcoin": {"price_trend": "rising", "market_cap": "high", "energy_use": "high", "sustainability_score": 0.3},
    "Ethereum": {"price_trend": "stable", "market_cap": "high", "energy_use": "medium", "sustainability_score": 0.6},
    "Cardano": {"price_trend": "rising", "market_cap": "medium", "energy_use": "low", "sustainability_score": 0.8},
}

# ---------------- Decision rules (from your original CLI) ----------------
def profitability_score(coin):
    c = crypto_db.get(coin, {})
    score = 0
    if c.get('price_trend') == 'rising':
        score += 2
    elif c.get('price_trend') == 'stable':
        score += 1
    if c.get('market_cap') == 'high':
        score += 2
    elif c.get('market_cap') == 'medium':
        score += 1
    return score

def sustainability_score(coin):
    c = crypto_db.get(coin, {})
    score = 0
    energy = c.get('energy_use')
    if energy == 'low':
        score += 2
    elif energy == 'medium':
        score += 1
    score += float(c.get('sustainability_score', 0)) * 2
    return score

def recommend_for_goal(user_goal: str):
    user_goal = user_goal.lower()
    if any(k in user_goal for k in ('sustain', 'green', 'eco', 'energy')):
        top = max(crypto_db.keys(), key=lambda x: sustainability_score(x))
        return f"Invest in {top}! 🌱 It has the highest sustainability score in our dataset."
    if any(k in user_goal for k in ('trend', 'trending', 'long-term', 'growth', 'buy')):
        candidates = sorted(crypto_db.keys(), key=lambda x: (profitability_score(x), sustainability_score(x)), reverse=True)
        top = candidates[0]
        return f"{top} looks promising. Price trend: {crypto_db[top]['price_trend']}, market cap: {crypto_db[top]['market_cap']}."
    if 'most sustainable' in user_goal or 'most eco' in user_goal:
        top = max(crypto_db.keys(), key=lambda x: sustainability_score(x))
        return f"{top} is the most sustainable in our dataset (score {crypto_db[top]['sustainability_score']})."
    ranking = sorted(crypto_db.keys(), key=lambda x: profitability_score(x) + sustainability_score(x), reverse=True)
    return "Top coins (by composite score): " + ', '.join(ranking)

# ---------------- Fuzzy Q/A matching ----------------
def _tokenize_text(text):
    """Tokenizes text, converts to lowercase, and removes punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    return set(text.split()) # Use set for Jaccard similarity

def best_qa_match(user_text, top_n=3):
    """
    Returns a list of (question, answer, score) for the best matches found.
    Score is a combined similarity metric between 0 and 1.
    """
    user_text_norm = user_text.strip().lower()
    user_words = _tokenize_text(user_text_norm)
    matches = []
    for q in QA_QUESTIONS:
        q_norm = q.lower()
        q_words = _tokenize_text(q_norm)

        seq_ratio = SequenceMatcher(None, user_text_norm, q_norm).ratio()
        jaccard_sim = len(user_words.intersection(q_words)) / len(user_words.union(q_words)) if len(user_words.union(q_words)) > 0 else 0
        combined_score = (seq_ratio * 0.7) + (jaccard_sim * 0.3) # Weighted average
        matches.append((q, QA_DICT.get(q_norm, ""), combined_score))
    matches.sort(key=lambda x: x[2], reverse=True)
    return matches[:top_n]

def answer_user_query(user_text):
    # Exact match
    if user_text.strip().lower() in QA_DICT:
        return QA_DICT[user_text.strip().lower()], "direct"

    # Close fuzzy matches
    matches = best_qa_match(user_text, top_n=5)
    best_q, best_a, best_score = matches[0]
    # If combined similarity is high enough, return that answer
    if best_score >= 0.50: # Adjusted threshold for combined score
        # if there are very close alternatives, show best and other suggestions
        suggestions = [m for m in matches if m[2] >= 0.45 and m[0] != best_q]
        if suggestions:
            sugg_text = "\n\nRelated Q suggestions:\n" + "\n".join([f"- {s[0]} (score {s[2]:.2f})" for s in suggestions[:3]])
        else:
            sugg_text = ""
        return f"{best_a}{sugg_text}", f"fuzzy({best_score:.2f})"

    # Keyword-based fallback to rule-based recommendations (from original script)
    lb = user_text.lower()
    if any(k in lb for k in ('sustain', 'eco', 'green', 'energy', 'environment')):
        return recommend_for_goal(lb), "fallback-rule"
    if any(k in lb for k in ('trend', 'trending', 'long-term', 'growth', 'buy', 'which crypto', 'which coin')):
        return recommend_for_goal(lb), "fallback-rule"
    # No match at all - provide help
    help_text = ("I couldn't confidently match your question to my Q&A dataset.\n"
                 "Try asking simpler questions like:\n"
                 "- \"What is a blockchain?\"\n"
                 "- \"What is gas on Ethereum?\"\n"
                 "- \"Which crypto is trending up?\"\n"
                 "Or type 'list topics' to see sample questions.")
    return help_text, "no-match"

# ---------------- GUI ----------------
BOT_NAME = "CryptoBuddy"
DISCLAIMER = ("⚠️ Disclaimer: Cryptocurrency information is educational only. This bot is not financial advice. Always do your own research.")

# --- Modern UI Constants ---
BG_COLOR = "#F0F2F5"
TEXT_COLOR = "#050505"
BOT_BUBBLE_COLOR = "#FFFFFF"
USER_BUBBLE_COLOR = "#D9FDD3"
ACCENT_COLOR = "#007AFF"
BORDER_COLOR = "#D1D1D1"
FONT_NAME = "Segoe UI"

class CryptoBuddyGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(BOT_NAME + " — Q&A Chat")
        self.state('zoomed') # Start the window maximized
        self.minsize(600, 420)
        self.configure(bg=BG_COLOR)
        
        self._setup_styles()
        self._build_ui()
        self._greet()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam') # A good base theme for customization

        # General widget styles
        style.configure('.', background=BG_COLOR, foreground=TEXT_COLOR, font=(FONT_NAME, 10))
        style.configure('TFrame', background=BG_COLOR)
        style.configure('TLabel', background=BG_COLOR, foreground="#555555", font=(FONT_NAME, 9))

        # Button Style
        style.configure('TButton', font=(FONT_NAME, 10, 'bold'), background=ACCENT_COLOR, foreground='white')
        style.map('TButton',
                  background=[('active', '#0056b3')],
                  foreground=[('active', 'white')])
        
        # Entry Style
        style.configure('TEntry', fieldbackground='white', borderwidth=1, relief='solid', bordercolor=BORDER_COLOR)
        style.map('TEntry',
                  bordercolor=[('focus', ACCENT_COLOR)],
                  relief=[('focus', 'solid')])

    def _build_ui(self):
        # Top frame for controls
        top_frame = ttk.Frame(self, padding=(10, 10, 10, 0))
        top_frame.pack(side="top", fill="x")

        btn_clear = ttk.Button(top_frame, text="Clear Chat", command=self._clear_chat)
        btn_clear.pack(side="left", padx=(0, 6))

        btn_export = ttk.Button(top_frame, text="Export Chat...", command=self._export_chat)
        btn_export.pack(side="left")
        
        top_frame.columnconfigure(2, weight=1) # Spacer
        self.status_var = tk.StringVar(value="Ready")
        lbl_status = ttk.Label(top_frame, textvariable=self.status_var, anchor='e')
        lbl_status.pack(side="right")

        # Chat display area
        chat_frame = ttk.Frame(self, padding=10)
        chat_frame.pack(fill="both", expand=True)
        
        self.chat_area = tk.Text(chat_frame, wrap="word", state="disabled", height=20,
                                 bg=BG_COLOR, font=(FONT_NAME, 11), relief="solid", bd=1,
                                 padx=10, pady=10)
        self.chat_area.config(highlightbackground=BORDER_COLOR, highlightcolor=BORDER_COLOR)
        
        # --- Tag configurations for chat bubbles ---
        self.chat_area.tag_configure("bot_bubble", background=BOT_BUBBLE_COLOR, relief="raised", borderwidth=1,
                                     lmargin1=10, lmargin2=10, rmargin=60, spacing3=10,
                                     font=(FONT_NAME, 11), wrap="word", justify="left")
        self.chat_area.tag_configure("user_bubble", background=USER_BUBBLE_COLOR, relief="raised", borderwidth=1,
                                     lmargin1=60, lmargin2=60, rmargin=10, spacing3=10,
                                     font=(FONT_NAME, 11), wrap="word", justify="right")
        self.chat_area.tag_configure("meta_text", foreground="#888888", font=(FONT_NAME, 8), justify="left")
        self.chat_area.tag_configure("user_meta_text", foreground="#888888", font=(FONT_NAME, 8), justify="right")

        # Scrollbar
        scrollbar = ttk.Scrollbar(chat_frame, command=self.chat_area.yview)
        self.chat_area['yscrollcommand'] = scrollbar.set

        self.chat_area.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom frame for input
        bottom_frame = ttk.Frame(self, padding=(10, 10))
        bottom_frame.pack(side="bottom", fill="x", pady=(0, 10))
        bottom_frame.columnconfigure(0, weight=1)

        # Input Entry with Placeholder
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(bottom_frame, textvariable=self.entry_var, font=(FONT_NAME, 12))
        self.entry.grid(row=0, column=0, sticky="ew", ipady=8, padx=(0, 10))
        self.entry.bind("<Return>", self._on_send)
        self._set_placeholder()
        self.entry.bind("<FocusIn>", self._clear_placeholder)
        self.entry.bind("<FocusOut>", self._set_placeholder)

        btn_send = ttk.Button(bottom_frame, text="Send", command=self._on_send)
        btn_send.grid(row=0, column=1, sticky="ew", ipady=2)

    # --- Placeholder Logic ---
    def _set_placeholder(self, event=None):
        if not self.entry_var.get() and self.focus_get() != self.entry:
            self.entry.configure(foreground='grey')
            self.entry_var.set("Ask a question...")

    def _clear_placeholder(self, event=None):
        if self.entry.cget('foreground') == 'grey':
            self.entry_var.set("")
            self.entry.config(foreground=TEXT_COLOR)

    # Chat helpers
    def _greet(self):
        greeting = f"Hi — I'm {BOT_NAME}! Ask me crypto & blockchain questions."
        disclaimer_msg = f"{DISCLAIMER}\n\nTry: \"What is a blockchain?\" or \"Which crypto is trending up?\""
        self._post_bot_message(greeting)
        self._post_bot_message(disclaimer_msg)

    def _post_bot_message(self, text, meta=None):
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        self._post_message(f"{BOT_NAME} [{ts}]\n", "meta_text")
        self._post_message(f"{text}\n\n", "bot_bubble")

    def _post_user_message(self, text):
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        self._post_message(f"You [{ts}]\n", "user_meta_text")
        self._post_message(f"{text}\n\n", "user_bubble")

    def _post_message(self, text, tag):
        self.chat_area.configure(state="normal")
        self.chat_area.insert("end", text, tag)
        self.chat_area.see("end")
        self.chat_area.configure(state="disabled")

    def _clear_chat(self):
        if messagebox.askyesno("Clear chat", "Clear the conversation history?"):
            self.chat_area.config(state="normal")
            self.chat_area.delete('1.0', 'end')
            self.chat_area.config(state="disabled")
            self.status_var.set("Cleared")
            self._greet()

    def _export_chat(self):
        txt = self.chat_area.get("1.0", "end").strip()
        if not txt:
            messagebox.showinfo("Export chat", "No chat to export.")
            return
        default_name = f"cryptobuddy_chat_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default_name,
                                            filetypes=[("Text file", "*.txt"), ("All files", "*.*")])
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write("--- CryptoBuddy Chat Log ---\n\n" + txt)
                messagebox.showinfo("Export chat", f"Chat exported to:\n{path}")
            except Exception as e:
                messagebox.showerror("Export chat", f"Failed to save file:\n{e}")

    def _on_send(self, event=None):
        user_text = self.entry.get().strip()
        if not user_text or self.entry.cget('foreground') == 'grey': # Don't send placeholder
            return

        # Handle exit commands
        if user_text.lower() in ('quit', 'exit', 'bye'):
            self._post_user_message(user_text)
            self.entry_var.set("")
            self._set_placeholder()
            return

        # list topics command
        if user_text.lower() in ('list topics', 'topics', 'help topics'):
            sample = "\n".join([f"- {q}" for q in QA_QUESTIONS[:12]]) + "\n... (133 total)"
            self._post_user_message(user_text)
            self.entry_var.set("")
            self._set_placeholder()
            return

        self._post_user_message(user_text)
        self.entry.delete(0, "end")

        self.status_var.set("Thinking...")
        self.update_idletasks()

        # generate answer
        try:
            answer, meta = answer_user_query(user_text)
            self._post_bot_message(answer)
            self.status_var.set(f"Answered ({meta})")
        except Exception as e:
            self._post_bot_message("Sorry, I encountered an error while answering.")
            self.status_var.set("Error")
            print("Error while answering:", e)

# ---------------- Run app ----------------
def main():
    root = CryptoBuddyGUI()
    root.mainloop()

if __name__ == '__main__':
    main()
