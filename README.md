# BOT-Injective

**⚠️** This project is no longer functional due to updates in the Injective API that have rendered the code obsolete. **⚠️**

**Note:** The commit history of this project has been removed before making it public because my private key appeared multiple times in the files.

## Overview

This repository contains two main components for interacting with the Injective ecosystem:

- **Bot**: Automated scripts for executing tasks on the Injective blockchain.
- **hand**: This was the initial version of the script, which was originally designed to scrape smart contracts and suggest potential purchases, without executing automatic buys.

## Repository Structure

### Bot

This directory contains the core automation scripts. 
#### How `main.py` Works

The `main.py` script automates the detection and purchase of newly created coins on the Injective blockchain. It follows these steps:

1. **Scrape Smart Contracts**:  
   The script scans all smart contracts deployed on the blockchain.

2. **Detect Coin Creation**:  
   It checks if a new coin creation event is present in the messages associated with each smart contract.

3. **Identify Factory-Type Contracts**:  
   The script verifies if the smart contract is a "factory" type, typically used for generating new tokens.

4. **Automate the Purchase**:  
   Once a valid smart contract is found, the script launches a purchase function. This function runs in a loop until the purchase succeeds, as the coin’s liquidity pool might not yet be available.

This process ensures that the bot can detect and buy new coins as soon as they become available.


### Hand

This directory includes supplementary tools to enhance the bot's performance. Features include:
