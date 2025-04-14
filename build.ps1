$exclude = @("venv", "botToner.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "ICTBOT.zip" -Force