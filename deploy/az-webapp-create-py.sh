#!/bin/bash
while [[ $# -gt 0 ]]
do
    case "$1" in
        -g|--resource-group)
            AZRGNAME="$2"
            shift 2
            ;;
        -l|--location)
            AZLOCATION="$2"
            shift 2
            ;;
        -n|-n)
            AZAPPNAME="$2"
            shift 2
            ;;
        -p|--plan)
            AZAPPPLAN="$2"
            shift 2
            ;;
    esac
done

# create the RG if it doesn't exists
if [ $(az group exists -n $AZRGNAME) == 'false' ]; then
    echo "create ResourceGroup=$AZRGNAME"
    az group create -n $AZRGNAME -l "$AZLOCATION"
fi

# create the AppService Plan if it doesn't exists
VAR0=$(az appservice plan show -n "$AZAPPPLAN" -g "$AZRGNAME" --query "name" -o tsv)
if [ -z "$VAR0" ]; then
    echo "create AppPlan=$AZAPPPLAN"
    az appservice plan create -n "$AZAPPPLAN" -g "$AZRGNAME" -l "$AZLOCATION" --is-linux --sku FREE #S1
fi

# create the AppService if it doesn't exists
VAR0=$(az webapp show -n "$AZAPPNAME" -g "$AZRGNAME" --query "defaultHostName" -o tsv )
if [ -z "$VAR0" ]; then
    echo "create AppService=$AZAPPNAME"
    az webapp create -n "$AZAPPNAME" -g "$AZRGNAME" -p "$AZAPPPLAN" -r "python|3.7" \
                    --deployment-local-git
    az webapp config set -g $AZRGNAME -n $AZAPPNAME \
                    --min-tls-version 1.2 \
                    --linux-fx-version "PYTHON|3.7"
    az webapp log config -n "$AZAPPNAME" -g "$AZRGNAME" --web-server-logging filesystem --docker-container-logging filesystem
fi

