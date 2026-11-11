#!/usr/bin/env bash
# =============================================================================
#  Run on YOUR LAPTOP (needs Azure CLI: https://learn.microsoft.com/cli/azure/install-azure-cli)
#  Creates: resource group + Ubuntu 22.04 VM + opens HTTP port 80.
#  MySQL port 3306 is NOT opened – the database is only reachable from the VM.
# =============================================================================
set -euo pipefail

RG="${RG:-bookverse-rg}"
LOCATION="${LOCATION:-centralindia}"
VM="${VM:-bookverse-vm}"
SIZE="${SIZE:-Standard_B2s}"          # 2 vCPU / 4 GB RAM – enough for app + MySQL
ADMIN="${ADMIN:-azureuser}"

echo "==> Logging in check"
az account show >/dev/null 2>&1 || az login

echo "==> Creating resource group $RG in $LOCATION"
az group create --name "$RG" --location "$LOCATION" -o none

echo "==> Creating VM $VM ($SIZE) – this takes ~2 minutes"
az vm create \
  --resource-group "$RG" \
  --name "$VM" \
  --image Ubuntu2204 \
  --size "$SIZE" \
  --admin-username "$ADMIN" \
  --generate-ssh-keys \
  --public-ip-sku Standard \
  -o none

echo "==> Opening port 80 (HTTP)"
az vm open-port --resource-group "$RG" --name "$VM" --port 80 --priority 1010 -o none

IP=$(az vm show -d -g "$RG" -n "$VM" --query publicIps -o tsv)
cat <<EOF

✅ VM ready:  $IP

Next steps (from the project folder):
  1) Copy the code:   scp -r . $ADMIN@$IP:~/bookverse
  2) SSH in:          ssh $ADMIN@$IP
  3) Install:         cd ~/bookverse && sudo bash deploy/setup_vm.sh
  4) Open:            http://$IP

Delete everything later with:  az group delete --name $RG --yes --no-wait
EOF
