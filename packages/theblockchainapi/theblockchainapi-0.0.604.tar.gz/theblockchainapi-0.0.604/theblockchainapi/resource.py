import json
from enum import Enum
import requests
from typing import Optional, List, Union
from requests import Response


class SolanaMintAddresses:

    USDC_MAINNET_BETA = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
    MANGO_MAINNET_BETA = "MangoCzJ36AjZyKwVj3VnYU4GTonjfVEnJmvvWaxLac"
    SERUM_MAINNET_BETA = "SRMuApVNdxXokk5GT7XD5cUUgXMBCoAz2LHeuAoKWRt"
    RAYDIUM_MAINNET_BETA = "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"
    WRAPPED_SOL_MAINNET_BETA = "So11111111111111111111111111111111111111112"
    ATLAS_MAINNET_BETA = "ATLASXmbPQxBUYbxPsV97usA3fPQYEqzQBUHgiFCUsXx"

    # Make a pull request and add more! That would be cool.


class SolanaNetwork(Enum):
    DEVNET = "devnet"
    MAINNET_BETA = "mainnet-beta"


class SolanaCurrencyUnit(Enum):
    LAMPORT = "lamport"
    SOL = "sol"


class SolanaNFTUploadMethod(Enum):
    S3 = "S3"
    URI = "URI"


class SearchMethod(Enum):
    BEGINS_WITH = "begins_with"
    EXACT_MATCH = "exact_match"


class DerivationPath(Enum):

    CLI_PATH = ""
    PHANTOM_AND_SOLLET_PATH = "m/44/501/0/0"
    SOLFLARE_PATH = "m/44/501/0"

    @staticmethod
    def get_phantom_wallet_derivation_path(wallet_index: int) -> str:
        try:
            assert isinstance(wallet_index, int)
            assert wallet_index >= 0
        except AssertionError:
            raise Exception("Wallet index must be an integer greater than or equal to 0.")
        return f"m/44/501/{wallet_index}/0"


class SolanaWallet:

    def __init__(
        self,
        secret_recovery_phrase: str = None,
        private_key: List[int] = None,
        b58_private_key: str = None,
        derivation_path: Union[str, DerivationPath] = DerivationPath.PHANTOM_AND_SOLLET_PATH,
        passphrase: str = str()
    ):
        supplied = int(secret_recovery_phrase is not None) + int(private_key is not None) \
                   + int(b58_private_key is not None)
        if supplied != 1:
            raise Exception("Provide EXACTLY ONE of `secret_recovery_phrase` OR `private_key` OR `b58_private_key`.")
        if secret_recovery_phrase is not None and not isinstance(secret_recovery_phrase, str):
            raise Exception("`secret_recovery_phrase` must be a `str`.")
        if private_key is not None and not isinstance(private_key, list):
            raise Exception(
                "`private_key` must be a `list`. Example: [99, 110, 111, ..., 88, 88, 17]. "
                "If you are trying to provide a `str` private key from Phantom, use the argument "
                "`b58_private_key`"
            )
        if b58_private_key is not None and not isinstance(b58_private_key, str):
            raise Exception("`b58_private_key` must be a `str`.")

        self.secret_recovery_phrase = secret_recovery_phrase
        self.private_key = private_key
        self.b58_private_key = b58_private_key

        if secret_recovery_phrase is not None:

            if derivation_path is not None:
                if isinstance(derivation_path, DerivationPath):
                    derivation_path = derivation_path.value
                elif not isinstance(derivation_path, str):
                    raise Exception("`derivation_path` must be a `str` or instance of the enum `DerivationPath`.")

            if passphrase is not None:
                if not isinstance(passphrase, str):
                    raise Exception("`passphrase` must be a `str`.")

        self.derivation_path = derivation_path
        self.passphrase = passphrase

    def get_formatted_request_payload(self) -> dict:
        if self.secret_recovery_phrase is not None:
            wallet = {
                'secret_recovery_phrase': self.secret_recovery_phrase
            }
            if self.derivation_path is not None:
                wallet['derivation_path'] = self.derivation_path
            if self.passphrase is not None:
                wallet['passphrase'] = self.passphrase
            return {
                'wallet': wallet
            }
        elif self.private_key is not None:
            return {
                'wallet': {
                    'private_key': self.private_key
                }
            }
        elif self.b58_private_key is not None:
            return {
                'wallet': {
                    'b58_private_key': self.b58_private_key
                }
            }
        else:
            raise Exception("Unknown error. Improperly initialized instance of `SolanaWallet`.")


class APIResource:

    _url = "https://api.blockchainapi.com/v1/"
    __timeout = 300

    class _RequestMethod(Enum):
        GET = "GET"
        POST = "POST"
        PATCH = "PATCH"
        DELETE = "DELETE"

    def __init__(self, api_key_id: str, api_secret_key: str, timeout=None):
        """

        To get an API key pair, go to https://dashboard.blockchainapi.com/.

        Sign in and then click on the "API KEYS" tab.

        :param api_key_id: Your API key ID
        :param api_secret_key: Your API secret key
        """
        self.__api_key_id = api_key_id
        self.__api_secret_key = api_secret_key
        if timeout is not None:
            if not isinstance(timeout, int):
                raise Exception("`timeout` must be an integer")
            if timeout < 1:
                raise Exception("`timeout` must be at least 1 second.")
            if timeout > 300:
                raise Exception("`timeout` must be at most 120 second.")
            self.__timeout = timeout

    def __get_headers(self):
        """
        Get the headers with the appropriate authentication parameters
        :return: The headers
        """
        return {
            'APIKeyID': self.__api_key_id,
            'APISecretKey': self.__api_secret_key,
            'Language': 'Python'
        }

    def _request(
        self,
        endpoint,
        request_method,
        files=None,
        headers=None,
        payload=None,
        params=None
    ):
        """
        Makes an API request.
        :param payload: the payload containing the parameters
        :param endpoint: the desired endpoint
        :param request_method: the method (e.g. POST, GET, PATCH, DELETE)
        :param files: files to send. only used when changing a profile image
        :param headers: headers for the request. only specified when changing a profile image
        :return:
        """
        if headers is None:
            headers = self.__get_headers()

        args = {
            'method': request_method.value,
            'headers': headers,
            'url': self._url + endpoint,
            'timeout': self.__timeout
        }
        if files is not None:
            args['files'] = files
        if payload is not None and len(payload) > 0:
            args['data'] = json.dumps(payload)
        if params is not None:
            args['params'] = params

        r = requests.request(**args)
        try:
            json_content = json.loads(r.content)
        except json.decoder.JSONDecodeError:
            return r
        return json_content


class SolanaAPIResource(APIResource):

    def generate_secret_key(self) -> str:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGenerateSecretRecoveryPhrase
        :return:
        """
        response = self._request(
            payload=dict(),
            endpoint="solana/wallet/generate/secret_recovery_phrase",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['secret_recovery_phrase']

    def generate_private_key(self) -> dict:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGeneratePrivateKey
        :return:
        """
        response = self._request(
            payload=dict(),
            endpoint="solana/wallet/generate/private_key",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def derive_public_key(self, wallet: SolanaWallet) -> str:
        """
        Derives a public key given the info.
        More info:
        https://docs.blockchainapi.com/#operation/solanaDerivePublicKey
        :param wallet:
        :return:
        """

        response = self._request(
            payload=wallet.get_formatted_request_payload(),
            endpoint="solana/wallet/public_key",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['public_key']

    def derive_private_key(self, wallet: SolanaWallet) -> str:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaDerivePrivateKey
        :return:
        """
        response = self._request(
            payload=wallet.get_formatted_request_payload(),
            endpoint="solana/wallet/private_key",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_balance(
        self,
        public_key: str,
        unit: SolanaCurrencyUnit = SolanaCurrencyUnit.LAMPORT,
        network: SolanaNetwork = SolanaNetwork.DEVNET,
        mint_address: str = None
    ) -> dict:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetBalance
        :param public_key:
        :param unit: Ignored if `mint_address` provided
        :param network:
        :param mint_address:
        :return:
        """
        payload = {
            "public_key": public_key,
            "unit": unit.value,
            "network": network.value
        }
        if mint_address is not None:
            payload['mint_address'] = mint_address

        response = self._request(
            payload=payload,
            endpoint="solana/wallet/balance",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_wallet_token_holdings(
        self,
        public_key: str,
        include_nfts: bool = False,
        include_zero_balance_holdings: bool = False,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ) -> list:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetTokensBelongingToWallet
        :param public_key:
        :param include_nfts:
        :param include_zero_balance_holdings:
        :param network:
        :return:
        """
        response = self._request(
            params={
                'include_nfts': include_nfts,
                'include_zero_balance_holdings': include_zero_balance_holdings
            },
            endpoint=f"solana/wallet/{network.value}/{public_key}/tokens",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])

        return response

    def get_wallet_transactions(
        self,
        public_key: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ) -> list:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetWalletTransactions
        :param public_key:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/wallet/{network.value}/{public_key}/transactions",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_nfts_belonging_to_address(
        self,
        public_key: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ) -> list:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetNFTsBelongingToWallet
        :param public_key:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/wallet/{network.value}/{public_key}/nfts",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['nfts_metadata']

    def get_is_candy_machine(
        self,
        public_key: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetAccountIsCandyMachine
        :param public_key:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/account/{network.value}/{public_key}/is_candy_machine",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_is_nft(
        self,
        public_key: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetAccountIsNFT
        :param public_key:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/account/{network.value}/{public_key}/is_nft",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['is_nft']

    def get_nft_owner(
        self,
        mint_address: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ) -> str:
        response = self._request(
            endpoint=f"solana/nft/{network.value}/{mint_address}/owner",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['nft_owner']

    def get_nft_owner_advanced(
        self,
        mint_address: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ) -> dict:
        """
        https://docs.blockchainapi.com/#tag/Solana-NFT/operation/solanaGetNFTOwnerAdvanced
        :param mint_address:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/nft/{network.value}/{mint_address}/owner_advanced",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_associated_token_account_address(
        self,
        mint_address: str,
        public_key: str
    ) -> str:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaDeriveAssociatedTokenAccountAddress
        :param mint_address: The mint address of the NFT or SPL token
        :param public_key: The public key of the account that owns the associated token account address
        :return:
        """
        payload = {
            "mint_address": mint_address,
            "public_key": public_key
        }

        response = self._request(
            params=payload,
            endpoint=f"solana/wallet/{public_key}/associated_token_account/{mint_address}",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['associated_token_address']

    def transfer(
        self,
        wallet: Optional[SolanaWallet],
        recipient_address: str,
        token_address: Optional[str] = None,
        network: SolanaNetwork = SolanaNetwork.DEVNET,
        wait_for_confirmation: Optional[bool] = None,
        amount: str = "1",
        fee_payer_wallet: Optional[SolanaWallet] = None,
        sender_public_key: Optional[str] = None,
        return_compiled_transaction: bool = False
    ) -> str:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaTransfer
        :param wallet: The source of the transfer
        :param recipient_address: The recipient of the transfer
        :param token_address: If not provided, defaults to transferring SOL
        :param network: The network, e.g. mainnet-beta or devnet
        :param wait_for_confirmation: Whether to wait for the tx to be confirmed. See docs for more info.
        :param amount: The amount to transfer
        :param fee_payer_wallet: OPTIONAL: The fee payer of the transaction.
        The default is the wallet from which the transfer is occurring
        :param sender_public_key: OPTIONAL: The public key of the sender. You do NOT have to specify this if are
        providing a value for `wallet`. If you set `return_compiled_transaction` to True, then this will compile the
        transaction using the `sender_public_key` you provided. You can then sign and send it. You might want to do
        this for security purposes
        :param return_compiled_transaction: OPTIONAL: Whether or not to simply return the compiled transaction rather
        than actually submitting it the blockchain. By default,
        :return:
        """
        payload = dict()

        if wallet is not None:
            payload = wallet.get_formatted_request_payload()

        payload["network"] = network.value
        payload["amount"] = amount
        payload["recipient_address"] = recipient_address
        payload["return_compiled_transaction"] = return_compiled_transaction

        if sender_public_key is not None:
            payload["sender_public_key"] = sender_public_key

        if token_address is not None:
            payload["token_address"] = token_address

        if fee_payer_wallet is not None:
            payload["fee_payer_wallet"] = fee_payer_wallet.get_formatted_request_payload()['wallet']

        if wait_for_confirmation is not None:
            payload['wait_for_confirmation'] = wait_for_confirmation

        response = self._request(
            payload=payload,
            endpoint="solana/wallet/transfer",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['transaction_signature']

    def create_nft(
        self,
        wallet: SolanaWallet,
        network: SolanaNetwork = SolanaNetwork.DEVNET,
        mint_to_public_key: str = None,
        name: Optional[str] = None,
        symbol: Optional[str] = None,
        description: Optional[str] = None,
        wait_for_confirmation: Optional[bool] = None,
        uri: Optional[str] = None,
        image_url: Optional[str] = None,
        uri_metadata: Optional[dict] = None,
        upload_method: SolanaNFTUploadMethod = SolanaNFTUploadMethod.S3,
        creators: Optional[List[str]] = None,
        share: Optional[List[int]] = None,
        seller_fee_basis_points: int = 0,
        is_mutable: bool = True,
        is_master_edition: bool = True
    ) -> dict:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaCreateNFT
        :param wallet:
        :param network:
        :param mint_to_public_key: Assign ownership of the NFT after minting it
        :param name: The name of the NFT
        :param symbol: The symbol of the NFT
        :param description: The description of the NFT
        :param wait_for_confirmation: Whether to wait for the tx to be confirmed. See docs for more info.
        :param uri: The image of the NFT. Please see the description in the documentation
         (docs.blockchainapi.com/#operation/solanaCreateNFT)
        :param image_url: Please see the description in the documentation.
        :param uri_metadata: The metadata of the NFT. Please see the description in the documentation.
        :param upload_method: The upload method of the NFT. Please see the description in the documentation.
        to the NFT
        :param creators:
        :param share:
        :param seller_fee_basis_points:
        :param is_mutable:
        :param is_master_edition:
        :return:
        """

        wallet_payload = wallet.get_formatted_request_payload()
        payload = {
            "network": network.value,
            "name": name,
            "symbol": symbol,
            "description": description,
            "uri": uri,
            "image_url": image_url,
            "upload_method": upload_method.value,
            "is_mutable": is_mutable,
            "is_master_edition": is_master_edition,
            "seller_fee_basis_points": seller_fee_basis_points
        }

        payload = {**payload, **wallet_payload}
        if uri_metadata is not None:
            payload['uri_metadata'] = uri_metadata
        if creators is not None:
            payload['creators'] = creators
        if share is not None:
            payload['share'] = share
        if mint_to_public_key is not None:
            payload['mint_to_public_key'] = mint_to_public_key
        if wait_for_confirmation is not None:
            payload['wait_for_confirmation'] = wait_for_confirmation

        response = self._request(
            payload=payload,
            endpoint="solana/nft",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def search_nfts(
        self,
        update_authority: Optional[str] = None,
        update_authority_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        mint_address: Optional[str] = None,
        mint_address_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        nft_name: Optional[str] = None,
        nft_name_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        nft_uri: Optional[str] = None,
        nft_uri_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        symbol: Optional[str] = None,
        symbol_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        payload = {
            'network': network.value
        }
        if update_authority is not None:
            payload['update_authority'] = update_authority
            payload['update_authority_search_method'] = update_authority_search_method.value
        if mint_address is not None:
            payload['mint_address'] = mint_address
            payload['mint_address_search_method'] = mint_address_search_method.value
        if nft_uri is not None:
            payload['uri'] = nft_uri
            payload['uri_search_method'] = nft_uri_search_method.value
        if symbol is not None:
            payload['symbol'] = symbol
            payload['symbol_search_method'] = symbol_search_method.value
        if nft_name is not None:
            payload['name'] = nft_name
            payload['name_search_method'] = nft_name_search_method.value
        response = self._request(
            payload=payload,
            endpoint="solana/nft/search",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_nft_metadata(
        self,
        mint_address: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ) -> Optional[dict]:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetNFT
        :param mint_address:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/nft/{network.value}/{mint_address}",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        if isinstance(response, Response):
            if response.status_code == 404:
                return None
            else:
                raise Exception("Unknown error: ", response.status_code)
        return response

    def get_nft_mint_fee(
        self
    ) -> dict:
        """
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetNFTMintFee
        :return:
        """
        response = self._request(
            endpoint="solana/nft/mint/fee",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_airdrop(
        self,
        recipient_address: str
    ) -> str:
        """
        Get an airdrop of 0.015 SOL on the devnet
        More info:
        https://docs.blockchainapi.com/#operation/solanaGetAirdrop
        :param recipient_address:
        :return: Transaction signature
        """
        response = self._request(
            payload={
                "recipient_address": recipient_address
            },
            endpoint="solana/wallet/airdrop",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response['transaction_signature']

    def get_candy_machine_metadata(
        self,
        candy_machine_id: Optional[str] = None,
        config_address: Optional[str] = None,
        uuid: Optional[str] = None,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        More Info:
        https://docs.blockchainapi.com/#operation/solanaGetCandyMachineDetails
        :param candy_machine_id: The candy_machine_id. Same as config_address in v2.
        :param config_address: The config_address. Same as candy_machine_id in v2.
        :param uuid: The first six characters of config_address. Sometimes, you can only find the uuid.
        :param network: e.g., mainnet-beta, devnet
        :return:
        """
        payload = {
            "network": network.value,
            "candy_machine_contract_version": "v2"
        }
        if candy_machine_id is not None:
            payload['candy_machine_id'] = candy_machine_id
        if config_address is not None:
            payload['config_address'] = config_address
        if uuid is not None:
            payload['uuid'] = uuid
        response = self._request(
            payload=payload,
            endpoint="solana/nft/candy_machine/metadata",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def list_all_candy_machines(self):
        """

        :return:
        """
        response = self._request(
            endpoint="solana/nft/candy_machine/list",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def search_candy_machines(
        self,
        update_authority: Optional[str] = None,
        update_authority_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        config_address: Optional[str] = None,
        config_address_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        uuid: Optional[str] = None,
        uuid_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        symbol: Optional[str] = None,
        symbol_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        nft_name: Optional[str] = None,
        nft_name_index: Optional[int] = None,
        nft_name_search_method: SearchMethod = SearchMethod.EXACT_MATCH,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        payload = {
            'network': network.value,
            'candy_machine_contract_version': 'v2'
        }
        if update_authority is not None:
            payload['update_authority'] = update_authority
            payload['update_authority_search_method'] = update_authority_search_method.value
        if config_address is not None:
            payload['config_address'] = config_address
            payload['config_address_search_method'] = config_address_search_method.value
        if uuid is not None:
            payload['uuid'] = uuid
            payload['uuid_search_method'] = uuid_search_method.value
        if symbol is not None:
            payload['symbol'] = symbol
            payload['symbol_search_method'] = symbol_search_method.value
        if nft_name is not None:
            payload['nft_name'] = nft_name
            payload['nft_name_index'] = nft_name_index
            payload['nft_name_search_method'] = nft_name_search_method.value
        response = self._request(
            payload=payload,
            endpoint="solana/nft/candy_machine/search",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_solana_transaction(
        self,
        tx_signature: str,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        https://docs.blockchainapi.com/#operation/solanaGetTransaction
        :param tx_signature:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/transaction/{network.value}/{tx_signature}",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_all_nfts_from_candy_machine(
        self,
        candy_machine_id,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        Retrieves all NFTs from a Solana candy machine - both minted and unminted

        See the returned attributes `all_nfts`, `unminted_nfts`, and `minted_nfts`

        https://docs.blockchainapi.com/#operation/solanaGetAllNFTsFromCandyMachine
        :param candy_machine_id:
        :param network:
        :return:
        """
        response = self._request(
            payload={},
            endpoint=f"solana/nft/candy_machine/{network.value}/{candy_machine_id}/nfts",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_candy_machine_id_from_nft(
        self,
        mint_address,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        https://docs.blockchainapi.com/#operation/solanaGetNFTsCandyMachineId
        :param mint_address:
        :param network:
        :return:
        """
        payload = {
            "network": network.value,
            "mint_address": mint_address
        }
        response = self._request(
            payload=payload,
            endpoint="solana/nft/candy_machine_id",
            request_method=self._RequestMethod.POST
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_account_info(
        self,
        public_key,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        https://docs.blockchainapi.com/#operation/solanaGetAccount
        :param public_key:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/account/{network.value}/{public_key}",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response

    def get_spl_token(
        self,
        public_key,
        network: SolanaNetwork = SolanaNetwork.DEVNET
    ):
        """
        https://docs.blockchainapi.com/#operation/solanaGetAccount
        :param public_key:
        :param network:
        :return:
        """
        response = self._request(
            endpoint=f"solana/spl-token/{network.value}/{public_key}",
            request_method=self._RequestMethod.GET
        )
        if 'error_message' in response:
            raise Exception(response['error_message'])
        return response
