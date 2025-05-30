cls

[String[]]$empDepots = @('s-m42-it-dp01','s-m42-it-dp02','s-swv-dp00','s-m42-it-dmz01')
[String]$empMaster = 's-m42-it-emp'
[String[]]$excludeList = @('SyncFiles.ps1','syncpath.ps1')

#check script runs from empirum master
[String]$path = (Get-Location).ProviderPath
if($path -notmatch '^\\\\{0}' -f $empMaster)
{
	Write-Host ('Fehler! Script wurde nicht von {0} aus gestartet' -f $empMaster) -ForegroundColor Red
	Sleep 3
	Exit 100
}

#get all files
$files = Get-ChildItem -Path $path -File | Where { $_.Name -notmatch '{0}' -f ($excludeList -join '|') }

#list all files
Write-Host ('Copy: {0} files' -f $files.Count)
foreach ($file in $files) {
    Write-Host $file.Name
}

#copy files
Write-Host "To:"
foreach ($empDepot in $empDepots) {
    $pathNew = ('{0}' -f ($path -replace $empMaster,$empDepot))
    Write-Host ('{0}' -f $pathNew)
    if (-not (Test-Path -Path $pathNew)) {
        Write-Host ('Skip! Path does not exist.') -ForegroundColor Red
        Continue
    }
    foreach ($file in $files) {
        Copy-Item -path ('{0}' -f $file.FullName) -Destination ('{0}' -f ($file.FullName -replace $empMaster,$empDepot)) -Force -ErrorAction Continue
    }
}

Sleep 3