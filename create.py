from collections import Counter

ARQUIVO_LOG = "/var/log/auth.log"
ARQUIVO_RELATORIO = "log.txt"

ips_aprovados = []
eventos = []

with open(ARQUIVO_LOG, "r", encoding="utf-8", errors="replace") as arquivo:
    for linha in arquivo:
        partes = linha.strip().split(maxsplit=1)
        data = partes[0] if partes else "Data não identificada"

        if "Accepted password" in linha:
            tipo = "SSH_SUCCESS"
            dados = linha.split("Accepted password for ", 1)[1]
            usuario, restante = dados.split(" from ", 1)
            campos_origem = restante.split()
            ip = campos_origem[0]
            porta = campos_origem[2] if len(campos_origem) > 2 and campos_origem[1] == "port" else "Não identificada"
            protocolo = campos_origem[3] if len(campos_origem) > 3 else "Não identificado"

            ips_aprovados.append(ip)
            eventos.append(
                f"[SUCCESS] {tipo}\nData: {data}\nUsuário: {usuario}\n"
                f"IP: {ip}\nPorta de origem: {porta}\nProtocolo: {protocolo}\n"
            )

        elif "Failed password for " in linha:
            tipo = "SSH_FAILURE"
            dados = linha.split("Failed password for ", 1)[1]
            usuario_e_origem = dados.split(" from ", 1)

            if len(usuario_e_origem) == 2:
                usuario = usuario_e_origem[0].replace("invalid user ", "")
                campos_origem = usuario_e_origem[1].split()
                ip = campos_origem[0]
                eventos.append(
                    f"[ERROR] {tipo}\nData: {data}\nUsuário: {usuario}\nIP: {ip}\n"
                )

        elif "authentication failure" in linha.lower():
            tipo = "LOCAL_FAILURE"
            campo_usuario = "user="
            usuario = "Não identificado"

            if campo_usuario in linha:
                usuario = linha.split(campo_usuario, 1)[1].split()[0]

            eventos.append(
                f"[ERROR] {tipo}\nData: {data}\nUsuário: {usuario}\n"
                f"Descrição: {linha.strip()}\n"
            )

        elif "sudo:" in linha and "session opened" in linha:
            eventos.append(
                f"[INFO] SUDO\nData: {data}\nDescrição: {linha.strip()}\n"
            )

contagem_aprovados = Counter(ips_aprovados)

with open(ARQUIVO_RELATORIO, "w", encoding="utf-8") as relatorio:
    relatorio.write("LINUX SECURITY MONITOR - RELATÓRIO\n")
    relatorio.write("=" * 40 + "\n\n")

    for evento in eventos:
        relatorio.write(evento)
        relatorio.write("-" * 40 + "\n")

    relatorio.write("\nRESUMO DE AUTENTICAÇÕES SSH APROVADAS POR IP\n")
    relatorio.write("=" * 40 + "\n")
    if contagem_aprovados:
        for ip, quantidade in sorted(contagem_aprovados.items()):
            relatorio.write(f"{ip}: {quantidade}\n")
    else:
        relatorio.write("Nenhuma autenticação SSH aprovada encontrada.\n")

print(f"Relatório gerado em: {ARQUIVO_RELATORIO}")
print(f"Eventos identificados: {len(eventos)}")
