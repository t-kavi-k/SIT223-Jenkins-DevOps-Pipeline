pipeline {
    agent any

    environment {
        DOCKER_HOST = 'tcp://localhost:2375'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                bat '"C:\\Users\\thamasha\\AppData\\Local\\Programs\\DockerDesktop\\resources\\bin\\docker.exe" build -t sit223-devops-app .'
            }
        }

        stage('Test') {
            steps {
                echo 'Installing dependencies...'
                bat '"C:\\Users\\thamasha\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m pip install -r requirements.txt'

                echo 'Running automated tests...'
                bat '"C:\\Users\\thamasha\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m pytest -v'
            }
        }

        stage('Code Quality') {
            steps {
                echo 'Installing Flake8...'
                bat '"C:\\Users\\thamasha\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m pip install flake8'

                echo 'Running Flake8 code quality checks...'
                bat '"C:\\Users\\thamasha\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m flake8 app.py test_app.py'
            }
        }
    }
}
