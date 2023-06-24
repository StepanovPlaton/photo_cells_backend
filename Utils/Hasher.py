import passlib.context
from passlib.hash import hex_sha512 as hex_sha512

class HasherClass:
    def __init__(self):
        self.PasswordHasher = passlib.context.CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.TokenGenerate = passlib.context.CryptContext(schemes=['des_crypt'], deprecated='auto')
        self.ImageHasher = passlib.context.CryptContext(schemes=['sha512_crypt'], deprecated='auto')

    def PasswordHash(self, Password: str) -> str:
        return self.PasswordHasher.hash(Password)  # type: ignore

    def CheckPassword(self, Hash: str, Password: str) -> bool:
        return self.PasswordHasher.verify(Password, Hash)  # type: ignore

    def GetToken(self, HashedPassword: str) -> str:
        return self.TokenGenerate.hash(HashedPassword)  # type: ignore

    def CheckToken(self, Token: str, HashedPassword: str) -> bool:
        return self.TokenGenerate.verify(HashedPassword, Token)  # type: ignore

    def CreateImageFileNameHash(self, FileName: str) -> str:
        return hex_sha512.hash(FileName)+"."+FileName.split(".")[1]  # type: ignore
