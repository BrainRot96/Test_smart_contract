def main():
    from ape import accounts, project
    
    # Charger ton compte
    deployer = accounts.load("testaccount")
    
    # Déployer le contrat
    contract = deployer.deploy(project.tip_jar)
    
    print(f"Contrat deploye a : {contract.address}")

