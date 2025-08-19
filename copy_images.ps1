# PowerShell script to copy images from Next.js to Django
$sourceDir = "c:\Users\Admin\Documents\Github\airnbn\nguyenvietanhnov-main\public\images"
$destDir = "c:\Users\Admin\Documents\Github\airnbn\core\static\core\images"

# Function to copy files with error handling
function Copy-ImageFiles {
    param(
        [string]$Source,
        [string]$Destination
    )
    
    try {
        if (Test-Path $Source) {
            Write-Host "Copying from: $Source"
            Write-Host "To: $Destination"
            
            # Ensure destination directory exists
            if (!(Test-Path $Destination)) {
                New-Item -ItemType Directory -Path $Destination -Force | Out-Null
            }
            
            # Copy files
            Get-ChildItem -Path $Source -Recurse -File | ForEach-Object {
                $relativePath = $_.FullName.Substring($Source.Length + 1)
                $destPath = Join-Path $Destination $relativePath
                $destParent = Split-Path $destPath -Parent
                
                if (!(Test-Path $destParent)) {
                    New-Item -ItemType Directory -Path $destParent -Force | Out-Null
                }
                
                Copy-Item $_.FullName $destPath -Force
                Write-Host "Copied: $relativePath"
            }
        } else {
            Write-Host "Source directory does not exist: $Source"
        }
    } catch {
        Write-Host "Error: $($_.Exception.Message)"
    }
}

# Copy all images
Copy-ImageFiles -Source $sourceDir -Destination $destDir

Write-Host "Image copy operation completed."
