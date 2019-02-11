# Set us up to write out UTF-8 data which is what Docker Compose expects
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

$pwd = (Get-Location).Path

# Build .env file
Remove-Item .env
"PWD=" + $pwd > .env
echo "COMPOSE_CONVERT_WINDOWS_PATHS=true" >> .env

# Copy requirements to the docker context
Copy-Item -Path $pwd\backend\uclapi\requirements.txt -Destination $pwd\docker

# Bring up containers
docker-compose up
