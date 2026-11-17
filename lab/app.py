import getpass
import hashlib
import hmac
import secrets
import sqlite3


def gerar_hash(senha: str, sal: bytes) -> bytes:
    return hashlib.scrypt(senha.encode(), salt=sal, n=2**14, r=8, p=1)


def criar_banco(senha_admin: str) -> sqlite3.Connection:
    conexao = sqlite3.connect(":memory:")
    conexao.execute(
        "CREATE TABLE usuarios ("
        "id INTEGER PRIMARY KEY, usuario TEXT UNIQUE NOT NULL, "
        "sal BLOB NOT NULL, hash_senha BLOB NOT NULL)"
    )
    sal = secrets.token_bytes(16)
    conexao.execute(
        "INSERT INTO usuarios (usuario, sal, hash_senha) VALUES (?, ?, ?)",
        ("admin", sal, gerar_hash(senha_admin, sal)),
    )
    conexao.commit()
    return conexao


def login(conexao: sqlite3.Connection, usuario: str, senha: str) -> bool:
    linha = conexao.execute(
        "SELECT sal, hash_senha FROM usuarios WHERE usuario = ?", (usuario,)
    ).fetchone()
    if linha is None:
        return False
    sal, hash_salvo = linha
    return hmac.compare_digest(gerar_hash(senha, sal), hash_salvo)


if __name__ == "__main__":
    banco = criar_banco(getpass.getpass("Defina a senha do admin do lab: "))
    usuario = input("Usuário: ")
    senha = getpass.getpass("Senha: ")
    print("Acesso liberado" if login(banco, usuario, senha) else "Acesso negado")
