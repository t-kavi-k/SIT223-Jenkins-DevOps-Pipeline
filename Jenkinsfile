pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                bat 'docker build -t sit223-devops-app .'
            }
        }

        stage('Test') {
            steps {
                echo 'Running automated tests...'
                bat 'python -m pytest -v'
            }
        }
    }
}