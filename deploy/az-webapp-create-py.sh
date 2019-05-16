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
        -t|--tenantid)
            AZTENANTID="$2"
            shift 2
            ;;
        -a|--appid)
            AZAPPID="$2"
            shift 2
            ;;
        -z|--zipfolder)
            ZIPFOLDER="$2"
            shift 2
            ;;
        -b|--buildtag)
            BUILDTAG="$2"  
            shift 2
            ;;
    esac
done

echo "RG=$AZRGNAME, LOCATION=$AZLOCATION, PLAN=$AZAPPPLAN, APP=$AZAPPNAME, ZIPFOLDER=$ZIPFOLDER, tenantid=$AZTENANTID, AppID=$AZAPPID, BuildTag=$BUILDTAG"

rm -f ./deploy.zip
zip -r ./deploy.zip $ZIPFOLDER -x ./.git\* ./.vscode\* ./deploy\*

# create the RG if it doesn't exists
if [ $(az group exists -n $AZRGNAME) == 'false' ]; then
    echo "create ResourceGroup=$AZRGNAME"
    az group create -n $AZRGNAME -l "$AZLOCATION"
fi

# create the AppService Plan if it doesn't exists
VAR0=$(az appservice plan show -n "$AZAPPPLAN" -g "$AZRGNAME" --query "name" -o tsv)
if [ -z "$VAR0" ]; then
    echo "create AppPlan=$AZAPPPLAN"
    az appservice plan create -g "$AZRGNAME" -n "$AZAPPPLAN" -l "$AZLOCATION" --is-linux --sku FREE #S1
fi

# create the AppService if it doesn't exists
VAR0=$(az webapp show -n "$AZAPPNAME" -g "$AZRGNAME" --query "defaultHostName" -o tsv )
if [ -z "$VAR0" ]; then
    echo "create AppService=$AZAPPNAME"
    az webapp create -g "$AZRGNAME" -p "$AZAPPPLAN" -n "$AZAPPNAME" -r "python|3.7" 
    az webapp config set -g "$AZRGNAME" -n "$AZAPPNAME" --min-tls-version 1.2 --linux-fx-version "PYTHON|3.7"
    az webapp log config -g "$AZRGNAME" -n "$AZAPPNAME" --web-server-logging filesystem --docker-container-logging filesystem
fi
az webapp config appsettings set -g "$AZRGNAME" -n "$AZAPPNAME" --settings "SCM_DO_BUILD_DURING_DEPLOYMENT=true" "AZTENANTID=$AZTENANTID" "AZAPPID=$AZAPPID"
if [ ! -z "$BUILDTAG" ]; then
    az webapp config appsettings set -g "$AZRGNAME" -n "$AZAPPNAME" --settings "BUILDTAG=$BUILDTAG"
fi
az webapp deployment source config-zip -g "$AZRGNAME" -n "$AZAPPNAME" --src ./deploy.zip
