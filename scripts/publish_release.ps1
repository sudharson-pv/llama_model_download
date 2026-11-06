<#
.SYNOPSIS
    Publishes a model release to GitHub Releases for LearnMate AI.
.PARAMETER Tag
    Release tag (e.g. llama-3.2-1b-v1).
.PARAMETER Name
    Release title.
.PARAMETER Files
    File paths to upload as release assets.
#>
param(
    [Parameter(Mandatory=$true)][string]$Tag,
    [Parameter(Mandatory=$true)][string]$Name,
    [Parameter(Mandatory=$false)][string]$Body = "Official on-device ExecuTorch model release for LearnMate AI.",
    [Parameter(Mandatory=$true)][string[]]$Files
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
python "$scriptDir\publish_release.py" --tag $Tag --name $Name --body $Body --files $Files
