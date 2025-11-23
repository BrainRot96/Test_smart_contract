# @version ~=0.4.0

# ════════════════════════════════════════════
# STORAGE
# ════════════════════════════════════════════

owner: public(address)
pourboires: public(HashMap[address, uint256])
total: public(uint256)

# ════════════════════════════════════════════
# CONSTRUCTEUR
# ════════════════════════════════════════════

@deploy
def __init__():
    self.owner = msg.sender
    self.total = 0

# ════════════════════════════════════════════
# FONCTION : Donner un pourboire
# ════════════════════════════════════════════

@external
@payable
def donner():
    assert msg.value > 0, "Envoie quelque chose!"
    
    self.pourboires[msg.sender] += msg.value
    self.total += msg.value

# ════════════════════════════════════════════
# FONCTION : Retirer (owner seulement)
# ════════════════════════════════════════════

@external
def retirer():
    assert msg.sender == self.owner, "Pas autorise!"
    assert self.balance > 0, "Contrat vide!"
    
    send(self.owner, self.balance)