# @version ~=0.4.0

"""
@title BotanIA
@author VicDaHood
@notice Token ERC20 pour l'écosystème BotanIA
@dev Token avec fonctionnalités et récompenses
"""

# ════════════════════════════════════════════════════════════════
# EVENTS (Standard ERC20)
# ════════════════════════════════════════════════════════════════

event Transfer:
    sender: indexed(address)
    receiver: indexed(address)
    amount: uint256

event Approval:
    owner: indexed(address)
    spender: indexed(address)
    amount: uint256

event Mint:
    receiver: indexed(address)
    amount: uint256
    raison: String[100]

# ════════════════════════════════════════════════════════════════
# STORAGE - Métadonnées du token
# ════════════════════════════════════════════════════════════════

name: public(constant(String[32])) = "BotanIA Token"
symbol: public(constant(String[8])) = "BTIA"
decimals: public(constant(uint8)) = 18

# ════════════════════════════════════════════════════════════════
# STORAGE - Supply et balances
# ════════════════════════════════════════════════════════════════

totalSupply: public(uint256)
balanceOf: public(HashMap[address, uint256])
allowance: public(HashMap[address, HashMap[address, uint256]])

# ════════════════════════════════════════════════════════════════
# STORAGE - Contrôle d'accès
# ════════════════════════════════════════════════════════════════

owner: public(address)
minters: public(HashMap[address, bool])

# ════════════════════════════════════════════════════════════════
# CONSTANTES - Tokenomics
# ════════════════════════════════════════════════════════════════

# Supply maximum : 1 milliard de tokens
MAX_SUPPLY: constant(uint256) = 1_000_000_000 * 10**18

# Récompense standardisées 
REWARD_NEW_PLANT: public(constant(uint256)) = 100 * 10**18 # = 100 BTIA
REWARD_PHOTO: public(constant(uint256)) = 150 * 10**18 # = 150 BTIA
REWARD_VOTE: public(constant(uint256)) = 10 * 10**18 # = 10 BTIA

# ════════════════════════════════════════════════════════════════
# MODIFICATEURS (fonctions internes)
# ════════════════════════════════════════════════════════════════

@internal
@view
def _only_owner():
   """Vérifie que l'appellant est le owner"""
   assert msg.sender == self.owner, "Pas le owner"

@internal
@view
def _only_minter():
    """Vérifie que l'appellant est autorisé à mint"""
    assert self.minters[msg.sender], "Pas autorise a mint"

# ════════════════════════════════════════════════════════════════
# CONSTRUCTEUR
# ════════════════════════════════════════════════════════════════

@deploy
def __init__():
    """
    Initialise le token
    - Owner = déployeur
    - Supply initiale = 0 (tokens créés via mint uniquement)
    """
    self.owner = msg.sender
    self.totalSupply = 0
    
    # Le owner peut mint au début pour setup
    self.minters[msg.sender] = True


# ════════════════════════════════════════════════════════════════
# FONCTIONS ERC20 STANDARD
# ════════════════════════════════════════════════════════════════

@external
def transfer(receiver: address, amount: uint256) -> bool:
    """ 
    Transfère des tokens a une autre addresse

    Args:
        receiver: Addresse du destinataire
        amount: Montant à transférer (en wei, avec 18 décimales)
     
    Returns:
    True si succès
    """

    assert receiver != empty(address), "Addresse invalide"
    assert self.balanceOf[msg.sender] >= amount, "Solde insuffisant"

    self.balanceOf[msg.sender] -= amount
    self.balanceOf[receiver] += amount

    log Transfer(msg.sender, receiver, amount)
    return True

@external
def approve(spender: address, amount: uint256) -> bool:
    """
    Autorise une adresse a dépenser des toekns
    
    Args:
         spender: Adresse autorisée
         amount: Montant autorisé
    Return: 
    True si succès
    """

    assert spender != empty(address), "Adresse invalide"
    self.allowance[msg.sender][spender] = amount

    log Approval(msg.sender, spender, amount)
    return True

@external
def transferFrom(sender: address, receiver: address, amount: uint256) -> bool:
    """Transfère des tokens depuis une autre adresse (nécessite approval)

    Args: 
        sender: Adresse source
        receiver: Adresse destination
        amount/ Montant à transférer
    Returns:
        True si succès
    """
    assert receiver != empty(address), "Adresse invalide"
    assert self.balanceOf[sender] >= amount, "Solde insuffisant"
    assert self.allowance[sender][msg.sender] >= amount, "Allowance insuffisante"

    self.balanceOf[sender] -= amount
    self.balanceOf[receiver] += amount
    self.allowance[sender][msg.sender] -= amount

    log Transfer(sender, receiver, amount)
    return True


# ════════════════════════════════════════════════════════════════
# FONCTIONS DE MINT (Distribution de récompenses)
# ════════════════════════════════════════════════════════════════

@external
def mint(receiver: address, amount: uint256, raison: String[100]):
    """
    Crée de nouveaux tokens (minters seulement)
    
    Args:
        receiver: Qui reçoit les tokens
        amount: Montant à créer
        raison: Raison du mint (ex: "Nouvelle plante validee")
    """

# Vérification
    self._only_minter()
    assert receiver != empty(address), "Adresse invalide"
    assert self.totalSupply + amount <= MAX_SUPPLY, "Max supply atteint"

    self.totalSupply += amount
    self.balanceOf[receiver] += amount
    
    log Transfer(empty(address), receiver, amount)
    log Mint(receiver, amount, raison)


# Mint 
@external
def mint_reward_new_plant(receiver: address):
    """
    Mint la récompense pour ajout d'une nouvelle plante (100 BTIA)
    Appelé par le contrat PlantRegistry
    """
    self._only_minter()
    amount: uint256 = REWARD_NEW_PLANT

    assert receiver != empty(address), "Adresse invalide"
    assert self.totalSupply + amount <= MAX_SUPPLY, "Max supply atteint"

    self.totalSupply += amount
    self.balanceOf[receiver] += amount

    log Transfer(empty(address), receiver, amount)
    log Mint(receiver, amount, "Nouvelle plante ajoutee")

@external
def mint_reward_photo(receiver: address):
    """
    Mint la récompense pour la photo validée (150 BTIA)
     Appelé par le contrat Plantregistry
    """

    self._only_minter()
    amount: uint256 = REWARD_PHOTO

    assert receiver != empty(address), "Adresse invalide"
    assert self.totalSupply + amount <= MAX_SUPPLY, "Max supply atteint"

    self.totalSupply += amount
    self.balanceOf[receiver] += amount
    
    log Transfer(empty(address), receiver, amount)
    log Mint(receiver, amount, "Photo validee")


@external
def mint_reward_vote(receiver: address):
    """
    Mint la récompense pour vote de validation (10 BTIA)
    Appelé par le contrat Governance
    """
    self._only_minter()
    amount: uint256 = REWARD_VOTE
    
    assert receiver != empty(address), "Adresse invalide"
    assert self.totalSupply + amount <= MAX_SUPPLY, "Max supply atteint"
    
    self.totalSupply += amount
    self.balanceOf[receiver] += amount
    
    log Transfer(empty(address), receiver, amount)
    log Mint(receiver, amount, "Vote de validation")


# ════════════════════════════════════════════════════════════════
# FONCTIONS DE BURN
# ════════════════════════════════════════════════════════════════

@external
def burn(amount: uint256):
    """
    Détruit des tokens (réduit la supply)

    Args:
        amount: Montant à détruire
    """
    assert self.balanceOf[msg.sender] >= amount, "Solde insuffisant"
    self.balanceOf[msg.sender] -= amount
    self.totalSupply -= amount

    log Transfer(msg.sender, empty(address), amount)

# ════════════════════════════════════════════════════════════════
# GESTION DES MINTERS (Owner seulement)
# ════════════════════════════════════════════════════════════════

@external
def add_minter(minter: address):
    """
    Autorise un contrat à mint des tokens
    EX: PlanteRegistry, Governance

    Args:
        minter: adresse du contratà autoriser
    """
    self._only_owner()
    assert minter != empty(address), "Adresse invalide"
    self.minters[minter] = True

@external
def remove_minter(minter: address):
    """Retire le droit de mint
    Args:
        minter: Adresse à retirer
    """
    self._only_owner()
    self.minters[minter] = False

# ════════════════════════════════════════════════════════════════
# GESTION DE L'OWNERSHIP
# ════════════════════════════════════════════════════════════════

@external
def transfer_ownership(new_owner: address):
    """
    Transfère la propriété du contrat
    
    Args:
        new_owner: Nouvelle adresse owner
    """
    self._only_owner()
    assert new_owner != empty(address), "Adresse invalide"
    self.owner = new_owner


# ════════════════════════════════════════════════════════════════
# FONCTIONS DE LECTURE (View)
# ════════════════════════════════════════════════════════════════

@external
@view
def get_reward_amounts() -> (uint256, uint256, uint256):
    """
    Retourne les montants de récompenses
    
    Returns:
        (reward_plant, reward_photo, reward_vote)
    """
    return (REWARD_NEW_PLANT, REWARD_PHOTO, REWARD_VOTE)


@external
@view
def get_balance(account: address) -> uint256:
    """
    Retourne le solde d'une adresse
    
    Args:
        account: Adresse à vérifier
    
    Returns:
        Solde en BTIA (wei)
    """
    return self.balanceOf[account]


@external
@view
def is_minter(account: address) -> bool:
    """
    Vérifie si une adresse peut mint
    
    Args:
        account: Adresse à vérifier
    
    Returns:
        True si autorisé
    """
    return self.minters[account]

# ════════════════════════════════════════════════════════════════
# FIN DU CONTRAT
# ════════════════════════════════════════════════════════════════

