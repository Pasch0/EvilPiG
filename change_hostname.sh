#!/bin/bash

# Verifica se um novo hostname foi fornecido
if [ -z "$1" ]; then
    echo "Uso: $0 novo_hostname"
    exit 1
fi

# Define o novo hostname
novo_hostname="$1"

# Muda o hostname
sudo hostnamectl set-hostname "$novo_hostname"
echo "Hostname alterado para: $novo_hostname"

#!/bin/bash

# Caminho do arquivo EvilPiG.txt
evilpi_file="/opt/EvilPiG/EvilPiG.txt"
destination_file="/etc/update-motd.d/10-orangepi-header"

# Verifica se o arquivo EvilPiG.txt existe
if [ ! -f "$evilpi_file" ]; then
    echo "Erro: O arquivo EvilPiG.txt não foi encontrado em $evilpi_file"
    exit 1
fi

# Faz uma cópia de segurança do arquivo original
sudo cp "$destination_file" "${destination_file}.bak"
echo "Cópia de segurança do arquivo original criada em ${destination_file}.bak"

# Edita o arquivo 10-orangepi-header para usar EvilPiG.txt
sudo bash -c "cat > $destination_file" << 'EOF'
#!/bin/bash
#
# Copyright (c) Authors: https://www.armbian.com/authors
#
# This file is licensed under the terms of the GNU General Public
# License version 2. This program is licensed "as is" without any
# warranty of any kind, whether express or implied.

THIS_SCRIPT="header"
MOTD_DISABLE=""

[[ -f /etc/default/orangepi-motd ]] && . /etc/default/orangepi-motd

for f in $MOTD_DISABLE; do
        [[ $f == $THIS_SCRIPT ]] && exit 0
done

# Exibe a arte ASCII do EvilPiG.txt
cat /etc/EvilPiG.txt

. /etc/os-release
. /etc/orangepi-release

KERNELID=$(uname -r)
echo -e "Bem-vindo ao \e[0;91mOrange Pi ${VERSION} ${DISTRIBUTION_CODENAME^}\x1B[0m com Linux $KERNELID\n"
EOF

# Copia o arquivo EvilPiG.txt para o diretório correto
sudo cp "$evilpi_file" /etc/EvilPiG.txt
echo "Arquivo EvilPiG.txt copiado para /etc/EvilPiG.txt"

# Concede permissões de execução ao script modificado
sudo chmod +x "$destination_file"
echo "Permissões de execução concedidas ao script $destination_file"

echo "Banner atualizado com sucesso!"