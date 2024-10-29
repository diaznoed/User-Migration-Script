

$inputFile = ".\user_migration.csv"
$lastRptDate = Get-Date -Format "yyyy-MM-dd"
#$lastRptDate = "2024-07-30"

$lookupSuceed = $true
$timeStr = Get-Date -Format "yyyy-MM-dd-HHmm"
$outputFile = ".\User Migration Enriched $timeStr.csv"
##
## For VLOOKUP to work, UPNc has to be first column in table
## but not if output file is a combo of both
##
$fileHeader = "OldGeoName|NewGeoName|OldIDPName|NewIDPName|RptDate|Name|Dept|Company|City|lookupName|domain"
Set-Content -Path $outputFile -Encoding Ascii -Value "$fileHeader" -Force
# not used $totrows = (Get-Content $inputFile).Length


## User UPN property to locate
##[String[]] $userUPNLists = Get-Content -Path $inputFil
$TempLists = Import-Csv -Path $inputFile -Header 'OldGeoName','NewGeoName','OldIDPName','NewIDPName','RptDate'
$userUPNLists = $TempLists | Where-Object {$_.rptDate -ge $lastRptDate }
Write-Host "Report Date: $lastRptDate" -ForegroundColor Cyan
Write-Host "New records found: " $userUPNLists.Length -ForegroundColor Cyan
$z = 0

ForEach ($NewIDPName in $userUPNLists)
{
    $CSVName = $NewIDPName.NewIDPName
    $CSVOGName = $NewIDPName.OldGeoName
    $CSVNGName = $NewIDPName.NewGeoName
    $CSVOIName = $NewIDPName.OldIDPName
    $CSVRecDate = $NewIDPName.RptDate
    $lookupName =  $CSVName.substring(6)
    $domain =  "STATE"
    $domainController = "ad.domaincontroller"

    ## Do the lookup. If not found, alert, but output anyway
    try {$LookUpResult = Get-ADUser -Server $domainController -Identity $lookupName -Properties department, company, city, name | Select name, department, company, city}
    catch {
        Write-Host "$lookupName not found" -ForegroundColor Magenta -NoNewline
        Write-Host " (Rec $z) " -ForegroundColor Yellow
        $lookupSuceed = $false
        }

        $upnc = $domain + "\" + $lookupName
        $LUname = $LookUpResult.name
        $LUDept = $LookUpResult.department
        $LUCo = $LookUpResult.company
        $LUCity = $LookUpResult.city

    if ($lookupSuceed)
        {
        $str = "$CSVOGName|$CSVNGName|$CSVOIName|$CSVName|$CSVRecDate|$LUname|$LUDept|$LUCo|$LUCity|$lookupName|$domain" | Out-File $outputFile -Append -Encoding Ascii
        }
        else
        {
        $str = "$CSVOGName|$CSVNGName|$CSVOIName|$CSVName|$CSVRecDate|$lookupName|$domain|NOT FOUND|NOT FOUND|NOT FOUND|NOT FOUND" | Out-File $outputFile -Append -Encoding Ascii
        }

    #Write-Host "." -NoNewline
    $lookupSuceed = $true
    $z++
}
####