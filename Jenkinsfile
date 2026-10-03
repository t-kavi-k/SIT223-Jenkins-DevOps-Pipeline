pipeline {
    agent any

    environment {
        DOCKER_HOST = 'tcp://localhost:2375'
        DOCKER_EXE = 'C:\\Users\\thamasha\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe'
        PYTHON_EXE = 'C:\\Users\\thamasha\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'

                bat '"%DOCKER_EXE%" build -t sit223-devops-app .'
            }
        }

        stage('Test') {
            steps {
                echo 'Installing dependencies...'

                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'

                echo 'Running automated tests...'

                bat '"%PYTHON_EXE%" -m pytest -v'
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Installing Flake8...'

                bat '"%PYTHON_EXE%" -m pip install flake8'

                echo 'Running Flake8 code quality checks...'

                bat '"%PYTHON_EXE%" -m flake8 app.py test_app.py'
            }
        }

        stage('Security') {
            steps {
                echo 'Installing Bandit...'

                bat '"%PYTHON_EXE%" -m pip install bandit'

                echo 'Running Bandit security scan...'

                bat '"%PYTHON_EXE%" -m bandit -r app.py'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying application container...'

                bat '''
                "%DOCKER_EXE%" rm -f sit223-app 2>nul || exit /b 0
                "%DOCKER_EXE%" run -d -p 5000:5000 --name sit223-app -e FLASK_HOST=0.0.0.0 sit223-devops-app
                '''
            }
        }

        stage('Release') {
            steps {
                echo 'Creating release image tag...'

                bat '"%DOCKER_EXE%" tag sit223-devops-app sit223-devops-app:release'

                echo 'Release image created.'
            }
        }

        stage('Monitoring') {
            steps {
                echo 'Checking deployed Flask application...'

                powershell '''
                $response = Invoke-RestMethod -Uri http://localhost:5000/health

                if ($response.status -ne "healthy") {
                    Write-Error "Application health check failed"
                    exit 1
                }

                Write-Host "Application health check passed."
                '''

                echo 'Checking Prometheus availability...'

                powershell '''
                $response = Invoke-WebRequest `
                    -Uri http://localhost:9090/-/ready `
                    -UseBasicParsing

                if ($response.StatusCode -ne 200) {
                    Write-Error "Prometheus is not ready"
                    exit 1
                }

                Write-Host "Prometheus is ready."
                '''

                echo 'Checking Prometheus target status...'

                powershell '''
                $response = Invoke-RestMethod `
                    -Uri "http://localhost:9090/api/v1/query?query=up%7Bjob%3D%22sit223-flask-app%22%7D"

                if ($response.status -ne "success") {
                    Write-Error "Prometheus query failed"
                    exit 1
                }

                if ($response.data.result.Count -eq 0) {
                    Write-Error "Prometheus target was not found"
                    exit 1
                }

                $targetValue = $response.data.result[0].value[1]

                if ($targetValue -ne "1") {
                    Write-Error "Prometheus target is DOWN"
                    exit 1
                }

                Write-Host "Prometheus target is UP."
                '''

                echo 'Checking Alertmanager availability...'

                powershell '''
                $response = Invoke-WebRequest `
                    -Uri http://localhost:9093/-/ready `
                    -UseBasicParsing

                if ($response.StatusCode -ne 200) {
                    Write-Error "Alertmanager is not ready"
                    exit 1
                }

                Write-Host "Alertmanager is ready."
                '''

                echo 'Monitoring checks completed successfully.'
            }
        }
    }
}