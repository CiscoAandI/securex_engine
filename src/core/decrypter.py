from ansible_vault import Vault

class Decrypter(Vault):
    def decrypt(self, stream):
        return self.vault.decrypt(stream)