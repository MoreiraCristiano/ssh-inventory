function Connect-SSH {
    param (
        [string]$sshCommand
    )

    Write-Host "Connecting to $sshCommand..."
    Invoke-Expression $sshCommand
}

Connect-SSH($args[0])